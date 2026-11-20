# -*- coding: UTF-8 -*-
from fastapi import APIRouter
import hashlib
import json
import uuid
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from throttled import Throttled, per_sec, MemoryStore

from constants import VolcengineASRResponseStatusCode, AsrTaskStatus
from models import FileNameRequest
from core.exceptions import BusinessException, ExternalServiceException
from core.response import success_response, APIResponse
from config.log import get_logger
import env
from utils.s3 import generate_download_url

router = APIRouter(prefix="/audio", tags=["Audio"])
logger = get_logger(__name__)
STORE = MemoryStore()

SUBMIT_URL = "https://openspeech.bytedance.com/api/v3/auc/bigmodel/submit"
QUERY_URL = "https://openspeech.bytedance.com/api/v3/auc/bigmodel/query"

# DNS 解析器偶尔会瞬断（VPN 切换/解析缓存），对连接错误做重试
SESSION = requests.Session()
SESSION.mount(
    "https://",
    HTTPAdapter(
        max_retries=Retry(
            total=3,
            connect=3,
            read=2,
            backoff_factor=0.8,
            status_forcelist=(429, 500, 502, 503, 504),
            allowed_methods=frozenset(["GET", "POST"]),
            raise_on_status=False,
        )
    ),
)


def generate_local_uuid():
    """生成本地UUID"""
    mac = uuid.getnode()
    mac_address = ":".join(("%012X" % mac)[i : i + 2] for i in range(0, 12, 2))
    md5_obj = hashlib.md5(mac_address.encode("utf-8"))
    return md5_obj.hexdigest()


def build_asr_headers(request_id: str, sequence: str = None):
    """构造火山语音新版鉴权请求头（API Key）"""
    headers = {
        "X-Api-Key": env.AUC_API_KEY,
        "X-Api-Resource-Id": env.AUC_RESOURCE_ID,
        "X-Api-Request-Id": request_id,
        "Content-Type": "application/json",
    }
    if sequence is not None:
        headers["X-Api-Sequence"] = sequence
    return headers


@router.post("/transcription-tasks", response_model=APIResponse)
async def create_transcription_task(request: FileNameRequest):
    """创建音频转写任务

    RESTful路径: POST /api/v1/audio/transcription-tasks
    """
    logger.info(f"Creating transcription task for file: {request.filename}")

    try:
        download_url = generate_download_url(request.filename)
        # 新版接口以提交时生成的 request id 作为任务 id，查询时复用
        task_id = str(uuid.uuid4())

        data = {
            "user": {
                "uid": generate_local_uuid(),
            },
            "audio": {"format": "mp3", "url": download_url},
            "request": {
                "model_name": "bigmodel",
                "enable_itn": True,
                "enable_punc": True,
                "show_utterances": True,
            },
        }

        with Throttled(
            key=env.AUC_API_KEY, store=STORE, quota=per_sec(limit=100, burst=100)
        ):
            response = SESSION.post(
                SUBMIT_URL,
                data=json.dumps(data),
                headers=build_asr_headers(task_id, sequence="-1"),
                timeout=60,
            )

        response.raise_for_status()
        status_code = response.headers.get("X-Api-Status-Code")
        status_message = response.headers.get("X-Api-Message", "")

        if status_code != VolcengineASRResponseStatusCode.SUCCESS.value:
            logger.error(
                f"ASR submit failed: code={status_code}, message={status_message}"
            )
            raise ExternalServiceException(
                "Volcengine ASR",
                f"Submit task failed: {status_code} {status_message}",
            )

        logger.info(f"Transcription task created successfully with ID: {task_id}")

        return success_response(
            data={"task_id": task_id}, message="Transcription task created successfully"
        )

    except requests.RequestException as e:
        logger.error(f"Request failed when creating transcription task: {str(e)}")
        raise ExternalServiceException("Volcengine ASR", f"Request failed: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error when creating transcription task: {str(e)}")
        raise BusinessException(f"Failed to create transcription task: {str(e)}")


@router.get("/transcription-tasks/{task_id}", response_model=APIResponse)
async def get_transcription_task(task_id: str):
    """获取音频转写任务状态

    RESTful路径: GET /api/v1/audio/transcription-tasks/{task_id}
    """
    logger.info(f"Querying transcription task status: {task_id}")

    try:
        with Throttled(
            key=env.AUC_API_KEY, store=STORE, quota=per_sec(limit=100, burst=100)
        ):
            response = SESSION.post(
                QUERY_URL,
                data=json.dumps({}),
                headers=build_asr_headers(task_id),
                timeout=60,
            )

        response.raise_for_status()
        status_code = response.headers.get("X-Api-Status-Code")
        status_message = response.headers.get("X-Api-Message", "")

        if status_code == VolcengineASRResponseStatusCode.SUCCESS.value:
            result = response.json().get("result") or {}
            utterances = result.get("utterances") or []
            segments = [
                {
                    "start_time": utterance.get("start_time", 0),
                    "end_time": utterance.get("end_time", 0),
                    "text": utterance.get("text", ""),
                }
                for utterance in utterances
            ]
            if not segments and result.get("text"):
                segments = [{"start_time": 0, "end_time": 0, "text": result["text"]}]

            logger.info(f"Transcription task {task_id} completed successfully")

            return success_response(
                data={"status": AsrTaskStatus.FINISHED.value, "result": segments},
                message="Transcription completed",
            )

        elif status_code in [
            VolcengineASRResponseStatusCode.PENDING.value,
            VolcengineASRResponseStatusCode.RUNNING.value,
        ]:
            logger.info(f"Transcription task {task_id} is still running")

            return success_response(
                data={"status": AsrTaskStatus.RUNNING.value, "result": None},
                message="Transcription in progress",
            )
        else:
            logger.error(
                f"Transcription task {task_id} failed: code={status_code}, message={status_message}"
            )

            return success_response(
                data={"status": AsrTaskStatus.FAILED.value, "result": None},
                message="Transcription failed",
            )

    except requests.RequestException as e:
        logger.error(
            f"Request failed when querying transcription task {task_id}: {str(e)}"
        )
        raise ExternalServiceException(
            "Volcengine ASR", f"Query request failed: {str(e)}"
        )
    except Exception as e:
        logger.error(
            f"Unexpected error when querying transcription task {task_id}: {str(e)}"
        )
        raise BusinessException(f"Failed to query transcription task: {str(e)}")
