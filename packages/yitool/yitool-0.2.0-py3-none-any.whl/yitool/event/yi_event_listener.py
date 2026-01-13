"""事件装饰器模块"""

from __future__ import annotations

from collections.abc import Callable
from typing import TypeVar

from yitool.event.yi_event import YiEvent
from yitool.event.yi_event_hub import event_hub

T = TypeVar("T")


def yi_event_listener(event_name: str, sync: bool = False) -> Callable[[Callable[[YiEvent], T]], Callable[[YiEvent], T]]:
    """事件监听器装饰器

    用于将函数装饰为事件监听器，自动订阅指定事件

    Args:
        event_name: 事件名称
        sync: 是否同步执行

    Returns:
        装饰器函数
    """
    def decorator(func: Callable[[YiEvent], T]) -> Callable[[YiEvent], T]:
        """装饰器内部函数

        Args:
            func: 被装饰的函数

        Returns:
            装饰后的函数
        """
        # 订阅事件
        event_hub.subscribe(event_name, func)

        def wrapper(event: YiEvent) -> T:
            """包装函数

            Args:
                event: 事件对象

            Returns:
                函数执行结果
            """
            return func(event)

        # 保存事件名称和原始函数，方便后续取消订阅
        wrapper.__event_name__ = event_name
        wrapper.__original_func__ = func

        return wrapper

    return decorator
