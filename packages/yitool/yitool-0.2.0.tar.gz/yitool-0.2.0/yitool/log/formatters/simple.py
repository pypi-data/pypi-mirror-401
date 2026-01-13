"""简单日志格式化器"""

import logging

from yitool.log.context import get_log_context


class SimpleFormatter(logging.Formatter):
    """简单日志格式化器

    提供简单的日志格式化，支持日志上下文
    """

    def __init__(self, fmt: str | None = None, datefmt: str | None = None, style: str = "%"):
        """初始化简单日志格式化器

        Args:
            fmt: 日志格式字符串，默认包含时间、级别、名称、消息和上下文
            datefmt: 日期格式字符串，默认使用ISO格式
            style: 格式样式，支持 %, {, $
        """
        if fmt is None:
            fmt = "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
        if datefmt is None:
            datefmt = "%Y-%m-%d %H:%M:%S"

        super().__init__(fmt, datefmt, style)

    def format(self, record: logging.LogRecord) -> str:
        """格式化日志记录

        Args:
            record: 日志记录对象

        Returns:
            格式化后的日志字符串
        """
        # 获取日志上下文
        context = get_log_context()

        # 添加上下文信息到日志记录
        if context:
            record.__dict__.update(context)

        # 添加额外的日志属性
        if hasattr(record, "extra") and isinstance(record.extra, dict):
            record.__dict__.update(record.extra)

        return super().format(record)
