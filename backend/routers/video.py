# -*- coding: UTF-8 -*-
from fastapi import APIRouter

from core.exceptions import BusinessException, ExternalServiceException
from core.response import success_response, APIResponse
from config.log import get_logger
from models import VisualAnalysisRequest
import env
from utils.s3 import generate_download_url

router = APIRouter(prefix="/video", tags=["Video"])
logger = get_logger(__name__)

# Pegasus 1.5 要求分析窗口至少 4 秒, 且通过公网 URL 拉取的视频最大 4GB
DEFAULT_VISUAL_PROMPT = (
    "请用中文客观描述这段视频的画面内容, 包括出现的场景、人物动作、"
    "屏幕上展示的文字/图表/演示, 以及任何仅凭语音无法获取的视觉信息。"
    "请分条列出关键画面, 不要复述旁白。"
)


@router.post("/visual-analysis", response_model=APIResponse)
async def analyze_video_visual(request: VisualAnalysisRequest):
    """使用 TwelveLabs Pegasus 对视频画面做视觉理解 (可选能力)

    现有流程仅依赖 ASR 字幕生成文档, 看不到画面里的演示、图表、字幕等信息。
    本接口对已上传到对象存储的视频调用 Pegasus, 返回一段画面描述文本,
    前端可将其与 ASR 字幕一起送入大模型, 让生成的文档同时反映"听到的"和"看到的"。

    该能力默认关闭: 仅当配置了 TWELVELABS_API_KEY 时启用, 否则返回明确的未配置错误,
    不影响原有的纯字幕流程。

    RESTful路径: POST /api/v1/video/visual-analysis
    """
    if not env.TWELVELABS_API_KEY:
        logger.info(
            "Visual analysis requested but TWELVELABS_API_KEY is not configured"
        )
        raise BusinessException(
            "Visual analysis is not enabled. Set TWELVELABS_API_KEY to use TwelveLabs Pegasus."
        )

    # 延迟导入: 未启用该功能时无需安装 twelvelabs 依赖
    try:
        from twelvelabs import TwelveLabs
        from twelvelabs.types import VideoContext_Url
    except ImportError as e:
        logger.error(f"twelvelabs SDK not installed: {str(e)}")
        raise BusinessException(
            "twelvelabs SDK is not installed. Run `pip install twelvelabs` to enable visual analysis."
        )

    logger.info(f"Creating visual analysis task for file: {request.filename}")

    # Pegasus 通过公网 URL 拉取视频, 复用对象存储的预签名下载地址
    download_url = generate_download_url(request.filename)
    prompt = request.prompt or DEFAULT_VISUAL_PROMPT

    try:
        client = TwelveLabs(api_key=env.TWELVELABS_API_KEY)
        response = client.analyze(
            model_name=env.TWELVELABS_MODEL_NAME,
            video=VideoContext_Url(url=download_url),
            prompt=prompt,
            max_tokens=request.max_tokens,
        )
    except Exception as e:
        logger.error(
            f"TwelveLabs visual analysis failed for {request.filename}: {str(e)}"
        )
        raise ExternalServiceException(
            "TwelveLabs", f"Visual analysis failed: {str(e)}"
        )

    logger.info(f"Visual analysis completed for file: {request.filename}")
    return success_response(
        data={"visual_description": response.data or ""},
        message="Visual analysis completed successfully",
    )
