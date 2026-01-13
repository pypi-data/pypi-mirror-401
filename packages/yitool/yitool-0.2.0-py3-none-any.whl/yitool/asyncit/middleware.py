"""异步中间件模块"""

from __future__ import annotations

import threading
from typing import Any

from yitool.log import logger
from yitool.middleware.middleware import MiddlewareResult, MiddlewareResultStatus


class AsyncMiddleware:
    """异步中间件基类

    所有异步中间件都应该继承自这个基类

    Attributes:
        name: 中间件名称
        priority: 中间件优先级，数值越小优先级越高
    """

    def __init__(self, name: str, priority: int = 100):
        """初始化异步中间件

        Args:
            name: 中间件名称
            priority: 中间件优先级
        """
        self.name = name
        self.priority = priority

    async def process(self, data: Any) -> MiddlewareResult:
        """异步处理数据

        Args:
            data: 要处理的数据

        Returns:
            中间件执行结果
        """
        raise NotImplementedError("async process method must be implemented")

    def __str__(self) -> str:
        """字符串表示

        Returns:
            中间件字符串
        """
        return f"AsyncMiddleware(name={self.name!r}, priority={self.priority!r})"

    def __repr__(self) -> str:
        """repr表示

        Returns:
            中间件repr
        """
        return self.__str__()


class AsyncMiddlewareManager:
    """异步中间件管理器类

    用于管理异步中间件的注册、注销和执行

    Attributes:
        middlewares: 异步中间件列表
        lock: 线程锁
    """

    def __init__(self):
        """初始化异步中间件管理器"""
        self.middlewares: list[AsyncMiddleware] = []
        self.lock = threading.RLock()

    def register(self, middleware: AsyncMiddleware) -> None:
        """注册异步中间件

        Args:
            middleware: 异步中间件对象
        """
        with self.lock:
            # 检查中间件是否已注册
            if middleware not in self.middlewares:
                self.middlewares.append(middleware)
                # 按优先级排序，优先级数值越小越靠前
                self.middlewares.sort(key=lambda m: m.priority)
                logger.debug(f"Registered async middleware: {middleware}")

    def unregister(self, middleware: AsyncMiddleware) -> bool:
        """注销异步中间件

        Args:
            middleware: 异步中间件对象

        Returns:
            是否成功注销
        """
        with self.lock:
            if middleware in self.middlewares:
                self.middlewares.remove(middleware)
                logger.debug(f"Unregistered async middleware: {middleware}")
                return True
            return False

    def unregister_by_name(self, name: str) -> bool:
        """根据名称注销异步中间件

        Args:
            name: 中间件名称

        Returns:
            是否成功注销
        """
        with self.lock:
            for middleware in self.middlewares:
                if middleware.name == name:
                    self.middlewares.remove(middleware)
                    logger.debug(f"Unregistered async middleware by name: {name}")
                    return True
            return False

    def get_middleware_by_name(self, name: str) -> AsyncMiddleware | None:
        """根据名称获取异步中间件

        Args:
            name: 中间件名称

        Returns:
            异步中间件对象，None表示未找到
        """
        with self.lock:
            for middleware in self.middlewares:
                if middleware.name == name:
                    return middleware
            return None

    async def execute(self, data: Any) -> tuple[MiddlewareResultStatus, Any, str | None]:
        """执行异步中间件链

        Args:
            data: 要处理的数据

        Returns:
            元组(状态, 最终数据, 错误信息)
        """
        with self.lock:
            # 获取中间件列表副本，避免在执行过程中修改
            middlewares_copy = self.middlewares.copy()

        logger.debug(f"Executing async middleware chain with {len(middlewares_copy)} middlewares")

        current_data = data

        for middleware in middlewares_copy:
            try:
                logger.debug(f"Executing async middleware: {middleware}")
                result = await middleware.process(current_data)
                logger.debug(f"Async middleware {middleware} executed with result: {result.to_dict()}")

                # 更新当前数据
                if result.data is not None:
                    current_data = result.data

                # 根据中间件结果决定后续操作
                if result.status == MiddlewareResultStatus.STOP:
                    logger.debug(f"Async middleware {middleware} requested to stop the chain")
                    return MiddlewareResultStatus.STOP, current_data, None
                elif result.status == MiddlewareResultStatus.ERROR:
                    logger.error(f"Async middleware {middleware} executed with error: {result.error}")
                    return MiddlewareResultStatus.ERROR, current_data, result.error
                # 否则继续执行下一个中间件
            except Exception as e:
                logger.error(f"Error executing async middleware {middleware}: {e}")
                return MiddlewareResultStatus.ERROR, current_data, str(e)

        logger.debug("Async middleware chain execution completed successfully")
        return MiddlewareResultStatus.CONTINUE, current_data, None

    def clear(self) -> None:
        """清除所有异步中间件"""
        with self.lock:
            self.middlewares.clear()
            logger.debug("Cleared all async middlewares")

    def get_middleware_count(self) -> int:
        """获取异步中间件数量

        Returns:
            异步中间件数量
        """
        with self.lock:
            return len(self.middlewares)

    def get_sorted_middlewares(self) -> list[AsyncMiddleware]:
        """获取排序后的异步中间件列表

        Returns:
            排序后的异步中间件列表
        """
        with self.lock:
            return self.middlewares.copy()


# 创建全局异步中间件管理器实例
async_middleware_manager = AsyncMiddlewareManager()
