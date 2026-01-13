from __future__ import annotations

import logging
import threading
from contextlib import contextmanager
from os import path
from typing import Any

from rich.console import Console
from rich.logging import RichHandler

from yitool.const import __PKG__

logger = logging.getLogger(__PKG__)
"""yitool的全局日志对象，基于rich的增强日志系统"""

# 日志上下文存储
_log_context = threading.local()


class StructuredFormatter(logging.Formatter):
    """结构化日志格式化器

    支持将日志格式化为JSON或其他结构化格式
    """

    def __init__(self, fmt: str | None = None, datefmt: str | None = None, style: str = "%", use_json: bool = False):
        """初始化结构化日志格式化器

        Args:
            fmt: 日志格式字符串
            datefmt: 日期格式字符串
            style: 格式样式
            use_json: 是否使用JSON格式
        """
        super().__init__(fmt, datefmt, style)
        self.use_json = use_json

    def format(self, record: logging.LogRecord) -> str:
        """格式化日志记录

        Args:
            record: 日志记录对象

        Returns:
            格式化后的日志字符串
        """
        # 获取日志上下文
        context = getattr(_log_context, "context", {})

        # 基本日志数据
        log_data = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "name": record.name,
            "message": super().format(record),
            "pathname": record.pathname,
            "filename": record.filename,
            "lineno": record.lineno,
            "funcName": record.funcName,
        }

        # 添加上下文数据
        log_data.update(context)

        # 添加额外的日志属性
        if hasattr(record, "extra"):
            log_data.update(record.extra)

        # 如果是JSON格式，返回JSON字符串
        if self.use_json:
            import json
            return json.dumps(log_data, ensure_ascii=False)

        # 否则返回格式化的字符串
        return super().format(record)


def setup_logging(
    terminal_width: int | None = None,
    level: int = logging.INFO,
    log_file: str | None = None,
    rotation: str | None = None,
    retention: str | None = None,
    use_json: bool = False,
    structured: bool = False,
    filters: list[logging.Filter] | None = None
) -> None:
    """配置日志系统，支持终端美化输出和文件日志

    功能特点：
    - 基于rich库的彩色日志输出
    - 支持堆栈跟踪的美化显示
    - 可配置日志文件、轮转和保留策略
    - 自动显示时间、路径和行号信息
    - 支持结构化日志和JSON格式
    - 支持日志上下文
    - 支持日志过滤器
    - 支持动态调整日志级别

    Args:
        terminal_width: 终端输出宽度，控制日志显示格式
        level: 日志级别，如logging.DEBUG, logging.INFO, logging.WARNING等
        log_file: 日志文件路径，设置后会同时输出到文件
        rotation: 日志轮转策略，如'10 MB', '1 day'
        retention: 日志保留时间，如'7 days'
        use_json: 是否使用JSON格式输出
        structured: 是否使用结构化日志
        filters: 日志过滤器列表

    Example:
        >>> setup_logging(
        ...     level=logging.DEBUG,  # 日志级别
        ...     log_file='app.log',   # 日志文件（可选）
        ...     rotation='10 MB',     # 日志轮转（可选）
        ...     retention='7 days',   # 日志保留时间（可选）
        ...     use_json=True,        # 使用JSON格式（可选）
        ...     structured=True       # 使用结构化日志（可选）
        ... )
    """
    # 清除已有的处理器
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # 创建rich处理器用于终端输出
    console = Console(width=terminal_width) if terminal_width else None
    rich_handler = RichHandler(
        show_time=True,           # 显示时间戳
        rich_tracebacks=True,     # 美化异常堆栈
        tracebacks_show_locals=True, # 显示本地变量
        markup=True,              # 支持标记语法
        show_path=True,           # 显示文件路径和行号
        console=console,
    )
    rich_handler.setFormatter(logging.Formatter("%(message)s"))

    # 添加过滤器
    if filters:
        for filter in filters:
            rich_handler.addFilter(filter)

    logger.addHandler(rich_handler)

    # 如果指定了日志文件，添加文件处理器
    if log_file:
        try:
            # 确保日志目录存在
            log_dir = path.dirname(log_file)
            if log_dir and not path.exists(log_dir):
                import os
                os.makedirs(log_dir, exist_ok=True)

            # 创建文件处理器
            file_handler = logging.handlers.RotatingFileHandler(
                filename=log_file,
                maxBytes=int(rotation.replace(" MB", "")) * 1024 * 1024 if rotation and "MB" in rotation else 10*1024*1024,
                backupCount=7 if not retention else int(retention.replace(" days", ""))
            )

            # 设置文件日志格式化器
            if structured or use_json:
                file_formatter = StructuredFormatter(
                    fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    use_json=use_json
                )
            else:
                file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

            file_handler.setFormatter(file_formatter)

            # 添加过滤器
            if filters:
                for filter in filters:
                    file_handler.addFilter(filter)

            logger.addHandler(file_handler)
            logger.info(f"Logging to file: {log_file}")
        except Exception as e:
            logger.error(f"Failed to set up file logging: {e}")

    # 设置日志级别并关闭传播
    logger.setLevel(level)
    logger.propagate = False

    # 记录日志配置信息
    log_level_name = logging.getLevelName(level)
    logger.debug(f"Logging system initialized with level: {log_level_name}")


def set_log_level(level: int | str) -> None:
    """动态设置日志级别

    Args:
        level: 日志级别，可以是数字或字符串，如logging.DEBUG, 'DEBUG', 10
    """
    if isinstance(level, str):
        level = logging.getLevelName(level.upper())
    logger.setLevel(level)
    logger.info(f"Log level changed to: {logging.getLevelName(level)}")


@contextmanager
def log_context(**kwargs):
    """日志上下文管理器

    用于在特定上下文中添加日志上下文信息

    Args:
        **kwargs: 上下文键值对

    Example:
        >>> with log_context(user_id=123, request_id='abc123'):
        ...     logger.info('Processing request')
        ...     # 日志会包含user_id和request_id
    """
    # 获取当前上下文
    current_context = getattr(_log_context, "context", {})

    # 创建新的上下文
    new_context = current_context.copy()
    new_context.update(kwargs)

    # 设置新的上下文
    _log_context.context = new_context

    try:
        yield
    finally:
        # 恢复原来的上下文
        _log_context.context = current_context


def get_log_context() -> dict[str, Any]:
    """获取当前日志上下文

    Returns:
        当前日志上下文字典
    """
    return getattr(_log_context, "context", {})


def clear_log_context() -> None:
    """清除日志上下文"""
    if hasattr(_log_context, "context"):
        delattr(_log_context, "context")

# 导出常用的日志级别常量，方便用户使用
def debug(msg, *args, **kwargs):
    """记录调试信息"""
    return logger.debug(msg, *args, **kwargs)

def info(msg, *args, **kwargs):
    """记录一般信息"""
    return logger.info(msg, *args, **kwargs)

def warning(msg, *args, **kwargs):
    """记录警告信息"""
    return logger.warning(msg, *args, **kwargs)

def error(msg, *args, **kwargs):
    """记录错误信息"""
    return logger.error(msg, *args, **kwargs)

def critical(msg, *args, **kwargs):
    """记录严重错误信息"""
    return logger.critical(msg, *args, **kwargs)

def exception(msg, *args, **kwargs):
    """记录异常信息，自动包含堆栈跟踪"""
    return logger.exception(msg, *args, **kwargs)


def structured_log(
    level: int,
    message: str,
    **kwargs
) -> None:
    """记录结构化日志

    Args:
        level: 日志级别
        message: 日志消息
        **kwargs: 额外的结构化数据
    """
    extra = kwargs.copy()
    logger.log(level, message, extra=extra)


# 导出日志级别常量
DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL
