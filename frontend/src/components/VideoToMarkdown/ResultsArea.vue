<script setup>
import { ElIcon, ElButton, ElMessage } from 'element-plus'
import MarkdownIt from 'markdown-it'
import { ref, nextTick, onMounted, onBeforeUnmount, watchEffect } from 'vue'
import { Headset, Document, Download, CopyDocument } from '@element-plus/icons-vue'

const md = new MarkdownIt()

const props = defineProps({
  audioExtracted: Boolean,
  textTranscribed: Boolean,
  audioUrl: String,
  audioFilename: String,
  transcriptionText: String,
  markdownContent: String,
  contentStyle: String
})

const emit = defineEmits(['download-audio', 'download-text', 'download-markdown'])

const copyToClipboard = async (text, type) => {
  try {
    await navigator.clipboard.writeText(text)
    ElMessage.success(`${type}已复制到剪贴板`)
  } catch (err) {
    ElMessage.error('复制失败，请手动复制')
  }
}
</script>

<template>
  <div class="results-2col-container">
    <!-- 左侧：Markdown 图文内容 -->
    <div class="left-markdown-panel">
      <div class="markdown-header">
        <el-icon>
          <Document />
        </el-icon>
        <span>{{ contentStyle === 'mind' ? '思维导图' : '图文内容' }}</span>
        <div class="markdown-actions">
          <el-button class="action-btn" type="primary" circle size="small"
            @click="copyToClipboard(markdownContent, 'Markdown')" :icon="CopyDocument" />
          <el-button class="action-btn" type="primary" circle size="small" @click="$emit('download-markdown')"
            :icon="Download" />
        </div>
      </div>
      <div class="markdown-content" v-html="md.render(markdownContent)"></div>
    </div>
    <!-- 右侧：音频播放器 + 原始文本 -->
    <div class="right-info-panel">
      <div class="audio-card">
        <div class="audio-header">
          <el-icon>
            <Headset />
          </el-icon>
          <span>音频播放</span>
          <el-button class="action-btn" type="primary" circle size="small" @click="$emit('download-audio')"
            :icon="Download" />
        </div>
        <audio controls :src="audioUrl" class="custom-audio-player" />
      </div>
      <div class="text-card">
        <div class="text-header">
          <el-icon>
            <Document />
          </el-icon>
          <span>原始文本</span>
          <div class="text-actions">
            <el-button class="action-btn" type="primary" circle size="small"
              @click="copyToClipboard(transcriptionText, '文本')" :icon="CopyDocument" />
            <el-button class="action-btn" type="primary" circle size="small" @click="$emit('download-text')"
              :icon="Download" />
          </div>
        </div>
        <div class="text-content">{{ transcriptionText }}</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.results-2col-container {
  display: flex;
  flex-direction: row;
  gap: 32px;
  width: 100%;
  min-height: 520px;
  box-sizing: border-box;
  margin: 0 auto;
  align-items: flex-start;
}

.left-markdown-panel {
  flex: 7;
  background: #fff;
  border-radius: 14px;
  box-shadow: 0 2px 12px 0 rgba(60, 80, 120, 0.07);
  border: 1.5px solid #f2f3f5;
  padding: 28px 32px 32px 32px;
  min-width: 0;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.markdown-header {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 1.13rem;
  font-weight: 700;
  color: #23272f;
  margin-bottom: 18px;
  border-bottom: 1px solid #f3f4f6;
  padding-bottom: 10px;
  justify-content: space-between;
}

.markdown-header>span {
  flex: 1;
  margin-left: 8px;
}

.markdown-actions {
  display: flex;
  gap: 0.5rem;
}

.markdown-content {
  flex: 1;
  line-height: 1.7;
  font-size: 15px;
  color: #303133;
  padding: 12px 0 0 0;
  background: #fff;
  border-radius: 8px;
  overflow-y: auto;
  text-align: left;
  min-height: 320px;
  max-height: 700px;
}

.markdown-content :deep(*) {
  text-align: left !important;
}

.markdown-content :deep(ul),
.markdown-content :deep(ol) {
  padding-left: 2em;
  margin: 0.5em 0;
}

.markdown-content :deep(p),
.markdown-content :deep(h1),
.markdown-content :deep(h2),
.markdown-content :deep(h3),
.markdown-content :deep(h4) {
  margin: 0.5em 0;
}

.right-info-panel {
  flex: 3;
  display: flex;
  flex-direction: column;
  gap: 24px;
  min-width: 0;
}

.audio-card,
.text-card {
  background: #f8f9fa;
  border-radius: 12px;
  box-shadow: 0 1px 6px 0 rgba(60, 80, 120, 0.06);
  border: 1.5px solid #f2f3f5;
  padding: 22px 20px 18px 20px;
  display: flex;
  flex-direction: column;
  margin-bottom: 0;
}

.audio-header,
.text-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 1.05rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 12px;
  justify-content: space-between;
}

.audio-header>span,
.text-header>span {
  flex: 1;
  margin-left: 6px;
}

.text-actions {
  display: flex;
  gap: 0.5rem;
}

.custom-audio-player {
  width: 100%;
  margin-top: 0.5rem;
  border-radius: 6px;
  background: #fff;
}

.text-content {
  white-space: pre-wrap;
  line-height: 1.6;
  font-size: 13px;
  color: #4a5568;
  padding: 12px 10px;
  border: 1px solid #edf2f7;
  border-radius: 8px;
  background: #fff;
  max-height: 180px;
  overflow-y: auto;
  text-align: left;
  font-family: inherit;
}

@media screen and (max-width: 1100px) {
  .results-2col-container {
    flex-direction: column;
    gap: 18px;
  }

  .left-markdown-panel,
  .right-info-panel {
    width: 100%;
    min-width: 0;
    max-width: 100vw;
    padding: 18px 8px 18px 8px;
  }

  .left-markdown-panel {
    padding: 18px 8px 18px 8px;
  }
}

@media screen and (max-width: 768px) {
  .results-2col-container {
    flex-direction: column;
    gap: 12px;
    min-height: auto;
  }

  .left-markdown-panel,
  .right-info-panel {
    padding: 10px 2px 10px 2px;
    border-radius: 8px;
  }

  .markdown-header {
    font-size: 1rem;
    padding-bottom: 6px;
    margin-bottom: 10px;
  }

  .audio-card,
  .text-card {
    padding: 12px 6px 10px 6px;
    border-radius: 8px;
  }

  .text-content {
    font-size: 12px;
    max-height: 120px;
    padding: 8px 4px;
  }
}
</style>
