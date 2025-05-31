# -*- coding: UTF-8 -*-

from arkitect.core.component.llm import ArkChatRequest, BaseChatLanguageModel
from arkitect.core.component.llm.model import ArkChatParameters

from .dispatcher import ActionDispatcher
from env import ENDPOINT_ID


@ActionDispatcher.register("generate_markdown_text")
async def generate_markdown_text(request: ArkChatRequest):
    parameters = ArkChatParameters(**request.__dict__)
    llm = BaseChatLanguageModel(
        endpoint_id=ENDPOINT_ID,
        messages=request.messages,
        parameters=parameters,
    )
    if request.stream:
        async for resp in llm.astream():
            yield resp
    else:
        yield await llm.arun()


@ActionDispatcher.register("default")
async def default_llm_action(request: ArkChatRequest):
    parameters = ArkChatParameters(**request.__dict__)
    llm = BaseChatLanguageModel(
        endpoint_id=ENDPOINT_ID,
        messages=request.messages,
        parameters=parameters,
    )
    if request.stream:
        async for resp in llm.astream():
            yield resp
    else:
        yield await llm.arun()
