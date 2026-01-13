"""异步事件模块"""

from __future__ import annotations

import asyncio
import threading
from collections.abc import Awaitable, Callable
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Generic, TypeVar

from yitool.event.yi_event import YiEvent
from yitool.log import logger

T = TypeVar("T")


class AsyncYiEvent(YiEvent, Generic[T]):
    """异步事件类

    继承自同步事件类，用于异步事件处理
    """

    pass


class AsyncYiEventHub:
    """异步事件中心类

    用于管理异步事件的发布和订阅

    Attributes:
        listeners: 异步事件监听器映射
        executor: 线程池执行器
        lock: 线程锁
    """

    def __init__(self, max_workers: int | None = None):
        """初始化异步事件中心

        Args:
            max_workers: 线程池最大工作线程数
        """
        self.listeners: dict[str, set[Callable[[AsyncYiEvent], Awaitable[None]]]] = {}
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.lock = threading.RLock()

    def subscribe(self, event_name: str, listener: Callable[[AsyncYiEvent], Awaitable[None]]) -> None:
        """订阅异步事件

        Args:
            event_name: 事件名称
            listener: 异步事件监听器
        """
        with self.lock:
            if event_name not in self.listeners:
                self.listeners[event_name] = set()
            self.listeners[event_name].add(listener)
        logger.debug(f"Subscribed to async event: {event_name}, listener: {listener.__name__}")

    def unsubscribe(self, event_name: str, listener: Callable[[AsyncYiEvent], Awaitable[None]]) -> bool:
        """取消订阅异步事件

        Args:
            event_name: 事件名称
            listener: 异步事件监听器

        Returns:
            是否成功取消订阅
        """
        with self.lock:
            if event_name in self.listeners:
                if listener in self.listeners[event_name]:
                    self.listeners[event_name].remove(listener)
                    logger.debug(f"Unsubscribed from async event: {event_name}, listener: {listener.__name__}")
                    # 清理空的事件监听器集合
                    if not self.listeners[event_name]:
                        del self.listeners[event_name]
                    return True
        return False

    async def publish(self, event: AsyncYiEvent, sync: bool = False) -> None:
        """发布异步事件

        Args:
            event: 异步事件对象
            sync: 是否同步执行事件监听器
        """
        with self.lock:
            # 获取事件监听器副本，避免在遍历过程中修改集合
            event_listeners = self.listeners.get(event.name, set()).copy()

        logger.debug(f"Publishing async event: {event.name}, sync: {sync}, listeners: {len(event_listeners)}")

        if sync:
            # 同步执行
            for listener in event_listeners:
                try:
                    await listener(event)
                except Exception as e:
                    logger.error(f"Error in async event listener {listener.__name__} for event {event.name}: {e}")
        else:
            # 异步执行
            tasks = []
            for listener in event_listeners:
                tasks.append(self._execute_listener(listener, event))

            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)

    async def _execute_listener(self, listener: Callable[[AsyncYiEvent], Awaitable[None]], event: AsyncYiEvent) -> None:
        """执行异步事件监听器

        Args:
            listener: 异步事件监听器
            event: 异步事件对象
        """
        try:
            await listener(event)
        except Exception as e:
            logger.error(f"Error in async event listener {listener.__name__} for event {event.name}: {e}")

    def has_listeners(self, event_name: str) -> bool:
        """检查异步事件是否有监听器

        Args:
            event_name: 事件名称

        Returns:
            是否有监听器
        """
        with self.lock:
            return event_name in self.listeners and bool(self.listeners[event_name])

    def get_listener_count(self, event_name: str) -> int:
        """获取异步事件监听器数量

        Args:
            event_name: 事件名称

        Returns:
            监听器数量
        """
        with self.lock:
            return len(self.listeners.get(event_name, set()))

    def clear_listeners(self, event_name: str | None = None) -> None:
        """清除异步事件监听器

        Args:
            event_name: 事件名称，None表示清除所有事件监听器
        """
        with self.lock:
            if event_name:
                if event_name in self.listeners:
                    del self.listeners[event_name]
                    logger.debug(f"Cleared async listeners for event: {event_name}")
            else:
                self.listeners.clear()
                logger.debug("Cleared all async event listeners")

    def shutdown(self) -> None:
        """关闭异步事件中心

        关闭线程池执行器
        """
        self.executor.shutdown(wait=True)
        logger.debug("Async event hub shutdown")


# 创建全局异步事件中心实例
async_event_hub = AsyncYiEventHub()


def async_yi_event_listener(event_name: str, sync: bool = False) -> Callable[[Callable[[AsyncYiEvent], Awaitable[Any]]], Callable[[AsyncYiEvent], Awaitable[Any]]]:
    """异步事件监听器装饰器

    用于将异步函数装饰为异步事件监听器，自动订阅指定事件

    Args:
        event_name: 事件名称
        sync: 是否同步执行

    Returns:
        装饰器函数
    """
    def decorator(func: Callable[[AsyncYiEvent], Awaitable[Any]]) -> Callable[[AsyncYiEvent], Awaitable[Any]]:
        """装饰器内部函数

        Args:
            func: 被装饰的异步函数

        Returns:
            装饰后的函数
        """
        # 订阅事件
        async_event_hub.subscribe(event_name, func)

        async def wrapper(event: AsyncYiEvent) -> Any:
            """包装函数

            Args:
                event: 异步事件对象

            Returns:
                函数执行结果
            """
            return await func(event)

        # 保存事件名称和原始函数，方便后续取消订阅
        wrapper.__event_name__ = event_name
        wrapper.__original_func__ = func

        return wrapper

    return decorator
