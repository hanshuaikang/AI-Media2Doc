<script setup>
import { ElIcon, ElButton, ElMessage } from 'element-plus'
import MarkdownIt from 'markdown-it'
import { onMounted, ref, watchEffect, nextTick, onBeforeUnmount } from 'vue'
import MindMap from 'simple-mind-map'
import { Headset, Document, Download, CopyDocument, FullScreen, ScaleToOriginal } from '@element-plus/icons-vue'
const md = new MarkdownIt()
const mindMapInstance = ref(null)

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

const isFullscreen = ref(false)

const toggleFullscreen = async () => {
  try {
    if (!isFullscreen.value) {
      isFullscreen.value = true
      const container = document.getElementById('mindMapContainer')
      if (container) {
        await container.requestFullscreen()
        nextTick(() => {
          if (mindMapInstance.value) {
            mindMapInstance.value.resize(window.innerWidth - 48, window.innerHeight - 48)
            mindMapInstance.value.render()
            mindMapInstance.value.view.fit()
          }
        })
      }
    } else {
      // 退出全屏
      if (document.fullscreenElement) {
        await document.exitFullscreen()
        isFullscreen.value = false
        // 恢复原始大小
        nextTick(() => {
          const container = document.getElementById('mindMapContainer')
          if (container && mindMapInstance.value) {
            mindMapInstance.value.resize(container.clientWidth, container.clientHeight)
            mindMapInstance.value.render()
            mindMapInstance.value.view.fit()
          }
        })
      }
    }
  } catch (error) {
    console.error('全屏切换失败:', error)
    ElMessage.error('全屏切换失败')
  }
}

// 修改全屏变化监听
const handleFullscreenChange = () => {
  const isFullscreenNow = !!document.fullscreenElement
  if (isFullscreen.value !== isFullscreenNow) {
    isFullscreen.value = isFullscreenNow
    if (!isFullscreenNow && mindMapInstance.value) {
      // 退出全屏时调整大小
      nextTick(() => {
        const container = document.getElementById('mindMapContainer')
        if (container) {
          mindMapInstance.value.resize(container.clientWidth, container.clientHeight)
          mindMapInstance.value.render()
          mindMapInstance.value.view.fit()
        }
      })
    }
  }
}

onMounted(() => {
  document.addEventListener('fullscreenchange', handleFullscreenChange)
})

onBeforeUnmount(() => {
  document.removeEventListener('fullscreenchange', handleFullscreenChange)
})

// 初始化思维导图
const initMindMap = (data) => {
  try {
    if (mindMapInstance.value) {
      mindMapInstance.value.destroy()
    }
    const container = document.getElementById('mindMapContainer')
    if (container) {
      mindMapInstance.value = new MindMap({
        el: container,
        data: JSON.parse(data),
        width: container.clientWidth,
        height: container.clientHeight
      })
    }
  } catch (error) {
    console.error('初始化思维导图失败:', error)
    ElMessage.error('思维导图渲染失败')
  }
}

// 监听 markdownContent 变化
watchEffect(() => {
  if (props.contentStyle === 'mind' && props.markdownContent) {
    nextTick(() => {
      initMindMap(props.markdownContent)
    })
  }
})

// 在组件卸载时销毁实例
onBeforeUnmount(() => {
  if (mindMapInstance.value) {
    mindMapInstance.value.destroy()
  }
})

// 复制文本到剪贴板
const copyToClipboard = async (text, type) => {
  try {
    await navigator.clipboard.writeText(text);
    ElMessage.success(`${type}已复制到剪贴板`);
  } catch (err) {
    ElMessage.error('复制失败，请手动复制');
    console.error('复制失败:', err);
  }
}

// 下载思维导图 JSON 文件
const downloadMindMapJson = (jsonContent) => {
  try {
    // 创建 Blob 对象
    const blob = new Blob([jsonContent], { type: 'application/json' });
    const url = URL.createObjectURL(blob);

    // 创建下载链接
    const a = document.createElement('a');
    a.href = url;
    a.download = `mindmap_${new Date().getTime()}.json`;
    document.body.appendChild(a);
    a.click();

    // 清理
    setTimeout(() => {
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }, 100);

    ElMessage.success('思维导图 JSON 文件下载成功');
  } catch (err) {
    ElMessage.error('下载失败');
    console.error('下载思维导图 JSON 失败:', err);
  }
}
</script>

<template>
  <div class="results-container">
    <!-- 纵向布局：音频、文本和图文垂直排列 -->
    <!-- 音频结果卡片 -->
    <div v-if="audioExtracted" class="result-card audio-result">
      <div class="card-header">
        <div class="header-left">
          <el-icon>
            <Headset />
          </el-icon>
          <span>音频下载</span>
        </div>
        <el-button class="download-btn" type="primary" circle size="small" @click="$emit('download-audio')"
          :icon="Download" />
      </div>
      <div class="card-content">
        <audio controls :src="audioUrl" class="custom-audio-player" />
      </div>
    </div>

    <!-- 文本结果卡片 -->
    <div v-if="textTranscribed" class="result-card text-result">
      <div class="card-header">
        <div class="header-left">
          <el-icon>
            <Document />
          </el-icon>
          <span>原始文本</span>
        </div>
        <div class="action-buttons">
          <el-button class="action-btn" type="primary" circle size="small"
            @click="copyToClipboard(transcriptionText, '文本')" :icon="CopyDocument" />
          <el-button class="action-btn" type="primary" circle size="small" @click="$emit('download-text')"
            :icon="Download" />
        </div>
      </div>
      <div class="card-content">
        <div class="text-content">{{ transcriptionText }}</div>
      </div>
    </div>

    <!-- Markdown 结果卡片 -->
    <div v-if="markdownContent" class="result-card markdown-result">
      <div class="card-header">
        <div class="header-left">
          <el-icon>
            <Document />
          </el-icon>
          <span>{{ contentStyle === 'mind' ? '思维导图' : '图文内容' }}</span>
        </div>
        <div class="action-buttons">
          <template v-if="contentStyle === 'mind'">
            <el-button class="action-btn" type="primary" circle size="small" @click="toggleFullscreen"
              :icon="isFullscreen ? ScaleToOriginal : FullScreen" />
          </template>
          <el-button class="action-btn" type="primary" circle size="small"
            @click="copyToClipboard(markdownContent, 'Markdown')" :icon="CopyDocument" />
          <el-button class="action-btn" type="primary" circle size="small"
            @click="contentStyle === 'mind' ? downloadMindMapJson(markdownContent) : $emit('download-markdown')"
            :icon="Download" />
        </div>
      </div>
      <div class="card-content">
        <template v-if="contentStyle === 'mind'">
          <div id="mindMapContainer" class="mind-map-container"></div>
        </template>
        <template v-else>
          <div class="markdown-content" v-html="md.render(markdownContent)"></div>
        </template>
      </div>
    </div>
  </div>
</template>

<style scoped>
.results-container {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 1rem;
  background: #ffffff;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  box-sizing: border-box;
  margin: 0;
}

.result-card {
  background: white;
  border-radius: 8px;
  padding: 1rem;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  border: 1px solid #e5e7eb;
  transition: box-shadow 0.2s ease;
}

.result-card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.07);
}

.card-header {
  display: flex;
  align-items: center;
  margin-bottom: 0.8rem;
  font-size: 1rem;
  font-weight: 600;
  color: #374151;
  position: relative;
  justify-content: space-between;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.card-header .el-icon {
  font-size: 1.1rem;
  color: #6b7280;
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
}

.download-btn {}

.custom-audio-player {
  width: 100%;
  margin-top: 0.5rem;
  border-radius: 6px;
}

.text-content {
  white-space: pre-wrap;
  line-height: 1.6;
  font-size: 13px;
  color: #4a5568;
  padding: 12px 16px;
  border: 1px solid #edf2f7;
  border-radius: 8px;
  background: #f8f9fa;
  max-height: 150px;
  overflow-y: auto;
  text-align: left;
  font-family: inherit;
}

.markdown-content {
  line-height: 1.6;
  font-size: 13px;
  color: #303133;
  padding: 12px 16px;
  border: 1px solid #edf2f7;
  border-radius: 8px;
  background: #f8f9fa;
  max-height: 400px;
  overflow-y: auto;
  text-align: left;
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

.markdown-content::-webkit-scrollbar,
.text-content::-webkit-scrollbar {
  width: 5px;
}

.markdown-content::-webkit-scrollbar-thumb,
.text-content::-webkit-scrollbar-thumb {
  background: #dcdfe6;
  border-radius: 10px;
}

.markdown-content::-webkit-scrollbar-track,
.text-content::-webkit-scrollbar-track {
  background: transparent;
}

@media screen and (max-width: 768px) {
  .results-container {
    padding: 1rem;
    gap: 1rem;
  }

  .result-card {
    padding: 1rem;
  }

  .card-header {
    font-size: 0.95rem;
  }

  .text-content {
    font-size: 12px;
    max-height: 120px;
  }

  .markdown-content {
    font-size: 12px;
    max-height: 300px;
  }
}

.mind-map-container {
  width: 100%;
  height: 500px;
  background: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
  position: relative;
}

.mind-map-container:fullscreen {
  padding: 24px;
  background: #ffffff;
  width: 100vw !important;
  height: 100vh !important;
  display: flex;
  align-items: center;
  justify-content: center;
}

:deep(.mind-map-container svg) {
  width: 100%;
  height: 100%;
}

.mind-map-container * {
  margin: 0;
  padding: 0;
}
</style>
