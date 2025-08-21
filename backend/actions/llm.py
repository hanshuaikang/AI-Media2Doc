# -*- coding: UTF-8 -*-
from arkitect.core.component.llm import ArkChatRequest
from openai import OpenAI

import env
from .dispatcher import ActionDispatcher


@ActionDispatcher.register("generate_markdown_text")
async def generate_markdown_text(request: ArkChatRequest):
    client = OpenAI(
        base_url=env.LLM_BASE_URL,
        api_key=env.LLM_API_KEY,
    )
    messages = [
        {"role": message.role, "content": message.content}
        for message in request.messages
    ]

    yield client.chat.completions.create(
        model=env.LLM_MODEL_ID,
        messages=messages,
        timeout=120,
        max_tokens=env.LLM_MAX_TOKENS,
    )


@ActionDispatcher.register("default")
async def default_llm_action(request: ArkChatRequest):
    client = OpenAI(
        base_url=env.LLM_BASE_URL,
        api_key=env.LLM_API_KEY,
    )
    messages = [
        {"role": message.role, "content": message.content}
        for message in request.messages
    ]

    yield client.chat.completions.create(
        model=env.LLM_MODEL_ID,
        timeout=120,
        messages=messages,
        max_tokens=env.LLM_MAX_TOKENS,
    )
