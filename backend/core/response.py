# -*- coding: UTF-8 -*-
from typing import Any, Optional, Dict
from pydantic import BaseModel


class APIResponse(BaseModel):
    """统一API响应格式"""

    success: bool = True
    message: str = "success"
    data: Optional[Any] = None
    error: Optional[Dict[str, Any]] = None


def success_response(data: Any = None, message: str = "success") -> APIResponse:
    """成功响应"""
    return APIResponse(success=True, message=message, data=data, error=None)


def error_response(
    message: str, error_code: str = "ERROR", details: Any = None
) -> APIResponse:
    """错误响应"""
    return APIResponse(
        success=False,
        message="error",
        data=None,
        error={"code": error_code, "message": message, "details": details},
    )
