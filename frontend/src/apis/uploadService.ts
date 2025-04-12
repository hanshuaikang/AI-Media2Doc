import httpService from './http'
import { API_PATHS } from '../config'
import { AudioTaskResponse } from './types'

/**
 * 获取音频文件上传链接
 * @param filename 音频文件名
 * @returns 上传URL
 */
export const getAudioUploadUrl = async (filename: string): Promise<string> => {
  try {
    const response = await httpService.request<AudioTaskResponse>({
      url: API_PATHS.UPLOAD_URL,
      method: 'POST',
      headers: {
        'request-action': 'generate_upload_url'
      },
      data: {
        model: 'my-bot',
        messages: [
          {
            role: 'user',
            content: filename
          }
        ]
      }
    })
    
    if (response.error) {
      throw new Error(response.error)
    }
    
    if (!response.metadata?.upload_url) {
      throw new Error('响应中未找到上传链接')
    }
    
    return response.metadata.upload_url
  } catch (error) {
    console.error('获取上传链接失败:', error)
    throw error
  }
}

/**
 * 上传文件到预签名URL
 * @param uploadUrl 上传链接
 * @param file 文件对象
 * @param onProgress 进度回调
 * @returns 上传结果
 */
export const uploadFile = async (
  uploadUrl: string, 
  file: Blob,
  onProgress?: (percent: number) => void
): Promise<{ success: boolean }> => {
  try {
    console.log('开始上传文件到:', uploadUrl)
    
    const result = await httpService.uploadFile(uploadUrl, file, onProgress)
    return { success: true }
  } catch (error) {
    console.error('文件上传失败:', error)
    throw error
  }
}
