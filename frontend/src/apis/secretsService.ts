import httpService from './http'
import type { SecretsResponse, SecretsData } from './types'

/**
 * 获取后端脱敏环境变量
 */
export const getSecrets = async (): Promise<SecretsData> => {
  const resp = await httpService.request<SecretsResponse>({
    url: '/api/v1/secrets',
    method: 'GET'
  })
  if (!resp.success || !resp.data) {
    throw new Error(resp?.message || '获取环境变量失败')
  }
  return resp.data
}
