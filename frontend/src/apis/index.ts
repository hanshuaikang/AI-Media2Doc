import * as audioService from './asrService'
import * as markdownService from './markdownService'
import * as uploadService from './uploadService'
import * as chatService from './chatService'
import * as healthService from './healthService'
import * as secretsService from './secretsService' // 新增
import httpService from './http'

// 从各个服务中导出常用函数
export const { submitAsrTask, pollAsrTask: pollAudioTask, queryAsrTask } = audioService
export const { generateMarkdownText } = markdownService
export const { getAudioUploadUrl, uploadFile } = uploadService
export const { sendChatMessage } = chatService
export const { checkHealth } = healthService
export const { getSecrets } = secretsService // 新增

// 导出所有服务
export {
  audioService,
  markdownService,
  uploadService,
  chatService,
  healthService,
  secretsService, // 新增
  httpService
}

// 导出类型
export * from './types'

// 默认导出所有服务的集合
export default {
  audio: audioService,
  markdown: markdownService,
  upload: uploadService,
  chat: chatService,
  health: healthService,
  secrets: secretsService, // 新增
  http: httpService
}
