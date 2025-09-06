# -*- coding: UTF-8 -*-
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from typing import Union
import traceback
from config.log import get_logger

logger = get_logger(__name__)


class APIException(HTTPException):
    """自定义API异常"""

    def __init__(
        self,
        status_code: int,
        message: str,
        error_code: str = None,
        details: Union[str, dict] = None,
    ):
        super().__init__(status_code=status_code, detail=message)
        self.message = message
        self.error_code = error_code or f"API_ERROR_{status_code}"
        self.details = details


class BusinessException(APIException):
    """业务逻辑异常"""

    def __init__(
        self, message: str, error_code: str = None, details: Union[str, dict] = None
    ):
        super().__init__(
            status_code=400,
            message=message,
            error_code=error_code or "BUSINESS_ERROR",
            details=details,
        )


class ExternalServiceException(APIException):
    """外部服务异常"""

    def __init__(
        self, service_name: str, message: str, details: Union[str, dict] = None
    ):
        super().__init__(
            status_code=502,
            message=f"External service error from {service_name}: {message}",
            error_code="EXTERNAL_SERVICE_ERROR",
            details=details,
        )


async def api_exception_handler(request: Request, exc: APIException) -> JSONResponse:
    """API异常处理器"""
    logger.error(
        "API Exception occurred",
        extra={
            "error_code": exc.error_code,
            "error_message": exc.message,
            "details": exc.details,
            "path": request.url.path,
            "method": request.method,
            "status_code": exc.status_code,
        },
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.error_code,
                "message": exc.message,
                "details": exc.details,
            },
            "data": None,
        },
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """通用异常处理器"""
    logger.error(
        "Unexpected exception occurred",
        extra={
            "exception_type": type(exc).__name__,
            "error_message": str(exc),
            "path": request.url.path,
            "method": request.method,
            "traceback": traceback.format_exc(),
        },
    )

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred",
                "details": None,
            },
            "data": None,
        },
    )
