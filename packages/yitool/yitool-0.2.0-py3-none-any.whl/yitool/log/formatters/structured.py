"""结构化日志格式化器"""

import logging
from typing import Any

from yitool.log.context import get_log_context


class StructuredFormatter(logging.Formatter):
    """结构化日志格式化器

    支持将日志格式化为结构化格式，支持日志上下文
    """

    def __init__(self, fmt: str | None = None, datefmt: str | None = None, style: str = "%", use_json: bool = False):
        """初始化结构化日志格式化器

        Args:
            fmt: 日志格式字符串
            datefmt: 日期格式字符串
            style: 格式样式
            use_json: 是否使用JSON格式输出
        """
        if fmt is None:
            fmt = "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
        if datefmt is None:
            datefmt = "%Y-%m-%d %H:%M:%S"

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
        context = get_log_context()

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
            return json.dumps(log_data, ensure_ascii=False, default=str)

        # 否则返回格式化的字符串
        return super().format(record)

    def get_structured_data(self, record: logging.LogRecord) -> dict[str, Any]:
        """获取结构化日志数据

        Args:
            record: 日志记录对象

        Returns:
            结构化日志数据
        """
        # 获取日志上下文
        context = get_log_context()

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

        return log_data
