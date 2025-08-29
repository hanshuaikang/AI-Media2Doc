import httpService from './http'
import { APIResponse, UploadUrlResponse } from './types'

/**
 * 获取音频文件上传链接
 * @param filename 音频文件名
 * @returns 上传URL
 */
export const getAudioUploadUrl = async (filename: string): Promise<string> => {
  try {
    const response = await httpService.request<APIResponse<UploadUrlResponse>>({
      url: '/api/v1/files/upload-urls', // 新的RESTful路径
      method: 'POST',
      data: {
        filename
      }
    })
    
    if (!response.success || !response.data?.upload_url) {
      throw new Error(response.error?.message || '获取上传链接失败')
    }
    
    return response.data.upload_url
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

