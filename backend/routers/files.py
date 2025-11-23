# -*- coding: UTF-8 -*-
from fastapi import APIRouter
from config.log import get_logger
from core.exceptions import ExternalServiceException
from core.response import success_response, APIResponse
from models import FileNameRequest
from utils import s3

router = APIRouter(prefix="/files", tags=["storage"])
logger = get_logger(__name__)


@router.post("/upload-urls", response_model=APIResponse)
async def create_upload_url(request: FileNameRequest):
    """创建文件上传URL

    RESTful路径: POST /api/v1/files/upload-urls
    """
    logger.info(f"Creating upload URL for file: {request.filename}")

    try:
        url = s3.generate_upload_url(request.filename)

        logger.info(f"Upload URL created successfully for file: {request.filename}")

        return success_response(
            data={"upload_url": url}, message="Upload URL created successfully"
        )

    except Exception as e:
        logger.error(
            f"Failed to create upload URL for file {request.filename}: {str(e)}"
        )
        raise ExternalServiceException(
            "TOS", f"Failed to generate upload URL: {str(e)}"
        )
