"""Celery application configuration"""

from celery import Celery


class YiCelery(Celery):
    """自定义 Celery 应用类，提供更灵活的配置和扩展能力

    其他项目可以通过继承这个类来自定义自己的 Celery 应用，
    并根据需要覆盖或扩展其功能。
    """

    _instance = None

    def __new__(cls, app_name, broker=None, backend=None, include=None, celery_config=None, singleton=True, **kwargs):
        """实现单例模式，支持创建自定义实例

        Args:
            app_name: 应用名称
            broker: 消息代理 URL，默认从配置中获取
            backend: 结果后端 URL，默认从配置中获取
            include: 要包含的任务模块列表
            celery_config: Celery 配置对象或配置字典，可选
            singleton: 是否创建单例实例，True 表示使用或创建单例，False 表示创建新实例
            **kwargs: 其他 Celery 配置参数
        """
        if not singleton or cls._instance is None:
            instance = super().__new__(cls)
            instance.__init__(app_name, broker, backend, include, celery_config, **kwargs)
            if singleton:
                cls._instance = instance
        return cls._instance if singleton else instance

    def __init__(self, app_name, broker=None, backend=None, include=None, celery_config=None, **kwargs):
        """初始化 Celery 应用

        Args:
            app_name: 应用名称
            broker: 消息代理 URL，默认从配置中获取
            backend: 结果后端 URL，默认从配置中获取
            include: 要包含的任务模块列表
            celery_config: Celery 配置对象或配置字典，可选
            **kwargs: 其他 Celery 配置参数
        """
        # 只有当实例是新创建的时候才执行初始化
        if not hasattr(self, "_initialized"):
            # 初始化父类
            super().__init__(
                app_name,
                broker=broker,
                backend=backend,
                include=include or [],
                **kwargs
            )

            # 支持配置字典转换为配置对象
            if isinstance(celery_config, dict):
                from yitool.yi_config.celery import CeleryConfig
                celery_config = CeleryConfig(**celery_config)

            # 加载默认配置
            self._load_default_config(celery_config)
            self._initialized = True

    @classmethod
    def instance(cls):
        """获取单例实例"""
        if cls._instance is None:
            # 如果实例不存在，创建默认实例
            cls._instance = cls.create(
                app_name="yitool-tasks",
                include=["yitool.yi_celery.email_tasks"]
            )
            # 为 yitool 内置的邮件任务添加特定路由
            cls._instance.conf.task_routes = {
                # 将 yitool 内置的 email_tasks 路由到 email 队列
                "yitool.yi_celery.email_tasks.*": {
                    "queue": "email"
                },
                # 其他任务使用默认路由
                **cls._instance.conf.task_routes
            }
        return cls._instance

    def _load_default_config(self, celery_config=None):
        """加载默认配置

        从配置对象加载 Celery 配置，如果配置不存在，则使用默认值。

        Args:
            celery_config: Celery 配置对象，可选
        """
        # 默认配置值
        default_config = {
            "task_serializer": "json",
            "result_serializer": "json",
            "accept_content": ["json"],
            "timezone": "UTC",
            "enable_utc": True,
            "worker_concurrency": 4,
            "worker_max_tasks_per_child": 100,
            "worker_log_level": "info",
            "beat_schedule": {}
        }

        # 如果提供了配置对象，使用它
        if celery_config:
            # 从配置对象加载设置
            self.config_from_object(celery_config)

            # 获取配置值，使用默认值作为后备
            worker_config = celery_config.worker or {}
            beat_config = celery_config.beat or {}

            # 更新其他配置项
            self.conf.update(
                task_serializer=celery_config.task_serializer,
                result_serializer=celery_config.result_serializer,
                accept_content=celery_config.accept_content,
                timezone=celery_config.timezone,
                enable_utc=celery_config.enable_utc,
                worker_concurrency=worker_config.get("concurrency", default_config["worker_concurrency"]),
                worker_max_tasks_per_child=worker_config.get("max_tasks_per_child", default_config["worker_max_tasks_per_child"]),
                worker_log_level=worker_config.get("log_level", default_config["worker_log_level"]),
                beat_schedule=beat_config.get("schedule", default_config["beat_schedule"])
            )
        else:
            # 使用默认配置
            self.conf.update(default_config)

        # 设置默认队列和路由
        self.conf.task_default_queue = "default"
        self.conf.task_routes = {
            # 默认路由配置
            "*": {
                "queue": "default"
            }
        }

    @classmethod
    def create(cls, app_name, broker=None, backend=None, include=None, config=None, singleton=True, **kwargs):
        """创建并配置 Celery 应用实例

        这是一个类方法，用于创建 Celery 应用实例，
        提供了更灵活的配置方式和更好的扩展性。

        Args:
            app_name: 应用名称
            broker: 消息代理 URL，默认从配置中获取
            backend: 结果后端 URL，默认从配置中获取
            include: 要包含的任务模块列表
            config: Celery 配置对象或配置字典，可选
            singleton: 是否创建单例实例，True 表示使用或创建单例，False 表示创建新实例
            **kwargs: 其他 Celery 配置参数

        Returns:
            YiCeleryApp: 配置好的 Celery 应用实例
        """
        return cls(app_name, broker=broker, backend=backend, include=include, celery_config=config, singleton=singleton, **kwargs)

    @classmethod
    def create_by(cls, source, app_name=None, broker=None, backend=None, include=None, singleton=True, **kwargs):
        """从指定源创建 Celery 应用实例

        Args:
            source: 配置源，可以是文件路径或字典
            app_name: 应用名称
            broker: 消息代理 URL，默认从配置中获取
            backend: 结果后端 URL，默认从配置中获取
            include: 要包含的任务模块列表
            singleton: 是否创建单例实例，True 表示使用或创建单例，False 表示创建新实例
            **kwargs: 其他 Celery 配置参数

        Returns:
            YiCeleryApp: 配置好的 Celery 应用实例
        """
        from yitool.yi_config.celery import CeleryConfig

        # 从指定源加载配置
        if isinstance(source, str):
            # 从文件加载配置
            import yaml
            with open(source) as f:
                config_dict = yaml.safe_load(f)
            config = CeleryConfig(**config_dict.get("celery", {}))
        elif isinstance(source, dict):
            # 从字典加载配置
            config = CeleryConfig(**source.get("celery", source))
        else:
            # 直接使用配置对象
            config = source

        # 如果没有指定应用名称，从配置中获取
        if not app_name and hasattr(config, "app_name"):
            app_name = config.app_name

        return cls.create(app_name, broker=broker, backend=backend, include=include, config=config, singleton=singleton, **kwargs)


