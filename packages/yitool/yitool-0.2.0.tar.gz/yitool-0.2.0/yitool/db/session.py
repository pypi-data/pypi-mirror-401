"""数据库会话管理模块"""

from __future__ import annotations

from collections.abc import Generator
from contextlib import contextmanager

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker

from yitool.db.engine import get_engine
from yitool.log import logger

# 会话工厂缓存
session_factory_map: dict[tuple[str, str, str | None], sessionmaker] = {}


def get_session_factory(
    db_type: str,
    db_name: str,
    env_file: str,
    charset: str | None = None
) -> sessionmaker:
    """获取会话工厂

    Args:
        db_type: 数据库类型
        db_name: 数据库名称
        env_file: 环境文件路径
        charset: 字符集

    Returns:
        会话工厂对象
    """
    key = (db_type, db_name, charset)
    if key not in session_factory_map:
        engine = get_engine(db_type, db_name, env_file, charset)
        session_factory_map[key] = sessionmaker(bind=engine)
    return session_factory_map[key]


@contextmanager
def get_db_session(
    db_type: str,
    db_name: str,
    env_file: str,
    charset: str | None = None
) -> Generator[Session, None, None]:
    """获取数据库会话上下文管理器

    Args:
        db_type: 数据库类型
        db_name: 数据库名称
        env_file: 环境文件路径
        charset: 字符集

    Yields:
        数据库会话对象
    """
    session_factory = get_session_factory(db_type, db_name, env_file, charset)
    session = session_factory()
    try:
        yield session
        session.commit()
    except SQLAlchemyError as err:
        session.rollback()
        logger.error(f"Database session error: {err}")
        raise
    finally:
        session.close()


def create_scoped_session(
    db_type: str,
    db_name: str,
    env_file: str,
    charset: str | None = None
) -> Session:
    """创建作用域会话

    Args:
        db_type: 数据库类型
        db_name: 数据库名称
        env_file: 环境文件路径
        charset: 字符集

    Returns:
        数据库会话对象
    """
    session_factory = get_session_factory(db_type, db_name, env_file, charset)
    return session_factory()
