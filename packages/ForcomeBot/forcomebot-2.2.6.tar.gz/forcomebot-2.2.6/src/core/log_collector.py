"""日志收集器 - 收集消息处理日志，支持WebSocket推送

功能：
- 日志添加（deque + maxlen=100）
- 日志查询（支持类型筛选）
- 订阅/取消订阅（asyncio.Queue）
"""
import asyncio
import logging
from collections import deque
from datetime import datetime
from typing import Optional, List, Dict, Any, Set

logger = logging.getLogger(__name__)


class LogCollector:
    """日志收集器"""
    
    def __init__(self, max_logs: int = 100):
        """初始化日志收集器
        
        Args:
            max_logs: 最大日志条数
        """
        self._logs: deque = deque(maxlen=max_logs)
        self._subscribers: Set[asyncio.Queue] = set()
        self._lock = asyncio.Lock()
    
    async def add_log(self, log_type: str, content: Dict[str, Any]):
        """添加日志并推送给订阅者
        
        Args:
            log_type: 日志类型（private, group, error, system）
            content: 日志内容
        """
        log_entry = {
            "id": f"{datetime.now().timestamp():.6f}",
            "timestamp": datetime.now().isoformat(),
            "type": log_type,
            **content
        }
        
        async with self._lock:
            self._logs.append(log_entry)
        
        # 推送给所有订阅者
        await self._broadcast(log_entry)
    
    async def _broadcast(self, log_entry: Dict[str, Any]):
        """广播日志给所有订阅者"""
        dead_subscribers = set()
        
        for queue in self._subscribers.copy():
            try:
                # 使用 put_nowait 避免阻塞
                queue.put_nowait(log_entry)
            except asyncio.QueueFull:
                # 队列满了，跳过这条日志
                logger.debug("订阅者队列已满，跳过日志")
            except Exception as e:
                logger.debug(f"推送日志失败: {e}")
                dead_subscribers.add(queue)
        
        # 清理失效的订阅者
        for queue in dead_subscribers:
            self._subscribers.discard(queue)
    
    def get_logs(self, log_type: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """获取日志列表
        
        Args:
            log_type: 日志类型筛选（None表示全部）
            limit: 返回条数限制
            
        Returns:
            日志列表（最新的在前）
        """
        logs = list(self._logs)
        
        # 按类型筛选
        if log_type:
            logs = [log for log in logs if log.get("type") == log_type]
        
        # 返回最新的日志（倒序）
        logs = list(reversed(logs))
        
        # 限制条数
        return logs[:limit]
    
    def subscribe(self, max_queue_size: int = 100) -> asyncio.Queue:
        """订阅日志更新
        
        Args:
            max_queue_size: 队列最大大小
            
        Returns:
            用于接收日志的队列
        """
        queue = asyncio.Queue(maxsize=max_queue_size)
        self._subscribers.add(queue)
        logger.debug(f"新增日志订阅者，当前共 {len(self._subscribers)} 个")
        return queue
    
    def unsubscribe(self, queue: asyncio.Queue):
        """取消订阅
        
        Args:
            queue: 要取消的订阅队列
        """
        self._subscribers.discard(queue)
        logger.debug(f"移除日志订阅者，当前共 {len(self._subscribers)} 个")
    
    def clear(self):
        """清空所有日志"""
        self._logs.clear()
        logger.info("日志已清空")
    
    @property
    def subscriber_count(self) -> int:
        """获取当前订阅者数量"""
        return len(self._subscribers)
    
    @property
    def log_count(self) -> int:
        """获取当前日志数量"""
        return len(self._logs)


# 便捷函数，用于记录不同类型的日志
async def log_private_message(collector: LogCollector, from_wxid: str, content: str, 
                              status: str = "received", error: Optional[str] = None):
    """记录私聊消息日志"""
    await collector.add_log("private", {
        "from_wxid": from_wxid,
        "content": content[:200],  # 截断过长内容
        "status": status,
        "error": error
    })


async def log_group_message(collector: LogCollector, group_wxid: str, sender_wxid: str,
                            content: str, status: str = "received", error: Optional[str] = None):
    """记录群聊消息日志"""
    await collector.add_log("group", {
        "group_wxid": group_wxid,
        "sender_wxid": sender_wxid,
        "content": content[:200],  # 截断过长内容
        "status": status,
        "error": error
    })


async def log_error(collector: LogCollector, message: str, details: Optional[Dict] = None):
    """记录错误日志"""
    await collector.add_log("error", {
        "message": message,
        "details": details
    })


async def log_system(collector: LogCollector, message: str, details: Optional[Dict] = None):
    """记录系统日志"""
    await collector.add_log("system", {
        "message": message,
        "details": details
    })
