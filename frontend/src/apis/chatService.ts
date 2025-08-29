import httpService from './http'
import { ChatMessage, APIResponse, ChatResponse } from './types'

/**
 * 发送聊天消息
 * @param messages 聊天消息列表
 * @returns 助手响应消息
 */
export const sendChatMessage = async (messages: ChatMessage[]): Promise<ChatMessage> => {
  try {
    const response = await httpService.request<APIResponse<ChatResponse>>({
      url: '/api/v1/llm/completions', // 新的RESTful路径
      method: 'POST',
      data: {
        messages
      }
    })
    
    if (!response.success) {
      throw new Error(response.error?.message || '聊天请求失败')
    }
    
    if (!response.data?.choices?.[0]?.message) {
      throw new Error('无效的响应格式')
    }
    
    return response.data.choices[0].message as ChatMessage
  } catch (error) {
    console.error('聊天请求失败:', error)
    throw error
  }
}