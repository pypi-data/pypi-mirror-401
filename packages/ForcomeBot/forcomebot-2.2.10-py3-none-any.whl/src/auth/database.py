"""数据库连接管理"""
import logging
from pathlib import Path
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

logger = logging.getLogger(__name__)


class Base(DeclarativeBase):
    """SQLAlchemy 基类"""
    pass


class Database:
    """数据库管理器"""

    def __init__(self, db_path: str = "data/app.db"):
        self.db_path = db_path
        self.engine = None
        self.session_factory = None

    async def init(self):
        """初始化数据库连接"""
        # 确保目录存在
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

        # 创建异步引擎
        self.engine = create_async_engine(
            f"sqlite+aiosqlite:///{self.db_path}",
            echo=False,
            future=True
        )

        # 创建会话工厂
        self.session_factory = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

        # 创建表
        async with self.engine.begin() as conn:
            from .models import User, OperationLog  # 导入模型以注册
            await conn.run_sync(Base.metadata.create_all)

        logger.info(f"数据库初始化完成: {self.db_path}")

    async def close(self):
        """关闭数据库连接"""
        if self.engine:
            await self.engine.dispose()
            logger.info("数据库连接已关闭")

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """获取数据库会话"""
        if not self.session_factory:
            raise RuntimeError("数据库未初始化")

        async with self.session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise


# 全局数据库实例
_database: Database = None


async def init_database(db_path: str = "data/app.db") -> Database:
    """初始化全局数据库实例"""
    global _database
    _database = Database(db_path)
    await _database.init()
    return _database


def get_db() -> Database:
    """获取全局数据库实例"""
    if _database is None:
        raise RuntimeError("数据库未初始化，请先调用 init_database()")
    return _database
