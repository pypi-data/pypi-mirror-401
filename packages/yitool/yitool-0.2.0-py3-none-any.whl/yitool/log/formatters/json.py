"""JSON日志格式化器"""

import json
import logging

from yitool.log.context import get_log_context


class JSONFormatter(logging.Formatter):
    """JSON日志格式化器

    将日志记录格式化为JSON字符串，支持日志上下文
    """

    def __init__(self, datefmt: str | None = None):
        """初始化JSON日志格式化器

        Args:
            datefmt: 日期格式字符串，默认使用ISO格式
        """
        if datefmt is None:
            datefmt = "%Y-%m-%d %H:%M:%S"

        super().__init__(datefmt=datefmt)

    def format(self, record: logging.LogRecord) -> str:
        """格式化日志记录为JSON字符串

        Args:
            record: 日志记录对象

        Returns:
            格式化后的JSON字符串
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
            "process": record.process,
            "thread": record.thread,
        }

        # 添加上下文数据
        log_data.update(context)

        # 添加额外的日志属性
        if hasattr(record, "extra") and isinstance(record.extra, dict):
            log_data.update(record.extra)

        # 添加异常信息
        if record.exc_info:
            log_data["exc_info"] = self.formatException(record.exc_info)

        # 返回JSON字符串
        return json.dumps(log_data, ensure_ascii=False, default=str)
