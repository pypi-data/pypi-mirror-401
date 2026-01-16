"""数据模型定义"""
from pydantic import BaseModel
from typing import Optional, Any, Dict, List
from enum import IntEnum


class QianXunEvent(IntEnum):
    """千寻框架事件类型"""
    INJECT_SUCCESS = 10000      # 注入成功
    PRIVATE_MSG = 10009         # 私聊消息
    GROUP_MSG = 10008           # 群聊消息
    USER_CHANGE = 10014         # 账号变动
    FRIEND_REQUEST = 10011      # 好友请求
    GROUP_INVITE = 10012        # 群邀请
    GROUP_MEMBER_CHANGE = 10016 # 群成员变动


class QianXunCallback(BaseModel):
    """千寻框架回调数据"""
    event: int
    wxid: str  # 机器人wxid
    data: Dict[str, Any]


class PrivateMsgData(BaseModel):
    """私聊消息数据"""
    fromWxid: str           # 发送者wxid
    msg: str                # 消息内容
    msgType: int            # 消息类型 1=文本
    toWxid: Optional[str] = None  # 接收者wxid（机器人）
    finalFromWxid: Optional[str] = None
    atWxidList: Optional[List[str]] = None
    msgId: Optional[str] = None
    timeStamp: Optional[str] = None
    timestamp: Optional[str] = None
    fromType: Optional[int] = None
    msgSource: Optional[int] = None
    silence: Optional[int] = None
    membercount: Optional[int] = None
    signature: Optional[str] = None
    sendId: Optional[str] = None
    msgXml: Optional[str] = None


class GroupMsgData(BaseModel):
    """群聊消息数据"""
    fromWxid: str           # 群wxid
    msg: str                # 消息内容
    msgType: int            # 消息类型
    finalFromWxid: Optional[str] = None  # 实际发送者wxid
    toWxid: Optional[str] = None
    atWxidList: Optional[List[str]] = None  # @的wxid列表
    msgId: Optional[str] = None
    timeStamp: Optional[str] = None
    timestamp: Optional[str] = None
    fromType: Optional[int] = None
    msgSource: Optional[int] = None
    silence: Optional[int] = None
    membercount: Optional[int] = None
    signature: Optional[str] = None
    sendId: Optional[str] = None
    msgXml: Optional[str] = None


class LangBotMessage(BaseModel):
    """LangBot消息格式"""
    type: str = "Plain"
    text: str


class LangBotRequest(BaseModel):
    """LangBot请求格式"""
    bot_uuid: str
    user_id: str
    group_id: Optional[str] = None
    message: List[LangBotMessage]
    pipeline_uuid: Optional[str] = None
