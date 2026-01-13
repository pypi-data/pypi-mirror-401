"""日志配置管理"""

import logging
from typing import Any


class TerminalConfig:
    """终端日志配置"""

    def __init__(self):
        self.enabled: bool = True
        self.width: int | None = None
        self.show_time: bool = True
        self.rich_tracebacks: bool = True
        self.tracebacks_show_locals: bool = True
        self.markup: bool = True
        self.show_path: bool = True
        self.console: Any = None


class FileConfig:
    """文件日志配置"""

    def __init__(self):
        self.enabled: bool = False
        self.path: str | None = None
        self.rotation: str = "10 MB"
        self.retention: str = "7 days"
        self.encoding: str = "utf-8"
        self.backup_count: int = 7


class StructuredConfig:
    """结构化日志配置"""

    def __init__(self):
        self.enabled: bool = False
        self.use_json: bool = False
        self.extra_fields: list[str] = []


class LogConfig:
    """日志配置类"""

    def __init__(self):
        self.level: int = logging.INFO
        self.terminal: TerminalConfig = TerminalConfig()
        self.file: FileConfig = FileConfig()
        self.structured: StructuredConfig = StructuredConfig()
        self.filters: list[logging.Filter] = []
        self.propagate: bool = False

    @classmethod
    def from_dict(cls, config_dict: dict) -> "LogConfig":
        """从字典创建日志配置"""
        config = cls()

        if "level" in config_dict:
            config.level = logging.getLevelName(config_dict["level"].upper())

        if "terminal" in config_dict:
            terminal_config = config_dict["terminal"]
            config.terminal.enabled = terminal_config.get("enabled", True)
            config.terminal.width = terminal_config.get("width")
            config.terminal.show_time = terminal_config.get("show_time", True)
            config.terminal.rich_tracebacks = terminal_config.get("rich_tracebacks", True)
            config.terminal.tracebacks_show_locals = terminal_config.get("tracebacks_show_locals", True)
            config.terminal.markup = terminal_config.get("markup", True)
            config.terminal.show_path = terminal_config.get("show_path", True)

        if "file" in config_dict:
            file_config = config_dict["file"]
            config.file.enabled = file_config.get("enabled", False)
            config.file.path = file_config.get("path")
            config.file.rotation = file_config.get("rotation", "10 MB")
            config.file.retention = file_config.get("retention", "7 days")
            config.file.encoding = file_config.get("encoding", "utf-8")
            config.file.backup_count = file_config.get("backup_count", 7)

        if "structured" in config_dict:
            structured_config = config_dict["structured"]
            config.structured.enabled = structured_config.get("enabled", False)
            config.structured.use_json = structured_config.get("use_json", False)
            config.structured.extra_fields = structured_config.get("extra_fields", [])

        if "filters" in config_dict:
            config.filters = config_dict["filters"]

        if "propagate" in config_dict:
            config.propagate = config_dict["propagate"]

        return config
