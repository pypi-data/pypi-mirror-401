"""WebSocket推送模块 - 实时状态更新

功能：
- WebSocketManager 连接管理
- 日志实时推送
- 状态变更推送
"""
import asyncio
import logging
from typing import Set, Optional, Dict, Any, TYPE_CHECKING

from fastapi import WebSocket, WebSocketDisconnect

if TYPE_CHECKING:
    from ..core.log_collector import LogCollector
    from ..clients.langbot import LangBotClient

logger = logging.getLogger(__name__)


class WebSocketManager:
    """WebSocket连接管理器"""
    
    def __init__(self, max_connections: int = 100):
        """初始化WebSocket管理器
        
        Args:
            max_connections: 最大连接数
        """
        self._connections: Set[WebSocket] = set()
        self._max_connections = max_connections
        self._lock = asyncio.Lock()
    
    async def connect(self, websocket: WebSocket) -> bool:
        """接受WebSocket连接
        
        Args:
            websocket: WebSocket连接
            
        Returns:
            是否成功连接
        """
        async with self._lock:
            if len(self._connections) >= self._max_connections:
                logger.warning(f"WebSocket连接数已达上限: {self._max_connections}")
                await websocket.close(code=1013, reason="连接数已达上限")
                return False
            
            await websocket.accept()
            self._connections.add(websocket)
            logger.info(f"WebSocket连接已建立，当前连接数: {len(self._connections)}")
            return True
    
    def disconnect(self, websocket: WebSocket):
        """断开WebSocket连接
        
        Args:
            websocket: WebSocket连接
        """
        self._connections.discard(websocket)
        logger.info(f"WebSocket连接已断开，当前连接数: {len(self._connections)}")
    
    async def broadcast(self, message: Dict[str, Any]):
        """广播消息给所有连接
        
        Args:
            message: 要广播的消息
        """
        if not self._connections:
            return
        
        dead_connections = set()
        
        for ws in self._connections.copy():
            try:
                await ws.send_json(message)
            except Exception as e:
                logger.debug(f"发送WebSocket消息失败: {e}")
                dead_connections.add(ws)
        
        # 清理失效连接
        for ws in dead_connections:
            self._connections.discard(ws)
    
    async def send_to(self, websocket: WebSocket, message: Dict[str, Any]) -> bool:
        """发送消息给指定连接
        
        Args:
            websocket: 目标WebSocket连接
            message: 要发送的消息
            
        Returns:
            是否发送成功
        """
        try:
            await websocket.send_json(message)
            return True
        except Exception as e:
            logger.debug(f"发送WebSocket消息失败: {e}")
            self._connections.discard(websocket)
            return False
    
    @property
    def connection_count(self) -> int:
        """获取当前连接数"""
        return len(self._connections)


# 全局WebSocket管理器实例
ws_manager = WebSocketManager()

# 全局引用（由main.py设置）
_log_collector: Optional["LogCollector"] = None
_langbot_client: Optional["LangBotClient"] = None


def set_websocket_dependencies(
    log_collector: "LogCollector",
    langbot_client: "LangBotClient"
):
    """设置WebSocket依赖
    
    Args:
        log_collector: 日志收集器
        langbot_client: LangBot客户端
    """
    global _log_collector, _langbot_client
    _log_collector = log_collector
    _langbot_client = langbot_client
    logger.info("WebSocket依赖已设置")


async def websocket_endpoint(websocket: WebSocket):
    """WebSocket端点处理函数
    
    处理WebSocket连接，推送日志更新和状态变更
    """
    # 尝试连接
    if not await ws_manager.connect(websocket):
        return
    
    # 订阅日志更新
    log_queue = None
    if _log_collector:
        log_queue = _log_collector.subscribe()
    
    # 启动状态推送任务
    status_task = asyncio.create_task(_push_status_updates(websocket))
    
    try:
        # 发送初始状态
        await _send_initial_status(websocket)
        
        # 主循环：推送日志更新
        while True:
            if log_queue:
                try:
                    # 等待日志更新（带超时，以便检查连接状态）
                    log_entry = await asyncio.wait_for(
                        log_queue.get(), 
                        timeout=30.0
                    )
                    await ws_manager.send_to(websocket, {
                        "type": "log",
                        "data": log_entry
                    })
                except asyncio.TimeoutError:
                    # 发送心跳
                    try:
                        await websocket.send_json({"type": "ping"})
                    except:
                        break
            else:
                # 没有日志收集器，只发送心跳
                await asyncio.sleep(30)
                try:
                    await websocket.send_json({"type": "ping"})
                except:
                    break
                    
    except WebSocketDisconnect:
        logger.debug("WebSocket客户端断开连接")
    except Exception as e:
        logger.error(f"WebSocket处理异常: {e}")
    finally:
        # 取消状态推送任务
        status_task.cancel()
        try:
            await status_task
        except asyncio.CancelledError:
            pass
        
        # 取消日志订阅
        if log_queue and _log_collector:
            _log_collector.unsubscribe(log_queue)
        
        # 断开连接
        ws_manager.disconnect(websocket)


async def _send_initial_status(websocket: WebSocket):
    """发送初始状态
    
    Args:
        websocket: WebSocket连接
    """
    status = _get_current_status()
    await ws_manager.send_to(websocket, {
        "type": "status",
        "data": status
    })


async def _push_status_updates(websocket: WebSocket):
    """定期推送状态更新
    
    Args:
        websocket: WebSocket连接
    """
    last_status = None
    
    try:
        while True:
            await asyncio.sleep(5)  # 每5秒检查一次状态变化
            
            current_status = _get_current_status()
            
            # 只在状态变化时推送
            if current_status != last_status:
                success = await ws_manager.send_to(websocket, {
                    "type": "status",
                    "data": current_status
                })
                if not success:
                    break
                last_status = current_status
                
    except asyncio.CancelledError:
        pass
    except Exception as e:
        logger.debug(f"状态推送任务异常: {e}")


def _get_current_status() -> Dict[str, Any]:
    """获取当前状态
    
    Returns:
        状态字典
    """
    return {
        "langbot_connected": _langbot_client.is_connected if _langbot_client else False,
        "langbot_reconnecting": _langbot_client.is_reconnecting if _langbot_client else False,
        "websocket_connections": ws_manager.connection_count
    }


async def broadcast_status_change(status_type: str, data: Dict[str, Any]):
    """广播状态变更
    
    Args:
        status_type: 状态类型（如 langbot_connected, config_updated）
        data: 状态数据
    """
    await ws_manager.broadcast({
        "type": "status_change",
        "status_type": status_type,
        "data": data
    })


async def broadcast_log(log_entry: Dict[str, Any]):
    """广播日志条目
    
    Args:
        log_entry: 日志条目
    """
    await ws_manager.broadcast({
        "type": "log",
        "data": log_entry
    })
