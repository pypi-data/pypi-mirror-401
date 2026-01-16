"""API路由模块 - RESTful API接口

提供以下API：
- 配置管理：GET/POST /api/config, POST /api/config/validate
- 状态监控：GET /api/status, /api/status/langbot, /api/status/memory, /api/status/queue
- 日志：GET /api/logs
- 任务：GET /api/tasks, POST /api/tasks/{id}/run, GET /api/tasks/history
- 缓存：POST /api/cache/clear
- 列表：GET /api/chatrooms, /api/friends, /api/group_members/{id}, /api/robot_info
- 群发：POST /api/broadcast/*
"""
import logging
from typing import Optional, Dict, Any, List, TYPE_CHECKING

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

if TYPE_CHECKING:
    from ..core.config_manager import ConfigManager
    from ..core.state_store import StateStore
    from ..core.log_collector import LogCollector
    from ..core.message_queue import MessageQueue
    from ..clients.qianxun import QianXunClient
    from ..clients.langbot import LangBotClient
    from ..handlers.scheduler import TaskScheduler

from ..core.message_queue import MessagePriority

logger = logging.getLogger(__name__)

# 创建路由器
router = APIRouter(prefix="/api", tags=["admin"])

# 全局引用（由main.py设置）
_config_manager: Optional["ConfigManager"] = None
_state_store: Optional["StateStore"] = None
_log_collector: Optional["LogCollector"] = None
_message_queue: Optional["MessageQueue"] = None
_qianxun_client: Optional["QianXunClient"] = None
_langbot_client: Optional["LangBotClient"] = None
_scheduler: Optional["TaskScheduler"] = None


def set_dependencies(
    config_manager: "ConfigManager",
    state_store: "StateStore",
    log_collector: "LogCollector",
    qianxun_client: "QianXunClient",
    langbot_client: "LangBotClient",
    scheduler: "TaskScheduler",
    message_queue: "MessageQueue" = None
):
    """设置API依赖的服务实例
    
    Args:
        config_manager: 配置管理器
        state_store: 状态存储器
        log_collector: 日志收集器
        qianxun_client: 千寻客户端
        langbot_client: LangBot客户端
        scheduler: 任务调度器
        message_queue: 消息队列
    """
    global _config_manager, _state_store, _log_collector
    global _qianxun_client, _langbot_client, _scheduler, _message_queue
    
    _config_manager = config_manager
    _state_store = state_store
    _log_collector = log_collector
    _qianxun_client = qianxun_client
    _langbot_client = langbot_client
    _scheduler = scheduler
    _message_queue = message_queue
    
    logger.info("API路由依赖已设置")


# ============ 请求/响应模型 ============

class ConfigUpdate(BaseModel):
    """配置更新请求"""
    config: Dict[str, Any]


class CacheClearRequest(BaseModel):
    """缓存清理请求"""
    cache_type: str  # all, image, msg_ids, group_mapping, message_mapping


# ============ 配置管理API ============

@router.get("/config")
async def get_config():
    """获取当前配置"""
    if not _config_manager:
        raise HTTPException(status_code=503, detail="服务未初始化")
    
    return _config_manager.config


@router.post("/config")
async def update_config(data: ConfigUpdate):
    """更新配置"""
    if not _config_manager:
        raise HTTPException(status_code=503, detail="服务未初始化")
    
    success, message = await _config_manager.save(data.config)
    
    if not success:
        raise HTTPException(status_code=400, detail=message)
    
    # 重新加载调度器任务
    if _scheduler:
        _scheduler.reload_tasks()
    
    return {"status": "ok", "message": message}


@router.post("/config/validate")
async def validate_config(data: ConfigUpdate):
    """验证配置格式"""
    if not _config_manager:
        raise HTTPException(status_code=503, detail="服务未初始化")
    
    valid, error = _config_manager.validate(data.config)
    
    return {
        "valid": valid,
        "error": error if not valid else None
    }


# ============ 状态监控API ============

@router.get("/status")
async def get_status():
    """获取系统状态概览"""
    robot_wxid = _config_manager.robot_wxid if _config_manager else None
    
    # 获取调度任务信息
    scheduled_jobs = []
    if _scheduler and _scheduler.scheduler:
        for job in _scheduler.scheduler.get_jobs():
            next_run = None
            try:
                if hasattr(job, 'next_run_time') and job.next_run_time:
                    next_run = job.next_run_time.isoformat()
            except:
                pass
            scheduled_jobs.append({
                "id": job.id,
                "next_run": next_run
            })
    
    # 获取内存使用情况
    memory_usage = _state_store.get_stats() if _state_store else {}
    
    return {
        "robot_wxid": robot_wxid,
        "langbot_connected": _langbot_client.is_connected if _langbot_client else False,
        "langbot_reconnecting": _langbot_client.is_reconnecting if _langbot_client else False,
        "scheduled_jobs": scheduled_jobs,
        "memory_usage": memory_usage
    }


@router.get("/status/langbot")
async def get_langbot_status():
    """获取LangBot连接状态"""
    if not _langbot_client:
        return {
            "connected": False,
            "reconnecting": False,
            "error": "LangBot客户端未初始化"
        }
    
    return {
        "connected": _langbot_client.is_connected,
        "reconnecting": _langbot_client.is_reconnecting,
        "reconnect_delay": _langbot_client.get_reconnect_delay(),
        "host": _langbot_client.host,
        "port": _langbot_client.port
    }


@router.get("/status/memory")
async def get_memory_status():
    """获取内存缓存状态"""
    if not _state_store:
        return {"error": "状态存储器未初始化"}
    
    stats = _state_store.get_stats()
    
    return {
        "stats": stats,
        "limits": {
            "max_msg_ids": _state_store.max_msg_ids,
            "max_image_cache": _state_store.max_image_cache,
            "max_group_mapping": _state_store.max_group_mapping,
            "max_message_mapping": _state_store.max_message_mapping
        },
        "ttl": {
            "msg_id_ttl": _state_store.msg_id_ttl,
            "image_cache_ttl": _state_store.image_cache_ttl
        }
    }


@router.get("/status/queue")
async def get_queue_status():
    """获取消息队列状态"""
    if not _message_queue:
        return {"error": "消息队列未初始化"}
    
    return _message_queue.get_status()


# ============ 日志API ============

@router.get("/logs")
async def get_logs(type: Optional[str] = None, limit: int = 100):
    """获取消息处理日志
    
    Args:
        type: 日志类型筛选（private, group, error, system）
        limit: 返回条数限制
    """
    if not _log_collector:
        return {"logs": [], "error": "日志收集器未初始化"}
    
    logs = _log_collector.get_logs(log_type=type, limit=limit)
    
    return {
        "logs": logs,
        "total": _log_collector.log_count,
        "subscribers": _log_collector.subscriber_count
    }


# ============ 任务API ============

@router.get("/tasks")
async def get_tasks():
    """获取所有定时任务"""
    if not _scheduler:
        return {"tasks": [], "error": "调度器未初始化"}
    
    tasks = _scheduler.get_tasks()
    
    return {"tasks": tasks}


@router.post("/tasks/{task_id}/run")
async def run_task(task_id: str):
    """手动触发任务执行"""
    if not _scheduler:
        raise HTTPException(status_code=503, detail="调度器未初始化")
    
    result = await _scheduler.run_task_manually(task_id)
    
    if result.get("status") == "error":
        raise HTTPException(status_code=400, detail=result.get("message"))
    
    return result


@router.get("/tasks/history")
async def get_task_history(limit: int = 50):
    """获取任务执行历史"""
    if not _scheduler:
        return {"history": [], "error": "调度器未初始化"}
    
    history = _scheduler.get_task_history(limit=limit)
    
    return {"history": history}


# ============ 缓存API ============

@router.post("/cache/clear")
async def clear_cache(data: CacheClearRequest):
    """清理缓存
    
    Args:
        cache_type: 缓存类型
            - all: 清空所有缓存
            - image: 清空图片缓存
    """
    if not _state_store:
        raise HTTPException(status_code=503, detail="状态存储器未初始化")
    
    cache_type = data.cache_type
    
    if cache_type == "all":
        _state_store.clear_all()
        return {"status": "ok", "message": "所有缓存已清空"}
    elif cache_type == "image":
        _state_store.clear_image_cache()
        return {"status": "ok", "message": "图片缓存已清空"}
    else:
        raise HTTPException(status_code=400, detail=f"未知的缓存类型: {cache_type}")


# ============ 列表API ============

@router.get("/chatrooms")
async def get_chatrooms():
    """获取群聊列表"""
    if not _qianxun_client or not _config_manager:
        return {"chatrooms": [], "error": "服务未初始化"}
    
    robot_wxid = _config_manager.robot_wxid
    if not robot_wxid:
        return {"chatrooms": [], "error": "机器人wxid未配置"}
    
    try:
        chatrooms = await _qianxun_client.get_chatroom_list(robot_wxid)
        return {"chatrooms": chatrooms}
    except Exception as e:
        logger.error(f"获取群聊列表失败: {e}")
        return {"chatrooms": [], "error": str(e)}


@router.get("/friends")
async def get_friends():
    """获取好友列表"""
    if not _qianxun_client or not _config_manager:
        return {"friends": [], "error": "服务未初始化"}
    
    robot_wxid = _config_manager.robot_wxid
    if not robot_wxid:
        return {"friends": [], "error": "机器人wxid未配置"}
    
    try:
        friends = await _qianxun_client.get_friend_list(robot_wxid)
        return {"friends": friends}
    except Exception as e:
        logger.error(f"获取好友列表失败: {e}")
        return {"friends": [], "error": str(e)}


@router.get("/group_members/{group_wxid}")
async def get_group_members(group_wxid: str):
    """获取群成员列表"""
    if not _qianxun_client or not _config_manager:
        return {"members": [], "error": "服务未初始化"}
    
    robot_wxid = _config_manager.robot_wxid
    if not robot_wxid:
        return {"members": [], "error": "机器人wxid未配置"}
    
    try:
        members = await _qianxun_client.get_group_member_list(
            robot_wxid, group_wxid, get_nick=True
        )
        # 格式化返回数据
        result = []
        for m in members:
            result.append({
                "wxid": m.get("wxid", ""),
                "nickname": m.get("groupNick", "") or m.get("nickname", "") or m.get("wxid", "")
            })
        return {"members": result}
    except Exception as e:
        logger.error(f"获取群成员列表失败: {e}")
        return {"members": [], "error": str(e)}


@router.get("/robot_info")
async def get_robot_info():
    """获取机器人自身信息"""
    if not _qianxun_client or not _config_manager:
        return {"wxid": "", "nickname": "", "error": "服务未初始化"}
    
    robot_wxid = _config_manager.robot_wxid
    if not robot_wxid:
        return {"wxid": "", "nickname": "", "error": "机器人wxid未配置"}
    
    try:
        info = await _qianxun_client.get_self_info(robot_wxid)
        if info:
            # 尝试多个可能的字段名
            nickname = (
                info.get("nick") or 
                info.get("nickname") or 
                info.get("nickName") or 
                info.get("name") or 
                robot_wxid
            )
            return {"wxid": robot_wxid, "nickname": nickname}
        return {"wxid": robot_wxid, "nickname": robot_wxid}
    except Exception as e:
        logger.error(f"获取机器人信息失败: {e}")
        return {"wxid": robot_wxid, "nickname": robot_wxid, "error": str(e)}


# ============ 群发API ============

class BroadcastTextRequest(BaseModel):
    """群发文本请求"""
    targets: List[str]  # 目标wxid列表
    message: str  # 消息内容


class BroadcastImageRequest(BaseModel):
    """群发图片请求"""
    targets: List[str]  # 目标wxid列表
    image_path: str  # 图片路径（本地路径、网络直链或base64）
    file_name: str = ""  # 保存文件名（网络直链时必填）


class BroadcastFileRequest(BaseModel):
    """群发文件请求"""
    targets: List[str]  # 目标wxid列表
    file_path: str  # 文件路径
    file_name: str = ""  # 保存文件名


class BroadcastShareUrlRequest(BaseModel):
    """群发分享链接请求"""
    targets: List[str]  # 目标wxid列表
    title: str  # 标题
    content: str  # 内容描述
    jump_url: str  # 跳转地址
    thumb_path: str = ""  # 缩略图路径
    app: str = ""  # 小尾巴


class BroadcastAppletRequest(BaseModel):
    """群发小程序请求"""
    targets: List[str]  # 目标wxid列表
    title: str  # 标题
    content: str  # 内容描述
    jump_path: str  # 跳转路径
    gh: str  # 小程序gh
    thumb_path: str = ""  # 缩略图路径


@router.post("/broadcast/text")
async def broadcast_text(data: BroadcastTextRequest):
    """群发文本消息（通过消息队列）"""
    if not _qianxun_client or not _config_manager:
        raise HTTPException(status_code=503, detail="服务未初始化")
    
    if not _message_queue:
        raise HTTPException(status_code=503, detail="消息队列未初始化")
    
    robot_wxid = _config_manager.robot_wxid
    if not robot_wxid:
        raise HTTPException(status_code=400, detail="机器人wxid未配置")
    
    if not data.targets:
        raise HTTPException(status_code=400, detail="请选择发送目标")
    
    if not data.message.strip():
        raise HTTPException(status_code=400, detail="消息内容不能为空")
    
    # 将所有消息加入队列
    message_ids = []
    for target in data.targets:
        msg_id = await _message_queue.enqueue_text(
            _qianxun_client,
            robot_wxid,
            target,
            data.message,
            priority=MessagePriority.LOW  # 群发使用低优先级
        )
        message_ids.append({"target": target, "message_id": msg_id})
    
    # 记录群发日志
    if _log_collector:
        await _log_collector.add_log("system", {
            "message": f"群发文本已加入队列: {len(data.targets)} 条消息",
            "details": {"type": "text", "total": len(data.targets)}
        })
    
    return {
        "status": "queued",
        "total": len(data.targets),
        "queue_size": _message_queue.queue_size,
        "message_ids": message_ids,
        "message": f"已将 {len(data.targets)} 条消息加入发送队列"
    }


@router.post("/broadcast/image")
async def broadcast_image(data: BroadcastImageRequest):
    """群发图片（通过消息队列）"""
    if not _qianxun_client or not _config_manager:
        raise HTTPException(status_code=503, detail="服务未初始化")
    
    if not _message_queue:
        raise HTTPException(status_code=503, detail="消息队列未初始化")
    
    robot_wxid = _config_manager.robot_wxid
    if not robot_wxid:
        raise HTTPException(status_code=400, detail="机器人wxid未配置")
    
    if not data.targets:
        raise HTTPException(status_code=400, detail="请选择发送目标")
    
    if not data.image_path.strip():
        raise HTTPException(status_code=400, detail="图片路径不能为空")
    
    # 将所有消息加入队列
    message_ids = []
    for target in data.targets:
        msg_id = await _message_queue.enqueue_image(
            _qianxun_client,
            robot_wxid,
            target,
            data.image_path,
            data.file_name,
            priority=MessagePriority.LOW
        )
        message_ids.append({"target": target, "message_id": msg_id})
    
    # 记录群发日志
    if _log_collector:
        await _log_collector.add_log("system", {
            "message": f"群发图片已加入队列: {len(data.targets)} 条消息",
            "details": {"type": "image", "total": len(data.targets), "path": data.image_path[:50]}
        })
    
    return {
        "status": "queued",
        "total": len(data.targets),
        "queue_size": _message_queue.queue_size,
        "message_ids": message_ids,
        "message": f"已将 {len(data.targets)} 条消息加入发送队列"
    }


@router.post("/broadcast/file")
async def broadcast_file(data: BroadcastFileRequest):
    """群发文件（通过消息队列）"""
    if not _qianxun_client or not _config_manager:
        raise HTTPException(status_code=503, detail="服务未初始化")
    
    if not _message_queue:
        raise HTTPException(status_code=503, detail="消息队列未初始化")
    
    robot_wxid = _config_manager.robot_wxid
    if not robot_wxid:
        raise HTTPException(status_code=400, detail="机器人wxid未配置")
    
    if not data.targets:
        raise HTTPException(status_code=400, detail="请选择发送目标")
    
    if not data.file_path.strip():
        raise HTTPException(status_code=400, detail="文件路径不能为空")
    
    # 提前捕获文件路径和文件名，避免闭包问题
    file_path = data.file_path
    file_name = data.file_name
    
    # 将所有消息加入队列
    message_ids = []
    for target in data.targets:
        # 使用默认参数捕获当前值，避免闭包延迟绑定问题
        async def send_file(t=target, fp=file_path, fn=file_name):
            return await _qianxun_client.send_file(robot_wxid, t, fp, fn)
        
        msg_id = await _message_queue.enqueue(
            send_func=send_file,
            priority=MessagePriority.LOW,
            message_type="file",
            target=target,
            content_preview=file_path
        )
        message_ids.append({"target": target, "message_id": msg_id})
    
    # 记录群发日志
    if _log_collector:
        await _log_collector.add_log("system", {
            "message": f"群发文件已加入队列: {len(data.targets)} 条消息",
            "details": {"type": "file", "total": len(data.targets), "path": data.file_path[:50]}
        })
    
    return {
        "status": "queued",
        "total": len(data.targets),
        "queue_size": _message_queue.queue_size,
        "message_ids": message_ids,
        "message": f"已将 {len(data.targets)} 条消息加入发送队列"
    }


@router.post("/broadcast/share_url")
async def broadcast_share_url(data: BroadcastShareUrlRequest):
    """群发分享链接（通过消息队列）"""
    if not _qianxun_client or not _config_manager:
        raise HTTPException(status_code=503, detail="服务未初始化")
    
    if not _message_queue:
        raise HTTPException(status_code=503, detail="消息队列未初始化")
    
    robot_wxid = _config_manager.robot_wxid
    if not robot_wxid:
        raise HTTPException(status_code=400, detail="机器人wxid未配置")
    
    if not data.targets:
        raise HTTPException(status_code=400, detail="请选择发送目标")
    
    if not data.title.strip():
        raise HTTPException(status_code=400, detail="标题不能为空")
    
    if not data.jump_url.strip():
        raise HTTPException(status_code=400, detail="跳转地址不能为空")
    
    # 将所有消息加入队列
    message_ids = []
    for target in data.targets:
        async def send_share(t=target):
            return await _qianxun_client.send_share_url(
                robot_wxid, t, data.title, data.content,
                data.jump_url, data.thumb_path, data.app
            )
        
        msg_id = await _message_queue.enqueue(
            send_func=send_share,
            priority=MessagePriority.LOW,
            message_type="share_url",
            target=target,
            content_preview=data.title
        )
        message_ids.append({"target": target, "message_id": msg_id})
    
    # 记录群发日志
    if _log_collector:
        await _log_collector.add_log("system", {
            "message": f"群发链接已加入队列: {len(data.targets)} 条消息",
            "details": {"type": "share_url", "total": len(data.targets), "title": data.title}
        })
    
    return {
        "status": "queued",
        "total": len(data.targets),
        "queue_size": _message_queue.queue_size,
        "message_ids": message_ids,
        "message": f"已将 {len(data.targets)} 条消息加入发送队列"
    }


@router.post("/broadcast/applet")
async def broadcast_applet(data: BroadcastAppletRequest):
    """群发小程序（通过消息队列）"""
    if not _qianxun_client or not _config_manager:
        raise HTTPException(status_code=503, detail="服务未初始化")
    
    if not _message_queue:
        raise HTTPException(status_code=503, detail="消息队列未初始化")
    
    robot_wxid = _config_manager.robot_wxid
    if not robot_wxid:
        raise HTTPException(status_code=400, detail="机器人wxid未配置")
    
    if not data.targets:
        raise HTTPException(status_code=400, detail="请选择发送目标")
    
    if not data.title.strip():
        raise HTTPException(status_code=400, detail="标题不能为空")
    
    if not data.gh.strip():
        raise HTTPException(status_code=400, detail="小程序gh不能为空")
    
    # 将所有消息加入队列
    message_ids = []
    for target in data.targets:
        async def send_applet(t=target):
            return await _qianxun_client.send_applet(
                robot_wxid, t, data.title, data.content,
                data.jump_path, data.gh, data.thumb_path
            )
        
        msg_id = await _message_queue.enqueue(
            send_func=send_applet,
            priority=MessagePriority.LOW,
            message_type="applet",
            target=target,
            content_preview=data.title
        )
        message_ids.append({"target": target, "message_id": msg_id})
    
    # 记录群发日志
    if _log_collector:
        await _log_collector.add_log("system", {
            "message": f"群发小程序已加入队列: {len(data.targets)} 条消息",
            "details": {"type": "applet", "total": len(data.targets), "title": data.title, "gh": data.gh}
        })
    
    return {
        "status": "queued",
        "total": len(data.targets),
        "queue_size": _message_queue.queue_size,
        "message_ids": message_ids,
        "message": f"已将 {len(data.targets)} 条消息加入发送队列"
    }


# ============ 节假日API ============

# 尝试导入中国节假日库
try:
    import chinese_calendar
    HAS_CHINESE_CALENDAR = True
except ImportError:
    HAS_CHINESE_CALENDAR = False


@router.get("/holidays/{year}")
async def get_holidays(year: int):
    """获取指定年份的中国法定节假日列表
    
    Args:
        year: 年份，如 2026
        
    Returns:
        {
            "year": 2026,
            "holidays": ["2026-01-01", "2026-01-28", ...],  # 节假日列表
            "workdays": ["2026-01-25", ...],  # 调休补班日列表
            "available": true  # 是否有节假日数据
        }
    """
    if not HAS_CHINESE_CALENDAR:
        return {
            "year": year,
            "holidays": [],
            "workdays": [],
            "available": False,
            "error": "chinese-calendar 库未安装"
        }
    
    try:
        from datetime import date, timedelta
        
        holidays: List[str] = []
        workdays: List[str] = []
        
        # 遍历全年每一天
        start_date = date(year, 1, 1)
        end_date = date(year, 12, 31)
        current = start_date
        
        while current <= end_date:
            try:
                is_holiday = chinese_calendar.is_holiday(current)
                is_workday = chinese_calendar.is_workday(current)
                weekday = current.weekday()
                
                if is_holiday:
                    holidays.append(current.isoformat())
                elif is_workday and weekday >= 5:
                    # 周末但是工作日 = 调休补班
                    workdays.append(current.isoformat())
            except Exception:
                pass
            current += timedelta(days=1)
        
        return {
            "year": year,
            "holidays": holidays,
            "workdays": workdays,
            "available": True
        }
    except Exception as e:
        logger.error(f"获取节假日数据失败: {e}")
        return {
            "year": year,
            "holidays": [],
            "workdays": [],
            "available": False,
            "error": str(e)
        }
