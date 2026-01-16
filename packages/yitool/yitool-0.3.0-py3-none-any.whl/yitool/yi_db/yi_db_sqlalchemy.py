from __future__ import annotations

from time import sleep
from typing import Any

from pymysql import OperationalError
from sqlalchemy import Connection, Engine, MetaData, Table, create_engine, inspect, text
from sqlalchemy.engine.reflection import Inspector
from sqlalchemy.orm import Session

from yitool.const import __ENV__
from yitool.enums import DB_TYPE
from yitool.log import logger
from yitool.utils.dict_utils import DictUtils
from yitool.utils.env_utils import EnvUtils
from yitool.utils.url_utils import UrlUtils
from yitool.yi_db._abc import AbcYiDB

DB_CHARSET_GBK = "cp936"

class YiDB(AbcYiDB):
    """数据库工具，engine 为 sqlalchemy 的 Engine"""

    _connection: Connection = None
    _engine: Engine = None
    _slave_db: YiDB | None = None
    _tasks_db: YiDB | None = None
    _datasource: Any | None = None

    def __init__(self, engine: Engine, max_retries: int = 3):
        self._engine = engine
        self._connection = None
        self._slave_db = None
        self._tasks_db = None
        self._datasource = None
        self._max_retries = max_retries

    @property
    def engine(self) -> Engine:
        return self._engine

    @property
    def connection(self) -> Connection:
        return self._connection

    @property
    def closed(self) -> bool:
        return self._connection is None or self._connection.closed

    def connect(self):
        """连接数据库"""
        if self.closed:
            self._connection = self._engine.connect()
        return self._connection

    def close(self):
        """关闭数据库连接"""
        try:
            if self._connection and not self._connection.closed:
                self._connection.close()
        except Exception as err:
            logger.error(f"close db connection error: {err}")

    def get_session(self) -> Session:
        """获取 SQLAlchemy ORM 会话"""
        return Session(self._engine)

    def execute(self, query: str, params: dict[str, Any] | None = None, retry_times: int | None = None) -> Any:
        """执行 SQL 查询

        Args:
            query: SQL查询语句
            params: 查询参数
            retry_times: 重试次数

        Returns:
            查询结果
        """
        # 使用实例配置的重试次数，或方法参数提供的重试次数
        max_retries = retry_times if retry_times is not None else self._max_retries
        params = params or {}

        # 预编译SQL语句，提高执行效率
        compiled_query = text(query)

        try:
            # 如果已经有活跃的连接并且在事务中，使用该连接
            if not self.closed and self._connection.in_transaction():
                result = self._connection.execute(compiled_query, params)
                # 事务中的操作由外部控制提交/回滚
                return result
            # 否则使用新连接
            else:
                with self._engine.connect() as conn:
                    result = conn.execute(compiled_query, params)
                    conn.commit()
                    return result
        except Exception as err:
            logger.error(f"execute sql error (query: {query}): {err}")
            # 检查是否在事务中，如果在事务中则不dispose引擎，否则dispose
            if not (not self.closed and self._connection.in_transaction()):
                self._engine.dispose()
            sleep(3)
            if max_retries <= 0:
                raise
            return self.execute(query, params, retry_times=max_retries-1)

    def execute_many(self, query: str, params_list: list[dict[str, Any]] | None = None, retry_times: int | None = None) -> Any:
        """批量执行 SQL 查询，提高批量操作效率

        Args:
            query: SQL查询语句
            params_list: 查询参数列表
            retry_times: 重试次数

        Returns:
            查询结果
        """
        if not params_list:
            return None

        # 使用实例配置的重试次数，或方法参数提供的重试次数
        max_retries = retry_times if retry_times is not None else self._max_retries

        # 预编译SQL语句
        compiled_query = text(query)

        try:
            # 检查是否有活跃的连接并且在事务中
            in_transaction = not self.closed and self._connection.in_transaction()
            conn = self._connection if in_transaction else self._engine.connect()
            
            try:
                # SQLAlchemy的Connection对象没有executemany方法，使用execute处理批量参数
                result = conn.execute(compiled_query, params_list)
                if not in_transaction:
                    conn.commit()
                return result
            finally:
                if not in_transaction:
                    conn.close()
        except Exception as err:
            logger.error(f"execute_many sql error (query: {query}): {err}")
            # 检查是否在事务中，如果在事务中则不dispose引擎，否则dispose
            if not (not self.closed and self._connection.in_transaction()):
                self._engine.dispose()
            sleep(3)
            if max_retries <= 0:
                raise
            return self.execute_many(query, params_list, retry_times=max_retries-1)

    def begin(self) -> None:
        """开始事务"""
        if self.closed:
            self.connect()
        if not self._connection.in_transaction():
            self._connection.begin()

    def commit(self) -> None:
        """提交事务"""
        if not self.closed and self._connection.in_transaction():
            self._connection.commit()

    def rollback(self) -> None:
        """回滚事务"""
        if not self.closed and self._connection.in_transaction():
            self._connection.rollback()

    def add(self, instance: Any) -> None:
        """添加单个 ORM 实例"""
        with self.get_session() as session:
            session.add(instance)
            session.commit()

    def add_all(self, instances: list[Any]) -> None:
        """添加多个 ORM 实例"""
        with self.get_session() as session:
            session.add_all(instances)
            session.commit()

    def query(self, model: Any, *criteria: Any, **filters: Any) -> list[Any]:
        """使用 ORM 模型查询数据"""
        with self.get_session() as session:
            query = session.query(model)
            if criteria:
                query = query.filter(*criteria)
            if filters:
                query = query.filter_by(**filters)
            return query.all()

    @property
    def inspector(self) -> Inspector:
        """获取数据库检查器"""
        return inspect(self._engine)

    @property
    def metadata(self) -> MetaData:
        """获取数据库元数据"""
        # SQLAlchemy 2.0+ 不再支持在 MetaData 构造函数中使用 bind 参数
        return MetaData()

    @property
    def tables(self) -> dict[str, Table]:
        """获取数据库所有表"""
        meta = self.metadata
        meta.reflect(bind=self._engine)
        return meta.tables

    def exists(self, table_name: str) -> bool:
        """检查表是否存在"""
        inspector = inspect(self._engine)
        return table_name in inspector.get_table_names()

    def columns(self, table_name: str) -> list:
        """获取表的所有列名"""
        if not self.exists(table_name):
            return []
        inspector = inspect(self._engine)
        return inspector.get_columns(table_name)

    def column_names(self, table_name: str) -> list[str] | None:
        """获取表的所有列名"""
        columns = self.columns(table_name)
        if columns is None:
            return None
        return [col["name"] for col in columns]

    def primary_key(self, table_name: str) -> list[str] | None:
        """获取表的主键列名"""
        if not self.exists(table_name):
            return None
        pk = self.inspector.get_pk_constraint(table_name)
        return pk.get("constrained_columns", []) if pk else []

    def read(self, query: str, schema_overrides: dict | None = None, retry_times: int | None = None) -> list[dict[str, Any]]:
        """从数据库读取数据"""
        # 使用实例配置的重试次数，或方法参数提供的重试次数
        max_retries = retry_times if retry_times is not None else self._max_retries
        try:
            result = []
            params = schema_overrides or {}
            compiled_query = text(query)
            
            # 如果已经有活跃的连接并且在事务中，使用该连接
            if not self.closed and self._connection.in_transaction():
                cursor = self._connection.execute(compiled_query, params)
                columns = cursor.keys()
                result = [dict(zip(columns, row, strict=True)) for row in cursor.fetchall()]
            # 否则使用新连接
            else:
                with self._engine.connect() as conn:
                    cursor = conn.execute(compiled_query, params)
                    columns = cursor.keys()
                    result = [dict(zip(columns, row, strict=True)) for row in cursor.fetchall()]
            return result
        except Exception as err:
            logger.error(f"read from db error (query: {query}): {err}")
            # 检查是否在事务中，如果在事务中则不dispose引擎，否则dispose
            if not (not self.closed and self._connection.in_transaction()):
                self._engine.dispose()
            sleep(3)
            if max_retries <= 0:
                return []
            return self.read(query, schema_overrides, retry_times=max_retries-1)

    def write(self, data: list[dict[str, Any]] | Any, table_name: str, if_table_exists: str = "append", retry_times: int | None = None, batch_size: int = 1000) -> int:
        """写入数据库表，支持批量操作优化

        Args:
            data: 要写入的数据，可以是字典列表或ORM实例
            table_name: 表名
            if_table_exists: 表存在时的处理方式，append或replace
            retry_times: 重试次数
            batch_size: 批量写入大小，默认1000条

        Returns:
            写入的记录数
        """
        num = 0
        # 使用实例配置的重试次数，或方法参数提供的重试次数
        max_retries = retry_times if retry_times is not None else self._max_retries

        try:
            if isinstance(data, list):
                if not data:
                    return 0

                if isinstance(data[0], dict):
                    # 批量插入字典列表，优化为分批处理
                    metadata = MetaData()
                    table = Table(table_name, metadata, autoload_with=self._engine)
                    
                    # 获取表的所有列名
                    table_columns = [column.name for column in table.columns]
                    
                    # 检查是否有活跃的连接并且在事务中
                    in_transaction = not self.closed and self._connection.in_transaction()
                    conn = self._connection if in_transaction else self._engine.connect()
                    
                    try:
                        if if_table_exists == "replace":
                            conn.execute(table.delete())
                            if not in_transaction:
                                conn.commit()

                        # 分批插入，避免内存占用过高
                        for i in range(0, len(data), batch_size):
                            batch_data = data[i:i+batch_size]
                            
                            # 过滤数据，只保留表中存在的列
                            filtered_batch = []
                            for item in batch_data:
                                filtered_item = {k: v for k, v in item.items() if k in table_columns}
                                filtered_batch.append(filtered_item)
                            
                            result = conn.execute(table.insert().values(filtered_batch))
                            if not in_transaction:
                                conn.commit()
                            num += result.rowcount
                    finally:
                        if not in_transaction:
                            conn.close()
                else:
                    # 支持ORM模型实例，优化为分批处理
                    # ORM实例使用Session，不支持事务连接共享
                    with Session(self._engine) as session:
                        if if_table_exists == "replace":
                            # 清空表
                            session.query(type(data[0])).delete()
                            session.commit()

                        # 分批添加，避免内存占用过高
                        for i in range(0, len(data), batch_size):
                            batch_data = data[i:i+batch_size]
                            session.add_all(batch_data)
                            session.commit()
                            session.flush()  # 清空session，释放内存
                            session.expunge_all()  # 清除所有实例
                            num += len(batch_data)
            else:
                # 单个ORM实例
                with Session(self._engine) as session:
                    session.add(data)
                    session.commit()
                    num = 1
        except OperationalError as db_error:
            logger.error(f"write to db error (table: {table_name}): {db_error}")
            # 检查是否在事务中，如果在事务中则不dispose引擎，否则dispose
            if not (not self.closed and self._connection.in_transaction()):
                self._engine.dispose()
            sleep(3)
            if max_retries <= 0:
                return num
            return self.write(data, table_name, if_table_exists=if_table_exists, retry_times=max_retries-1, batch_size=batch_size)
        except Exception as err:
            logger.error(f"write to db error (table: {table_name}): {err}")
            # 检查是否在事务中，如果在事务中则不dispose引擎，否则dispose
            if not (not self.closed and self._connection.in_transaction()):
                self._engine.dispose()
            sleep(3)
            if max_retries <= 0:
                return num
            return self.write(data, table_name, if_table_exists=if_table_exists, retry_times=max_retries-1, batch_size=batch_size)
        return num

    @staticmethod
    def load_env_values(values: dict[str, str], db_type: str = DB_TYPE.MYSQL.value) -> dict[str, str]:
        db_prefix = db_type.upper()
        return {
            "username": DictUtils.get_value_or_raise(values, f"{db_prefix}_USERNAME"),
            "password": DictUtils.get_value_or_raise(values, f"{db_prefix}_PASSWORD"),
            "host": DictUtils.get_value_or_raise(values, f"{db_prefix}_HOST"),
            "port": DictUtils.get_value_or_raise(values, f"{db_prefix}_PORT"),
        }

    @staticmethod
    def create_engine(
        database: str | None = None,
        db_type_value: str = DB_TYPE.MYSQL.value,
        env_path: str = __ENV__,
        charset: str | None = None,
        config: Any | None = None
    ) -> Engine:
        """创建数据库引擎

        支持两种方式创建引擎：
        1. 从环境变量创建（传统方式）
        2. 从 DatabaseConfig 创建（推荐方式，支持连接池配置）
        """
        if config:
            # 从 DatabaseConfig 创建引擎
            from yitool.yi_config.database import DatabaseConfig
            if isinstance(config, DatabaseConfig):
                logger.debug(f"Creating engine from DatabaseConfig: {config.url}")
                engine_kwargs = {
                    "pool_size": config.pool_size,
                    "max_overflow": config.max_overflow,
                    "pool_timeout": config.pool_timeout,
                    "pool_recycle": config.pool_recycle
                }
                return create_engine(config.url, **engine_kwargs)
            else:
                raise TypeError(f"Expected DatabaseConfig, got {type(config).__name__}")

        # 传统方式：从环境变量创建
        if not DB_TYPE.has(db_type_value):
            raise ValueError(f"不支持的数据库类型: {db_type_value}")

        if not database:
            raise ValueError("Database name is required when not using DatabaseConfig")

        values = EnvUtils.dotenv_values(env_path)
        db_values = YiDB.load_env_values(values, db_type_value)
        db_url = UrlUtils.url_from_db_type(db_type_value)(**db_values, database=database)
        logger.debug(f"Connecting to database with URL: {db_url}")

        # 优化连接池配置，提高性能和可靠性
        engine_kwargs = {
            "pool_size": 10,  # 默认连接池大小
            "max_overflow": 20,  # 最大溢出连接数
            "pool_timeout": 30,  # 连接超时时间
            "pool_recycle": 3600,  # 连接回收时间
            "pool_pre_ping": True,  # 连接池预检测，确保连接有效
            "pool_use_lifo": True,  # 使用LIFO策略，提高连接复用率
            "echo": False,  # 关闭SQL日志，提高性能
            "echo_pool": False  # 关闭连接池日志，提高性能
        }

        if db_type_value == DB_TYPE.MSSQL.value:
            if charset is not None:
                engine_kwargs["connect_args"] = {"charset": charset}
            else:
                engine_kwargs["connect_args"] = {"charset": "utf8"}

        return create_engine(db_url, **engine_kwargs)

    @classmethod
    def from_env(cls, database: str, db_type_value: str = DB_TYPE.MYSQL.value, env_path: str = __ENV__, charset: str | None = None) -> YiDB:
        engine = cls.create_engine(database, db_type_value, env_path, charset)
        return cls(engine)

    @classmethod
    def from_config(cls, config: Any) -> YiDB:
        """从 DatabaseConfig 创建 YiDB 实例

        Args:
            config: DatabaseConfig 对象，包含数据库连接信息和连接池配置

        Returns:
            YiDB 实例
        """
        from yitool.yi_config.database import DatabaseConfig
        if not isinstance(config, DatabaseConfig):
            raise TypeError(f"Expected DatabaseConfig, got {type(config).__name__}")
        engine = cls.create_engine(config=config)
        return cls(engine)

    @classmethod
    def from_datasource(cls, datasource: Any) -> YiDB:
        """从 DataSourceConfig 创建 YiDB 实例

        Args:
            datasource: DataSourceConfig 对象，包含主从等数据源配置

        Returns:
            YiDB 实例，其中包含主库连接，从库和任务库连接可通过属性访问
        """
        from yitool.yi_config.datasource import DataSourceConfig

        if not isinstance(datasource, DataSourceConfig):
            raise TypeError(f"Expected DataSourceConfig, got {type(datasource).__name__}")

        # 创建主库实例
        master_db = cls.from_config(datasource.master)
        master_db._datasource = datasource

        # 创建从库实例（如果有）
        if datasource.slave:
            master_db._slave_db = cls.from_config(datasource.slave)

        # 创建任务库实例（如果有）
        if datasource.tasks:
            master_db._tasks_db = cls.from_config(datasource.tasks)

        return master_db

    @property
    def slave(self) -> YiDB | None:
        """获取从库 YiDB 实例

        Returns:
            从库 YiDB 实例，如果没有配置从库则返回 None
        """
        return self._slave_db

    @property
    def tasks(self) -> YiDB | None:
        """获取任务库 YiDB 实例

        Returns:
            任务库 YiDB 实例，如果没有配置任务库则返回 None
        """
        return self._tasks_db

    @property
    def has_slave(self) -> bool:
        """是否配置了从库

        Returns:
            如果配置了从库则返回 True，否则返回 False
        """
        return self._slave_db is not None

    @property
    def has_tasks(self) -> bool:
        """是否配置了任务库

        Returns:
            如果配置了任务库则返回 True，否则返回 False
        """
        return self._tasks_db is not None


# 延迟注册 YiDB 到工厂类，避免循环导入
try:
    from yitool.yi_db.yi_db import YiDBFactory, YiDBType
    YiDBFactory.register(YiDBType.SQLALCHEMY, YiDB)
except ImportError:
    pass
