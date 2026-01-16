"""认证中间件"""
import logging
from typing import Optional, Callable, List
from datetime import datetime

from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .database import get_db
from .models import User, OperationLog
from .jwt_handler import JWTHandler

logger = logging.getLogger(__name__)

# HTTP Bearer认证
security = HTTPBearer(auto_error=False)

# 全局JWT处理器
_jwt_handler: Optional[JWTHandler] = None

# 认证开关
_auth_enabled: bool = True

# 白名单路由（不需要认证）
AUTH_WHITELIST = [
    "/health",
    "/qianxun/callback",
    "/api/auth/dingtalk/login",
    "/api/auth/dingtalk/h5-login",
    "/api/auth/dingtalk/qrcode-url",
    "/api/auth/dingtalk/config",
    "/docs",
    "/openapi.json",
    "/redoc",
]


def init_auth(jwt_handler: JWTHandler, auth_enabled: bool = True):
    """初始化认证模块"""
    global _jwt_handler, _auth_enabled
    _jwt_handler = jwt_handler
    _auth_enabled = auth_enabled
    logger.info(f"认证模块已初始化, 认证开关: {auth_enabled}")


def is_auth_enabled() -> bool:
    """检查认证是否启用"""
    return _auth_enabled


def get_jwt_handler() -> JWTHandler:
    """获取JWT处理器"""
    if _jwt_handler is None:
        raise RuntimeError("JWT处理器未初始化")
    return _jwt_handler


class AuthMiddleware:
    """认证中间件"""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            # 检查是否需要认证
            path = scope.get("path", "")

            # 白名单路由跳过认证
            if self._is_whitelisted(path):
                await self.app(scope, receive, send)
                return

            # 静态文件跳过认证
            if path.startswith("/app/") or path.startswith("/static/"):
                await self.app(scope, receive, send)
                return

            # 认证未启用时跳过
            if not _auth_enabled:
                await self.app(scope, receive, send)
                return

        await self.app(scope, receive, send)

    def _is_whitelisted(self, path: str) -> bool:
        """检查路径是否在白名单中"""
        for whitelist_path in AUTH_WHITELIST:
            if path == whitelist_path or path.startswith(whitelist_path + "/"):
                return True
        return False


async def get_current_user(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> User:
    """
    获取当前登录用户（必须登录）

    用于需要强制登录的接口
    """
    # 认证未启用时返回模拟用户
    if not _auth_enabled:
        return _create_mock_user()

    if not credentials:
        raise HTTPException(status_code=401, detail="未提供认证凭证")

    if not _jwt_handler:
        raise HTTPException(status_code=500, detail="认证服务未初始化")

    # 验证Token
    payload = _jwt_handler.verify_token(credentials.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="无效的认证凭证")

    # 获取用户ID
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="无效的用户信息")

    # 从数据库获取用户
    db = get_db()
    async with db.session_factory() as session:
        result = await session.execute(
            select(User).where(User.id == int(user_id))
        )
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=401, detail="用户不存在")

        if not user.is_active:
            raise HTTPException(status_code=403, detail="用户已被禁用")

        return user


async def get_optional_user(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Optional[User]:
    """
    获取当前登录用户（可选）

    用于不强制登录但需要用户信息的接口
    """
    # 认证未启用时返回模拟用户
    if not _auth_enabled:
        return _create_mock_user()

    if not credentials:
        return None

    if not _jwt_handler:
        return None

    # 验证Token
    payload = _jwt_handler.verify_token(credentials.credentials)
    if not payload:
        return None

    # 获取用户ID
    user_id = payload.get("sub")
    if not user_id:
        return None

    # 从数据库获取用户
    try:
        db = get_db()
        async with db.session_factory() as session:
            result = await session.execute(
                select(User).where(User.id == int(user_id))
            )
            user = result.scalar_one_or_none()
            return user if user and user.is_active else None
    except Exception as e:
        logger.warning(f"获取用户信息失败: {e}")
        return None


def _create_mock_user() -> User:
    """创建模拟用户（认证关闭时使用）"""
    user = User(
        id=0,
        dingtalk_userid="mock_user",
        name="系统用户",
        is_active=True,
        is_admin=True
    )
    return user


async def log_operation(
    user: Optional[User],
    action: str,
    resource: str,
    resource_id: Optional[str] = None,
    detail: Optional[dict] = None,
    request: Optional[Request] = None,
    status: str = "success",
    error_message: Optional[str] = None
):
    """
    记录操作日志

    Args:
        user: 操作用户
        action: 操作类型
        resource: 操作资源
        resource_id: 资源ID
        detail: 操作详情
        request: 请求对象
        status: 操作状态
        error_message: 错误信息
    """
    try:
        db = get_db()
        async with db.session_factory() as session:
            log = OperationLog(
                user_id=user.id if user and user.id else None,
                user_name=user.name if user else None,
                action=action,
                resource=resource,
                resource_id=resource_id,
                detail=detail,
                method=request.method if request else None,
                path=str(request.url.path) if request else None,
                ip_address=_get_client_ip(request) if request else None,
                user_agent=request.headers.get("user-agent", "")[:512] if request else None,
                status=status,
                error_message=error_message,
                created_at=datetime.now()
            )
            session.add(log)
            await session.commit()
    except Exception as e:
        logger.error(f"记录操作日志失败: {e}")


def _get_client_ip(request: Request) -> str:
    """获取客户端IP"""
    # 优先从X-Forwarded-For获取
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()

    # 从X-Real-IP获取
    real_ip = request.headers.get("x-real-ip")
    if real_ip:
        return real_ip

    # 从连接获取
    if request.client:
        return request.client.host

    return "unknown"
