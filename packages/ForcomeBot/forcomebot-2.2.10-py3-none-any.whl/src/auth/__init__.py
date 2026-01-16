"""认证模块"""
from .database import Database, get_db, init_database
from .models import User, OperationLog
from .jwt_handler import JWTHandler
from .dingtalk import DingTalkClient, init_dingtalk_client, get_dingtalk_client
from .middleware import (
    AuthMiddleware,
    get_current_user,
    get_optional_user,
    init_auth,
    is_auth_enabled,
    log_operation
)
from .routes import router as auth_router

__all__ = [
    "Database",
    "get_db",
    "init_database",
    "User",
    "OperationLog",
    "JWTHandler",
    "DingTalkClient",
    "init_dingtalk_client",
    "get_dingtalk_client",
    "AuthMiddleware",
    "get_current_user",
    "get_optional_user",
    "init_auth",
    "is_auth_enabled",
    "log_operation",
    "auth_router",
]
