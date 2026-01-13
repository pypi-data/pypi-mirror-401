"""中间件基础类定义"""

from __future__ import annotations

from enum import Enum
from typing import Any


class MiddlewareResultStatus(Enum):
    """中间件结果状态枚举"""

    CONTINUE = "continue"  # 继续执行下一个中间件
    STOP = "stop"  # 停止执行中间件链
    ERROR = "error"  # 执行出错


class MiddlewareResult:
    """中间件结果类

    用于封装中间件执行的结果

    Attributes:
        status: 中间件执行状态
        data: 中间件处理后的数据
        error: 错误信息
    """

    def __init__(
        self,
        status: MiddlewareResultStatus = MiddlewareResultStatus.CONTINUE,
        data: Any | None = None,
        error: str | None = None,
    ):
        """初始化中间件结果

        Args:
            status: 中间件执行状态
            data: 中间件处理后的数据
            error: 错误信息
        """
        self.status = status
        self.data = data
        self.error = error

    def to_dict(self) -> dict[str, Any]:
        """转换为字典

        Returns:
            中间件结果字典
        """
        return {
            "status": self.status.value,
            "data": self.data,
            "error": self.error,
        }

    @classmethod
    def continue_(cls, data: Any | None = None) -> MiddlewareResult:
        """创建继续执行的结果

        Args:
            data: 中间件处理后的数据

        Returns:
            中间件结果对象
        """
        return cls(MiddlewareResultStatus.CONTINUE, data)

    @classmethod
    def stop(cls, data: Any | None = None) -> MiddlewareResult:
        """创建停止执行的结果

        Args:
            data: 中间件处理后的数据

        Returns:
            中间件结果对象
        """
        return cls(MiddlewareResultStatus.STOP, data)

    @classmethod
    def error(cls, error: str, data: Any | None = None) -> MiddlewareResult:
        """创建执行出错的结果

        Args:
            error: 错误信息
            data: 中间件处理后的数据

        Returns:
            中间件结果对象
        """
        return cls(MiddlewareResultStatus.ERROR, data, error)


class Middleware:
    """中间件基类

    所有中间件都应该继承自这个基类

    Attributes:
        name: 中间件名称
        priority: 中间件优先级，数值越小优先级越高
    """

    def __init__(self, name: str, priority: int = 100):
        """初始化中间件

        Args:
            name: 中间件名称
            priority: 中间件优先级
        """
        self.name = name
        self.priority = priority

    def process(self, data: Any) -> MiddlewareResult:
        """处理数据

        Args:
            data: 要处理的数据

        Returns:
            中间件执行结果
        """
        raise NotImplementedError("process method must be implemented")

    def __str__(self) -> str:
        """字符串表示

        Returns:
            中间件字符串
        """
        return f"Middleware(name={self.name!r}, priority={self.priority!r})"

    def __repr__(self) -> str:
        """repr表示

        Returns:
            中间件repr
        """
        return self.__str__()
