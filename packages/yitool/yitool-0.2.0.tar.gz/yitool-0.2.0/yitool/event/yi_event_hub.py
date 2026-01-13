
"""事件中心类定义"""

from __future__ import annotations

import threading
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from typing import TypeVar

from yitool.event.yi_event import YiEvent
from yitool.log import logger

T = TypeVar("T")


class YiEventHub:
    """事件中心类

    用于管理事件的发布和订阅，支持同步和异步事件处理

    Attributes:
        listeners: 事件监听器映射
        executor: 线程池执行器
        lock: 线程锁
    """

    def __init__(self, max_workers: int | None = None):
        """初始化事件中心

        Args:
            max_workers: 线程池最大工作线程数
        """
        self.listeners: dict[str, set[Callable[[YiEvent], None]]] = {}
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.lock = threading.RLock()

    def subscribe(self, event_name: str, listener: Callable[[YiEvent], None]) -> None:
        """订阅事件

        Args:
            event_name: 事件名称
            listener: 事件监听器
        """
        with self.lock:
            if event_name not in self.listeners:
                self.listeners[event_name] = set()
            self.listeners[event_name].add(listener)
        logger.debug(f"Subscribed to event: {event_name}, listener: {listener.__name__}")

    def unsubscribe(self, event_name: str, listener: Callable[[YiEvent], None]) -> bool:
        """取消订阅事件

        Args:
            event_name: 事件名称
            listener: 事件监听器

        Returns:
            是否成功取消订阅
        """
        with self.lock:
            if event_name in self.listeners:
                if listener in self.listeners[event_name]:
                    self.listeners[event_name].remove(listener)
                    logger.debug(f"Unsubscribed from event: {event_name}, listener: {listener.__name__}")
                    # 清理空的事件监听器集合
                    if not self.listeners[event_name]:
                        del self.listeners[event_name]
                    return True
        return False

    def publish(self, event: YiEvent, sync: bool = False) -> None:
        """发布事件

        Args:
            event: 事件对象
            sync: 是否同步执行事件监听器
        """
        with self.lock:
            # 获取事件监听器副本，避免在遍历过程中修改集合
            event_listeners = self.listeners.get(event.name, set()).copy()

        logger.debug(f"Publishing event: {event.name}, sync: {sync}, listeners: {len(event_listeners)}")

        if sync:
            # 同步执行
            for listener in event_listeners:
                try:
                    listener(event)
                except Exception as e:
                    logger.error(f"Error in event listener {listener.__name__} for event {event.name}: {e}")
        else:
            # 异步执行
            for listener in event_listeners:
                self.executor.submit(self._execute_listener, listener, event)

    def _execute_listener(self, listener: Callable[[YiEvent], None], event: YiEvent) -> None:
        """执行事件监听器

        Args:
            listener: 事件监听器
            event: 事件对象
        """
        try:
            listener(event)
        except Exception as e:
            logger.error(f"Error in event listener {listener.__name__} for event {event.name}: {e}")

    def has_listeners(self, event_name: str) -> bool:
        """检查事件是否有监听器

        Args:
            event_name: 事件名称

        Returns:
            是否有监听器
        """
        with self.lock:
            return event_name in self.listeners and bool(self.listeners[event_name])

    def get_listener_count(self, event_name: str) -> int:
        """获取事件监听器数量

        Args:
            event_name: 事件名称

        Returns:
            监听器数量
        """
        with self.lock:
            return len(self.listeners.get(event_name, set()))

    def clear_listeners(self, event_name: str | None = None) -> None:
        """清除事件监听器

        Args:
            event_name: 事件名称，None表示清除所有事件监听器
        """
        with self.lock:
            if event_name:
                if event_name in self.listeners:
                    del self.listeners[event_name]
                    logger.debug(f"Cleared listeners for event: {event_name}")
            else:
                self.listeners.clear()
                logger.debug("Cleared all event listeners")

    def shutdown(self) -> None:
        """关闭事件中心

        关闭线程池执行器
        """
        self.executor.shutdown(wait=True)
        logger.debug("Event hub shutdown")


# 创建全局事件中心实例
event_hub = YiEventHub()
