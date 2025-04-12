# -*- coding: UTF-8 -*-
import json
import uuid
import time

import requests
from arkitect.core.component.llm import ArkChatRequest
from arkitect.core.component.llm.model import ArkChatResponse
from .dispatcher import ActionDispatcher

from actions.tos import generate_download_url
from env import AUC_APP_ID, AUC_ACCESS_TOKEN


@ActionDispatcher.register("submit_audio_task")
async def submit_audio_task(request: ArkChatRequest):
    submit_url = "https://openspeech.bytedance.com/api/v3/auc/bigmodel/submit"
    file_name = request.messages[0].content
    download_url = generate_download_url(file_name)
    task_id = uuid.uuid4().hex

    data = {
        "audio": {
            "format": "mp3",
            "url": download_url
        },
        "request": {
            "model_name": "bigmodel",
            "enable_itn": True
        }
    }
    print(task_id)

    headers = {
        "X-Api-App-Key": AUC_APP_ID,
        "X-Api-Access-Key": AUC_ACCESS_TOKEN,
        "X-Api-Resource-Id": "volc.bigasr.auc",
        "X-Api-Request-Id": task_id,
        "X-Api-Sequence": "-1"
    }

    response = requests.post(submit_url, data=json.dumps(data), headers=headers)
    print(f'Submit task response header X-Tt-Logid: {response.headers["X-Tt-Logid"]}\n')
    if 'X-Api-Status-Code' in response.headers and response.headers["X-Api-Status-Code"] == "20000000":
        print(f'Submit task response header X-Api-Status-Code: {response.headers["X-Api-Status-Code"]}')
        print(f'Submit task response header X-Api-Message: {response.headers["X-Api-Message"]}')
        print(f'Submit task response header X-Tt-Logid: {response.headers["X-Tt-Logid"]}\n')
        yield ArkChatResponse(
            id="upload_url",
            choices=[],
            created=int(time.time()),
            model="",
            object="chat.completion",
            usage=None,
            bot_usage=None,
            metadata={"task_id": task_id}
        )
    else:
        raise Exception(f'Submit task failed and the response headers are: {response.headers}')


@ActionDispatcher.register("query_audio_task")
async def query_audio_task(request: ArkChatRequest):
    task_id = request.messages[0].content
    headers = {
        "X-Api-App-Key": AUC_APP_ID,
        "X-Api-Access-Key": AUC_ACCESS_TOKEN,
        "X-Api-Resource-Id": "volc.bigasr.auc",
        "X-Api-Request-Id": task_id,
    }

    print(f"query task id: {task_id}")

    query_url = "https://openspeech.bytedance.com/api/v3/auc/bigmodel/query"

    response = requests.post(query_url, json.dumps({}), headers=headers)

    if 'X-Api-Status-Code' in response.headers:
        if response.headers["X-Api-Status-Code"] == "20000000":
            print(f'Query task response header X-Api-Status-Code: {response.headers["X-Api-Status-Code"]}')
            print(f'Query task response header X-Api-Message: {response.headers["X-Api-Message"]}')
            print(f'Query task response header X-Tt-Logid: {response.headers["X-Tt-Logid"]}\n')
            yield ArkChatResponse(
                id="query_audio_task",
                choices=[],
                created=int(time.time()),
                model="",
                object="chat.completion",
                usage=None,
                bot_usage=None,
                metadata={"result": response.json()['result']['text'], "status": "finished"}
            )
        elif response.headers["X-Api-Status-Code"] in ["20000001", "20000002"]:
            yield ArkChatResponse(
                id="query_audio_task",
                choices=[],
                created=int(time.time()),
                model="",
                object="chat.completion",
                usage=None,
                bot_usage=None,
                metadata={"result": "", "status": "running"}
            )
        else:
            print(response.json())
            yield ArkChatResponse(
                id="query_audio_task",
                choices=[],
                created=int(time.time()),
                model="",
                object="chat.completion",
                usage=None,
                bot_usage=None,
                metadata={"result": "", "status": "failed"}
            )
    else:
        print(f'Query task failed and the response headers are: {response.headers}')
        raise Exception(f'Query task failed and the response headers are: {response.headers}')
