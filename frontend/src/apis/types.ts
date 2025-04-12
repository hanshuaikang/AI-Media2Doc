/**
 * 通用API响应接口
 */
export interface ApiResponse<T = any> {
  error: string | null;
  data?: T;
  message?: string;
}

/**
 * Chat API响应格式
 */
export interface ChatResponse {
  id: string;
  choices: {
    message: {
      role: string;
      content: string;
    };
  }[];
  error?: string | null;
  metadata?: Record<string, any>;
}

/**
 * 聊天消息接口
 */
export interface ChatMessage {
  role: 'user' | 'assistant' | 'system';
  content: string;
}

/**
 * 音频任务响应接口
 */
export interface AudioTaskResponse {
  id: string;
  error: string | null;
  metadata: {
    task_id?: string;
    result?: string;
    status?: string;
    upload_url?: string;
  };
}

/**
 * 任务状态类型
 */
export type TaskStatus = 'pending' | 'processing' | 'finished' | 'failed';

/**
 * 音频任务结果接口
 */
export interface AudioTaskResult {
  text: string;
  status: TaskStatus;
}

/**
 * 内容风格类型
 */
export type ContentStyle = 'note' | 'summary' | 'xiaohongshu' | 'wechat' | 'mind';

/**
 * 上传链接响应接口
 */
export interface UploadUrlResponse {
  upload_url: string;
}

/**
 * 任务记录接口
 */
export interface Task {
  id?: number;
  fileName: string;
  md5: string;
  transcriptionText: string;
  markdownContent: string;
  contentStyle: ContentStyle;
  createdAt: string;
}
