"""JWT Token 处理"""
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from jose import jwt, JWTError

logger = logging.getLogger(__name__)


class JWTHandler:
    """JWT Token 处理器"""

    def __init__(
        self,
        secret_key: str,
        algorithm: str = "HS256",
        expire_hours: int = 24
    ):
        """
        初始化JWT处理器

        Args:
            secret_key: 密钥
            algorithm: 加密算法
            expire_hours: Token过期时间（小时）
        """
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expire_hours = expire_hours

    def create_token(
        self,
        user_id: int,
        dingtalk_userid: str,
        name: str,
        extra_data: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        创建JWT Token

        Args:
            user_id: 用户ID
            dingtalk_userid: 钉钉用户ID
            name: 用户名称
            extra_data: 额外数据

        Returns:
            JWT Token字符串
        """
        expire = datetime.utcnow() + timedelta(hours=self.expire_hours)

        payload = {
            "sub": str(user_id),
            "dingtalk_userid": dingtalk_userid,
            "name": name,
            "exp": expire,
            "iat": datetime.utcnow(),
        }

        if extra_data:
            payload.update(extra_data)

        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return token

    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        验证JWT Token

        Args:
            token: JWT Token字符串

        Returns:
            解码后的payload，验证失败返回None
        """
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm]
            )
            return payload
        except JWTError as e:
            logger.warning(f"JWT验证失败: {e}")
            return None

    def get_user_id(self, token: str) -> Optional[int]:
        """
        从Token中获取用户ID

        Args:
            token: JWT Token字符串

        Returns:
            用户ID，验证失败返回None
        """
        payload = self.verify_token(token)
        if payload and "sub" in payload:
            try:
                return int(payload["sub"])
            except (ValueError, TypeError):
                return None
        return None

    def refresh_token(self, token: str) -> Optional[str]:
        """
        刷新Token（延长过期时间）

        Args:
            token: 原JWT Token

        Returns:
            新的JWT Token，验证失败返回None
        """
        payload = self.verify_token(token)
        if not payload:
            return None

        # 创建新Token
        return self.create_token(
            user_id=int(payload["sub"]),
            dingtalk_userid=payload.get("dingtalk_userid", ""),
            name=payload.get("name", ""),
            extra_data={
                k: v for k, v in payload.items()
                if k not in ("sub", "dingtalk_userid", "name", "exp", "iat")
            }
        )
