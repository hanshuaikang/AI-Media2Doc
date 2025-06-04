# -*- coding: UTF-8 -*-
import time
import tos
from arkitect.core.component.llm import ArkChatRequest
from arkitect.types.llm.model import ArkChatResponse

from .dispatcher import ActionDispatcher
from env import TOS_ACCESS_KEY, TOS_SECRET_KEY, TOS_REGION, TOS_BUCKET, TOS_ENDPOINT


@ActionDispatcher.register("generate_upload_url")
async def generate_upload_url(request: ArkChatRequest):
    file_name = request.messages[0].content
    tos_client = tos.TosClient(
        tos.Auth(TOS_ACCESS_KEY, TOS_SECRET_KEY, TOS_REGION), TOS_ENDPOINT
    )
    url = tos_client.generate_presigned_url(
        Method="PUT", Bucket=TOS_BUCKET, Key=file_name, ExpiresIn=3600
    )

    yield ArkChatResponse(
        id="upload_url",
        choices=[],
        created=int(time.time()),
        model="",
        object="chat.completion",
        usage=None,
        bot_usage=None,
        metadata={"upload_url": url},
    )


def generate_download_url(file_name: str):
    tos_client = tos.TosClient(
        tos.Auth(TOS_ACCESS_KEY, TOS_SECRET_KEY, TOS_REGION), TOS_ENDPOINT
    )
    return tos_client.generate_presigned_url(
        Method="GET", Bucket=TOS_BUCKET, Key=file_name, ExpiresIn=3600
    )
