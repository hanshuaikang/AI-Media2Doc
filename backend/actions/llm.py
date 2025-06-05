# -*- coding: UTF-8 -*-
from arkitect.core.component.context.context import Context
from arkitect.core.component.llm import ArkChatRequest
from arkitect.types.llm.model import ArkChatParameters

from env import MODEL_ID
from .dispatcher import ActionDispatcher


@ActionDispatcher.register("generate_markdown_text")
async def generate_markdown_text(request: ArkChatRequest):
    parameters = ArkChatParameters(**request.__dict__)
    ctx = Context(model=MODEL_ID, parameters=parameters)
    await ctx.init()
    messages = [
        {"role": message.role, "content": message.content}
        for message in request.messages
    ]
    resp = await ctx.completions.create(messages=messages, stream=request.stream)

    if request.stream:
        async for chunk in resp:
            yield chunk
    else:
        yield resp


@ActionDispatcher.register("default")
async def default_llm_action(request: ArkChatRequest):
    parameters = ArkChatParameters(**request.__dict__)
    ctx = Context(model=MODEL_ID, parameters=parameters)
    await ctx.init()
    messages = [
        {"role": message.role, "content": message.content}
        for message in request.messages
    ]
    resp = await ctx.completions.create(messages=messages, stream=request.stream)
    if request.stream:
        async for chunk in resp:
            yield chunk
    else:
        yield resp
