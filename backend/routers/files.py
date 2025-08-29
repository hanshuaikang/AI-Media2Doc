from fastapi import APIRouter
from config.log import get_logger
from core.exceptions import ExternalServiceException
from core.response import success_response, APIResponse
from models import FileNameRequest
import tos
import env

router = APIRouter(prefix="/files", tags=["Tos"])
logger = get_logger(__name__)


@router.post("/upload-urls", response_model=APIResponse)
async def create_upload_url(request: FileNameRequest):
    """创建文件上传URL

    RESTful路径: POST /api/v1/files/upload-urls
    """
    logger.info(f"Creating upload URL for file: {request.filename}")

    try:
        tos_client = tos.TosClient(
            tos.Auth(env.TOS_ACCESS_KEY, env.TOS_SECRET_KEY, env.TOS_REGION),
            env.TOS_ENDPOINT,
        )

        url = tos_client.generate_presigned_url(
            Method="PUT", Bucket=env.TOS_BUCKET, Key=request.filename, ExpiresIn=3600
        )

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
