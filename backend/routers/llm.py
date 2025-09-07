# -*- coding: UTF-8 -*-

from fastapi import APIRouter
from openai import OpenAI

import env
from core.response import success_response, APIResponse
from models import ChatRequest

router = APIRouter(prefix="/llm", tags=["LLM"])


@router.post("/completions", response_model=APIResponse)
async def default_chat(request: ChatRequest):
    """默认聊天接口"""
    client = OpenAI(
        base_url=env.LLM_BASE_URL,
        api_key=env.LLM_API_KEY,
    )

    messages = [
        {"role": message.role, "content": message.content}
        for message in request.messages
    ]

    response = client.chat.completions.create(
        model=env.LLM_MODEL_ID,
        messages=messages,
        timeout=120,
        max_tokens=env.LLM_MAX_TOKENS,
    )
    return success_response(
        data={"choices": [choices.model_dump() for choices in response.choices]},
        message="Chat completed successfully",
    )


@router.post("/markdown-generation", response_model=APIResponse)
async def generate_markdown_text(request: ChatRequest):
    """生成 Markdown 文本"""
    client = OpenAI(
        base_url=env.LLM_BASE_URL,
        api_key=env.LLM_API_KEY,
    )

    messages = [
        {"role": message.role, "content": message.content}
        for message in request.messages
    ]

    response = client.chat.completions.create(
        model=env.LLM_MODEL_ID,
        messages=messages,
        timeout=120,
        max_tokens=env.LLM_MAX_TOKENS,
    )

    return success_response(
        data={"choices": [choices.model_dump() for choices in response.choices]},
        message="Chat completed successfully",
    )
