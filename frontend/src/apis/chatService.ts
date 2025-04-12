import httpService from './http'
import { API_PATHS } from '../config'
import { ChatMessage, ChatResponse } from './types'

/**
 * 发送聊天消息
 * @param messages 聊天消息列表
 * @returns 助手响应消息
 */
export const sendChatMessage = async (messages: ChatMessage[]): Promise<ChatMessage> => {
  try {
    const response = await httpService.request<ChatResponse>({
      url: API_PATHS.CHAT_COMPLETIONS,
      method: 'POST',
      data: {
        model: 'my-bot',
        messages
      }
    })
    
    if (response.error) {
      throw new Error(response.error)
    }
    
    if (!response.choices?.[0]?.message) {
      throw new Error('无效的响应格式')
    }
    
    return response.choices[0].message as ChatMessage
  } catch (error) {
    console.error('聊天请求失败:', error)
    throw error
  }
}
