import httpService from './http'
import { API_PATHS } from '../config'
import { ChatResponse, ContentStyle } from './types'
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
    const response = await httpService.request<ChatResponse>({
      url: API_PATHS.CHAT_COMPLETIONS,
      method: 'POST',
      headers: {
        'request-action': 'generate_markdown_text',
      },
      data: {
        model: 'my-bot',
        messages: [
          {
            role: 'user',
            content: prompt
          }
        ]
      }
    })

    if (response.error) {
      throw new Error(response.error)
    }

    return response.choices[0]?.message?.content || ''
  } catch (error) {
    console.error('生成Markdown失败:', error)
    throw error
  }
}
