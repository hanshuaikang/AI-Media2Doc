<script setup>
import { ref, onMounted, watch } from 'vue'
import { ElButton, ElInput, ElMessage, ElAvatar } from 'element-plus'
import { Close, Monitor, User, Loading } from '@element-plus/icons-vue'
import { sendChatMessage } from '../../apis/chatService'
import MarkdownIt from 'markdown-it'

const props = defineProps({
  task: {
    type: Object,
    required: true
  },
  embedded: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close'])
const message = ref('')
const chatMessages = ref([])
const loading = ref(false)
const isThinking = ref(false) // 添加状态

const initSystemPrompt = () => {
  // 兼容新版协议：只拼接文本内容
  let textContent
  const t = props.task.transcriptionText
  if (Array.isArray(t) && t.length > 0 && typeof t[0] === 'object' && 'text' in t[0]) {
    textContent = t.map(seg => seg.text).join('\n')
  } else {
    textContent = t
  }
  const systemMessage = {
    role: 'user',
    content: `你是一个优秀的人工智能助手，现在我有一个视频生成的文字，你总是可以根据我提供的内容准确回答我的问题。你的第一句问候固定回复: 你好, 我是AI助手, 你可以针对视频内容向我提问~ \n\n${textContent}`
  }
  return systemMessage
}

// 初始化 MarkdownIt 实例
const md = new MarkdownIt()

// 将 Markdown 转换为 HTML
const renderMarkdown = (content) => {
  return md.render(content)
}

// 获取要发送的消息列表（包含历史记录）
const getMessagesToSend = () => {
  const messages = [initSystemPrompt()]

  // 获取最近5条聊天记录
  const recentMessages = chatMessages.value
    .slice(-10) // 获取最后10条（5轮对话）
    .map(msg => ({
      role: msg.role,
      content: msg.content
    }))

  return [...messages, ...recentMessages]
}

// 发送消息
const handleSend = async () => {
  if (!message.value.trim() || loading.value) return

  const userMessage = {
    role: 'user',
    content: message.value.trim()
  }

  // 添加用户消息到聊天记录
  chatMessages.value.push(userMessage)
  message.value = ''
  loading.value = true
  isThinking.value = true

  try {
    const messagesToSend = getMessagesToSend()

    const response = await sendChatMessage(messagesToSend)

    // 添加助手回复到聊天记录
    chatMessages.value.push({
      role: 'assistant',
      content: response.content
    })

  } catch (error) {
    ElMessage.error('发送消息失败：' + error.message)
  } finally {
    loading.value = false
    isThinking.value = false
  }
}

// init chant
const initChat = async () => {
  try {
    chatMessages.value = []
    loading.value = true
    const response = await sendChatMessage([initSystemPrompt()])
    chatMessages.value.push({
      role: 'assistant',
      content: response.content
    })
  } catch (error) {
    ElMessage.error('初始化聊天失败：' + error.message)
  } finally {
    loading.value = false
  }
}

watch(() => props.task.id, (newId, oldId) => {
  if (newId !== oldId) {
    initChat()
  }
}, { immediate: false })

// 初始化欢迎消息
onMounted(() => {
  initChat()
})
</script>

<template>
  <div class="chat-panel" :class="{ 'embedded-mode': embedded }">
    <div class="chat-header">
      <div class="header-info">
        <div class="header-icon">
          <el-avatar :src="'/src/assets/system.jpeg'" :size="40" />
        </div>
        <div class="header-title">
          <h3>AI 智能助手</h3>
          <p>基于视频内容，向我提问吧</p>
        </div>
      </div>
      <el-button v-if="!embedded" class="close-btn" @click="$emit('close')">
        <el-icon>
          <Close />
        </el-icon>
      </el-button>
    </div>

    <div class="chat-content">
      <div v-for="(msg, index) in chatMessages" :key="index" class="message-wrapper" :class="msg.role">
        <div class="avatar-container">
          <el-avatar :size="40" :src="msg.role === 'assistant' ? '/src/assets/system.jpeg' : '/src/assets/user.jpeg'"
            :icon="msg.role === 'assistant' ? '' : User" :class="msg.role" />
        </div>
        <div class="message-bubble">
          <div class="message-content" :class="msg.role">
            <!-- 对助手回复使用 Markdown 渲染 -->
            <div v-if="msg.role === 'assistant'" v-html="renderMarkdown(msg.content)" class="markdown-content"></div>
            <!-- 用户消息仍然显示为纯文本 -->
            <template v-else>{{ msg.content }}</template>
          </div>
          <div class="message-time" v-if="msg.role === 'assistant'">AI 助手</div>
          <div class="message-time" v-else>我</div>
        </div>
      </div>

      <div v-if="isThinking" class="message-wrapper assistant thinking">
        <div class="avatar-container">
          <el-avatar :size="40" :src="'/src/assets/logo.jpeg'" class="assistant" />
        </div>
        <div class="message-bubble">
          <div class="message-content assistant thinking-content">
            <div class="thinking-dots">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
          <div class="message-time">AI 思考中</div>
        </div>
      </div>
    </div>

    <div class="chat-input">
      <div class="input-container">
        <el-input v-model="message" type="textarea" :rows="3" :placeholder="loading ? '请等待AI回复...' : '输入您的问题...'"
          @keyup.enter.exact="handleSend" :disabled="loading" resize="none" />
        <div class="send-button-wrapper">
          <el-button class="send-button" type="primary" @click="handleSend" :disabled="!message.trim() || loading"
            :loading="loading" round>
            发送
          </el-button>
        </div>
      </div>
      <div class="input-tips">
        提示：按Enter键发送，Shift+Enter换行
      </div>
    </div>
  </div>
</template>

<style scoped>
.chat-panel {
  width: 400px;
  height: 100vh;
  position: fixed;
  right: 0;
  top: 0;
  background: #fff;
  box-shadow: -5px 0 25px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  z-index: 2000;
  animation: slideIn 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  overflow: hidden;
}

.chat-panel.embedded-mode {
  position: relative;
  width: 100%;
  height: 100%;
  box-shadow: none;
  animation: none;
  border-radius: 12px;
  overflow: hidden;
}

.chat-header {
  padding: 16px 20px;
  border-bottom: 1px solid #ebeef5;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: linear-gradient(135deg, #ffffff, #f8fafd);
}

.header-info {
  display: flex;
  align-items: center;
  gap: 12px;
  /* 减小间距，确保无多余空白 */
}

.header-icon {
  width: 40px;
  height: 40px;
  min-width: 40px;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 10px rgba(64, 158, 255, 0.25);
}

.header-icon :deep(.el-avatar) {
  width: 100%;
  height: 100%;
}

.header-title {
  display: flex;
  flex-direction: column;
  flex: 1;
  /* 让标题区域占据剩余空间 */
  text-align: left;
  /* 确保文本左对齐 */
}

.header-title h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  line-height: 1.2;
  text-align: left;
  /* 明确设置左对齐 */
}

.header-title p {
  margin: 0;
  font-size: 12px;
  color: #909399;
  text-align: left;
  /* 明确设置左对齐 */
}

.close-btn {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  border: none;
  background: rgba(0, 0, 0, 0.05);
  color: #606266;
  transition: all 0.2s;
}

.close-btn:hover {
  background: rgba(0, 0, 0, 0.1);
  transform: rotate(90deg);
}

.chat-content {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  background-color: #f9fafc;
}

.message-wrapper {
  display: flex;
  gap: 12px;
  max-width: 100%;
}

.message-wrapper.user {
  flex-direction: row-reverse;
}

.avatar-container {
  margin-top: 4px;
}

.avatar-container :deep(.el-avatar) {
  border: 2px solid #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.avatar-container :deep(.el-avatar.assistant) {
  background: linear-gradient(135deg, #409EFF, #64b5f6);
  color: white;
}

.avatar-container :deep(.el-avatar.user) {
  background: linear-gradient(135deg, #67c23a, #95d475);
  color: white;
}

.message-bubble {
  max-width: calc(100% - 60px);
  display: flex;
  flex-direction: column;
}

.message-content {
  padding: 8px 12px;
  border-radius: 18px;
  font-size: 14px;
  line-height: 1;
  position: relative;
  white-space: pre-wrap;
  word-break: break-word;
  text-align: left;
}

.message-content.assistant {
  background-color: #fff;
  color: #303133;
  border: 1px solid #ebeef5;
  border-top-left-radius: 4px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.03);
}

.message-content.user {
  background: linear-gradient(135deg, #409EFF, #64b5f6);
  color: white;
  border-top-right-radius: 4px;
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.2);
}

.message-time {
  margin-top: 4px;
  font-size: 12px;
  color: #909399;
  padding-left: 8px;
}

.message-wrapper.user .message-time {
  text-align: right;
  padding-right: 8px;
}

.message-content :deep(p),
.message-content :deep(h1),
.message-content :deep(h2),
.message-content :deep(h3),
.message-content :deep(h4),
.message-content :deep(ul),
.message-content :deep(ol),
.message-content :deep(li) {
  margin-top: 0.3em;
  margin-bottom: 0.3em;
}

/* 确保列表项正确对齐 */
.message-content :deep(ul),
.message-content :deep(ol) {
  padding-left: 1.5em;
}

.chat-input {
  padding: 16px;
  border-top: 1px solid #ebeef5;
  background: #fff;
}

.input-container {
  position: relative;
  margin-bottom: 8px;
}

.input-container :deep(.el-textarea__inner) {
  padding: 12px 16px;
  border-radius: 18px;
  resize: none;
  transition: all 0.3s;
  font-size: 14px;
  line-height: 1.6;
  border: 1px solid #dcdfe6;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
}

.input-container :deep(.el-textarea__inner:focus) {
  border-color: #409EFF;
  box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.2);
}

.send-button-wrapper {
  position: absolute;
  right: 8px;
  bottom: 8px;
}

.send-button {
  height: 36px;
  padding: 0 16px;
  font-weight: 500;
  transition: all 0.3s;
}

.input-tips {
  font-size: 12px;
  color: #909399;
  text-align: center;
}

.thinking-content {
  min-height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 60px;
}

.thinking-dots {
  display: flex;
  align-items: center;
  gap: 4px;
}

.thinking-dots span {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #409EFF;
  opacity: 0.7;
  animation: bounce 1.4s infinite ease-in-out both;
}

.thinking-dots span:nth-child(1) {
  animation-delay: -0.32s;
}

.thinking-dots span:nth-child(2) {
  animation-delay: -0.16s;
}

@keyframes bounce {

  0%,
  80%,
  100% {
    transform: scale(0);
  }

  40% {
    transform: scale(1);
  }
}

@keyframes slideIn {
  0% {
    transform: translateX(100%);
    opacity: 0;
  }

  100% {
    transform: translateX(0);
    opacity: 1;
  }
}

/* 响应式布局 */
@media screen and (max-width: 768px) {
  .chat-panel {
    width: 100%;
  }
}

/* 滚动条样式 */
.chat-content::-webkit-scrollbar {
  width: 5px;
}

.chat-content::-webkit-scrollbar-thumb {
  background: #dcdfe6;
  border-radius: 10px;
}

.chat-content::-webkit-scrollbar-track {
  background: transparent;
}

/* Markdown 样式 */
.markdown-content :deep(h1),
.markdown-content :deep(h2),
.markdown-content :deep(h3),
.markdown-content :deep(h4),
.markdown-content :deep(h5),
.markdown-content :deep(h6) {
  margin: 8px 0 4px 0;
  font-weight: 600;
  line-height: 1.2;
}

.markdown-content :deep(p) {
  margin: 4px 0;
  line-height: 1.4;
}

.markdown-content :deep(ul),
.markdown-content :deep(ol) {
  padding-left: 16px;
  margin: 4px 0;
}

.markdown-content :deep(li) {
  margin: 2px 0;
  line-height: 1.4;
}

.markdown-content :deep(code) {
  background-color: #f5f5f5;
  padding: 2px 4px;
  border-radius: 3px;
  font-family: monospace;
  font-size: 13px;
  color: #e74c3c;
}

.markdown-content :deep(pre) {
  background-color: #f8f9fa;
  padding: 12px;
  border-radius: 6px;
  overflow-x: auto;
  margin: 8px 0;
}

.markdown-content :deep(pre code) {
  background: none;
  padding: 0;
  color: #333;
}

.markdown-content :deep(blockquote) {
  border-left: 3px solid #409EFF;
  padding-left: 12px;
  color: #666;
  margin: 8px 0;
  font-style: italic;
}

.markdown-content :deep(a) {
  color: #409EFF;
  text-decoration: none;
}

.markdown-content :deep(a:hover) {
  text-decoration: underline;
}

.markdown-content :deep(strong) {
  font-weight: 600;
  color: #303133;
}

.markdown-content :deep(em) {
  font-style: italic;
  color: #606266;
}
</style>
