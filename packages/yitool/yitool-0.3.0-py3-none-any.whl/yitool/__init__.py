"""导出公共接口"""

from __future__ import annotations

import importlib
import typing

from yitool.const import __VERSION__

__version__ = __VERSION__

__all__ = [
    # 核心模块
    "shared",
    "utils",
    "misc",
    "cli",
    "const",
    "enums",
    "exceptions",
    "log",
    "yi_serializer",
    "yi_db",
    "yi_cache",
    "yi_config",
    "yi_fast",
    "yi_celery",
    # 常用组件（简化导入）
    "YiDB",
    "YiRedis",
    "cache_manager",
]

# 常用组件的简化导入
try:
    from yitool.yi_db.yi_db import YiDB
except ImportError:
    pass

try:
    from yitool.yi_cache.yi_redis import YiRedis
except ImportError:
    pass

try:
    from yitool.yi_cache.yi_cache_manager import cache_manager
except ImportError:
    pass




# Copied from https://peps.python.org/pep-0562/
def __getattr__(name: str) -> typing.Any:
    if name in __all__:
        return importlib.import_module("." + name, __name__)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
