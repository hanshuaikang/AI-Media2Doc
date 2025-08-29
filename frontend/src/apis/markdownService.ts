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
export const generateMarkdownText = async (text: string, contentStyle: string): Promise<string> => {
  try {
    const prompt = renderPrompt(contentStyle, text)
    const response = await httpService.request<APIResponse<ChatResponse>>({
      url: '/api/v1/llm/markdown-generation', // 新的RESTful路径
      method: 'POST',
      data: {
        messages: [
          {
            role: 'user',
            content: prompt
          }
        ]
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

