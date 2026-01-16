"""统一消息发送队列

功能：
- 所有消息发送请求统一排队
- 随机延迟发送，避免并发过高
- 支持优先级（高优先级插队）
- 失败重试机制
- 队列状态监控
"""
import asyncio
import logging
import random
import time
from dataclasses import dataclass, field
from enum import IntEnum
from typing import Any, Callable, Awaitable, Optional, Dict, List
from datetime import datetime

logger = logging.getLogger(__name__)


class MessagePriority(IntEnum):
    """消息优先级（数字越小优先级越高）"""
    HIGH = 1      # 普通回复消息（用户触发）
    NORMAL = 5    # 定时任务消息
    LOW = 10      # 群发消息


@dataclass(order=True)
class QueuedMessage:
    """队列中的消息"""
    priority: int
    timestamp: float = field(compare=False)
    message_id: str = field(compare=False)
    send_func: Callable[[], Awaitable[bool]] = field(compare=False)
    message_type: str = field(compare=False, default="unknown")
    target: str = field(compare=False, default="")
    content_preview: str = field(compare=False, default="")
    retry_count: int = field(compare=False, default=0)
    max_retries: int = field(compare=False, default=2)
    callback: Optional[Callable[[bool, str], Awaitable[None]]] = field(compare=False, default=None)


class MessageQueue:
    """统一消息发送队列"""
    
    def __init__(
        self,
        min_interval: float = 1.0,
        max_interval: float = 3.0,
        batch_min_interval: float = 2.0,
        batch_max_interval: float = 5.0,
        max_queue_size: int = 1000
    ):
        """初始化消息队列
        
        Args:
            min_interval: 高优先级消息最小间隔（秒）
            max_interval: 高优先级消息最大间隔（秒）
            batch_min_interval: 低优先级消息最小间隔（秒）
            batch_max_interval: 低优先级消息最大间隔（秒）
            max_queue_size: 队列最大容量
        """
        self._queue: asyncio.PriorityQueue = asyncio.PriorityQueue(maxsize=max_queue_size)
        self._min_interval = min_interval
        self._max_interval = max_interval
        self._batch_min_interval = batch_min_interval
        self._batch_max_interval = batch_max_interval
        self._max_queue_size = max_queue_size
        
        self._running = False
        self._worker_task: Optional[asyncio.Task] = None
        self._last_send_time: float = 0
        self._message_counter: int = 0
        
        # 统计信息
        self._stats = {
            "total_sent": 0,
            "total_failed": 0,
            "total_retried": 0,
            "started_at": None
        }
        
        # 最近发送记录（用于监控）
        self._recent_sends: List[Dict[str, Any]] = []
        self._max_recent = 50
    
    def update_config(
        self,
        min_interval: float = None,
        max_interval: float = None,
        batch_min_interval: float = None,
        batch_max_interval: float = None
    ):
        """更新配置"""
        if min_interval is not None:
            self._min_interval = min_interval
        if max_interval is not None:
            self._max_interval = max_interval
        if batch_min_interval is not None:
            self._batch_min_interval = batch_min_interval
        if batch_max_interval is not None:
            self._batch_max_interval = batch_max_interval
        logger.info(f"消息队列配置已更新: interval={self._min_interval}-{self._max_interval}s, "
                   f"batch={self._batch_min_interval}-{self._batch_max_interval}s")
    
    async def start(self):
        """启动队列处理"""
        if self._running:
            return
        
        self._running = True
        self._stats["started_at"] = datetime.now().isoformat()
        self._worker_task = asyncio.create_task(self._worker())
        logger.info("消息队列已启动")
    
    async def stop(self):
        """停止队列处理"""
        self._running = False
        if self._worker_task:
            self._worker_task.cancel()
            try:
                await self._worker_task
            except asyncio.CancelledError:
                pass
        logger.info(f"消息队列已停止，统计: 发送={self._stats['total_sent']}, "
                   f"失败={self._stats['total_failed']}, 重试={self._stats['total_retried']}")
    
    def _generate_message_id(self) -> str:
        """生成消息ID"""
        self._message_counter += 1
        return f"msg_{int(time.time())}_{self._message_counter}"
    
    async def enqueue(
        self,
        send_func: Callable[[], Awaitable[bool]],
        priority: MessagePriority = MessagePriority.NORMAL,
        message_type: str = "unknown",
        target: str = "",
        content_preview: str = "",
        max_retries: int = 2,
        callback: Optional[Callable[[bool, str], Awaitable[None]]] = None
    ) -> str:
        """添加消息到队列
        
        Args:
            send_func: 发送函数，返回是否成功
            priority: 消息优先级
            message_type: 消息类型（text, image, file 等）
            target: 目标wxid
            content_preview: 内容预览（用于日志）
            max_retries: 最大重试次数
            callback: 发送完成回调，参数为 (success, message_id)
            
        Returns:
            消息ID
        """
        message_id = self._generate_message_id()
        
        msg = QueuedMessage(
            priority=priority,
            timestamp=time.time(),
            message_id=message_id,
            send_func=send_func,
            message_type=message_type,
            target=target,
            content_preview=content_preview[:50] if content_preview else "",
            max_retries=max_retries,
            callback=callback
        )
        
        try:
            self._queue.put_nowait(msg)
            logger.debug(f"消息入队: {message_id}, 优先级={priority}, 类型={message_type}, "
                        f"目标={target}, 队列长度={self._queue.qsize()}")
            return message_id
        except asyncio.QueueFull:
            logger.error(f"消息队列已满，丢弃消息: {message_id}")
            if callback:
                await callback(False, message_id)
            return message_id
    
    async def enqueue_text(
        self,
        qianxun_client,
        robot_wxid: str,
        target: str,
        message: str,
        priority: MessagePriority = MessagePriority.NORMAL,
        callback: Optional[Callable[[bool, str], Awaitable[None]]] = None
    ) -> str:
        """便捷方法：添加文本消息到队列"""
        async def send():
            return await qianxun_client.send_text(robot_wxid, target, message)
        
        return await self.enqueue(
            send_func=send,
            priority=priority,
            message_type="text",
            target=target,
            content_preview=message,
            callback=callback
        )
    
    async def enqueue_image(
        self,
        qianxun_client,
        robot_wxid: str,
        target: str,
        image_path: str,
        file_name: str = "",
        priority: MessagePriority = MessagePriority.NORMAL,
        callback: Optional[Callable[[bool, str], Awaitable[None]]] = None
    ) -> str:
        """便捷方法：添加图片消息到队列"""
        async def send():
            return await qianxun_client.send_image(robot_wxid, target, image_path, file_name)
        
        return await self.enqueue(
            send_func=send,
            priority=priority,
            message_type="image",
            target=target,
            content_preview=image_path,
            callback=callback
        )
    
    async def _worker(self):
        """队列处理工作线程"""
        logger.info("消息队列工作线程已启动")
        
        while self._running:
            try:
                # 等待消息，超时1秒检查运行状态
                try:
                    msg: QueuedMessage = await asyncio.wait_for(
                        self._queue.get(), timeout=1.0
                    )
                except asyncio.TimeoutError:
                    continue
                
                # 计算延迟
                delay = self._calculate_delay(msg.priority)
                
                # 等待延迟时间
                elapsed = time.time() - self._last_send_time
                if elapsed < delay:
                    wait_time = delay - elapsed
                    logger.debug(f"等待 {wait_time:.2f}s 后发送: {msg.message_id}")
                    await asyncio.sleep(wait_time)
                
                # 发送消息
                success = await self._send_message(msg)
                
                # 更新最后发送时间
                self._last_send_time = time.time()
                
                # 标记任务完成
                self._queue.task_done()
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"消息队列工作线程异常: {e}", exc_info=True)
                await asyncio.sleep(1)
        
        logger.info("消息队列工作线程已停止")
    
    def _calculate_delay(self, priority: int) -> float:
        """根据优先级计算延迟时间"""
        if priority <= MessagePriority.HIGH:
            # 高优先级：较短延迟
            return random.uniform(self._min_interval, self._max_interval)
        else:
            # 普通/低优先级：较长延迟
            return random.uniform(self._batch_min_interval, self._batch_max_interval)
    
    async def _send_message(self, msg: QueuedMessage) -> bool:
        """发送单条消息"""
        try:
            success = await msg.send_func()
            
            # 记录发送结果
            record = {
                "message_id": msg.message_id,
                "type": msg.message_type,
                "target": msg.target,
                "priority": msg.priority,
                "success": success,
                "retry_count": msg.retry_count,
                "sent_at": datetime.now().isoformat()
            }
            self._recent_sends.append(record)
            if len(self._recent_sends) > self._max_recent:
                self._recent_sends.pop(0)
            
            if success:
                self._stats["total_sent"] += 1
                logger.info(f"消息发送成功: {msg.message_id} -> {msg.target}")
                
                if msg.callback:
                    await msg.callback(True, msg.message_id)
                return True
            else:
                # 发送失败，尝试重试
                return await self._handle_failure(msg, "发送返回失败")
                
        except Exception as e:
            logger.error(f"消息发送异常: {msg.message_id}, {e}")
            return await self._handle_failure(msg, str(e))
    
    async def _handle_failure(self, msg: QueuedMessage, error: str) -> bool:
        """处理发送失败"""
        if msg.retry_count < msg.max_retries:
            # 重试
            msg.retry_count += 1
            self._stats["total_retried"] += 1
            logger.warning(f"消息发送失败，重试 {msg.retry_count}/{msg.max_retries}: "
                          f"{msg.message_id}, 错误: {error}")
            
            # 重新入队（降低优先级避免阻塞其他消息）
            msg.priority = max(msg.priority, MessagePriority.LOW)
            try:
                self._queue.put_nowait(msg)
            except asyncio.QueueFull:
                logger.error(f"重试入队失败，队列已满: {msg.message_id}")
                self._stats["total_failed"] += 1
                if msg.callback:
                    await msg.callback(False, msg.message_id)
            return False
        else:
            # 超过重试次数
            self._stats["total_failed"] += 1
            logger.error(f"消息发送最终失败: {msg.message_id} -> {msg.target}, 错误: {error}")
            
            if msg.callback:
                await msg.callback(False, msg.message_id)
            return False
    
    def get_status(self) -> Dict[str, Any]:
        """获取队列状态"""
        return {
            "running": self._running,
            "queue_size": self._queue.qsize(),
            "max_queue_size": self._max_queue_size,
            "config": {
                "min_interval": self._min_interval,
                "max_interval": self._max_interval,
                "batch_min_interval": self._batch_min_interval,
                "batch_max_interval": self._batch_max_interval
            },
            "stats": self._stats.copy(),
            "recent_sends": self._recent_sends[-10:]  # 最近10条
        }
    
    @property
    def queue_size(self) -> int:
        """当前队列长度"""
        return self._queue.qsize()
    
    @property
    def is_running(self) -> bool:
        """是否运行中"""
        return self._running
