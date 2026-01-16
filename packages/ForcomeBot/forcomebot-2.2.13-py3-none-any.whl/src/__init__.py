"""
FORCOME 康康 - 千寻微信框架Pro与LangBot中间件
通过 OneBot v11 WebSocket 协议与 LangBot 通信

重构后的模块结构：
- src/core/: 核心服务层（配置管理、状态存储、日志收集）
- src/clients/: 客户端层（千寻客户端、LangBot客户端）
- src/handlers/: 业务处理层（消息处理、定时任务）
- src/utils/: 工具模块（文本处理、XML解析）
- src/api/: API层（RESTful API、WebSocket）
"""

__version__ = "2.0.0"

# 核心服务
from .core import (
    ConfigManager,
    StateStore,
    LogCollector,
    log_private_message,
    log_group_message,
    log_error,
    log_system,
)

# 客户端
from .clients import QianXunClient, LangBotClient

# 业务处理
from .handlers import MessageParser, ParsedMessage, MessageHandler, TaskScheduler

# 工具模块
from .utils import TextProcessor, XMLParser, QuoteMessageResult, PatMessageResult, VoiceInfo

# 数据模型
from .models import QianXunEvent, QianXunCallback, PrivateMsgData, GroupMsgData

__all__ = [
    # 版本
    "__version__",
    # 核心服务
    "ConfigManager",
    "StateStore",
    "LogCollector",
    "log_private_message",
    "log_group_message",
    "log_error",
    "log_system",
    # 客户端
    "QianXunClient",
    "LangBotClient",
    # 业务处理
    "MessageParser",
    "ParsedMessage",
    "MessageHandler",
    "TaskScheduler",
    # 工具模块
    "TextProcessor",
    "XMLParser",
    "QuoteMessageResult",
    "PatMessageResult",
    "VoiceInfo",
    # 数据模型
    "QianXunEvent",
    "QianXunCallback",
    "PrivateMsgData",
    "GroupMsgData",
]
