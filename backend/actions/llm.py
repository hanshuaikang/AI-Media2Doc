# -*- coding: UTF-8 -*-
from arkitect.core.component.llm import ArkChatRequest
from openai import OpenAI

import env
from .dispatcher import ActionDispatcher


@ActionDispatcher.register("generate_markdown_text")
async def generate_markdown_text(request: ArkChatRequest):
    client = OpenAI(
        # 此为默认路径，您可根据业务所在地域进行配置
        base_url=env.BASE_URL,
        # 从环境变量中获取您的 API Key。此为默认方式，您可根据需要进行修改
        api_key=env.LLM_API_KEY,
    )
    messages = [
        {"role": message.role, "content": message.content}
        for message in request.messages
    ]

    yield client.chat.completions.create(
        # 指定您创建的方舟推理接入点 ID，此处已帮您修改为您的推理接入点 ID
        model=env.MODEL_ID,
        messages=messages,
    )


@ActionDispatcher.register("default")
async def default_llm_action(request: ArkChatRequest):
    client = OpenAI(
        # 此为默认路径，您可根据业务所在地域进行配置
        base_url=env.BASE_URL,
        # 从环境变量中获取您的 API Key。此为默认方式，您可根据需要进行修改
        api_key=env.LLM_API_KEY,
    )
    messages = [
        {"role": message.role, "content": message.content}
        for message in request.messages
    ]

    yield client.chat.completions.create(
        # 指定您创建的方舟推理接入点 ID，此处已帮您修改为您的推理接入点 ID
        model=env.MODEL_ID,
        messages=messages,
    )
