"""终端日志处理器"""


from rich.console import Console
from rich.logging import RichHandler

from yitool.log.config import TerminalConfig
from yitool.log.formatters import SimpleFormatter


class TerminalHandler(RichHandler):
    """终端日志处理器

    基于RichHandler的增强终端日志处理器，支持配置化管理
    """

    def __init__(self, config: TerminalConfig | None = None):
        """初始化终端日志处理器

        Args:
            config: 终端日志配置，如为None则使用默认配置
        """
        if config is None:
            config = TerminalConfig()

        # 创建Rich控制台
        console = config.console or Console(
            width=config.width,
        )

        # 初始化RichHandler
        super().__init__(
            show_time=config.show_time,
            rich_tracebacks=config.rich_tracebacks,
            tracebacks_show_locals=config.tracebacks_show_locals,
            markup=config.markup,
            show_path=config.show_path,
            console=console,
        )

        # 设置格式化器
        self.setFormatter(SimpleFormatter())

        self.config = config

    def set_log_config(self, config: TerminalConfig) -> None:
        """更新终端日志配置

        Args:
            config: 新的终端日志配置
        """
        self.config = config
        self.console.width = config.width
        self.show_time = config.show_time
        self.rich_tracebacks = config.rich_tracebacks
        self.tracebacks_show_locals = config.tracebacks_show_locals
        self.markup = config.markup
        self.show_path = config.show_path
