import httpService from './http'
import { API_PATHS } from '../config'
import { ChatResponse, ContentStyle } from './types'

/**
 * 根据文本生成Markdown内容
 * @param text 原始文本
 * @param style 内容风格
 * @returns 生成的Markdown内容
 */
export const generateMarkdownText = async (text: string, style: ContentStyle): Promise<string> => {
  try {
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
            content: JSON.stringify({
              style,
              text
            })
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
