"""认证相关API路由"""
import logging
from datetime import datetime
from typing import Optional, List

from fastapi import APIRouter, HTTPException, Depends, Request, Query
from pydantic import BaseModel
from sqlalchemy import select, desc, func

from .database import get_db
from .models import User, OperationLog
from .dingtalk import get_dingtalk_client
from .middleware import (
    get_current_user,
    get_optional_user,
    get_jwt_handler,
    is_auth_enabled,
    log_operation
)

logger = logging.getLogger(__name__)

# 创建路由器
router = APIRouter(prefix="/api/auth", tags=["auth"])


# ============ 请求/响应模型 ============

class DingTalkLoginRequest(BaseModel):
    """钉钉登录请求"""
    code: str  # 授权码


class DingTalkH5LoginRequest(BaseModel):
    """钉钉H5免登请求"""
    code: str  # 免登授权码


class LoginResponse(BaseModel):
    """登录响应"""
    token: str
    user: dict


class UserResponse(BaseModel):
    """用户信息响应"""
    user: dict


class OperationLogQuery(BaseModel):
    """操作日志查询参数"""
    user_id: Optional[int] = None
    action: Optional[str] = None
    resource: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    page: int = 1
    page_size: int = 20


# ============ 钉钉登录API ============

@router.post("/dingtalk/login", response_model=LoginResponse)
async def dingtalk_login(data: DingTalkLoginRequest, request: Request):
    """
    钉钉扫码登录

    通过钉钉授权码获取用户信息并登录
    """
    dingtalk_client = get_dingtalk_client()
    if not dingtalk_client:
        raise HTTPException(status_code=503, detail="钉钉服务未配置")

    try:
        # 通过授权码获取用户信息
        user_info = await dingtalk_client.get_user_info_by_code(data.code)

        # 查找或创建用户
        user = await _get_or_create_user(user_info)

        # 更新最后登录时间
        await _update_last_login(user.id)

        # 生成JWT Token
        jwt_handler = get_jwt_handler()
        token = jwt_handler.create_token(
            user_id=user.id,
            dingtalk_userid=user.dingtalk_userid,
            name=user.name,
            extra_data={"is_admin": user.is_admin}
        )

        # 记录登录日志
        await log_operation(
            user=user,
            action="login",
            resource="auth",
            detail={"method": "dingtalk_qrcode"},
            request=request
        )

        logger.info(f"用户登录成功: {user.name} ({user.dingtalk_userid})")

        return LoginResponse(token=token, user=user.to_dict())

    except Exception as e:
        logger.error(f"钉钉登录失败: {e}")
        raise HTTPException(status_code=401, detail=f"登录失败: {str(e)}")


@router.post("/dingtalk/h5-login", response_model=LoginResponse)
async def dingtalk_h5_login(data: DingTalkH5LoginRequest, request: Request):
    """
    钉钉H5免登（工作台内嵌应用）

    通过钉钉JSAPI获取的免登授权码登录
    """
    dingtalk_client = get_dingtalk_client()
    if not dingtalk_client:
        raise HTTPException(status_code=503, detail="钉钉服务未配置")

    try:
        # 通过授权码获取用户信息
        user_info = await dingtalk_client.get_user_info_by_code(data.code)

        # 查找或创建用户
        user = await _get_or_create_user(user_info)

        # 更新最后登录时间
        await _update_last_login(user.id)

        # 生成JWT Token
        jwt_handler = get_jwt_handler()
        token = jwt_handler.create_token(
            user_id=user.id,
            dingtalk_userid=user.dingtalk_userid,
            name=user.name,
            extra_data={"is_admin": user.is_admin}
        )

        # 记录登录日志
        await log_operation(
            user=user,
            action="login",
            resource="auth",
            detail={"method": "dingtalk_h5"},
            request=request
        )

        logger.info(f"用户H5免登成功: {user.name} ({user.dingtalk_userid})")

        return LoginResponse(token=token, user=user.to_dict())

    except Exception as e:
        logger.error(f"钉钉H5免登失败: {e}")
        raise HTTPException(status_code=401, detail=f"登录失败: {str(e)}")


@router.get("/dingtalk/qrcode-url")
async def get_qrcode_url(redirect_uri: str, state: str = ""):
    """
    获取钉钉扫码登录URL

    Args:
        redirect_uri: 回调地址
        state: 状态参数
    """
    dingtalk_client = get_dingtalk_client()
    if not dingtalk_client:
        raise HTTPException(status_code=503, detail="钉钉服务未配置")

    url = dingtalk_client.generate_qrcode_url(redirect_uri, state)
    return {"url": url}


@router.get("/dingtalk/config")
async def get_dingtalk_config():
    """
    获取钉钉配置信息（前端使用）

    返回AppKey和CorpId，用于前端初始化钉钉JSAPI
    """
    dingtalk_client = get_dingtalk_client()

    if not dingtalk_client:
        return {
            "enabled": False,
            "app_key": "",
            "corp_id": "",
            "agent_id": ""
        }

    return {
        "enabled": True,
        "app_key": dingtalk_client.app_key,
        "corp_id": dingtalk_client.corp_id,
        "agent_id": dingtalk_client.agent_id
    }


# ============ 用户信息API ============

@router.get("/user", response_model=UserResponse)
async def get_user_info(user: User = Depends(get_current_user)):
    """获取当前登录用户信息"""
    return UserResponse(user=user.to_dict())


@router.post("/logout")
async def logout(request: Request, user: User = Depends(get_current_user)):
    """登出"""
    # 记录登出日志
    await log_operation(
        user=user,
        action="logout",
        resource="auth",
        request=request
    )

    return {"status": "ok", "message": "已登出"}


@router.get("/status")
async def get_auth_status(user: Optional[User] = Depends(get_optional_user)):
    """
    获取认证状态

    返回当前认证是否启用，以及用户是否已登录
    """
    return {
        "auth_enabled": is_auth_enabled(),
        "logged_in": user is not None,
        "user": user.to_dict() if user else None
    }


# ============ 操作日志API ============

@router.get("/operation-logs")
async def get_operation_logs(
    user_id: Optional[int] = Query(None, description="用户ID"),
    action: Optional[str] = Query(None, description="操作类型"),
    resource: Optional[str] = Query(None, description="操作资源"),
    start_time: Optional[str] = Query(None, description="开始时间"),
    end_time: Optional[str] = Query(None, description="结束时间"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(get_current_user)
):
    """
    查询操作日志

    支持按用户、操作类型、资源、时间范围筛选
    """
    db = get_db()
    async with db.session_factory() as session:
        # 构建查询
        query = select(OperationLog)

        # 应用筛选条件
        if user_id:
            query = query.where(OperationLog.user_id == user_id)
        if action:
            query = query.where(OperationLog.action == action)
        if resource:
            query = query.where(OperationLog.resource == resource)
        if start_time:
            try:
                start_dt = datetime.fromisoformat(start_time)
                query = query.where(OperationLog.created_at >= start_dt)
            except ValueError:
                pass
        if end_time:
            try:
                end_dt = datetime.fromisoformat(end_time)
                query = query.where(OperationLog.created_at <= end_dt)
            except ValueError:
                pass

        # 获取总数
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await session.execute(count_query)
        total = total_result.scalar() or 0

        # 分页和排序
        query = query.order_by(desc(OperationLog.created_at))
        query = query.offset((page - 1) * page_size).limit(page_size)

        # 执行查询
        result = await session.execute(query)
        logs = result.scalars().all()

        return {
            "logs": [log.to_dict() for log in logs],
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size
        }


@router.get("/operation-logs/actions")
async def get_operation_actions(current_user: User = Depends(get_current_user)):
    """获取所有操作类型（用于筛选）"""
    db = get_db()
    async with db.session_factory() as session:
        query = select(OperationLog.action).distinct()
        result = await session.execute(query)
        actions = [row[0] for row in result.fetchall()]

        return {"actions": actions}


@router.get("/operation-logs/resources")
async def get_operation_resources(current_user: User = Depends(get_current_user)):
    """获取所有操作资源（用于筛选）"""
    db = get_db()
    async with db.session_factory() as session:
        query = select(OperationLog.resource).distinct()
        result = await session.execute(query)
        resources = [row[0] for row in result.fetchall()]

        return {"resources": resources}


# ============ 辅助函数 ============

async def _get_or_create_user(user_info: dict) -> User:
    """查找或创建用户"""
    db = get_db()
    async with db.session_factory() as session:
        # 查找现有用户
        result = await session.execute(
            select(User).where(User.dingtalk_userid == user_info["userid"])
        )
        user = result.scalar_one_or_none()

        if user:
            # 更新用户信息
            user.name = user_info.get("name", user.name)
            user.avatar = user_info.get("avatar", user.avatar)
            user.mobile = user_info.get("mobile", user.mobile)
            user.email = user_info.get("email", user.email)
            user.department = user_info.get("department", user.department)
            user.title = user_info.get("title", user.title)
            user.dingtalk_unionid = user_info.get("unionid", user.dingtalk_unionid)
            user.updated_at = datetime.now()
            await session.commit()
            await session.refresh(user)
        else:
            # 创建新用户
            user = User(
                dingtalk_userid=user_info["userid"],
                dingtalk_unionid=user_info.get("unionid"),
                name=user_info.get("name", ""),
                avatar=user_info.get("avatar"),
                mobile=user_info.get("mobile"),
                email=user_info.get("email"),
                department=user_info.get("department"),
                title=user_info.get("title"),
                is_active=True,
                is_admin=False,  # 默认非管理员
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)

            logger.info(f"创建新用户: {user.name} ({user.dingtalk_userid})")

        return user


async def _update_last_login(user_id: int):
    """更新用户最后登录时间"""
    db = get_db()
    async with db.session_factory() as session:
        result = await session.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalar_one_or_none()
        if user:
            user.last_login = datetime.now()
            await session.commit()
