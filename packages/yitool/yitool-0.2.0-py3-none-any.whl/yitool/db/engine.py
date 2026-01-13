"""数据库引擎管理模块"""

from __future__ import annotations

from sqlalchemy import Engine
from sqlalchemy.exc import SQLAlchemyError

from yitool.const import __ENV__
from yitool.db.yi_db import YiDB
from yitool.log import logger

# 数据库引擎缓存
engine_map: dict[str, dict[str, Engine]] = {}
charset_engine_map: dict[str, dict[str, Engine]] = {}


def get_engine(
    db_type: str,
    db_name: str,
    env_file: str = __ENV__,
    charset: str | None = None
) -> Engine:
    """获取数据库引擎

    Args:
        db_type: 数据库类型
        db_name: 数据库名称
        env_file: 环境文件路径
        charset: 字符集

    Returns:
        数据库引擎对象
    """
    if charset is not None:
        if db_type not in charset_engine_map:
            charset_engine_map[db_type] = {}
        if db_name not in charset_engine_map[db_type]:
            engine = YiDB.create_engine(db_name, db_type, env_file=env_file, charset=charset)
            charset_engine_map[db_type][db_name] = engine
        return charset_engine_map[db_type][db_name]

    if db_type not in engine_map:
        engine_map[db_type] = {}
    if db_name not in engine_map[db_type]:
        engine = YiDB.create_engine(db_name, db_type, env_file=env_file)
        engine_map[db_type][db_name] = engine
    return engine_map[db_type][db_name]


def close_engine(db_type: str, db_name: str, charset: str | None = None) -> bool:
    """关闭数据库引擎

    Args:
        db_type: 数据库类型
        db_name: 数据库名称
        charset: 字符集

    Returns:
        是否成功关闭
    """
    try:
        if charset is not None:
            if db_type in charset_engine_map and db_name in charset_engine_map[db_type]:
                engine = charset_engine_map[db_type].pop(db_name)
                engine.dispose()
                return True
        else:
            if db_type in engine_map and db_name in engine_map[db_type]:
                engine = engine_map[db_type].pop(db_name)
                engine.dispose()
                return True
        return False
    except SQLAlchemyError as err:
        logger.error(f"Error occurred while closing engine: {err}")
        return False


def close_all_engines() -> None:
    """关闭所有数据库引擎"""
    # 关闭字符集引擎
    for db_type in list(charset_engine_map.keys()):
        for db_name in list(charset_engine_map[db_type].keys()):
            close_engine(db_type, db_name, charset="utf8mb4")

    # 关闭普通引擎
    for db_type in list(engine_map.keys()):
        for db_name in list(engine_map[db_type].keys()):
            close_engine(db_type, db_name)
