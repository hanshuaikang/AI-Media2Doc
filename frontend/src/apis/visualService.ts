import httpService from './http'
import { APIResponse, VisualAnalysisResponse } from './types'

/**
 * 使用 TwelveLabs Pegasus 对视频画面做视觉理解 (可选能力)
 *
 * 现有流程只用 ASR 字幕生成文档, 看不到画面里的演示、图表、屏幕文字等信息。
 * 该接口对已上传的视频调用 Pegasus, 返回一段画面描述文本, 可与字幕一起送入大模型,
 * 让生成的文档同时反映"听到的"和"看到的"。
 *
 * 该能力默认关闭: 后端未配置 TWELVELABS_API_KEY 时会返回错误, 调用方可据此跳过视觉增强。
 *
 * @param filename 已上传到对象存储的视频文件名
 * @param prompt 可选, 自定义视觉分析提示词
 * @param maxTokens 可选, Pegasus 1.5 要求介于 512 与 98304 之间, 默认 2048
 * @returns 画面描述文本
 */
export const analyzeVideoVisual = async (
  filename: string,
  prompt?: string,
  maxTokens = 2048
): Promise<string> => {
  try {
    const response = await httpService.request<APIResponse<VisualAnalysisResponse>>({
      url: '/api/v1/video/visual-analysis',
      method: 'POST',
      data: {
        filename,
        prompt,
        max_tokens: maxTokens
      }
    })

    if (!response.success) {
      throw new Error(response.error?.message || '视觉分析失败')
    }

    return response.data?.visual_description || ''
  } catch (error) {
    console.error('视觉分析失败:', error)
    throw error
  }
}
