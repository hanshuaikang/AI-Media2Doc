# -*- coding: UTF-8 -*-

from fastapi import APIRouter

import env
from config.log import get_logger
from core.response import success_response
from models import EnvResponse
from utils.env import mask_middle

router = APIRouter(prefix="/secrets", tags=["Secrets"])
logger = get_logger(__name__)


@router.get("", response_model=EnvResponse)
async def get_environment_variables():
    """获取环境变量信息（敏感值已脱敏）

    RESTFul路径: GET /api/v1/env
    """

    # 获取env.py中定义的所有环境变量
    env_vars = {}

    # 明确指定需要打码的变量列表
    always_mask = [
        "LLM_API_KEY",
        "TOS_ACCESS_KEY",
        "TOS_SECRET_KEY",
        "AUC_APP_ID",
        "AUC_ACCESS_TOKEN",
    ]

    for key, value in vars(env).items():
        # 只处理全大写的变量（约定俗成的环境变量命名方式）
        if key.isupper():
            # 检查是否在强制打码列表中
            is_sensitive = key in always_mask

            if value is not None and value != "":
                if is_sensitive:
                    env_vars[key] = mask_middle(str(value))
                else:
                    # 非敏感信息显示完整值
                    env_vars[key] = value
            else:
                env_vars[key] = None

    logger.info("Environment variables retrieved with sensitive information masked")
    return success_response(
        data=env_vars, message="Environment variables retrieved successfully"
    )
