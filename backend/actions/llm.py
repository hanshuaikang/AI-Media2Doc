# -*- coding: UTF-8 -*-
import json

from arkitect.core.component.llm import ArkChatRequest, BaseChatLanguageModel
from arkitect.core.component.llm.model import ArkChatParameters

from .dispatcher import ActionDispatcher
from env import ENDPOINT_ID

prompt = """
你是一个优秀的 {}。你的任务是将给定的文字内容转换为{}风格的Markdown文本。请仔细阅读以下文本内容，并按照要求进行转换。
要转换的文本内容：
<text_content>
{}
</text_content>
转换要求如下：
1. 精简去除无关的内容。
2. 只返回Markdown格式的内容。

"""


mind_prompt = """
你的任务是将给定的文字内容转换为思维导图对应的 json 格式。我使用的是 mind-map 这个开源的思维导图框架, 请仔细阅读以下文本内容，并按照要求进行转换。
要转换的文本内容：
<text_content>
{}
</text_content>
转换要求如下：
1. 精简去除无关的内容。
2. 只返回 mind-map 兼容对应的 json格式。



"""
role_dict = {
    "note": "学习达人",
    "xiaohongshu": "小红书运营专家, 你非常擅长撰写小红书爆文",
    "weixin": "微信公众号运营专家, 你非常擅长撰写微信公众号爆文",
    "summary": "人工智能助手, 你非常擅长提炼文本内容的精华, 并生成摘要",
    "mind": "思维导图",
}

style_dict = {
    "note": "知识笔记",
    "xiaohongshu": "小红书爆文, 请尽量利用 Emoji 标签增加文章的丰富度。",
    "weixin": "微信公众号爆文",
    "summary": "视频摘要",
    "mind": "思维导图",
}


@ActionDispatcher.register("generate_markdown_text")
async def generate_markdown_text(request: ArkChatRequest):
    content = json.loads(request.messages[0].content)
    style = content.get("style", "note")
    if style == "mind":
        p = mind_prompt
        text = content.get("text", "")
        msg = p.format(text)
        msg += """
        请严格按照如下格式返回:
        {
            "data": {
                "text": "<p>根节点</p>",
                "expand": true,
                "uid": "430afa37-f0b5-4cf3-a270-d15028b413a9",
                "richText": true,
                "isActive": false
            },
            "children": [
                {
                    "data": {
                        "text": "<p>二级节点</p>",
                        "generalization": {
                            "text": "<p>概要</p>",
                            "uid": "aebb0b2a-35fb-4ae6-a346-87706145bce5",
                            "richText": true,
                            "expand": true,
                            "isActive": false
                        },
                        "uid": "b11c529a-3944-4c2f-ba6d-0cd2101ba6ab",
                        "richText": true,
                        "expand": true,
                        "isActive": false
                    },
                    "children": [
                        {
                            "data": {
                                "text": "<p>分支主题</p>",
                                "uid": "52579e9c-5a75-4dd7-b0dd-b67dc2ee38ab",
                                "richText": true,
                                "expand": true,
                                "isActive": false
                            },
                            "children": []
                        },
                        {
                            "data": {
                                "text": "<p>分支主题</p>",
                                "uid": "d29ff394-03bd-4cf6-a5fa-a2f368f538d3",
                                "richText": true,
                                "expand": true,
                                "isActive": false
                            },
                            "children": []
                        }
                    ]
                }
            ],
            "smmVersion": "0.13.1-fix.2"
        }
        """
        request.messages[0].content = msg
    else:
        p = prompt
        style_type = style_dict.get(style, "知识笔记")
        role = role_dict.get(style, "学习达人")

        text = content.get("text", "")
        request.messages[0].content = p.format(role, style_type, text)
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
