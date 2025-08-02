# -*- coding: UTF-8 -*-
import hashlib
import json
import uuid
import time

import requests
from arkitect.core.component.llm import ArkChatRequest
from arkitect.core.errors import APIException
from arkitect.types.llm.model import ArkChatResponse
from throttled import Throttled, per_sec, MemoryStore

from constants import VolcengineASRResponseStatusCode, AsrTaskStatus
from .dispatcher import ActionDispatcher

from actions.tos import generate_download_url
from env import AUC_APP_ID, AUC_ACCESS_TOKEN, AUC_CLUSTER_ID

STORE = MemoryStore()


def generate_local_uuid():
    # 获取本机 MAC 地址
    mac = uuid.getnode()
    # 将 MAC 地址格式化为标准形式
    mac_address = ":".join(("%012X" % mac)[i : i + 2] for i in range(0, 12, 2))
    md5_obj = hashlib.md5(mac_address.encode("utf-8"))
    return md5_obj.hexdigest()


@ActionDispatcher.register("submit_asr_task")
async def submit_asr_task(request: ArkChatRequest):
    """
    提交一个音频转写任务
    :param request: message: filename
    :return:
    """
    submit_url = "https://openspeech.bytedance.com/api/v1/auc/submit"
    # 音频文件名
    file_name = request.messages[0].content
    download_url = generate_download_url(file_name)
    # 生成人物 id

    data = {
        "app": {
            "appid": AUC_APP_ID,
            "token": AUC_ACCESS_TOKEN,
            "cluster": AUC_CLUSTER_ID,
        },
        "user": {
            "uid": generate_local_uuid(),
        },
        "audio": {"format": "mp3", "url": download_url},
        "request": {"model_name": "bigmodel", "enable_itn": True},
    }

    headers = {
        "Authorization": f"Bearer; {AUC_ACCESS_TOKEN}",
    }

    # 最大 QPS 限制在 100，避免频繁请求。
    with Throttled(key=AUC_APP_ID, store=STORE, quota=per_sec(limit=100, burst=100)):
        response = requests.post(submit_url, data=json.dumps(data), headers=headers)

    try:
        response.raise_for_status()
        resp = response.json()
        if resp["resp"]["message"] != "success":
            raise APIException(
                message=f"Submit asr task failed. Response: {resp}",
                code="500",
                http_code=500,
            )
        task_id = resp["resp"]["id"]
        yield ArkChatResponse(
            id="upload_url",
            choices=[],
            created=int(time.time()),
            model="",
            object="chat.completion",
            usage=None,
            bot_usage=None,
            metadata={"task_id": task_id},
        )
    except requests.RequestException as e:
        raise APIException(
            message=f"Submit asr task failed. Request error: {str(e)}",
            code="500",
            http_code=500,
        )


@ActionDispatcher.register("query_asr_task_status")
async def query_asr_task_status(request: ArkChatRequest):
    task_id = request.messages[0].content

    data = {
        "appid": AUC_APP_ID,
        "token": AUC_ACCESS_TOKEN,
        "cluster": AUC_CLUSTER_ID,
        "id": task_id,
    }
    query_url = "https://openspeech.bytedance.com/api/v1/auc/query"

    headers = {
        "Authorization": f"Bearer; {AUC_ACCESS_TOKEN}",
    }

    # 最大 QPS 限制在 100，避免频繁请求。
    with Throttled(key=AUC_APP_ID, store=STORE, quota=per_sec(limit=100, burst=100)):
        response = requests.post(query_url, json.dumps(data), headers=headers)

    try:
        response.raise_for_status()
        resp = response.json()
    except requests.RequestException as e:
        raise APIException(
            message=f"Query ASR task failed. Request error: {str(e)}",
            code="500",
            http_code=500,
        )

    code = resp["resp"]["code"]
    if code == VolcengineASRResponseStatusCode.SUCCESS.value:
        utterances = resp["resp"]["utterances"]
        result = [
            {
                "start_time": utterance["start_time"],
                "end_time": utterance["end_time"],
                "text": utterance["text"],
            }
            for utterance in utterances
        ]

        yield ArkChatResponse(
            id="query_asr_task_status",
            choices=[],
            created=int(time.time()),
            model="",
            object="chat.completion",
            usage=None,
            bot_usage=None,
            metadata={
                "result": result,
                "status": AsrTaskStatus.FINISHED.value,
            },
        )

    elif code in [
        VolcengineASRResponseStatusCode.PENDING.value,
        VolcengineASRResponseStatusCode.RUNNING.value,
    ]:
        yield ArkChatResponse(
            id="query_asr_task_status",
            choices=[],
            created=int(time.time()),
            model="",
            object="chat.completion",
            usage=None,
            bot_usage=None,
            metadata={"result": None, "status": AsrTaskStatus.RUNNING.value},
        )
    else:
        yield ArkChatResponse(
            id="query_asr_task_status",
            choices=[],
            created=int(time.time()),
            model="",
            object="chat.completion",
            usage=None,
            bot_usage=None,
            metadata={"result": None, "status": AsrTaskStatus.FAILED.value},
        )
