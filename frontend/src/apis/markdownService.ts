import httpService from './http'
import { APIResponse, ChatResponse, ContentStyle } from './types'
import { DEFAULT_PROMPTS } from '../constants'


// 获取本地自定义 prompt
function getCustomPrompt(style: string): string | undefined {
  try {
    const str = localStorage.getItem('customPrompts')
    if (str) {
      const obj = JSON.parse(str)
      if (obj && typeof obj[style] === 'string') {
        return obj[style]
      }
    }
  } catch {}
  return undefined
}

/**
 * 根据文本和内容风格生成最终 prompt
 */
function renderPrompt(style: string, text: string): string {
  const promptTpl = getCustomPrompt(style) || DEFAULT_PROMPTS[style] || ''
  return promptTpl.replace(/\{content\}/g, text)
}

/**
 * 根据文本生成Markdown内容
 * @param text 原始文本
 * @param contentStyle 内容风格
 * @returns 生成的Markdown内容
 */
export const generateMarkdownText = async (text: string, contentStyle: string, remarks: string, timeout: number, maxTokens: number): Promise<string> => {


  try {
    let prompt = renderPrompt(contentStyle, text)
    // add remarks
    if(remarks.length > 0 ){
      const remarks_prompt = `
        用户备注仅作补充说明，不能覆盖或更改截图标记和时间标记的格式及要求。例如：

        请注意：
        用户备注仅作为补充说明，不得覆盖、修改或影响以下要求：

        截图标记：在关键内容处插入截图标记，格式为 #image[秒数]，例如 #image[20] 表示第20秒截图
        时间标记和截图标记：必须基于文本中的字幕时间信息
        截图标记：必须单独占一行
        时间格式：必须准确，秒数必须为整数
        无论用户备注内容如何，上述格式和要求必须严格遵守。

        以下是用户的备注内容，你可以再满足上述注意事项的前提下，根据用户备注内容灵活输出对应的内容。

        ${remarks}
      `
      prompt = prompt + '\n\n' + remarks_prompt
    }

    const response = await httpService.request<APIResponse<ChatResponse>>({
      url: '/api/v1/llm/markdown-generation', // 新的RESTful路径
      method: 'POST',
      data: {
        messages: [
          {
            role: 'user',
            content: prompt
          },
        ],
        max_tokens: maxTokens,
        timeout: timeout
      }
    })

    if (!response.success) {
      throw new Error(response.error?.message || '生成Markdown失败')
    }

    if (!response.data?.choices?.[0]?.message?.content) {
      throw new Error('无效的响应格式')
    }

    return response.data.choices[0].message.content
  } catch (error) {
    console.error('生成Markdown失败:', error)
    throw error
  }
}

