"""数据库模型定义"""
from datetime import datetime
from typing import Optional

from sqlalchemy import String, Boolean, DateTime, Integer, Text, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class User(Base):
    """用户表"""
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # 钉钉用户信息
    dingtalk_userid: Mapped[str] = mapped_column(String(64), unique=True, index=True, comment="钉钉用户ID")
    dingtalk_unionid: Mapped[Optional[str]] = mapped_column(String(64), nullable=True, comment="钉钉UnionID")

    # 基本信息
    name: Mapped[str] = mapped_column(String(64), comment="姓名")
    avatar: Mapped[Optional[str]] = mapped_column(String(512), nullable=True, comment="头像URL")
    mobile: Mapped[Optional[str]] = mapped_column(String(20), nullable=True, comment="手机号")
    email: Mapped[Optional[str]] = mapped_column(String(128), nullable=True, comment="邮箱")
    department: Mapped[Optional[str]] = mapped_column(String(256), nullable=True, comment="部门")
    title: Mapped[Optional[str]] = mapped_column(String(64), nullable=True, comment="职位")

    # 状态
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, comment="是否启用")
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, comment="是否管理员")

    # 时间戳
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    last_login: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="最后登录时间")

    # 关联
    operation_logs: Mapped[list["OperationLog"]] = relationship("OperationLog", back_populates="user")

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "id": self.id,
            "dingtalk_userid": self.dingtalk_userid,
            "name": self.name,
            "avatar": self.avatar,
            "mobile": self.mobile,
            "email": self.email,
            "department": self.department,
            "title": self.title,
            "is_active": self.is_active,
            "is_admin": self.is_admin,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_login": self.last_login.isoformat() if self.last_login else None,
        }


class OperationLog(Base):
    """操作日志表"""
    __tablename__ = "operation_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # 用户信息
    user_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.id"), nullable=True, comment="用户ID")
    user_name: Mapped[Optional[str]] = mapped_column(String(64), nullable=True, comment="用户名称（冗余存储）")

    # 操作信息
    action: Mapped[str] = mapped_column(String(64), index=True, comment="操作类型")
    resource: Mapped[str] = mapped_column(String(128), comment="操作资源")
    resource_id: Mapped[Optional[str]] = mapped_column(String(64), nullable=True, comment="资源ID")
    detail: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True, comment="操作详情")

    # 请求信息
    method: Mapped[Optional[str]] = mapped_column(String(10), nullable=True, comment="请求方法")
    path: Mapped[Optional[str]] = mapped_column(String(256), nullable=True, comment="请求路径")
    ip_address: Mapped[Optional[str]] = mapped_column(String(64), nullable=True, comment="IP地址")
    user_agent: Mapped[Optional[str]] = mapped_column(String(512), nullable=True, comment="浏览器UA")

    # 结果
    status: Mapped[str] = mapped_column(String(16), default="success", comment="操作状态: success/failed")
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="错误信息")

    # 时间戳
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, index=True, comment="操作时间")

    # 关联
    user: Mapped[Optional["User"]] = relationship("User", back_populates="operation_logs")

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "user_name": self.user_name,
            "action": self.action,
            "resource": self.resource,
            "resource_id": self.resource_id,
            "detail": self.detail,
            "method": self.method,
            "path": self.path,
            "ip_address": self.ip_address,
            "status": self.status,
            "error_message": self.error_message,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
