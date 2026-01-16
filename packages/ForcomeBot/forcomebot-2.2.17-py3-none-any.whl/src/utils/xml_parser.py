"""XML解析工具 - 解析微信消息中的XML内容

支持解析：
- 引用消息（检查是否引用机器人）
- 拍一拍消息
- 语音消息
"""
import re
import logging
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class QuoteMessageResult:
    """引用消息解析结果"""
    user_msg: str  # 用户发送的新消息
    quoted_text: str  # 被引用的消息内容
    sender_name: str  # 被引用消息发送者的昵称
    quoted_image_path: Optional[str] = None  # 引用的图片路径（如果引用的是图片消息）


@dataclass
class PatMessageResult:
    """拍一拍消息解析结果"""
    from_user: str  # 发起拍一拍的用户
    patted_user: str  # 被拍的用户
    is_pat_me: bool  # 是否拍的是机器人


@dataclass
class VoiceInfo:
    """语音消息信息"""
    voicelength: int  # 语音长度（毫秒）


class XMLParser:
    """XML解析工具"""
    
    @staticmethod
    def parse_quote_message(xml_content: str, robot_wxid: str) -> Optional[QuoteMessageResult]:
        """解析引用消息，如果引用的是机器人的消息则返回解析结果
        
        Args:
            xml_content: 引用消息的XML内容
            robot_wxid: 机器人wxid，用于检查是否引用机器人
            
        Returns:
            QuoteMessageResult 如果引用的是机器人消息，否则返回 None
        """
        try:
            root = ET.fromstring(xml_content)
            
            # 获取引用信息
            refermsg = root.find('.//refermsg')
            if refermsg is None:
                return None
            
            # 检查被引用消息的发送者是否是机器人
            chatusr = refermsg.find('chatusr')
            if chatusr is None or chatusr.text != robot_wxid:
                return None
            
            # 获取用户发送的新消息（title标签）
            title = root.find('.//title')
            user_msg = title.text.strip() if title is not None and title.text else ""
            
            # 获取被引用的消息内容
            quote_content = refermsg.find('content')
            quoted_text = quote_content.text.strip() if quote_content is not None and quote_content.text else ""
            
            # 获取被引用消息发送者的昵称
            displayname = refermsg.find('displayname')
            sender_name = displayname.text.strip() if displayname is not None and displayname.text else "未知"
            
            if user_msg:
                return QuoteMessageResult(
                    user_msg=user_msg,
                    quoted_text=quoted_text,
                    sender_name=sender_name
                )
            
            return None
        except Exception as e:
            logger.error(f"解析引用消息XML失败: {e}")
            return None
    
    @staticmethod
    def parse_quote_message_any(xml_content: str) -> Optional[QuoteMessageResult]:
        """解析引用消息（不检查被引用者）
        
        Args:
            xml_content: 引用消息的XML内容
            
        Returns:
            QuoteMessageResult 包含用户消息、引用内容、发送者昵称和可能的图片路径
        """
        try:
            root = ET.fromstring(xml_content)
            
            # 获取用户发送的新消息
            title = root.find('.//title')
            user_msg = title.text.strip() if title is not None and title.text else ""
            
            # 获取被引用的消息内容和发送者昵称
            refermsg = root.find('.//refermsg')
            quoted_text = ""
            sender_name = "未知"
            quoted_image_path = None
            
            if refermsg is not None:
                quote_content = refermsg.find('content')
                quoted_text = quote_content.text.strip() if quote_content is not None and quote_content.text else ""
                displayname = refermsg.find('displayname')
                sender_name = displayname.text.strip() if displayname is not None and displayname.text else "未知"
                
                # 检查引用的是否是图片消息
                # 图片消息的 type 为 3，content 格式为 [pic=路径,isDecrypt=x]
                msg_type = refermsg.find('type')
                if msg_type is not None and msg_type.text == '3':
                    # 解析图片路径
                    match = re.search(r'\[pic=([^,\]]+)', quoted_text)
                    if match:
                        quoted_image_path = match.group(1)
                        quoted_text = "[图片]"  # 替换为友好文本
            
            if user_msg:
                return QuoteMessageResult(
                    user_msg=user_msg,
                    quoted_text=quoted_text,
                    sender_name=sender_name,
                    quoted_image_path=quoted_image_path
                )
            return None
        except Exception as e:
            logger.error(f"解析引用消息XML失败: {e}")
            return None
    
    @staticmethod
    def parse_pat_message(xml_content: str, robot_wxid: str) -> Optional[PatMessageResult]:
        """解析拍一拍消息（XML格式，私聊或部分群聊）
        
        Args:
            xml_content: 拍一拍消息的XML内容
            robot_wxid: 机器人wxid，用于判断是否拍的是机器人
            
        Returns:
            PatMessageResult 解析结果
        """
        try:
            root = ET.fromstring(xml_content)
            
            pat = root.find('pat')
            if pat is None:
                return None
            
            from_user = pat.findtext('fromusername', '')
            patted_user = pat.findtext('pattedusername', '')
            
            return PatMessageResult(
                from_user=from_user,
                patted_user=patted_user,
                is_pat_me=patted_user == robot_wxid
            )
        except Exception as e:
            logger.error(f"解析拍一拍XML失败: {e}")
            return None
    
    @staticmethod
    def parse_pat_text(text: str, robot_wxid: str) -> Optional[PatMessageResult]:
        """解析文本格式的拍一拍消息（群聊）
        
        群聊拍一拍文本格式: "xxx" 拍了拍 "yyy"
        由于文本中没有wxid，无法精确判断是否拍的是机器人，
        假设收到的拍一拍消息都是拍机器人的
        
        Args:
            text: 拍一拍消息文本
            robot_wxid: 机器人wxid（用于判断，但文本中没有wxid）
            
        Returns:
            PatMessageResult 解析结果
        """
        if "拍了拍" in text:
            return PatMessageResult(
                from_user="",  # 群聊文本格式无法获取wxid
                patted_user="",
                is_pat_me=True  # 假设收到的拍一拍都是拍机器人的
            )
        return None
    
    @staticmethod
    def parse_voice_info(xml_content: str) -> Optional[VoiceInfo]:
        """解析语音消息
        
        Args:
            xml_content: 语音消息的XML内容
            
        Returns:
            VoiceInfo 语音信息
        """
        try:
            root = ET.fromstring(xml_content)
            voicemsg = root.find('voicemsg')
            if voicemsg is not None:
                return VoiceInfo(
                    voicelength=int(voicemsg.get('voicelength', 0))
                )
            return None
        except Exception as e:
            logger.error(f"解析语音XML失败: {e}")
            return None
