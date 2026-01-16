"""消息解析器 - 统一消息类型判断和解析逻辑

支持消息类型：
- text(1): 文本消息
- image(3): 图片消息
- voice(34): 语音消息
- quote(49): 引用消息
- pat(10002): 拍一拍消息
- system(10000): 系统消息（入群等）

集成 XMLParser 和 TextProcessor
"""
import logging
from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING

from ..utils.xml_parser import XMLParser, QuoteMessageResult, PatMessageResult, VoiceInfo
from ..utils.text_processor import TextProcessor

if TYPE_CHECKING:
    from ..clients.qianxun import QianXunClient

logger = logging.getLogger(__name__)


@dataclass
class ParsedMessage:
    """解析后的消息"""
    type: str  # text, image, voice, quote, pat, system, unknown
    content: str  # 处理后的消息内容
    image_url: Optional[str] = None  # 图片URL（图片消息或引用图片）
    quoted_text: Optional[str] = None  # 被引用的消息内容
    quoted_sender: Optional[str] = None  # 被引用消息的发送者昵称
    quoted_image_path: Optional[str] = None  # 引用的图片路径
    is_quote_to_bot: bool = False  # 是否引用机器人的消息
    voice_duration: Optional[float] = None  # 语音时长（秒）
    should_process: bool = True  # 是否需要继续处理（发送到LangBot）
    is_join_group: bool = False  # 是否是入群消息
    pat_info: Optional[PatMessageResult] = None  # 拍一拍信息


class MessageParser:
    """消息解析器"""
    
    # 消息类型常量
    MSG_TYPE_TEXT = 1
    MSG_TYPE_IMAGE = 3
    MSG_TYPE_VOICE = 34
    MSG_TYPE_QUOTE = 49
    MSG_TYPE_SYSTEM = 10000
    MSG_TYPE_PAT = 10002
    
    def __init__(self, qianxun_client: "QianXunClient"):
        """初始化消息解析器
        
        Args:
            qianxun_client: 千寻客户端，用于获取图片URL等
        """
        self.qianxun = qianxun_client
        self.xml_parser = XMLParser()
        self.text_processor = TextProcessor()

    def parse_message(
        self, 
        msg_type: int, 
        content: str, 
        robot_wxid: str,
        at_wxid_list: Optional[list] = None
    ) -> ParsedMessage:
        """解析消息，返回统一格式
        
        Args:
            msg_type: 消息类型
            content: 消息内容
            robot_wxid: 机器人wxid
            at_wxid_list: @的wxid列表（群聊消息）
            
        Returns:
            ParsedMessage 解析结果
        """
        content = content.strip()
        
        if msg_type == self.MSG_TYPE_TEXT:
            return self._parse_text_message(content)
        
        elif msg_type == self.MSG_TYPE_IMAGE:
            return self._parse_image_message(content)
        
        elif msg_type == self.MSG_TYPE_VOICE:
            return self._parse_voice_message(content)
        
        elif msg_type == self.MSG_TYPE_QUOTE:
            return self._parse_quote_message(content, robot_wxid)
        
        elif msg_type == self.MSG_TYPE_PAT:
            return self._parse_pat_message(content, robot_wxid)
        
        elif msg_type == self.MSG_TYPE_SYSTEM:
            return self._parse_system_message(content, robot_wxid)
        
        else:
            # 未知消息类型
            logger.debug(f"未知消息类型: {msg_type}")
            return ParsedMessage(
                type="unknown",
                content=content,
                should_process=False
            )
    
    def _parse_text_message(self, content: str) -> ParsedMessage:
        """解析文本消息"""
        # 处理千寻框架的特殊@格式：把 \u2005 转换成普通空格
        content = content.replace('\\u2005', ' ')
        content = content.replace('\u2005', ' ')
        
        return ParsedMessage(
            type="text",
            content=content,
            should_process=True
        )
    
    def _parse_image_message(self, content: str) -> ParsedMessage:
        """解析图片消息"""
        image_path = self.qianxun.parse_image_path(content)
        
        if image_path:
            image_url = self.qianxun.get_image_url(image_path)
            logger.debug(f"解析图片消息: path={image_path}, url={image_url}")
            return ParsedMessage(
                type="image",
                content="[图片]",
                image_url=image_url,
                should_process=True
            )
        
        # 解析失败
        logger.warning(f"图片消息解析失败: {content}")
        return ParsedMessage(
            type="image",
            content="[用户发送了一张图片，但无法获取]",
            should_process=True
        )
    
    def _parse_voice_message(self, content: str) -> ParsedMessage:
        """解析语音消息"""
        voice_info = self.xml_parser.parse_voice_info(content)
        
        if voice_info:
            duration_sec = voice_info.voicelength / 1000
            logger.debug(f"解析语音消息: 长度={duration_sec:.1f}秒")
            return ParsedMessage(
                type="voice",
                content=f"[用户发送了一条{duration_sec:.1f}秒的语音消息]",
                voice_duration=duration_sec,
                should_process=True
            )
        
        return ParsedMessage(
            type="voice",
            content="[用户发送了一条语音消息]",
            should_process=True
        )
    
    def _parse_quote_message(self, content: str, robot_wxid: str) -> ParsedMessage:
        """解析引用消息"""
        # 先尝试解析引用机器人的消息
        quote_result = self.xml_parser.parse_quote_message(content, robot_wxid)
        
        if quote_result:
            # 引用机器人消息
            user_msg = quote_result.user_msg
            quoted_text = quote_result.quoted_text
            sender_name = quote_result.sender_name
            
            if quoted_text:
                final_content = f"[引用 {sender_name} 的消息: {quoted_text}]\n{user_msg}"
            else:
                final_content = user_msg
            
            logger.debug(f"解析引用消息(机器人): {final_content}")
            return ParsedMessage(
                type="quote",
                content=final_content,
                quoted_text=quoted_text,
                quoted_sender=sender_name,
                is_quote_to_bot=True,
                should_process=True
            )
        
        # 尝试解析引用非机器人的消息
        quote_any = self.xml_parser.parse_quote_message_any(content)
        
        if quote_any:
            user_msg = quote_any.user_msg
            quoted_text = quote_any.quoted_text
            sender_name = quote_any.sender_name
            quoted_image_path = quote_any.quoted_image_path
            
            # 检查是否引用了图片消息
            if quoted_image_path:
                image_url = self.qianxun.get_image_url(quoted_image_path)
                logger.debug(f"解析引用图片消息: {image_url}")
                return ParsedMessage(
                    type="quote",
                    content=user_msg,
                    image_url=image_url,
                    quoted_image_path=quoted_image_path,
                    quoted_sender=sender_name,
                    is_quote_to_bot=True,  # 引用图片消息视为需要机器人处理
                    should_process=True
                )
            
            # 普通引用消息
            if quoted_text:
                final_content = f"[引用 {sender_name} 的消息: {quoted_text}]\n{user_msg}"
            else:
                final_content = user_msg
            
            logger.debug(f"解析引用消息(非机器人): {final_content}")
            return ParsedMessage(
                type="quote",
                content=final_content,
                quoted_text=quoted_text,
                quoted_sender=sender_name,
                is_quote_to_bot=False,
                should_process=True
            )
        
        # 无法解析
        logger.debug("无法解析引用消息")
        return ParsedMessage(
            type="quote",
            content=content,
            should_process=False
        )
    
    def _parse_pat_message(self, content: str, robot_wxid: str) -> ParsedMessage:
        """解析拍一拍消息（XML格式，私聊或部分群聊）"""
        pat_info = self.xml_parser.parse_pat_message(content, robot_wxid)
        
        if pat_info and pat_info.is_pat_me:
            logger.debug(f"解析拍一拍消息: {pat_info.from_user} 拍了拍我")
            return ParsedMessage(
                type="pat",
                content="[用户拍了拍我]",
                pat_info=pat_info,
                should_process=True
            )
        
        logger.debug(f"忽略拍一拍消息: {pat_info}")
        return ParsedMessage(
            type="pat",
            content=content,
            pat_info=pat_info,
            should_process=False
        )
    
    def _parse_system_message(self, content: str, robot_wxid: str) -> ParsedMessage:
        """解析系统消息（入群、拍一拍等）"""
        # 检查是否是入群消息
        if "加入了群聊" in content or "加入群聊" in content:
            logger.debug(f"解析入群消息: {content}")
            return ParsedMessage(
                type="system",
                content=content,
                is_join_group=True,
                should_process=True
            )
        
        # 检查是否是文本格式的拍一拍消息（群聊）
        if "拍了拍" in content:
            pat_info = self.xml_parser.parse_pat_text(content, robot_wxid)
            if pat_info and pat_info.is_pat_me:
                logger.debug(f"解析群聊拍一拍消息: {content}")
                return ParsedMessage(
                    type="pat",
                    content="[用户拍了拍我]",
                    pat_info=pat_info,
                    should_process=True
                )
        
        # 其他系统消息，不处理
        logger.debug(f"忽略系统消息: {content}")
        return ParsedMessage(
            type="system",
            content=content,
            should_process=False
        )
    
    def check_at_bot(self, content: str, robot_wxid: str, at_wxid_list: Optional[list] = None) -> bool:
        """检查消息中是否@了机器人
        
        Args:
            content: 消息内容
            robot_wxid: 机器人wxid
            at_wxid_list: 千寻框架提供的@列表
            
        Returns:
            是否@了机器人
        """
        # 优先使用千寻框架提供的atWxidList字段（最准确）
        if at_wxid_list:
            if robot_wxid in at_wxid_list:
                return True
            # 如果 at_wxid_list 存在但不包含机器人，说明@的是其他人
            # 不需要继续检查内容
            return False
        
        # 如果没有 at_wxid_list，检查消息内容中是否包含机器人wxid
        # 千寻框架的@格式: [@,wxid=xxx,...]
        if f'wxid={robot_wxid}' in content:
            return True
        
        return False
    
    def check_at_all(self, at_wxid_list: Optional[list] = None) -> bool:
        """检查是否@所有人
        
        Args:
            at_wxid_list: 千寻框架提供的@列表
            
        Returns:
            是否@所有人
        """
        return at_wxid_list is not None and "notify@all" in at_wxid_list
