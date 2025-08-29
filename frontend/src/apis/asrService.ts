import httpService from './http'
import { APIResponse, SubmitAsrTaskResponse, QueryASRTaskResponse, AudioTaskResult, TaskStatus } from './types'

/**
 * 提交音频处理任务
 * @param audioFileName 音频文件名
 * @returns 任务ID
 */
export const submitAsrTask = async (audioFileName: string): Promise<string> => {
  try {
    const response = await httpService.request<APIResponse<SubmitAsrTaskResponse>>({
      url: '/api/v1/audio/transcription-tasks',
      method: 'POST',
      data: {
        filename: audioFileName
      }
    })
    
    if (!response.success) {
      throw new Error(response.error?.message || '提交音频任务失败')
    }
    
    return response.data?.task_id || ''
  } catch (error) {
    console.error('提交音频任务失败:', error)
    throw error
  }
}

/**
 * 查询音频处理任务状态
 * @param taskId 任务ID
 * @returns 任务结果和状态
 */
export const queryAsrTask = async (taskId: string): Promise<AudioTaskResult> => {
  try {
    const response = await httpService.request<APIResponse<QueryASRTaskResponse>>({
      url: `/api/v1/audio/transcription-tasks/${taskId}`,
      method: 'GET'
    })
    
    if (!response.success) {
      throw new Error(response.error?.message || '查询音频任务失败')
    }

    const status = response.data?.status as TaskStatus || 'running'
    let text: Array<Record<string, any>> | null = null    
    // 如果任务完成且有结果，拼接所有文本
    if (status === 'finished' && response.data?.result) {
      text = response.data.result
    }
    
    return {
      text,
      status
    }
  } catch (error) {
    console.error('查询音频任务失败:', error)
    throw error
  }
}

/**
 * 获取本地存储的最大轮询次数
 * @returns 最大轮询次数
 */
const getMaxPollingAttempts = (): number => {
  try {
    const v = localStorage.getItem('maxPollingAttempts')
    if (v) {
      const n = parseInt(v)
      if (!isNaN(n) && n >= 10) return n
    }
  } catch { }
  return 60 // 默认值
}

/**
 * 轮询音频处理任务直到完成
 * @param taskId 任务ID
 * @param onProgress 进度回调
 * @param maxAttempts 最大尝试次数，如果不传则从localStorage读取
 * @param interval 轮询间隔(ms)
 * @returns 处理结果文本
 */
export const pollAsrTask = async (
  taskId: string,
  maxAttempts?: number,
  interval = 3000
): Promise<string> => {
  const actualMaxAttempts = maxAttempts || getMaxPollingAttempts()
  let attempts = 0
  
  console.log(`开始轮询任务 ${taskId}，最大尝试次数: ${actualMaxAttempts}`)
  
  while (attempts < actualMaxAttempts) {
    const result = await queryAsrTask(taskId)
    console.log('Polling result:', result)
    
    if (result.status === 'finished') {
      return result.text
    }
    
    if (result.status === 'failed') {
      throw new Error('音频识别失败')
    }
    
    await new Promise(resolve => setTimeout(resolve, interval))
    attempts++
  }
  
  throw new Error(`音频识别超时，已尝试 ${actualMaxAttempts} 次`)
}
