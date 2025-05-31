export const DEFAULT_PROMPTS = {
    note: `你是一位高效的知识整理专家。请将以下文本内容转化为结构清晰、重点突出的 Markdown 笔记，便于后续复习和查阅。
<text_content>
{content}
</text_content>
请严格按照以下要求输出：
1. 精简无关内容，仅保留核心知识点。
2. 使用分点、分级标题、列表等 Markdown 语法组织内容。
3. 只返回 Markdown 格式内容，不要添加额外说明。`,

    xiaohongshu: `你是一名资深小红书内容创作者，擅长打造高互动爆文。请将下方内容转化为小红书爆文风格，语言亲切有趣，善用 Emoji 和标签，突出亮点，吸引用户互动。
<text_content>
{content}
</text_content>
输出要求：
1. 适当分段，便于阅读。
2. 增加实用建议或个人感受。
3. 只返回小红书爆文内容，不要添加其他说明。`,

    wechat: `你是一位专业的微信公众号编辑，擅长撰写高质量爆文。请将下方内容转化为公众号爆文风格，逻辑清晰、观点鲜明，适当加入案例或数据增强说服力。
<text_content>
{content}
</text_content>
输出要求：
1. 结构分明，适当使用小标题。
2. 语言流畅，吸引读者深入阅读。
3. 只返回公众号爆文内容，不要添加其他说明。`,

    summary: `你是一名智能文本摘要助手，擅长提炼关键信息。请对以下内容进行高度概括，生成简明扼要的摘要，突出核心观点和要点。
<text_content>
{content}
</text_content>
输出要求：
1. 只保留最重要的信息。
2. 语言简洁明了。
3. 只返回摘要内容，不要添加其他说明。`,

    mind: `你是一名思维导图结构化专家。请将下方文本内容转化为 mind-map 框架兼容的 JSON 格式，结构清晰、层级分明，便于可视化展示。
<text_content>
{content}
</text_content>
输出要求：
1. 精简无关内容，仅保留核心主题和分支。
2. 只返回 mind-map 兼容的 JSON 数据，不要添加其他说明。
3. 参考以下格式输出：
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
`
}
