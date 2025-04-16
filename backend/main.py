# -*- coding: UTF-8 -*-
"""
默认llm逻辑
"""
import os
from typing import AsyncIterable


from arkitect.core.component.llm.model import (
    ArkChatRequest,
    Response,
)
from arkitect.launcher.local.serve import launch_serve
from arkitect.telemetry.trace import task
from arkitect.utils.context import get_headers

from actions.dispatcher import ActionDispatcher


@task()
async def main(request: ArkChatRequest) -> AsyncIterable[Response]:
    dispatcher = ActionDispatcher()
    # 通过使用不同的 header 分发到不同的处理逻辑
    request_action = get_headers().get("request-action", "default")

    async for response in dispatcher.dispatch(request_action, request):
        yield response


if __name__ == "__main__":
    port = os.getenv("_FAAS_RUNTIME_PORT")
    launch_serve(
        package_path="main",
        port=int(port) if port else 8080,
        health_check_path="/v1/ping",
        endpoint_path="/api/v3/bots/chat/completions",
        clients={},
    )
