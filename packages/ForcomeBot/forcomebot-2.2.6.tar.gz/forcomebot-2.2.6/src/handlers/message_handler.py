"""消息处理器 - 重构版本

使用新模块：
- MessageParser 替换内联解析逻辑
- StateStore 替换内部缓存
- ConfigManager 获取配置
- LogCollector 记录消息日志

合并私聊/群聊公共逻辑到 _process_message()
添加异常处理确保不阻塞后续消息
保持所有消息处理逻辑不变
"""
import logging
import re
import asyncio
import random
from typing import Optional, Dict, Any, TYPE_CHECKING

from .message_parser import MessageParser, ParsedMessage
from ..models import QianXunEvent, QianXunCallback, PrivateMsgData, GroupMsgData
from ..core.log_collector import log_private_message, log_group_message, log_error

if TYPE_CHECKING:
    from ..clients.qianxun import QianXunClient
    from ..clients.langbot import LangBotClient
    from ..core.state_store import StateStore
    from ..core.config_manager import ConfigManager
    from ..core.log_collector import LogCollector

logger = logging.getLogger(__name__)


class MessageHandler:
    """消息处理器 - 重构版本"""
    
    def __init__(
        self,
        qianxun_client: "QianXunClient",
        langbot_client: "LangBotClient",
        config_manager: "ConfigManager",
        state_store: "StateStore",
        log_collector: "LogCollector"
    ):
        """初始化消息处理器
        
        Args:
            qianxun_client: 千寻客户端
            langbot_client: LangBot客户端
            config_manager: 配置管理器
            state_store: 状态存储器
            log_collector: 日志收集器
        """
        self.qianxun = qianxun_client
        self.langbot = langbot_client
        self.config_manager = config_manager
        self.state_store = state_store
        self.log_collector = log_collector
        
        # 消息解析器
        self.message_parser = MessageParser(qianxun_client)
        
        # 存储机器人wxid列表和当前机器人wxid
        self.robot_wxids = set()
        self.current_robot_wxid: Optional[str] = None
        
        # 设置 LangBot 回调
        self.langbot.set_event_callback(self._handle_langbot_action)
    
    @property
    def _config(self) -> Dict[str, Any]:
        """获取当前配置"""
        return self.config_manager.config
    
    @property
    def _ignore_wxids(self) -> list:
        """获取忽略的wxid列表"""
        return self.config_manager.get_filter_config().get("ignore_wxids", [])
    
    def _should_ignore_wxid(self, wxid: str) -> bool:
        """检查是否应该忽略该wxid（包括前缀匹配）"""
        from src.core.config_manager import DEFAULT_IGNORE_PREFIXES
        
        # 检查完整wxid匹配
        if wxid in self._ignore_wxids:
            logger.info(f"wxid {wxid} 在忽略列表中")
            return True
        
        # 检查前缀匹配（公众号、服务号等）
        for prefix in DEFAULT_IGNORE_PREFIXES:
            if wxid.startswith(prefix):
                logger.info(f"wxid {wxid} 匹配忽略前缀 {prefix}")
                return True
        
        return False
    
    @property
    def _reply_at_all(self) -> bool:
        """是否回复@所有人"""
        return self.config_manager.get_filter_config().get("reply_at_all", False)
    
    @property
    def _keywords_config(self) -> dict:
        """获取关键词触发配置"""
        return self.config_manager.get_filter_config().get("keywords", {})
    
    @property
    def _group_forward_mode(self) -> str:
        """获取群消息转发模式: strict(严格) 或 all(全部)"""
        return self.config_manager.get_filter_config().get("group_forward_mode", "strict")
    
    @property
    def _rate_limit(self) -> Dict[str, Any]:
        """获取限流配置"""
        return self.config_manager.get_rate_limit_config()
    
    @property
    def _image_cache_ttl(self) -> int:
        """获取图片缓存TTL"""
        return self._config.get('image_cache_ttl', 120)
    
    def _check_keyword_trigger(self, content: str) -> bool:
        """检查消息是否触发关键词
        
        Args:
            content: 消息内容
            
        Returns:
            是否触发关键词
        """
        keywords_config = self._keywords_config
        
        if not keywords_config.get('enabled', False):
            return False
        
        keywords = keywords_config.get('list', [])
        if not keywords:
            return False
        
        match_mode = keywords_config.get('match_mode', 'contains')
        content_lower = content.lower()
        
        for keyword in keywords:
            if not keyword:
                continue
            keyword_lower = keyword.lower()
            
            if match_mode == 'exact':
                if content_lower == keyword_lower:
                    logger.info(f"关键词触发(精确匹配): {keyword}")
                    return True
            elif match_mode == 'startswith':
                if content_lower.startswith(keyword_lower):
                    logger.info(f"关键词触发(开头匹配): {keyword}")
                    return True
            else:  # contains
                if keyword_lower in content_lower:
                    logger.info(f"关键词触发(包含匹配): {keyword}")
                    return True
        
        return False

    async def _random_delay(self):
        """随机延迟，模拟人工操作"""
        min_interval = self._rate_limit.get('min_interval', 1)
        max_interval = self._rate_limit.get('max_interval', 3)
        delay = random.uniform(min_interval, max_interval)
        logger.info(f"限流延迟: {delay:.2f}秒 (配置: {min_interval}-{max_interval}秒)")
        await asyncio.sleep(delay)
    
    async def _send_message_with_split(
        self, 
        robot_wxid: str, 
        to_wxid: str, 
        message: str, 
        at_prefix: str = ""
    ):
        """发送消息，支持按分隔符分段发送
        
        Args:
            robot_wxid: 机器人wxid
            to_wxid: 接收者wxid
            message: 消息内容
            at_prefix: @前缀（如 [@,wxid=xxx,nick=,isAuto=true]）
        """
        split_config = self._config.get('message_split', {})
        split_enabled = split_config.get('enabled', False)
        split_separator = split_config.get('separator', '/!')
        split_min_delay = split_config.get('min_delay', 1)
        split_max_delay = split_config.get('max_delay', 3)
        
        logger.info(f"分段配置: enabled={split_enabled}, separator='{split_separator}', 消息中包含分隔符={split_separator in message}")
        
        if not split_enabled or split_separator not in message:
            # 不启用分段或消息中没有分隔符，直接发送
            full_message = f"{at_prefix} {message}".strip() if at_prefix else message
            await self.qianxun.send_text(robot_wxid, to_wxid, full_message)
            return
        
        # 按分隔符分段
        parts = [p.strip() for p in message.split(split_separator) if p.strip()]
        logger.info(f"消息分段: {len(parts)} 段")
        
        if not parts:
            return
        
        # 第一段带@前缀
        first_message = f"{at_prefix} {parts[0]}".strip() if at_prefix else parts[0]
        await self.qianxun.send_text(robot_wxid, to_wxid, first_message)
        
        # 后续分段随机延迟发送
        for i, part in enumerate(parts[1:], 2):
            delay = random.uniform(split_min_delay, split_max_delay)
            logger.info(f"分段发送第{i}段，延迟 {delay:.1f}秒 (配置: {split_min_delay}-{split_max_delay}秒)")
            await asyncio.sleep(delay)
            await self.qianxun.send_text(robot_wxid, to_wxid, part)
    
    async def _handle_langbot_action(self, action: str, params: dict) -> dict:
        """处理 LangBot 发来的动作（如发送消息）"""
        logger.info(f"LangBot动作: {action}, 参数: {params}")
        
        if action == "send_private_msg":
            user_id = str(params.get("user_id", ""))
            message = self._extract_text_from_message(params.get("message", ""))
            
            # 检查是否应该忽略该用户（防止回复公众号等）
            if user_id and self._should_ignore_wxid(user_id):
                logger.debug(f"忽略发送私聊消息给: {user_id}")
                return {"message_id": 0}
            
            if user_id and message and self.current_robot_wxid:
                await self._random_delay()
                await self._send_message_with_split(self.current_robot_wxid, user_id, message)
                return {"message_id": 0}
        
        elif action == "send_group_msg":
            group_id = str(params.get("group_id", ""))
            message = self._extract_text_from_message(params.get("message", ""))
            
            if group_id and message and self.current_robot_wxid:
                # 从StateStore获取原始的微信群ID
                original_group_id = self.state_store.get_original_group_id(group_id)
                # 获取需要@的用户（从reply消息中提取）
                at_user = self._get_reply_user(params.get("message", []))
                at_prefix = f"[@,wxid={at_user},nick=,isAuto=true]" if at_user else ""
                await self._random_delay()
                await self._send_message_with_split(
                    self.current_robot_wxid, original_group_id, message, at_prefix
                )
                return {"message_id": 0}
        
        elif action == "send_msg":
            message_type = params.get("message_type", "private")
            user_id = str(params.get("user_id", ""))
            group_id = str(params.get("group_id", ""))
            message = self._extract_text_from_message(params.get("message", ""))
            
            # 检查是否应该忽略该用户（防止回复公众号等）
            if user_id and self._should_ignore_wxid(user_id):
                logger.info(f"已拦截发送消息给被忽略用户: {user_id}")
                return {"message_id": 0}
            
            if message and self.current_robot_wxid:
                await self._random_delay()
                if message_type == "group" and group_id:
                    original_group_id = self.state_store.get_original_group_id(group_id)
                    at_user = self._get_reply_user(params.get("message", []))
                    at_prefix = f"[@,wxid={at_user},nick=,isAuto=true]" if at_user else ""
                    await self._send_message_with_split(
                        self.current_robot_wxid, original_group_id, message, at_prefix
                    )
                elif user_id:
                    await self._send_message_with_split(self.current_robot_wxid, user_id, message)
                return {"message_id": 0}
        
        elif action == "get_login_info":
            return {
                "user_id": self.current_robot_wxid or "qianxun_bot",
                "nickname": "千寻机器人"
            }
        
        return {}
    
    def _extract_text_from_message(self, message) -> str:
        """从 OneBot 消息格式中提取文本"""
        if isinstance(message, str):
            # 移除 CQ 码
            text = re.sub(r'\[CQ:[^\]]+\]', '', message)
            return text.strip()
        elif isinstance(message, list):
            # 消息段数组格式
            texts = []
            for seg in message:
                if isinstance(seg, dict) and seg.get("type") == "text":
                    texts.append(seg.get("data", {}).get("text", ""))
            return "".join(texts).strip()
        return str(message)
    
    def _get_reply_user(self, message) -> Optional[str]:
        """从消息中获取需要@的用户（通过reply消息段的message_id查找）"""
        if not isinstance(message, list):
            return None
        
        for seg in message:
            if isinstance(seg, dict) and seg.get("type") == "reply":
                reply_id = seg.get("data", {}).get("id", "")
                if reply_id:
                    # 从StateStore查找对应的user_id
                    user_id = self.state_store.get_user_by_message(str(reply_id))
                    if user_id:
                        return user_id
        return None

    async def handle_callback(self, callback: QianXunCallback) -> dict:
        """处理千寻框架回调"""
        event = callback.event
        robot_wxid = callback.wxid
        data = callback.data
        
        logger.debug(f"收到事件: {event}, 机器人: {robot_wxid}")
        
        # 记录机器人wxid
        if robot_wxid:
            self.robot_wxids.add(robot_wxid)
            self.current_robot_wxid = robot_wxid
        
        try:
            if event == QianXunEvent.INJECT_SUCCESS:
                logger.info(f"微信注入成功: {data}")
                return {"status": "ok"}
            
            elif event == QianXunEvent.USER_CHANGE:
                change_type = data.get("type")
                wxid = data.get("wxid")
                if change_type == 1:
                    logger.info(f"账号上线: {wxid}")
                    self.robot_wxids.add(wxid)
                else:
                    logger.info(f"账号下线: {wxid}")
                    self.robot_wxids.discard(wxid)
                return {"status": "ok"}
            
            elif event == QianXunEvent.PRIVATE_MSG:
                await self._handle_private_msg(robot_wxid, data)
                return {"status": "ok"}
            
            elif event == QianXunEvent.GROUP_MSG:
                await self._handle_group_msg(robot_wxid, data)
                return {"status": "ok"}
            
            elif event == QianXunEvent.GROUP_MEMBER_CHANGE:
                await self._handle_group_member_change(robot_wxid, data)
                return {"status": "ok"}
            
            else:
                logger.debug(f"未处理的事件类型: {event}")
                return {"status": "ok"}
                
        except Exception as e:
            logger.error(f"处理回调异常: {e}", exc_info=True)
            # 记录错误日志
            await log_error(self.log_collector, f"处理回调异常: {e}", {"event": event})
            return {"status": "error", "message": str(e)}
    
    async def _handle_private_msg(self, robot_wxid: str, data: dict):
        """处理私聊消息"""
        msg_data_raw = data.get('data', data)
        
        try:
            msg_data = PrivateMsgData(**msg_data_raw)
        except Exception as e:
            logger.error(f"解析私聊消息失败: {e}")
            return
        
        # 消息去重（使用StateStore）
        if msg_data.msgId and self.state_store.is_duplicate_message(msg_data.msgId):
            logger.debug(f"忽略重复消息: {msg_data.msgId}")
            return
        
        from_wxid = msg_data.fromWxid
        content = msg_data.msg.strip()
        
        if self._should_ignore_wxid(from_wxid):
            logger.info(f"已拦截接收来自被忽略用户的消息: {from_wxid}")
            return
        
        try:
            # 使用MessageParser解析消息
            parsed = self.message_parser.parse_message(
                msg_data.msgType, content, robot_wxid
            )
            
            # 处理解析结果
            await self._process_private_message(from_wxid, parsed, msg_data)
            
        except Exception as e:
            logger.error(f"处理私聊消息异常: {e}", exc_info=True)
            await log_error(self.log_collector, f"处理私聊消息异常: {e}", {
                "from_wxid": from_wxid,
                "content": content[:100]
            })
    
    async def _process_private_message(
        self, 
        from_wxid: str, 
        parsed: ParsedMessage, 
        msg_data: PrivateMsgData
    ):
        """处理私聊消息的公共逻辑"""
        if not parsed.should_process:
            return
        
        content = parsed.content
        
        # 处理图片消息
        if parsed.type == "image" and parsed.image_url:
            logger.info(f"私聊图片消息 [{from_wxid}], URL: {parsed.image_url}")
            await self.langbot.send_private_message_with_image(from_wxid, parsed.image_url)
            await log_private_message(self.log_collector, from_wxid, "[图片]", "processed")
            return
        
        # 处理引用图片消息
        if parsed.type == "quote" and parsed.image_url:
            logger.info(f"私聊引用图片消息: {parsed.image_url}, 提问: {content}")
            await self.langbot.send_private_message_with_image_and_text(
                from_wxid, parsed.image_url, content
            )
            await log_private_message(self.log_collector, from_wxid, f"[引用图片] {content}", "processed")
            return
        
        if not content:
            return
        
        logger.info(f"私聊消息 [{from_wxid}]: {content}")
        
        # 发送到 LangBot
        await self.langbot.send_private_message(from_wxid, content)
        await log_private_message(self.log_collector, from_wxid, content, "processed")

    async def _handle_group_msg(self, robot_wxid: str, data: dict):
        """处理群聊消息"""
        msg_data_raw = data.get('data', data)
        logger.info(f"群聊原始数据: {msg_data_raw}")
        
        try:
            msg_data = GroupMsgData(**msg_data_raw)
        except Exception as e:
            logger.error(f"解析群聊消息失败: {e}")
            return
        
        # 消息去重（使用StateStore）
        if msg_data.msgId and self.state_store.is_duplicate_message(msg_data.msgId):
            logger.debug(f"忽略重复消息: {msg_data.msgId}")
            return
        
        group_wxid = msg_data.fromWxid
        sender_wxid = msg_data.finalFromWxid or msg_data.fromWxid
        content = msg_data.msg.strip()
        
        if self._should_ignore_wxid(sender_wxid):
            logger.debug(f"忽略用户: {sender_wxid}")
            return
        
        try:
            # 使用MessageParser解析消息
            parsed = self.message_parser.parse_message(
                msg_data.msgType, content, robot_wxid, msg_data.atWxidList
            )
            
            # 处理解析结果
            await self._process_group_message(
                robot_wxid, group_wxid, sender_wxid, parsed, msg_data
            )
            
        except Exception as e:
            logger.error(f"处理群聊消息异常: {e}", exc_info=True)
            await log_error(self.log_collector, f"处理群聊消息异常: {e}", {
                "group_wxid": group_wxid,
                "sender_wxid": sender_wxid,
                "content": content[:100]
            })
    
    async def _process_group_message(
        self,
        robot_wxid: str,
        group_wxid: str,
        sender_wxid: str,
        parsed: ParsedMessage,
        msg_data: GroupMsgData
    ):
        """处理群聊消息的公共逻辑"""
        # 处理入群消息
        if parsed.is_join_group:
            await self._handle_join_group_message(
                robot_wxid, group_wxid, parsed.content, msg_data.msgXml or ""
            )
            return
        
        # 处理拍一拍消息
        if parsed.type == "pat" and parsed.should_process:
            # 更新sender_wxid为拍一拍发起者
            if parsed.pat_info and parsed.pat_info.from_user:
                sender_wxid = parsed.pat_info.from_user
            
            # 拍一拍消息直接发送到 LangBot
            logger.info(f"群聊拍一拍消息 [{group_wxid}][{sender_wxid}]")
            await self.langbot.send_group_message(
                group_wxid, sender_wxid, parsed.content, at_bot=True
            )
            await log_group_message(
                self.log_collector, group_wxid, sender_wxid, parsed.content, "processed"
            )
            return
        
        if not parsed.should_process:
            return
        
        content = parsed.content
        
        # 处理图片消息
        if parsed.type == "image" and parsed.image_url:
            # 检查是否@了机器人
            is_at_bot = msg_data.atWxidList and robot_wxid in msg_data.atWxidList
            
            if is_at_bot:
                # @机器人 + 图片，直接发送给LangBot处理
                logger.info(f"群聊图片消息(@机器人) [{group_wxid}][{sender_wxid}], URL: {parsed.image_url}")
                await self.langbot.send_group_message_with_image(
                    group_wxid, sender_wxid, parsed.image_url, at_bot=True
                )
                await log_group_message(
                    self.log_collector, group_wxid, sender_wxid, "[图片@机器人]", "processed"
                )
            else:
                # 普通图片消息，缓存图片URL（使用StateStore）
                logger.info(f"群聊图片消息(缓存) [{group_wxid}][{sender_wxid}], URL: {parsed.image_url}")
                self.state_store.cache_image(group_wxid, sender_wxid, parsed.image_url)
            return
        
        # 检查是否@机器人
        is_at_bot_in_msg = self.message_parser.check_at_bot(
            content, robot_wxid, msg_data.atWxidList
        )
        
        # 检查是否@所有人，根据配置决定是否响应
        if self._reply_at_all and self.message_parser.check_at_all(msg_data.atWxidList):
            is_at_bot_in_msg = True
        
        # 引用机器人消息或语音消息也视为@机器人
        if parsed.is_quote_to_bot or parsed.type == "voice":
            is_at_bot_in_msg = True
        
        # 检查关键词触发
        is_keyword_trigger = self._check_keyword_trigger(content)
        
        # 如果引用了图片消息，直接发送图片+文本
        if parsed.image_url:
            logger.info(f"引用图片消息，发送图片+文本: {parsed.image_url}")
            await self.langbot.send_group_message_with_image_and_text(
                group_wxid, sender_wxid, parsed.image_url, content
            )
            await log_group_message(
                self.log_collector, group_wxid, sender_wxid, f"[引用图片] {content}", "processed"
            )
            return
        
        # 如果@机器人，检查是否有图片缓存需要关联（使用StateStore）
        if is_at_bot_in_msg:
            logger.debug(f"检查图片缓存: group={group_wxid}, user={sender_wxid}")
            cached_image_url = self.state_store.get_cached_image(group_wxid, sender_wxid)
            if cached_image_url:
                # 有图片缓存，带上图片一起发送
                logger.info(f"关联缓存图片: {cached_image_url}")
                await self.langbot.send_group_message_with_image_and_text(
                    group_wxid, sender_wxid, cached_image_url, content
                )
                await log_group_message(
                    self.log_collector, group_wxid, sender_wxid, f"[缓存图片] {content}", "processed"
                )
                return
            else:
                logger.debug(f"没有找到图片缓存")
        
        if not content:
            logger.info("消息内容为空，忽略")
            return
        
        # 判断是否需要转发到 LangBot
        # all 模式：所有群消息都转发，让 LangBot 决定是否响应
        # strict 模式：只有 @机器人 或 关键词触发 才转发
        forward_mode = self._group_forward_mode
        should_reply = is_at_bot_in_msg or is_keyword_trigger
        
        if forward_mode == "all":
            # 全部转发模式
            logger.info(f"群聊消息(全部转发) [{group_wxid}][{sender_wxid}]: {content}")
            await self.langbot.send_group_message(group_wxid, sender_wxid, content, at_bot=is_at_bot_in_msg)
            await log_group_message(self.log_collector, group_wxid, sender_wxid, content, "processed")
        elif should_reply:
            # 严格模式，只转发触发的消息
            trigger_type = "关键词" if is_keyword_trigger and not is_at_bot_in_msg else "@机器人"
            logger.info(f"群聊消息({trigger_type}) [{group_wxid}][{sender_wxid}]: {content}")
            await self.langbot.send_group_message(group_wxid, sender_wxid, content, at_bot=True)
            await log_group_message(self.log_collector, group_wxid, sender_wxid, content, "processed")
        else:
            logger.debug(f"群聊消息未触发机器人，忽略: [{group_wxid}][{sender_wxid}]")

    async def _handle_join_group_message(
        self, 
        robot_wxid: str, 
        group_wxid: str, 
        content: str, 
        msg_xml: str = ""
    ):
        """处理入群系统消息
        
        Args:
            robot_wxid: 机器人wxid
            group_wxid: 群wxid
            content: 系统消息内容
            msg_xml: 消息的XML内容
        """
        logger.info(f"检测到入群消息: [{group_wxid}] {content}")
        
        # 查找匹配的欢迎配置
        welcome_tasks = self.config_manager.get_welcome_tasks()
        
        welcome_config = None
        for task in welcome_tasks:
            if not task.get('enabled', False):
                continue
            target_groups = task.get('target_groups', [])
            # 如果 target_groups 为空，则匹配所有群；否则检查是否在列表中
            if not target_groups or group_wxid in target_groups:
                welcome_config = task
                break
        
        if not welcome_config:
            logger.info(f"群 {group_wxid} 没有启用的欢迎配置")
            return
        
        logger.info(f"使用欢迎配置: {welcome_config.get('task_id', 'unnamed')}")
        
        # 尝试从消息中提取新成员昵称
        new_member_names = self._parse_new_member_names(content)
        logger.info(f"解析到新成员昵称: {new_member_names}")
        
        # 通过群成员列表匹配昵称获取wxid
        new_member_wxids = []
        if new_member_names and welcome_config.get('at_new_member', True):
            # 等待一小段时间，让新成员数据同步到微信
            await asyncio.sleep(5)
            # 新成员刚入群，需要刷新缓存获取最新群成员列表
            members = await self.qianxun.get_group_member_list(
                robot_wxid, group_wxid, get_nick=True, refresh=True
            )
            if members:
                new_member_wxids = self._match_member_wxids(members, new_member_names)
            else:
                logger.warning("获取群成员列表为空")
        
        # 构建@新成员代码
        at_members_str = ""
        if welcome_config.get('at_new_member', True) and new_member_wxids:
            at_codes = [f"[@,wxid={wxid},nick=,isAuto=true]" for wxid in new_member_wxids]
            at_members_str = " ".join(at_codes)

        # 发送欢迎消息
        await self._send_welcome_messages(
            robot_wxid, group_wxid, welcome_config, at_members_str, new_member_names
        )
    
    def _parse_new_member_names(self, content: str) -> list:
        """从入群消息中解析新成员昵称
        
        Args:
            content: 系统消息内容
            
        Returns:
            新成员昵称列表
        """
        new_member_names = []
        
        # 格式1: "邀请者"邀请"新成员1、新成员2"加入了群聊
        match = re.search(r'邀请"([^"]+)"加入了群聊', content)
        if match:
            names_str = match.group(1)
            new_member_names = [n.strip() for n in names_str.split('、')]
        else:
            # 格式2: "新成员"通过扫描二维码加入群聊
            match = re.search(r'"([^"]+)"通过扫描', content)
            if match:
                new_member_names = [match.group(1)]
        
        return new_member_names
    
    async def _send_welcome_messages(
        self,
        robot_wxid: str,
        group_wxid: str,
        welcome_config: dict,
        at_members_str: str,
        new_member_names: Optional[list] = None
    ):
        """发送欢迎消息的通用方法

        Args:
            robot_wxid: 机器人wxid
            group_wxid: 群wxid
            welcome_config: 欢迎配置
            at_members_str: @成员字符串
            new_member_names: 新成员昵称列表（用于替换{nickname}变量）
        """
        # 获取欢迎词列表
        messages = welcome_config.get('messages', [])
        if not messages:
            # 兼容旧配置：使用单条 message 字段
            single_message = welcome_config.get('message', '欢迎新朋友！')
            messages = [single_message] if single_message else []

        if not messages:
            logger.warning("欢迎配置没有设置欢迎词")
            return

        # 分段发送配置
        split_send = welcome_config.get('split_send', False)
        split_min_delay = welcome_config.get('split_min_delay', 1)
        split_max_delay = welcome_config.get('split_max_delay', 3)

        # 发送欢迎消息
        for i, message in enumerate(messages):
            if not message.strip():
                continue

            # 替换变量
            if new_member_names:
                message = message.replace('{nickname}', '、'.join(new_member_names))

            # 替换 {at_members} 变量
            if '{at_members}' in message:
                message = message.replace('{at_members}', at_members_str)
            elif i == 0 and at_members_str:
                # 第一条消息：如果没有 {at_members} 变量，在消息前面加上@
                message = at_members_str + " " + message

            # 发送消息
            await self.qianxun.send_text(robot_wxid, group_wxid, message.strip())
            logger.info(f"已发送入群欢迎 ({i+1}/{len(messages)}): [{group_wxid}]")

            # 分段发送延迟（最后一条不需要延迟）
            if split_send and i < len(messages) - 1:
                delay = random.uniform(split_min_delay, split_max_delay)
                logger.debug(f"分段发送延迟 {delay:.1f}秒")
                await asyncio.sleep(delay)

    def _match_member_wxids(self, members: list, new_member_names: list) -> list:
        """匹配新成员wxid
        
        Args:
            members: 群成员列表
            new_member_names: 新成员昵称列表
            
        Returns:
            匹配到的wxid列表
        """
        # 构建昵称到wxid的映射
        nick_to_wxid = {}
        for m in members:
            nick = m.get('groupNick', '')
            wxid = m.get('wxid', '')
            if nick and wxid:
                nick_to_wxid[nick] = wxid
        
        logger.info(f"群成员昵称列表: {list(nick_to_wxid.keys())}")
        
        new_member_wxids = []
        for name in new_member_names:
            if name in nick_to_wxid:
                new_member_wxids.append(nick_to_wxid[name])
                logger.info(f"匹配到新成员: {name} -> {nick_to_wxid[name]}")
            else:
                # 尝试模糊匹配
                matched = False
                for nick, wxid in nick_to_wxid.items():
                    if name in nick or nick in name:
                        new_member_wxids.append(wxid)
                        logger.info(f"模糊匹配到新成员: {name} -> {nick} -> {wxid}")
                        matched = True
                        break
                if not matched:
                    logger.warning(f"未匹配到新成员wxid: {name}")
        
        return new_member_wxids
    
    async def _handle_group_member_change(self, robot_wxid: str, data: dict):
        """处理群成员变动事件（10016事件）"""
        member_data = data.get('data', data)
        
        group_wxid = member_data.get('fromWxid', '')
        member_wxid = member_data.get('finalFromWxid', '')
        event_type = member_data.get('eventType', -1)
        
        # eventType: 0=退群, 1=进群
        if event_type != 1:
            logger.debug(f"群成员退出: [{group_wxid}] {member_wxid}")
            return
        
        logger.info(f"新成员入群(10016事件): [{group_wxid}] {member_wxid}")
        
        # 查找匹配的欢迎配置
        welcome_tasks = self.config_manager.get_welcome_tasks()
        
        welcome_config = None
        for task in welcome_tasks:
            if not task.get('enabled', False):
                continue
            target_groups = task.get('target_groups', [])
            if not target_groups or group_wxid in target_groups:
                welcome_config = task
                break
        
        if not welcome_config:
            logger.debug(f"群 {group_wxid} 没有启用的欢迎配置")
            return
        
        # 构建@新成员代码
        at_member_str = ""
        if welcome_config.get('at_new_member', True) and member_wxid:
            at_member_str = f"[@,wxid={member_wxid},nick=,isAuto=true]"

        # 发送欢迎消息
        await self._send_welcome_messages(
            robot_wxid, group_wxid, welcome_config, at_member_str
        )
