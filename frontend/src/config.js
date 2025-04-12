/**
 * 项目统一配置文件
 * 从环境变量中读取配置
 */

// API服务基础URL
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8080'

// 各模块API路径
export const API_PATHS = {
    CHAT_COMPLETIONS: '/api/v3/bots/chat/completions',
    UPLOAD_URL: '/api/v3/bots/chat/completions', // 获取上传URL的API路径
    AUDIO_TASK: '/api/v3/bots/chat/completions' // 音频任务API路径
}

export default {
    API_BASE_URL,
    API_PATHS
}
