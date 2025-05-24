import * as audioService from './asrService'
import * as markdownService from './markdownService'
import * as uploadService from './uploadService'
import * as chatService from './chatService'
import httpService from './http'

// 从各个服务中导出常用函数
export const { submitAudioTask, pollAsrTask: pollAudioTask, queryAudioTask } = audioService
export const { generateMarkdownText } = markdownService
export const { getAudioUploadUrl, uploadFile } = uploadService
export const { sendChatMessage } = chatService

// 导出所有服务
export {
  audioService,
  markdownService,
  uploadService,
  chatService,
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
  http: httpService
}
