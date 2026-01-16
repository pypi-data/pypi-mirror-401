"""
FORCOME 康康 - 千寻微信框架Pro与LangBot中间件
包入口点 - 支持 uvx ForcomeBot 和 python -m src 运行
"""
import asyncio
import logging
import sys
import os
from pathlib import Path
from typing import Optional

import uvicorn
from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

# 导入核心模块
from .core.config_manager import ConfigManager
from .core.state_store import StateStore
from .core.log_collector import LogCollector, log_system
from .core.message_queue import MessageQueue, MessagePriority
from .clients.qianxun import QianXunClient
from .clients.langbot import LangBotClient
from .handlers.message_handler import MessageHandler
from .handlers.scheduler import TaskScheduler
from .models import QianXunCallback
from .api import router as api_router, set_dependencies, websocket_endpoint, set_websocket_dependencies
from .web import router as admin_router, set_references


def setup_logging(level: str = "INFO"):
    """配置日志"""
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )


# 创建 FastAPI 应用
app = FastAPI(
    title="FORCOME 康康",
    description="千寻微信框架Pro与LangBot中间件",
    version="2.0.0"
)

# 注册路由
app.include_router(api_router)
app.include_router(admin_router)

# 全局服务实例
config_manager: Optional[ConfigManager] = None
state_store: Optional[StateStore] = None
log_collector: Optional[LogCollector] = None
message_queue: Optional[MessageQueue] = None
qianxun_client: Optional[QianXunClient] = None
langbot_client: Optional[LangBotClient] = None
message_handler: Optional[MessageHandler] = None
scheduler: Optional[TaskScheduler] = None


def get_config_path() -> Path:
    """获取配置文件路径
    
    优先级：
    1. 当前工作目录的 config.yaml
    2. 用户目录的 ~/.forcome/config.yaml
    """
    # 当前目录
    cwd_config = Path.cwd() / "config.yaml"
    if cwd_config.exists():
        return cwd_config
    
    # 用户目录
    user_config_dir = Path.home() / ".forcome"
    user_config = user_config_dir / "config.yaml"
    if user_config.exists():
        return user_config
    
    # 如果都不存在，返回当前目录路径（后续会创建示例配置）
    return cwd_config


def get_data_dir() -> Path:
    """获取数据目录"""
    config_path = get_config_path()
    return config_path.parent / "data"


def create_example_config(config_path: Path):
    """创建示例配置文件"""
    example_config = '''# FORCOME 康康 配置文件
# 首次运行自动生成，请根据实际情况修改

# 服务器配置
server:
  host: "0.0.0.0"
  port: 789

# 千寻框架配置
qianxun:
  api_url: "http://127.0.0.1:7777/qianxun/httpapi"

# LangBot 配置
langbot:
  ws_host: "127.0.0.1"
  ws_port: 2280
  access_token: ""

# 机器人配置
robot:
  wxid: ""  # 机器人微信ID，留空自动获取

# 消息过滤配置
filter:
  ignore_wxids: []  # 忽略的wxid列表
  reply_at_all: false  # 是否回复@所有人

# 限流配置
rate_limit:
  min_interval: 1  # 最小回复间隔（秒）
  max_interval: 3  # 最大回复间隔（秒）
  batch_min_interval: 2  # 群发最小间隔（秒）
  batch_max_interval: 5  # 群发最大间隔（秒）

# 消息分段配置
message_split:
  enabled: false
  separator: "/!"
  min_delay: 1
  max_delay: 3

# 定时任务配置
scheduled_tasks: []

# 日志配置
logging:
  level: "INFO"
'''
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(example_config, encoding="utf-8")
    print(f"已创建示例配置文件: {config_path}")
    print("请修改配置后重新运行")


async def on_config_change(old_config: dict, new_config: dict):
    """配置变更回调"""
    logger = logging.getLogger(__name__)
    logger.info("检测到配置变更，正在应用...")
    
    old_langbot = old_config.get('langbot', {})
    new_langbot = new_config.get('langbot', {})
    
    if (old_langbot.get('ws_host') != new_langbot.get('ws_host') or
        old_langbot.get('ws_port') != new_langbot.get('ws_port') or
        old_langbot.get('access_token') != new_langbot.get('access_token')):
        
        logger.info("LangBot连接配置已变更，正在重新连接...")
        if langbot_client:
            await langbot_client.update_connection(
                new_langbot.get('ws_host', '127.0.0.1'),
                new_langbot.get('ws_port', 2280),
                new_langbot.get('access_token', '')
            )
    
    old_qianxun = old_config.get('qianxun', {})
    new_qianxun = new_config.get('qianxun', {})
    
    if old_qianxun.get('api_url') != new_qianxun.get('api_url'):
        logger.info("千寻API地址已变更，正在更新...")
        if qianxun_client:
            qianxun_client.update_api_url(new_qianxun.get('api_url', ''))
    
    if scheduler:
        scheduler.reload_tasks()
    
    # 更新消息队列配置
    if message_queue:
        new_rate_limit = new_config.get('rate_limit', {})
        message_queue.update_config(
            min_interval=new_rate_limit.get('min_interval'),
            max_interval=new_rate_limit.get('max_interval'),
            batch_min_interval=new_rate_limit.get('batch_min_interval'),
            batch_max_interval=new_rate_limit.get('batch_max_interval')
        )
    
    if log_collector:
        await log_system(log_collector, "配置已更新并生效")


@app.on_event("startup")
async def startup():
    """启动时初始化"""
    global config_manager, state_store, log_collector, message_queue
    global qianxun_client, langbot_client, message_handler, scheduler
    
    logger = logging.getLogger(__name__)
    
    config_path = get_config_path()
    data_dir = get_data_dir()
    
    # 初始化配置管理器
    config_manager = ConfigManager(str(config_path))
    try:
        config_manager.load()
    except Exception as e:
        logger.error(f"加载配置失败: {e}")
        sys.exit(1)
    
    log_level = config_manager.get("logging.level", "INFO")
    setup_logging(log_level)
    
    logger.info("正在启动中间件...")
    
    # 初始化状态存储器
    state_store = StateStore(data_dir=str(data_dir))
    await state_store.start()
    
    # 初始化日志收集器
    log_collector = LogCollector(max_logs=100)
    
    # 初始化消息队列
    rate_limit = config_manager.get_rate_limit_config()
    message_queue = MessageQueue(
        min_interval=rate_limit.get('min_interval', 1),
        max_interval=rate_limit.get('max_interval', 3),
        batch_min_interval=rate_limit.get('batch_min_interval', 2),
        batch_max_interval=rate_limit.get('batch_max_interval', 5)
    )
    await message_queue.start()
    logger.info("消息队列已启动")
    
    # 初始化千寻客户端
    qianxun_url = config_manager.get("qianxun.api_url", "http://127.0.0.1:7777/qianxun/httpapi")
    qianxun_client = QianXunClient(qianxun_url)
    logger.info(f"千寻框架API: {qianxun_url}")
    
    # 初始化LangBot客户端
    langbot_config = config_manager.get_langbot_config()
    ws_host = langbot_config.get("ws_host", "127.0.0.1")
    ws_port = langbot_config.get("ws_port", 2280)
    access_token = langbot_config.get("access_token", "")
    
    langbot_client = LangBotClient(ws_host, ws_port, access_token)
    langbot_client.set_state_store(state_store)
    
    # 初始化消息处理器
    message_handler = MessageHandler(
        qianxun_client,
        langbot_client,
        config_manager,
        state_store,
        log_collector
    )
    
    # 初始化定时任务调度器
    scheduler = TaskScheduler(
        qianxun_client,
        config_manager,
        state_store,
        log_collector,
        message_queue  # 传入消息队列
    )
    scheduler.start()
    
    # 注册配置变更观察者
    config_manager.register_observer(on_config_change)
    
    # 设置API依赖
    set_dependencies(
        config_manager,
        state_store,
        log_collector,
        qianxun_client,
        langbot_client,
        scheduler,
        message_queue
    )
    
    # 设置WebSocket依赖
    set_websocket_dependencies(log_collector, langbot_client)
    
    # 设置旧版Web管理界面的引用（兼容）
    class CompatHandler:
        def __init__(self, qianxun, config):
            self.qianxun = qianxun
            self.config = config
    
    compat_handler = CompatHandler(qianxun_client, config_manager.config)
    
    class CompatScheduler:
        def __init__(self, real_scheduler, config_manager):
            self._scheduler = real_scheduler
            self._config_manager = config_manager
        
        @property
        def robot_wxid(self):
            return self._scheduler.robot_wxid
        
        @property
        def scheduler(self):
            return self._scheduler.scheduler
        
        @property
        def config(self):
            return self._config_manager.config
        
        @config.setter
        def config(self, value):
            pass
        
        def _setup_nickname_check_tasks(self):
            self._scheduler.reload_tasks()
        
        def _setup_scheduled_reminders(self):
            pass
    
    compat_scheduler = CompatScheduler(scheduler, config_manager)
    set_references(compat_handler, compat_scheduler, config_manager.config)
    
    # 连接到LangBot
    asyncio.create_task(langbot_client.connect())
    
    await log_system(log_collector, "中间件启动完成")
    logger.info("中间件启动完成")


@app.on_event("shutdown")
async def shutdown():
    """关闭时清理"""
    logger = logging.getLogger(__name__)
    logger.info("正在关闭中间件...")
    
    if scheduler:
        scheduler.stop()
    if message_queue:
        await message_queue.stop()
    if state_store:
        await state_store.stop()
    if qianxun_client:
        await qianxun_client.close()
    if langbot_client:
        await langbot_client.close()
    
    logger.info("中间件已关闭")


@app.post("/qianxun/callback")
async def qianxun_callback(request: Request):
    """千寻框架回调接口"""
    logger = logging.getLogger(__name__)
    
    try:
        data = await request.json()
        logger.info(f"收到回调原始数据: {data}")
        
        callback = QianXunCallback(**data)
        
        if callback.wxid and scheduler:
            scheduler.set_robot_wxid(callback.wxid)
        
        result = await message_handler.handle_callback(callback)
        return JSONResponse(content=result)
    
    except Exception as e:
        logger.error(f"处理回调异常: {e}", exc_info=True)
        return JSONResponse(
            content={"status": "error", "message": str(e)},
            status_code=500
        )


@app.websocket("/api/ws")
async def websocket_route(websocket: WebSocket):
    """WebSocket端点"""
    await websocket_endpoint(websocket)


@app.get("/health")
async def health_check():
    """健康检查接口"""
    langbot_ok = langbot_client.is_connected if langbot_client else False
    return {
        "status": "ok",
        "langbot_connected": langbot_ok,
        "langbot_reconnecting": langbot_client.is_reconnecting if langbot_client else False
    }


@app.get("/")
async def root():
    """根路径"""
    if static_dir:
        return RedirectResponse(url="/app/")
    return {
        "name": "FORCOME 康康",
        "version": "2.0.0",
        "callback_url": "/qianxun/callback",
        "api_docs": "/docs",
        "admin": "/admin",
        "app": "/app/ (前端未安装)"
    }


# 挂载React前端静态文件
# 优先使用当前目录的 web/dist，其次使用包内的 static 目录
def get_static_dir() -> Path | None:
    """获取静态文件目录"""
    # 1. 当前目录的 web/dist
    local_dist = Path.cwd() / "web" / "dist"
    if local_dist.exists() and (local_dist / "index.html").exists():
        return local_dist
    
    # 2. 包内的 static 目录
    package_static = Path(__file__).parent / "static"
    if package_static.exists() and (package_static / "index.html").exists():
        return package_static
    
    return None

static_dir = get_static_dir()
if static_dir:
    from fastapi.responses import FileResponse
    
    # SPA catch-all 路由 - 处理前端路由刷新问题
    # 必须在 StaticFiles 挂载之前定义
    @app.get("/app/{full_path:path}")
    async def serve_spa(full_path: str):
        """处理 SPA 路由，所有 /app/* 路径都返回 index.html"""
        # 如果请求的是静态资源文件（有扩展名），尝试返回文件
        if "." in full_path:
            file_path = static_dir / full_path
            if file_path.exists() and file_path.is_file():
                return FileResponse(file_path)
        # 否则返回 index.html，让前端路由处理
        return FileResponse(static_dir / "index.html")
    
    # 挂载静态资源目录（用于 /app/assets/* 等静态文件）
    app.mount("/app", StaticFiles(directory=str(static_dir), html=True), name="react-app")


def main():
    """主入口函数 - 支持 uvx ForcomeBot 运行"""
    import yaml
    
    config_path = get_config_path()
    
    # 检查配置文件
    if not config_path.exists():
        print(f"配置文件不存在: {config_path}")
        create_example_config(config_path)
        return
    
    # 加载配置获取服务器设置
    with open(config_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    
    server_config = cfg.get("server", {})
    host = server_config.get("host", "0.0.0.0")
    port = server_config.get("port", 789)
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                   FORCOME 康康 v2.0                          ║
║           千寻微信框架Pro - LangBot 中间件                   ║
╠══════════════════════════════════════════════════════════════╣
║  配置文件: {config_path}
║  回调地址: http://{host}:{port}/qianxun/callback
║  React前端: http://{host}:{port}/app/
║  管理界面: http://{host}:{port}/admin (旧版)
║  API文档:  http://{host}:{port}/docs
║  健康检查: http://{host}:{port}/health
║  WebSocket: ws://{host}:{port}/api/ws
╚══════════════════════════════════════════════════════════════╝
    """)
    
    uvicorn.run(
        "src.__main__:app",
        host=host,
        port=port,
        reload=False,
        log_level="info"
    )


if __name__ == "__main__":
    main()
