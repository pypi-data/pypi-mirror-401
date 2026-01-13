from __future__ import annotations

import polars as pl

# Third-party imports
from sqlalchemy import Engine, Table, text
from sqlalchemy.exc import SQLAlchemyError

from yitool.const import __ENV__
from yitool.db.engine import get_engine
from yitool.db.yi_db import YiDB
from yitool.enums import DB_TYPE

# Local imports
from yitool.log import logger

# 元数据和表映射缓存
meta_table_map: dict[str, Table] = {}


class DB:
    def __init__(self, env_path: str = __ENV__, db_type: str = DB_TYPE.MYSQL.value):
        self._env_path = env_path
        self._db_type = db_type
        self._engine: Engine | None = None
        self._db: YiDB | None = None

    def init(self) -> YiDB:
        self._engine = get_engine(self._db_type, self._env_path)
        self._db = YiDB(self._engine)
        return self._db

    @property
    def engine(self) -> Engine | None:
        return self._engine

    @property
    def db(self) -> YiDB | None:
        return self._db

    @property
    def closed(self) -> bool:
        return self._db is None or self._db.closed

    def _ensure_db_initialized(self) -> bool:
        """确保数据库连接已初始化"""
        if self.closed:
            self.init()
        return self._db is not None

    def execute(self, sql: str) -> bool:
        if not self._ensure_db_initialized():
            return False
        try:
            with self._engine.connect() as conn:
                conn.execute(text(sql))
            return True
        except SQLAlchemyError as err:
            logger.error(f"Error occurred while executing SQL: {sql}, Error: {err}")
            return False

    def drop_table(self, table_name: str) -> bool:
        if not self._ensure_db_initialized():
            return False
        try:
            with self._engine.connect() as conn:
                conn.execute(text(f"DROP TABLE IF EXISTS {table_name}"))
            return True
        except SQLAlchemyError as err:
            logger.error(f"Error occurred while dropping table: {table_name}, Error: {err}")
            return False

    def exists(self, table_name: str) -> bool:
        if not self._ensure_db_initialized():
            return False
        return self._db.exists(table_name)

    def truncate(self, table_name: str) -> bool:
        if not self._ensure_db_initialized():
            return False
        if not self.exists(table_name):
            return False
        try:
            with self._engine.connect() as conn:
                conn.execute(text(f"TRUNCATE TABLE {table_name}"))
            return True
        except SQLAlchemyError as err:
            logger.error(f"Error occurred while truncating table: {table_name}, Error: {err}")
            return False

    def read(self, sql: str, schema_overrides=None) -> pl.DataFrame | None:
        if not self._ensure_db_initialized():
            return None
        try:
            df = self._db.read(sql, schema_overrides=schema_overrides)
            return df
        except SQLAlchemyError as err:
            logger.error(f"Error occurred while reading data with SQL: {sql}, Error: {err}")
            return pl.DataFrame()  # 统一返回空DataFrame以避免None处理

    def write(self, df: pl.DataFrame, table_name: str, if_table_exists: str = "append") -> int:
        if not self._ensure_db_initialized():
            return 0
        try:
            num = self._db.write(df, table_name, if_table_exists=if_table_exists)
            return num
        except SQLAlchemyError as err:
            logger.error(f"Error occurred while writing data to table: {table_name}, Error: {err}")
            return 0
