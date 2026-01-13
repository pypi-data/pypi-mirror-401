"""事件类定义"""

from __future__ import annotations

from typing import Any, Generic, TypeVar

T = TypeVar("T")


class YiEvent(Generic[T]):
    """事件类

    用于封装事件数据，支持泛型类型

    Attributes:
        name: 事件名称
        data: 事件数据
        source: 事件源
        timestamp: 事件时间戳
    """

    def __init__(
        self,
        name: str,
        data: T,
        source: Any | None = None,
        timestamp: float | None = None,
    ):
        """初始化事件

        Args:
            name: 事件名称
            data: 事件数据
            source: 事件源
            timestamp: 事件时间戳
        """
        self.name = name
        self.data = data
        self.source = source
        self.timestamp = timestamp or self._get_current_timestamp()

    @staticmethod
    def _get_current_timestamp() -> float:
        """获取当前时间戳

        Returns:
            当前时间戳
        """
        import time
        return time.time()

    def to_dict(self) -> dict[str, Any]:
        """转换为字典

        Returns:
            事件字典
        """
        return {
            "name": self.name,
            "data": self.data,
            "source": str(self.source) if self.source else None,
            "timestamp": self.timestamp,
        }

    def __str__(self) -> str:
        """字符串表示

        Returns:
            事件字符串
        """
        return f"YiEvent(name={self.name!r}, data={self.data!r}, source={self.source!r}, timestamp={self.timestamp!r})"

    def __repr__(self) -> str:
        """repr表示

        Returns:
            事件repr
        """
        return self.__str__()
