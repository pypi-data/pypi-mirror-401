import os

import yaml
from pydantic_settings import BaseSettings, SettingsConfigDict

from yitool.log import LogConfig, setup_logging
from yitool.utils.dict_utils import DictUtils
from yitool.yi_config.api_key import APIKeyConfig
from yitool.yi_config.app import AppConfig
from yitool.yi_config.celery import CeleryConfig
from yitool.yi_config.cors import CORSConfig
from yitool.yi_config.database import DatabaseConfig
from yitool.yi_config.datasource import DataSourceConfig
from yitool.yi_config.jwt import JWTConfig
from yitool.yi_config.middleware import MiddlewareConfig
from yitool.yi_config.server import ServerConfig


class YiSettings(BaseSettings):
    app: AppConfig
    server: ServerConfig
    database: DatabaseConfig | None = None
    datasource: DataSourceConfig
    jwt: JWTConfig | None = None
    cors: CORSConfig | None = None
    celery: CeleryConfig | None = None
    api_key: APIKeyConfig | None = None
    middleware: MiddlewareConfig | None = None
    log: LogConfig = LogConfig()

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="allow"
    )


class YiConfig:
    """全局配置管理类，实现单例模式"""

    _instance = None
    _settings = None

    # 配置缓存，避免重复加载相同的配置文件
    _config_cache = {}
    _datasource_cache = {}

    def __new__(cls, singleton: bool = True, config_source: str | dict | None = None):
        """实现单例模式，支持创建自定义实例

        Args:
            singleton: 是否创建单例实例，True 表示使用或创建单例，False 表示创建新实例
            config_source: 配置源，可以是文件路径字符串或配置字典
        """
        if not singleton or cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize(config_source)
        return cls._instance

    @classmethod
    def instance(cls):
        """获取单例实例"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _initialize(self, config_source: str | dict | None = None):
        """初始化配置

        Args:
            config_source: 配置源，可以是文件路径字符串或配置字典
        """
        # 保存配置源
        self._config_source = config_source

        # 根据配置源类型加载配置
        if isinstance(config_source, str):
            # 从指定文件加载配置
            self._load_from_file(config_source)
        elif isinstance(config_source, dict):
            # 从字典加载配置
            self._load_from_dict(config_source)
        else:
            # 默认行为：从文件系统加载
            yaml_config = self.load_yaml_config()
            datasource_config = self.load_datasource_config()
            self._set_settings(yaml_config, datasource_config)

        # 初始化日志系统
        setup_logging(self._settings.log)

    def _load_from_file(self, file_path: str):
        """从指定文件加载配置

        Args:
            file_path: 配置文件路径
        """
        with open(file_path) as f:
            config_dict = yaml.safe_load(f) or {}

        # 提取数据源配置
        datasource_config = config_dict.get("datasource", {})
        if not datasource_config:
            # 如果主配置中没有数据源，尝试从默认datasource.yml加载
            datasource_config = self.load_datasource_config()

        self._set_settings(config_dict, datasource_config)

    def _load_from_dict(self, config_dict: dict):
        """从字典加载配置

        Args:
            config_dict: 配置字典
        """
        config_dict = config_dict or {}

        # 提取数据源配置
        datasource_config = config_dict.get("datasource", {})
        if not datasource_config:
            # 如果字典中没有数据源，使用默认配置
            datasource_config = {
                "master": {
                    "url": "sqlite+aiosqlite:///:memory:",
                    "pool_size": 5,
                    "max_overflow": 10
                }
            }

        self._set_settings(config_dict, datasource_config)

    def _set_settings(self, yaml_config: dict, datasource_config: dict):
        # 确保 yaml_config 包含必要的键
        yaml_config = yaml_config or {}
        # 使用默认值或空字典，确保不会因为缺少键而报错
        self._settings = YiSettings(
            app=AppConfig(**yaml_config.get("app", {})),
            server=ServerConfig(**yaml_config.get("server", {})),
            database=DatabaseConfig(**yaml_config.get("database", {})) if yaml_config.get("database") else None,
            datasource=DataSourceConfig(**datasource_config),
            jwt=JWTConfig(**yaml_config.get("jwt", {})) if yaml_config.get("jwt") else None,
            cors=CORSConfig(**yaml_config.get("cors", {})) if yaml_config.get("cors") else None,
            celery=CeleryConfig(**yaml_config.get("celery", {})) if yaml_config.get("celery") else None,
            api_key=APIKeyConfig(**yaml_config.get("api_key", {})),
            middleware=None,
            log=LogConfig(**yaml_config.get("log", {})),
        )

    def load_yaml_config(self) -> dict:
        """Load configuration from YAML file, supporting environment-specific configs.

        Priority: environment-specific config > default config
        Environment is determined by __YI_ENV__ environment variable, defaulting to "dev"
        """
        # Get environment from env var, default to "dev"
        env = os.getenv("__YI_ENV__", "dev")

        # 构建缓存键
        cache_key = f"{env}:yaml"

        # 检查缓存
        if cache_key in self._config_cache:
            return self._config_cache[cache_key]

        # Default config file path
        default_config_path = "application.yml"

        # Environment-specific config file path
        env_config_path = f"application.{env}.yml"

        # Load default config
        config: dict = {}
        try:
            with open(default_config_path) as f:
                config = yaml.safe_load(f) or {}
        except FileNotFoundError:
            pass

        # Load and merge environment-specific config if it exists
        try:
            with open(env_config_path) as f:
                env_config = yaml.safe_load(f)
                if env_config:
                    # Merge environment config into default config
                    config = DictUtils.deep_merge(config, env_config)
        except FileNotFoundError:
            pass

        # 缓存结果
        self._config_cache[cache_key] = config

        return config

    def load_datasource_config(self, file_path: str = "datasource.yml") -> dict:
        """Load datasource configuration from YAML file."""
        # 检查缓存
        if file_path in self._datasource_cache:
            return self._datasource_cache[file_path]

        try:
            with open(file_path) as f:
                config = yaml.safe_load(f)
                if isinstance(config, dict):
                    if "datasource" in config:
                        result = config["datasource"]
                    else:
                        # 直接使用配置文件内容作为数据源配置
                        result = config
                else:
                    # 配置文件格式不正确，返回默认配置
                    result = {
                        "master": {
                            "url": "sqlite+aiosqlite:///:memory:",
                            "pool_size": 5,
                            "max_overflow": 10
                        }
                    }
        except FileNotFoundError:
            # 文件不存在，返回默认配置
            result = {
                "master": {
                    "url": "sqlite+aiosqlite:///:memory:",
                    "pool_size": 5,
                    "max_overflow": 10
                }
            }
        except Exception:
            # 其他异常，返回默认配置
            result = {
                "master": {
                    "url": "sqlite+aiosqlite:///:memory:",
                    "pool_size": 5,
                    "max_overflow": 10
                }
            }

        # 缓存结果
        self._datasource_cache[file_path] = result

        return result

    @property
    def settings(self) -> YiSettings:
        """获取全局 settings 实例"""
        return self._settings

    def update(self, config_dict: dict):
        """更新配置

        Args:
            config_dict: 新的配置字典，用于更新现有配置
        """
        from yitool.utils.dict_utils import DictUtils
        
        # 合并现有配置和新配置
        current_config = {
            "app": self._settings.app.model_dump(),
            "server": self._settings.server.model_dump(),
            "database": self._settings.database.model_dump() if self._settings.database else None,
            "jwt": self._settings.jwt.model_dump() if self._settings.jwt else None,
            "cors": self._settings.cors.model_dump() if self._settings.cors else None,
            "celery": self._settings.celery.model_dump() if self._settings.celery else None,
            "api_key": self._settings.api_key.model_dump() if self._settings.api_key else None,
        }
        
        # 过滤掉 None 值
        current_config = {k: v for k, v in current_config.items() if v is not None}
        
        # 合并新配置
        merged_config = DictUtils.deep_merge(current_config, config_dict)
        
        # 重新设置配置，保持现有数据源配置
        datasource_config = self._settings.datasource.model_dump() if self._settings.datasource else {}
        self._set_settings(merged_config, datasource_config)




    def with_database(self, **kwargs) -> "YiConfig":
        """设置数据库配置（链式 API）

        Args:
            **kwargs: 数据库配置参数

        Returns:
            YiConfig: 配置实例，用于链式调用
        """
        self._settings.database = DatabaseConfig(**kwargs)
        return self

    def with_jwt(self, **kwargs) -> "YiConfig":
        """设置 JWT 配置（链式 API）

        Args:
            **kwargs: JWT 配置参数

        Returns:
            YiConfig: 配置实例，用于链式调用
        """
        self._settings.jwt = JWTConfig(**kwargs)
        return self

    def with_cors(self, **kwargs) -> "YiConfig":
        """设置 CORS 配置（链式 API）

        Args:
            **kwargs: CORS 配置参数

        Returns:
            YiConfig: 配置实例，用于链式调用
        """
        self._settings.cors = CORSConfig(**kwargs)
        return self

    def with_celery(self, **kwargs) -> "YiConfig":
        """设置 Celery 配置（链式 API）

        Args:
            **kwargs: Celery 配置参数

        Returns:
            YiConfig: 配置实例，用于链式调用
        """
        self._settings.celery = CeleryConfig(**kwargs)
        return self

    def with_log(self, **kwargs) -> "YiConfig":
        """设置日志配置（链式 API）

        Args:
            **kwargs: 日志配置参数

        Returns:
            YiConfig: 配置实例，用于链式调用
        """
        self._settings.log = LogConfig(**kwargs)
        # 更新日志配置
        setup_logging(self._settings.log)
        return self

    @classmethod
    def create_by(cls, source, singleton: bool = True) -> "YiConfig":
        """从指定源创建配置实例

        Args:
            source: 配置源，可以是文件路径字符串或配置字典
            singleton: 是否创建单例实例，True 表示使用或创建单例，False 表示创建新实例

        Returns:
            YiConfig: 配置实例
        """
        # 直接使用构造函数的新功能，不再需要动态替换方法
        return cls(singleton=singleton, config_source=source)

    @classmethod
    def from_file(cls, file_path: str, singleton: bool = True) -> "YiConfig":
        """从指定文件创建配置实例

        Args:
            file_path: 配置文件路径
            singleton: 是否创建单例实例，True 表示使用或创建单例，False 表示创建新实例

        Returns:
            YiConfig: 配置实例
        """
        return cls(singleton=singleton, config_source=file_path)

    @classmethod
    def from_dict(cls, config_dict: dict, singleton: bool = True) -> "YiConfig":
        """从字典创建配置实例

        Args:
            config_dict: 配置字典
            singleton: 是否创建单例实例，True 表示使用或创建单例，False 表示创建新实例

        Returns:
            YiConfig: 配置实例
        """
        return cls(singleton=singleton, config_source=config_dict)

    @classmethod
    def create(cls, singleton: bool = True, config_source: str | dict | None = None) -> "YiConfig":
        """创建配置实例的工厂方法

        Args:
            singleton: 是否创建单例实例，True 表示使用或创建单例，False 表示创建新实例
            config_source: 配置源，可以是文件路径字符串或配置字典

        Returns:
            YiConfig: 配置实例
        """
        return cls(singleton=singleton, config_source=config_source)
