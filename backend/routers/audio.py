# -*- coding: UTF-8 -*-
from fastapi import APIRouter
import hashlib
import json
import uuid
import requests
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


def generate_local_uuid():
    """生成本地UUID"""
    mac = uuid.getnode()
    mac_address = ":".join(("%012X" % mac)[i : i + 2] for i in range(0, 12, 2))
    md5_obj = hashlib.md5(mac_address.encode("utf-8"))
    return md5_obj.hexdigest()


@router.post("/transcription-tasks", response_model=APIResponse)
async def create_transcription_task(request: FileNameRequest):
    """创建音频转写任务

    RESTful路径: POST /api/v1/audio/transcription-tasks
    """
    logger.info(f"Creating transcription task for file: {request.filename}")

    try:
        submit_url = "https://openspeech.bytedance.com/api/v3/auc/bigmodel/submit"
        download_url = generate_download_url(request.filename)
        uid = generate_local_uuid()
        task_id = str(uuid.uuid4())
        data = {
            "user": {
                "uid": uid,
            },
            "audio": {"format": "mp3", "url": download_url,"show_utterances": True,},
            "request": {"model_name": "bigmodel", "enable_itn": True},
        }

        headers = {
            "X-Api-App-Key":env.AUC_APP_ID,
            "X-Api-Access-Key":env.AUC_ACCESS_TOKEN,
            "X-Api-Resource-Id":"volc.bigasr.auc",
            "X-Api-Request-Id":task_id,
            "X-Api-Sequence":"-1",
        }
        with Throttled(
            key=env.AUC_APP_ID, store=STORE, quota=per_sec(limit=100, burst=100)
        ):
            response = requests.post(submit_url, data=json.dumps(data), headers=headers)
        response.raise_for_status()

        status = response.headers.get("X-Api-Message")
        logId = response.headers.get("X-Tt-Logid")
        if "OK" != status:
            logger.error(f"ASR service returned error status: {status}, logId: {logId}")
            raise ExternalServiceException(
                "Volcengine ASR", f"Submit task failed with status: {status}"
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
        query_url = "https://openspeech.bytedance.com/api/v3/auc/bigmodel/query"

        headers = {
            "X-Api-App-Key":env.AUC_APP_ID,
            "X-Api-Access-Key":env.AUC_ACCESS_TOKEN,
            "X-Api-Resource-Id":"volc.bigasr.auc",
            "X-Api-Request-Id":task_id,
        }

        with Throttled(
            key=env.AUC_APP_ID, store=STORE, quota=per_sec(limit=100, burst=100)
        ):
            response = requests.post(query_url, json.dumps({}),headers=headers)

        response.raise_for_status()
        heads = response.headers

        code = heads.get("X-Api-Status-Code")
        if code == VolcengineASRResponseStatusCode.SUCCESS.value:
            resp = response.json()
            result = [
                {
                    "start_time": utterance["start_time"],
                    "end_time": utterance["end_time"],
                    "text": utterance["text"],
                }
                for utterance in resp['result']['utterances']
            ]
            logger.info(f"Transcription task {task_id} completed successfully")

            return success_response(
                data={"status": AsrTaskStatus.FINISHED.value, "result": result},
                message="Transcription completed",
            )

        elif code in [
            VolcengineASRResponseStatusCode.PENDING.value,
            VolcengineASRResponseStatusCode.RUNNING.value,
        ]:
            logger.info(f"Transcription task {task_id} is still running")

            return success_response(
                data={"status": AsrTaskStatus.RUNNING.value, "result": None},
                message="Transcription in progress",
            )
        else:
            logger.error(f"Transcription task {task_id} failed with code: {code}")

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
