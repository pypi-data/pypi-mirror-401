"""LangBot OneBot v11 WebSocket 客户端 - 带指数退避重连

重构版本：
- 实现指数退避重连（1s→2s→4s→...→60s）
- 集成 StateStore（替换内部映射）
- 添加 update_connection() 方法（配置热更新）
- 保持所有原有方法签名不变
"""
import asyncio
import json
import logging
import time
from typing import Optional, Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from ..core.state_store import StateStore

logger = logging.getLogger(__name__)


class LangBotClient:
    """
    OneBot v11 反向 WebSocket 客户端（带指数退避重连）
    连接到 LangBot 的 aiocqhttp 适配器
    """
    
    def __init__(
        self, 
        host: str = "127.0.0.1", 
        port: int = 2280, 
        access_token: str = "",
        initial_reconnect_delay: float = 1.0,
        max_reconnect_delay: float = 60.0
    ):
        """初始化LangBot客户端
        
        Args:
            host: LangBot主机地址
            port: LangBot端口
            access_token: 访问令牌
            initial_reconnect_delay: 初始重连延迟（秒），默认1秒
            max_reconnect_delay: 最大重连延迟（秒），默认60秒
        """
        self.host = host
        self.port = port
        self.access_token = access_token
        self.ws = None
        self._connected = False
        self._reconnecting = False
        self._event_callback: Optional[Callable] = None
        self._receive_task: Optional[asyncio.Task] = None
        self._reconnect_task: Optional[asyncio.Task] = None
        self._self_id = "10000"  # 模拟的机器人ID
        
        # 指数退避重连配置
        self._initial_reconnect_delay = initial_reconnect_delay
        self._max_reconnect_delay = max_reconnect_delay
        self._current_reconnect_delay = initial_reconnect_delay
        
        # StateStore 集成（可选）
        self._state_store: Optional["StateStore"] = None
        
        # 内部映射（当没有 StateStore 时使用）
        self._group_id_mapping: dict = {}
        self._message_user_mapping: dict = {}

    def set_state_store(self, store: "StateStore"):
        """设置状态存储器
        
        Args:
            store: StateStore实例
        """
        self._state_store = store
        logger.info("LangBot客户端已集成StateStore")
    
    async def update_connection(self, host: str, port: int, access_token: str = ""):
        """更新连接配置并重连（配置热更新）
        
        Args:
            host: 新的主机地址
            port: 新的端口
            access_token: 新的访问令牌
        """
        logger.info(f"更新LangBot连接配置: {host}:{port}")
        self.host = host
        self.port = port
        self.access_token = access_token
        
        # 关闭现有连接
        await self.close()
        
        # 重置重连延迟
        self._current_reconnect_delay = self._initial_reconnect_delay
        
        # 重新连接
        await self.connect()
    
    @property
    def is_connected(self) -> bool:
        """是否已连接"""
        return self._connected
    
    @property
    def is_reconnecting(self) -> bool:
        """是否正在重连"""
        return self._reconnecting
    
    async def connect(self) -> bool:
        """连接到 LangBot
        
        Returns:
            是否连接成功
        """
        try:
            import websockets
            
            ws_url = f"ws://{self.host}:{self.port}/ws"
            logger.info(f"正在连接 LangBot: {ws_url}")
            
            # aiocqhttp 需要特定的请求头
            headers = {
                "X-Self-ID": self._self_id,
                "X-Client-Role": "Universal"  # 同时处理事件和API
            }
            
            if self.access_token:
                headers["Authorization"] = f"Bearer {self.access_token}"
            
            logger.info(f"连接头: {headers}")
            
            # 尝试不同版本的 websockets 库
            try:
                # websockets >= 10.0
                self.ws = await websockets.connect(
                    ws_url,
                    additional_headers=headers
                )
            except TypeError:
                try:
                    # websockets 旧版本
                    self.ws = await websockets.connect(
                        ws_url,
                        extra_headers=headers
                    )
                except TypeError:
                    # 更旧的版本
                    self.ws = await websockets.connect(ws_url)
            
            self._connected = True
            self._reconnecting = False
            # 重置重连延迟
            self._current_reconnect_delay = self._initial_reconnect_delay
            
            logger.info(f"WebSocket 连接成功: {ws_url}")
            
            # 发送生命周期连接事件
            await self._send_lifecycle_event()
            
            # 启动消息接收任务
            self._receive_task = asyncio.create_task(self._receive_loop())
            
            logger.info("已连接到 LangBot (OneBot v11)")
            return True
            
        except Exception as e:
            logger.error(f"连接 LangBot 失败: {e}", exc_info=True)
            self._connected = False
            return False

    async def reconnect(self):
        """指数退避重连
        
        重连延迟按指数增长：1s→2s→4s→8s→...→60s（最大）
        连接成功后重置延迟为初始值
        """
        if self._reconnecting:
            logger.debug("已在重连中，跳过")
            return
        
        self._reconnecting = True
        
        while not self._connected:
            try:
                logger.info(f"尝试重连 LangBot...")
                success = await self.connect()
                
                if success:
                    logger.info("重连成功")
                    self._reconnecting = False
                    return
                    
            except Exception as e:
                logger.error(f"重连失败: {e}")
            
            # 等待后重试
            logger.info(f"将在 {self._current_reconnect_delay} 秒后重试...")
            await asyncio.sleep(self._current_reconnect_delay)
            
            # 指数退避，最大不超过 max_reconnect_delay
            self._current_reconnect_delay = min(
                self._current_reconnect_delay * 2, 
                self._max_reconnect_delay
            )
        
        self._reconnecting = False
    
    def get_reconnect_delay(self) -> float:
        """获取当前重连延迟（用于测试）
        
        Returns:
            当前重连延迟（秒）
        """
        return self._current_reconnect_delay
    
    async def _send_lifecycle_event(self):
        """发送生命周期连接事件"""
        event = {
            "time": int(time.time()),
            "self_id": int(self._self_id),
            "post_type": "meta_event",
            "meta_event_type": "lifecycle",
            "sub_type": "connect"
        }
        await self._send(event)
    
    async def _send(self, data: dict):
        """发送数据"""
        if self.ws and self._connected:
            try:
                message = json.dumps(data)
                logger.info(f"WebSocket 发送: {message[:500]}")  # 限制日志长度
                await self.ws.send(message)
            except Exception as e:
                logger.error(f"发送失败: {e}")
                self._connected = False
        else:
            logger.warning(f"WebSocket 未连接，无法发送: connected={self._connected}, ws={self.ws is not None}")
    
    async def _receive_loop(self):
        """接收消息循环"""
        try:
            while self._connected and self.ws:
                try:
                    message = await self.ws.recv()
                    logger.info(f"WebSocket 收到: {message[:500]}")  # 限制日志长度
                    data = json.loads(message)
                    await self._handle_message(data)
                except Exception as e:
                    if self._connected:
                        logger.error(f"接收消息异常: {e}")
                        self._connected = False
                    break
        except asyncio.CancelledError:
            pass
        
        # 连接断开，启动重连
        if not self._connected and not self._reconnecting:
            logger.info("连接断开，启动指数退避重连...")
            self._reconnect_task = asyncio.create_task(self.reconnect())

    async def _handle_message(self, data: dict):
        """处理收到的消息"""
        # 检查是否是 API 调用请求（LangBot 发送消息）
        action = data.get("action")
        if action:
            params = data.get("params", {})
            echo = data.get("echo")
            
            logger.info(f"收到动作: {action}, 参数: {params}")
            
            # 调用回调处理
            result = {}
            if self._event_callback:
                try:
                    result = await self._event_callback(action, params) or {}
                except Exception as e:
                    logger.error(f"处理动作异常: {e}")
            
            # 发送响应
            response = {
                "status": "ok",
                "retcode": 0,
                "data": result
            }
            if echo:
                response["echo"] = echo
            
            await self._send(response)
    
    def set_event_callback(self, callback: Callable):
        """设置事件回调函数"""
        self._event_callback = callback
    
    def get_original_group_id(self, numeric_group_id: str) -> str:
        """获取原始的微信群ID
        
        Args:
            numeric_group_id: 数字格式的群ID
            
        Returns:
            原始微信群ID
        """
        # 优先使用 StateStore
        if self._state_store:
            return self._state_store.get_original_group_id(str(numeric_group_id))
        # 回退到内部映射
        return self._group_id_mapping.get(str(numeric_group_id), numeric_group_id)
    
    def get_user_id_by_message(self, message_id: str) -> Optional[str]:
        """根据消息ID获取发送者user_id
        
        Args:
            message_id: 消息ID
            
        Returns:
            用户ID，不存在则返回None
        """
        # 优先使用 StateStore
        if self._state_store:
            return self._state_store.get_user_by_message(str(message_id))
        # 回退到内部映射
        return self._message_user_mapping.get(str(message_id))
    
    def _save_group_mapping(self, numeric_id: str, original_id: str):
        """保存群ID映射
        
        Args:
            numeric_id: 数字ID
            original_id: 原始微信群ID
        """
        if self._state_store:
            self._state_store.set_group_mapping(str(numeric_id), original_id)
        else:
            self._group_id_mapping[str(numeric_id)] = original_id
    
    def _save_message_user_mapping(self, message_id: str, user_id: str):
        """保存消息-用户映射
        
        Args:
            message_id: 消息ID
            user_id: 用户ID
        """
        if self._state_store:
            self._state_store.set_message_user(str(message_id), user_id)
        else:
            self._message_user_mapping[str(message_id)] = user_id

    async def send_private_message(self, user_id: str, message: str) -> None:
        """发送私聊消息事件到 LangBot
        
        Args:
            user_id: 用户ID
            message: 消息内容
        """
        if not self._connected:
            logger.warning("未连接到 LangBot")
            return
        
        message_id = int(time.time() * 1000) % 2147483647
        
        event = {
            "time": int(time.time()),
            "self_id": int(self._self_id),
            "post_type": "message",
            "message_type": "private",
            "sub_type": "friend",
            "message_id": message_id,
            "user_id": user_id,
            "message": message,
            "raw_message": message,
            "font": 0,
            "sender": {
                "user_id": user_id,
                "nickname": user_id,
                "sex": "unknown",
                "age": 0
            }
        }
        
        await self._send(event)
        logger.info(f"已发送私聊消息事件: [{user_id}] {message}")
    
    async def send_group_message(
        self, 
        group_id: str, 
        user_id: str, 
        message: str, 
        at_bot: bool = False
    ) -> None:
        """发送群聊消息事件到 LangBot
        
        Args:
            group_id: 群ID
            user_id: 发送者ID
            message: 消息内容
            at_bot: 是否标记为@机器人（用于引用消息等场景）
        """
        if not self._connected:
            logger.warning("未连接到 LangBot")
            return
        
        message_id = int(time.time() * 1000) % 2147483647
        
        # 尝试将 group_id 转换为数字（微信群ID格式: 57388706417@chatroom）
        numeric_group_id = group_id
        if '@' in group_id:
            numeric_group_id = group_id.split('@')[0]
        
        try:
            numeric_group_id = int(numeric_group_id)
        except ValueError:
            pass
        
        # 根据 at_bot 参数决定是否添加 @机器人 标记
        cq_message = message
        if at_bot:
            # 引用机器人消息或明确需要触发机器人时，添加@标记
            cq_message = f'[CQ:at,qq={self._self_id}] {message}'
        
        event = {
            "time": int(time.time()),
            "self_id": int(self._self_id),
            "post_type": "message",
            "message_type": "group",
            "sub_type": "normal",
            "message_id": message_id,
            "group_id": numeric_group_id,
            "user_id": user_id,
            "message": cq_message,
            "raw_message": message,
            "font": 0,
            "sender": {
                "user_id": user_id,
                "nickname": user_id,
                "card": "",
                "sex": "unknown",
                "age": 0,
                "area": "",
                "level": "0",
                "role": "member",
                "title": ""
            }
        }
        
        # 保存映射（使用 StateStore 或内部映射）
        self._save_group_mapping(str(numeric_group_id), group_id)
        self._save_message_user_mapping(str(message_id), user_id)
        
        logger.info(f"发送群聊事件到 LangBot: group_id={numeric_group_id}, message={cq_message}")
        await self._send(event)
        logger.info(f"已发送群聊消息事件: [{group_id}][{user_id}] {message}")

    async def health_check(self) -> bool:
        """健康检查
        
        Returns:
            是否健康（已连接）
        """
        return self._connected and self.ws is not None
    
    async def close(self):
        """关闭客户端"""
        self._connected = False
        
        # 取消重连任务
        if self._reconnect_task:
            self._reconnect_task.cancel()
            try:
                await self._reconnect_task
            except asyncio.CancelledError:
                pass
            self._reconnect_task = None
        
        # 取消接收任务
        if self._receive_task:
            self._receive_task.cancel()
            try:
                await self._receive_task
            except asyncio.CancelledError:
                pass
            self._receive_task = None
        
        # 关闭WebSocket
        if self.ws:
            await self.ws.close()
            self.ws = None
        
        self._reconnecting = False

    async def send_private_message_with_image(self, user_id: str, image_url: str) -> None:
        """发送带图片的私聊消息事件到 LangBot
        
        Args:
            user_id: 用户ID
            image_url: 图片URL
        """
        if not self._connected:
            logger.warning("未连接到 LangBot")
            return
        
        message_id = int(time.time() * 1000) % 2147483647
        
        event = {
            "time": int(time.time()),
            "self_id": int(self._self_id),
            "post_type": "message",
            "message_type": "private",
            "sub_type": "friend",
            "message_id": message_id,
            "user_id": user_id,
            "message": [
                {
                    "type": "image", 
                    "data": {
                        "url": image_url
                    }
                }
            ],
            "raw_message": "[图片]",
            "font": 0,
            "sender": {
                "user_id": user_id,
                "nickname": user_id,
                "sex": "unknown",
                "age": 0
            }
        }
        
        logger.info(f"发送私聊图片事件到 LangBot: [{user_id}], url={image_url}")
        await self._send(event)

    async def send_private_message_with_image_and_text(
        self, 
        user_id: str, 
        image_url: str, 
        text: str
    ) -> None:
        """发送带图片和文本的私聊消息事件到 LangBot（用于引用图片场景）
        
        Args:
            user_id: 用户ID
            image_url: 图片URL
            text: 文本内容
        """
        if not self._connected:
            logger.warning("未连接到 LangBot")
            return
        
        message_id = int(time.time() * 1000) % 2147483647
        
        event = {
            "time": int(time.time()),
            "self_id": int(self._self_id),
            "post_type": "message",
            "message_type": "private",
            "sub_type": "friend",
            "message_id": message_id,
            "user_id": user_id,
            "message": [
                {"type": "image", "data": {"url": image_url}},
                {"type": "text", "data": {"text": text}}
            ],
            "raw_message": f"[图片] {text}",
            "font": 0,
            "sender": {
                "user_id": user_id,
                "nickname": user_id,
                "sex": "unknown",
                "age": 0
            }
        }
        
        logger.info(f"发送私聊图片+文本事件到 LangBot: [{user_id}], url={image_url}, text={text}")
        await self._send(event)

    async def send_group_message_with_image(
        self, 
        group_id: str, 
        user_id: str, 
        image_url: str, 
        at_bot: bool = False
    ) -> None:
        """发送带图片的群聊消息事件到 LangBot
        
        Args:
            group_id: 群ID
            user_id: 发送者ID
            image_url: 图片URL
            at_bot: 是否标记为@机器人
        """
        if not self._connected:
            logger.warning("未连接到 LangBot")
            return
        
        message_id = int(time.time() * 1000) % 2147483647
        
        # 转换 group_id
        numeric_group_id = group_id
        if '@' in group_id:
            numeric_group_id = group_id.split('@')[0]
        try:
            numeric_group_id = int(numeric_group_id)
        except ValueError:
            pass
        
        # 保存映射
        self._save_group_mapping(str(numeric_group_id), group_id)
        
        # 构建消息内容
        message_segments = []
        if at_bot:
            message_segments.append({"type": "at", "data": {"qq": str(self._self_id)}})
        message_segments.append({"type": "image", "data": {"url": image_url}})
        
        event = {
            "time": int(time.time()),
            "self_id": int(self._self_id),
            "post_type": "message",
            "message_type": "group",
            "sub_type": "normal",
            "message_id": message_id,
            "group_id": numeric_group_id,
            "user_id": user_id,
            "message": message_segments,
            "raw_message": "[图片]",
            "font": 0,
            "sender": {
                "user_id": user_id,
                "nickname": user_id,
                "card": "",
                "sex": "unknown",
                "age": 0,
                "area": "",
                "level": "0",
                "role": "member",
                "title": ""
            }
        }
        
        logger.info(f"发送群聊图片事件到 LangBot: [{group_id}][{user_id}], url={image_url}, at_bot={at_bot}")
        await self._send(event)

    async def send_group_message_with_image_and_text(
        self, 
        group_id: str, 
        user_id: str, 
        image_url: str, 
        text: str
    ) -> None:
        """发送带图片和文本的群聊消息事件到 LangBot（用于关联图片缓存场景）
        
        Args:
            group_id: 群ID
            user_id: 发送者ID
            image_url: 图片URL
            text: 文本内容
        """
        if not self._connected:
            logger.warning("未连接到 LangBot")
            return
        
        message_id = int(time.time() * 1000) % 2147483647
        
        # 转换 group_id
        numeric_group_id = group_id
        if '@' in group_id:
            numeric_group_id = group_id.split('@')[0]
        try:
            numeric_group_id = int(numeric_group_id)
        except ValueError:
            pass
        
        # 保存映射
        self._save_group_mapping(str(numeric_group_id), group_id)
        self._save_message_user_mapping(str(message_id), user_id)
        
        # 构建消息：@机器人 + 图片 + 文本
        message_segments = [
            {"type": "at", "data": {"qq": str(self._self_id)}},
            {"type": "image", "data": {"url": image_url}},
            {"type": "text", "data": {"text": text}}
        ]
        
        event = {
            "time": int(time.time()),
            "self_id": int(self._self_id),
            "post_type": "message",
            "message_type": "group",
            "sub_type": "normal",
            "message_id": message_id,
            "group_id": numeric_group_id,
            "user_id": user_id,
            "message": message_segments,
            "raw_message": f"[图片] {text}",
            "font": 0,
            "sender": {
                "user_id": user_id,
                "nickname": user_id,
                "card": "",
                "sex": "unknown",
                "age": 0,
                "area": "",
                "level": "0",
                "role": "member",
                "title": ""
            }
        }
        
        logger.info(f"发送群聊图片+文本事件到 LangBot: [{group_id}][{user_id}], url={image_url}, text={text}")
        await self._send(event)
