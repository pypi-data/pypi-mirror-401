from __future__ import annotations

from typing import Any


class YiException(Exception):
    """异常基类"""

    def __init__(
        self,
        message: str = "An error occurred",
        code: str = "ERROR",
        status_code: int = 500,
        data: Any = None,
    ):
        self.message = message
        self.code = code
        self.status_code = status_code
        self.data = data
        super().__init__(self.message)


class YiConfigError(YiException):
    """配置错误异常"""

    def __init__(
        self,
        message: str = "Config error",
        code: str = "CONFIG_ERROR",
        status_code: int = 500,
        data: Any = None,
    ):
        super().__init__(message, code, status_code, data)


class YiFileError(YiException):
    """文件操作异常"""

    def __init__(
        self,
        message: str = "File error",
        code: str = "FILE_ERROR",
        status_code: int = 500,
        data: Any = None,
    ):
        super().__init__(message, code, status_code, data)


class YiDatabaseError(YiException):
    """数据库操作异常"""

    def __init__(
        self,
        message: str = "Database error",
        code: str = "DATABASE_ERROR",
        status_code: int = 500,
        data: Any = None,
    ):
        super().__init__(message, code, status_code, data)


class YiRedisError(YiException):
    """Redis操作异常"""

    def __init__(
        self,
        message: str = "Redis error",
        code: str = "REDIS_ERROR",
        status_code: int = 500,
        data: Any = None,
    ):
        super().__init__(message, code, status_code, data)


class YiHttpBadRequestException(YiException):
    """请求参数错误异常"""

    def __init__(
        self,
        message: str = "Bad request",
        code: str = "BAD_REQUEST",
        status_code: int = 400,
        data: Any = None,
    ):
        super().__init__(message, code, status_code, data)


class YiHttpNotFoundException(YiException):
    """资源未找到异常"""

    def __init__(
        self,
        message: str = "Resource not found",
        code: str = "NOT_FOUND",
        status_code: int = 404,
        data: Any = None,
    ):
        super().__init__(message, code, status_code, data)


class YiHttpUnauthorizedException(YiException):
    """未授权异常"""

    def __init__(
        self,
        message: str = "Unauthorized",
        code: str = "UNAUTHORIZED",
        status_code: int = 401,
        data: Any = None,
    ):
        super().__init__(message, code, status_code, data)


class YiHttpForbiddenException(YiException):
    """禁止访问异常"""

    def __init__(
        self,
        message: str = "Forbidden",
        code: str = "FORBIDDEN",
        status_code: int = 403,
        data: Any = None,
    ):
        super().__init__(message, code, status_code, data)


class YiHttpConflictException(YiException):
    """资源冲突异常"""

    def __init__(
        self,
        message: str = "Conflict",
        code: str = "CONFLICT",
        status_code: int = 409,
        data: Any = None,
    ):
        super().__init__(message, code, status_code, data)


class YiHttpInternalServerErrorException(YiException):
    """服务器内部错误异常"""

    def __init__(
        self,
        message: str = "Internal server error",
        code: str = "INTERNAL_SERVER_ERROR",
        status_code: int = 500,
        data: Any = None,

    ):
        super().__init__(message, code, status_code, data)

