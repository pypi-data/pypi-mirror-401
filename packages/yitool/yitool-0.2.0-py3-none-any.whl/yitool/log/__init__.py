"""yitool日志系统，基于rich的增强日志框架"""

from __future__ import annotations

from yitool.log.config import FileConfig, LogConfig, StructuredConfig, TerminalConfig
from yitool.log.context import (
    clear_log_context,
    get_log_context,
    log_context,
    log_context_decorator,
    set_log_context,
)
from yitool.log.core import (
    DEBUG,
    ERROR,
    INFO,
    WARNING,
    critical,
    debug,
    error,
    exception,
    global_logger,
    info,
    setup_logging,
    structured_log,
    warning,
)
from yitool.log.decorators import (
    log_debug,
    log_exception,
    log_execution_time,
    log_function,
    log_with_context,
)
from yitool.log.formatters import JSONFormatter, SimpleFormatter, StructuredFormatter

__all__ = [
    # 配置类
    "FileConfig",
    "LogConfig",
    "StructuredConfig",
    "TerminalConfig",

    # 核心日志函数和常量
    "DEBUG",
    "INFO",
    "WARNING",
    "ERROR",
    "CRITICAL",
    "debug",
    "info",
    "warning",
    "error",
    "critical",
    "exception",
    "structured_log",
    "setup_logging",
    "set_log_level",
    "global_logger",

    # 日志上下文管理
    "get_log_context",
    "set_log_context",
    "clear_log_context",
    "log_context",
    "log_context_decorator",

    # 日志装饰器
    "log_function",
    "log_execution_time",
    "log_with_context",
    "log_exception",
    "log_debug",

    # 日志格式化器
    "SimpleFormatter",
    "JSONFormatter",
    "StructuredFormatter",
]

# 从core模块导入剩余的常量和函数
from yitool.log.core import CRITICAL, set_log_level

# 保持向后兼容性
default_logger = global_logger.logger
logger = default_logger

# 将logger添加到__all__
__all__.append("logger")
__all__.append("default_logger")

