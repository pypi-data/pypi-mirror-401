"""中间件管理器模块"""

from __future__ import annotations

import threading
from typing import Any

from yitool.log import logger
from yitool.middleware.middleware import Middleware, MiddlewareResultStatus


class MiddlewareManager:
    """中间件管理器类

    用于管理中间件的注册、注销和执行

    Attributes:
        middlewares: 中间件列表
        lock: 线程锁
    """

    def __init__(self):
        """初始化中间件管理器"""
        self.middlewares: list[Middleware] = []
        self.lock = threading.RLock()

    def register(self, middleware: Middleware) -> None:
        """注册中间件

        Args:
            middleware: 中间件对象
        """
        with self.lock:
            # 检查中间件是否已注册
            if middleware not in self.middlewares:
                self.middlewares.append(middleware)
                # 按优先级排序，优先级数值越小越靠前
                self.middlewares.sort(key=lambda m: m.priority)
                logger.debug(f"Registered middleware: {middleware}")

    def unregister(self, middleware: Middleware) -> bool:
        """注销中间件

        Args:
            middleware: 中间件对象

        Returns:
            是否成功注销
        """
        with self.lock:
            if middleware in self.middlewares:
                self.middlewares.remove(middleware)
                logger.debug(f"Unregistered middleware: {middleware}")
                return True
            return False

    def unregister_by_name(self, name: str) -> bool:
        """根据名称注销中间件

        Args:
            name: 中间件名称

        Returns:
            是否成功注销
        """
        with self.lock:
            for middleware in self.middlewares:
                if middleware.name == name:
                    self.middlewares.remove(middleware)
                    logger.debug(f"Unregistered middleware by name: {name}")
                    return True
            return False

    def get_middleware_by_name(self, name: str) -> Middleware | None:
        """根据名称获取中间件

        Args:
            name: 中间件名称

        Returns:
            中间件对象，None表示未找到
        """
        with self.lock:
            for middleware in self.middlewares:
                if middleware.name == name:
                    return middleware
            return None

    def execute(self, data: Any) -> tuple[MiddlewareResultStatus, Any, str | None]:
        """执行中间件链

        Args:
            data: 要处理的数据

        Returns:
            元组(状态, 最终数据, 错误信息)
        """
        with self.lock:
            # 获取中间件列表副本，避免在执行过程中修改
            middlewares_copy = self.middlewares.copy()

        logger.debug(f"Executing middleware chain with {len(middlewares_copy)} middlewares")

        current_data = data

        for middleware in middlewares_copy:
            try:
                logger.debug(f"Executing middleware: {middleware}")
                result = middleware.process(current_data)
                logger.debug(f"Middleware {middleware} executed with result: {result.to_dict()}")

                # 更新当前数据
                if result.data is not None:
                    current_data = result.data

                # 根据中间件结果决定后续操作
                if result.status == MiddlewareResultStatus.STOP:
                    logger.debug(f"Middleware {middleware} requested to stop the chain")
                    return MiddlewareResultStatus.STOP, current_data, None
                elif result.status == MiddlewareResultStatus.ERROR:
                    logger.error(f"Middleware {middleware} executed with error: {result.error}")
                    return MiddlewareResultStatus.ERROR, current_data, result.error
                # 否则继续执行下一个中间件
            except Exception as e:
                logger.error(f"Error executing middleware {middleware}: {e}")
                return MiddlewareResultStatus.ERROR, current_data, str(e)

        logger.debug("Middleware chain execution completed successfully")
        return MiddlewareResultStatus.CONTINUE, current_data, None

    def clear(self) -> None:
        """清除所有中间件"""
        with self.lock:
            self.middlewares.clear()
            logger.debug("Cleared all middlewares")

    def get_middleware_count(self) -> int:
        """获取中间件数量

        Returns:
            中间件数量
        """
        with self.lock:
            return len(self.middlewares)

    def get_sorted_middlewares(self) -> list[Middleware]:
        """获取排序后的中间件列表

        Returns:
            排序后的中间件列表
        """
        with self.lock:
            return self.middlewares.copy()


# 创建全局中间件管理器实例
middleware_manager = MiddlewareManager()
