# -*- coding: UTF-8 -*-

from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
import time
from typing import Optional

import env
from config.log import setup_logging, get_logger
from core.exceptions import (
    APIException,
    api_exception_handler,
    general_exception_handler,
)
from core.response import success_response, APIResponse
from routers import llm, files, audio, secrets

# 设置日志
setup_logging(log_level="INFO")
logger = get_logger(__name__)

app = FastAPI(
    title="AI Media2Doc API",
    description="Convert media files to documents using AI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 添加异常处理器
app.add_exception_handler(APIException, api_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)


async def verify_web_access_password(
    request_web_access_password: Optional[str] = Header(
        None, alias="request-web-access-password"
    )
):
    """验证访问密码"""
    if (
        env.WEB_ACCESS_PASSWORD
        and request_web_access_password != env.WEB_ACCESS_PASSWORD
    ):
        logger.warning("Unauthorized access attempt")
        raise HTTPException(
            status_code=401, detail="Unauthorized: Invalid or missing web-access-token"
        )
    return True


# 注册路由
app.include_router(
    llm.router, prefix="/api/v1", dependencies=[Depends(verify_web_access_password)]
)
app.include_router(
    files.router, prefix="/api/v1", dependencies=[Depends(verify_web_access_password)]
)
app.include_router(
    audio.router, prefix="/api/v1", dependencies=[Depends(verify_web_access_password)]
)

app.include_router(
    secrets.router, prefix="/api/v1", dependencies=[Depends(verify_web_access_password)]
)


@app.get("/health", response_model=APIResponse)
async def health_check():
    """健康检查接口"""
    logger.info("Health check requested")
    return success_response(
        data={"status": "healthy", "timestamp": int(time.time())},
        message="Service is healthy",
    )


if __name__ == "__main__":
    import uvicorn

    logger.info("Starting AI Media2Doc API server...")
    uvicorn.run("app:app", host="0.0.0.0", port=8080, reload=True)
