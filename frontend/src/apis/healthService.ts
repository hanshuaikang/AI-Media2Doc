import httpService from './http'
import { APIResponse, HealthCheckResponse } from './types'

/**
 * 检查服务健康状态
 * @returns 服务健康状态信息
 */
export const checkHealth = async (): Promise<HealthCheckResponse> => {
  try {
    const response = await httpService.request<APIResponse<HealthCheckResponse>>({
      url: '/health',
      method: 'GET'
    })
    
    if (!response.success) {
      throw new Error(response.error?.message || '健康检查失败')
    }
    
    if (!response.data) {
      throw new Error('无效的健康检查响应')
    }
    
    return response.data
  } catch (error) {
    console.error('健康检查失败:', error)
    throw error
  }
}
