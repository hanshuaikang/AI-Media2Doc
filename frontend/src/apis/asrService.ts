import httpService from './http'
import { API_PATHS } from '../config'
import { AudioTaskResponse, AudioTaskResult, TaskStatus } from './types'

/**
 * 提交音频处理任务
 * @param audioFileName 音频文件名
 * @returns 任务ID
 */
export const submitAsrTask = async (audioFileName: string): Promise<string> => {
  try {
    const response = await httpService.request<AudioTaskResponse>({
      url: API_PATHS.AUDIO_TASK,
      method: 'POST',
      headers: {
        'request-action': 'submit_asr_task',
      },
      data: {
        model: 'my-bot',
        messages: [
          {
            role: 'user',
            content: audioFileName
          }
        ]
      }
    })
    
    if (response.error) {
      throw new Error(response.error)
    }
    
    return response.metadata?.task_id || ''
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
    const response = await httpService.request<AudioTaskResponse>({
      url: API_PATHS.AUDIO_TASK,
      method: 'POST',
      headers: {
        'request-action': 'query_asr_task_status',
      },
      data: {
        model: 'my-bot',
        messages: [
          {
            role: 'user',
            content: taskId
          }
        ]
      }
    })
    
    if (response.error) {
      throw new Error(response.error)
    }
    
    return {
      text: response.metadata?.result || '',
      status: (response.metadata?.status || 'pending') as TaskStatus
    }
  } catch (error) {
    console.error('查询音频任务失败:', error)
    throw error
  }
}

/**
 * 轮询音频处理任务直到完成
 * @param taskId 任务ID
 * @param onProgress 进度回调
 * @param maxAttempts 最大尝试次数
 * @param interval 轮询间隔(ms)
 * @returns 处理结果文本
 */
export const pollAsrTask = async (
  taskId: string,
  maxAttempts = 60,
  interval = 3000
): Promise<string> => {
  let attempts = 0
  
  while (attempts < maxAttempts) {
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
  
  throw new Error('音频识别超时')
}
