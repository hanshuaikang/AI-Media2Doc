# -*- coding: UTF-8 -*-
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


@ActionDispatcher.register("submit_asr_task")
async def submit_asr_task(request: ArkChatRequest):
    """
    提交一个音频转写任务
    :param request: message: filename
    :return:
    """
    submit_url = "https://openspeech.bytedance.com/api/v3/auc/bigmodel/submit"
    # 音频文件名
    file_name = request.messages[0].content
    download_url = generate_download_url(file_name)
    # 生成人物 id
    task_id = uuid.uuid4().hex

    data = {
        "audio": {"format": "mp3", "url": download_url},
        "request": {"model_name": "bigmodel", "enable_itn": True},
    }

    if AUC_CLUSTER_ID:
        data["cluster"] = AUC_CLUSTER_ID

    headers = {
        "X-Api-App-Key": AUC_APP_ID,
        "X-Api-Access-Key": AUC_ACCESS_TOKEN,
        "X-Api-Resource-Id": "volc.bigasr.auc",
        "X-Api-Request-Id": task_id,
        "X-Api-Sequence": "-1",
    }

    # 最大 QPS 限制在 100，避免频繁请求。
    with Throttled(key=AUC_APP_ID, store=STORE, quota=per_sec(limit=100, burst=100)):
        response = requests.post(submit_url, data=json.dumps(data), headers=headers)

    # 判断任务是否成功
    if (
        "X-Api-Status-Code" in response.headers
        and response.headers["X-Api-Status-Code"] == "20000000"
    ):
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
    else:
        raise APIException(
            message=f"Submit asr task failed. Response headers: {response.headers}",
            code="500",
            http_code=500,
        )


@ActionDispatcher.register("query_asr_task_status")
async def query_asr_task_status(request: ArkChatRequest):
    task_id = request.messages[0].content
    headers = {
        "X-Api-App-Key": AUC_APP_ID,
        "X-Api-Access-Key": AUC_ACCESS_TOKEN,
        "X-Api-Resource-Id": "volc.bigasr.auc",
        "X-Api-Request-Id": task_id,
    }

    query_url = "https://openspeech.bytedance.com/api/v3/auc/bigmodel/query"

    # 最大 QPS 限制在 100，避免频繁请求。
    with Throttled(key=AUC_APP_ID, store=STORE, quota=per_sec(limit=100, burst=100)):
        response = requests.post(query_url, json.dumps({}), headers=headers)

    if "X-Api-Status-Code" in response.headers:
        if (
            response.headers["X-Api-Status-Code"]
            == VolcengineASRResponseStatusCode.SUCCESS.value
        ):

            data = response.json()
            utterances = data["result"]["utterances"]
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
        elif response.headers["X-Api-Status-Code"] in [
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
    else:
        raise APIException(
            message=f"Query ASR task failed. Response headers: {response.headers}. "
            f"Please check the task ID or API configuration.",
            code="500",
            http_code=500,
        )
