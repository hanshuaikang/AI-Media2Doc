<script setup>
import { ref, onMounted, computed, onBeforeUnmount, watch } from 'vue'
import { ElSkeleton, ElTag, ElButton, ElIcon, ElEmpty, ElMessage } from 'element-plus'
import { ArrowLeft, Document, Timer, VideoCamera, Headset, Reading, CopyDocument, Download } from '@element-plus/icons-vue'
import MarkdownIt from 'markdown-it'
import { nextTick } from 'vue'
import MindMap from 'simple-mind-map'
import ChatPanel from './ChatPanel.vue'

const props = defineProps({
    task: {
        type: Object,
        required: true
    }
})

const emit = defineEmits(['back'])

const md = new MarkdownIt()

const mindMapInstance = ref(null)

// 判断内容是否为JSON格式
const isJsonString = (str) => {
    if (typeof str !== 'string') return false;
    try {
        const result = JSON.parse(str);
        return typeof result === 'object' && result !== null;
    } catch (e) {
        return false;
    }
}

// 将思维导图JSON格式转换为MindMap所需格式
const convertToMindMapFormat = (jsonData) => {
    try {
        // 已经是对象就直接使用，否则尝试解析JSON字符串
        const data = typeof jsonData === 'object' ? jsonData : JSON.parse(jsonData);

        // 确保数据格式符合simple-mind-map要求
        if (data.data && (data.data.text || data.data.title)) {
            return data;
        }
        // 否则包装成标准格式
        return {
            data: {
                text: data.text || data.title || "思维导图",
            },
            children: data.children || []
        };
    } catch (error) {
        console.error('转换思维导图数据格式失败:', error);
        return {
            data: {
                text: "解析失败的思维导图",
            },
            children: []
        };
    }
}



// 判断内容是否应该显示为思维导图
const isContentMindMap = computed(() => {
    return isJsonString(props.task.markdownContent)
})

// 在组件挂载后初始化思维导图
onMounted(async () => {
    if (isContentMindMap.value) {
        await nextTick()
        initMindMap()
    }
})

// 监听任务变化
watch(() => props.task, (newTask, oldTask) => {
    // 如果是思维导图类型，重新初始化
    if (isContentMindMap.value) {
        // 需要先销毁旧实例，再初始化新的
        if (mindMapInstance.value) {
            mindMapInstance.value.destroy()
            mindMapInstance.value = null
        }
        nextTick(() => {
            initMindMap()
        })
    }
}, { deep: true })

// 初始化思维导图
const initMindMap = async () => {
    try {
        // 先清理旧实例
        if (mindMapInstance.value) {
            mindMapInstance.value.destroy()
            mindMapInstance.value = null
        }

        // 等待DOM更新
        await nextTick()

        const container = document.getElementById('mindMapContainer')
        if (!container) {
            console.error('找不到思维导图容器')
            return
        }

        // 设置容器样式
        container.style.width = '100%'
        container.style.height = '500px'
        container.style.margin = '0'
        container.style.padding = '0'

        // 转换数据
        const mindMapData = convertToMindMapFormat(props.task.markdownContent)

        // 创建思维导图实例
        mindMapInstance.value = new MindMap({
            el: container,
            data: mindMapData,
            theme: 'primary',
            layout: 'mindMap',
            enableNodeDragging: false,
            height: 500,
            width: container.clientWidth,
            keypress: false,
            contextMenu: false,
            fit: true,
            scale: 0.8,
            textAutoWrap: true,
            nodeTextEdit: false,
        })

        // 渲染
        mindMapInstance.value.render()

        // 稍后适应视图
        setTimeout(() => {
            if (mindMapInstance.value && mindMapInstance.value.command &&
                typeof mindMapInstance.value.command.executeCommand === 'function') {
                mindMapInstance.value.command.executeCommand('fit')
            }
        }, 300)
    } catch (error) {
        console.error('初始化思维导图失败:', error)
        ElMessage.error('思维导图初始化失败')
    }
}

// 在组件卸载前清理
onBeforeUnmount(() => {
    if (mindMapInstance.value) {
        mindMapInstance.value.destroy()
        mindMapInstance.value = null
    }
})

const chatPanelKey = computed(() => `chat-panel-${props.task.id}`)

// 复制文本到剪贴板
const copyText = (text) => {
    if (!text) {
        ElMessage.warning('没有可复制的文本')
        return
    }

    navigator.clipboard.writeText(text)
        .then(() => {
            ElMessage.success('文本已复制到剪贴板')
        })
        .catch(() => {
            ElMessage.error('复制失败')
        })
}

const downloadContent = () => {
    let filename, content, type
    if (isContentMindMap.value) {
        filename = `mindmap_${props.task.id}.json`
        content = props.task.markdownContent
        type = 'application/json'
    } else {
        filename = `markdown_${props.task.id}.md`
        content = props.task.markdownContent
        type = 'text/markdown'
    }

    const blob = new Blob([content], { type })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = filename
    document.body.appendChild(a)
    a.click()
    URL.revokeObjectURL(url)
    document.body.removeChild(a)
}
</script>

<template>
    <div class="task-detail-page">
        <div class="detail-container">
            <div class="left-panel">

                <div class="detail-card transcription-card">
                    <div class="card-header">
                        <div class="card-title">
                            <el-icon>
                                <Headset />
                            </el-icon>
                            <h3>原始文本</h3>
                        </div>
                        <el-button type="primary" :icon="CopyDocument" circle size="small" title="复制文本"
                            @click="copyText(task.transcriptionText)" />
                    </div>
                    <div class="card-body">
                        <div class="text-content">
                            {{ task.transcriptionText }}
                        </div>
                    </div>
                </div>

                <div class="detail-card content-card">
                    <div class="card-header">
                        <div class="card-title">
                            <el-icon>
                                <Reading />
                            </el-icon>
                            <h3>{{ isContentMindMap ? '思维导图' : '生成图文' }}</h3>
                        </div>
                        <el-button type="primary" :icon="Download" circle size="small" title="下载内容"
                            @click="downloadContent" />
                    </div>
                    <div class="card-body">
                        <template v-if="isContentMindMap">
                            <div id="mindMapContainer" class="mind-map-container"></div>
                            <div class="mindmap-tip">
                                点击下载思维导图, 导入到 <a href="https://wanglin2.github.io/mind-map/#/"
                                    target="_blank">https://wanglin2.github.io/mind-map/#/</a> 即可在线编辑
                            </div>
                        </template>
                        <template v-else>
                            <div v-html="md.render(task.markdownContent)" class="markdown-content"></div>
                        </template>
                    </div>
                </div>
            </div>

            <div class="right-panel">
                <ChatPanel :task="task" :embedded="true" class="embedded-chat" :key="chatPanelKey" />
            </div>
        </div>
    </div>
</template>

<style>
#mindMapContainer * {
    margin: 0;
    padding: 0;
}

/* 确保Markdown内容左对齐 */
.markdown-content * {
    text-align: left !important;
}

.markdown-content ul,
.markdown-content ol {
    padding-left: 2em;
    margin: 0.5em 0;
}

.markdown-content p,
.markdown-content h1,
.markdown-content h2,
.markdown-content h3,
.markdown-content h4 {
    margin: 0.5em 0;
}
</style>

<style scoped>
.task-detail-page {
    width: 90%;
    padding: 0;
    margin: 0 auto;
    height: 96vh;
    /* 固定为视窗高度的90% */
    display: flex;
    flex-direction: column;
    box-sizing: border-box;
    overflow: hidden;
    /* 修改：禁止溢出滚动 */
}

.detail-container {
    display: flex;
    gap: 20px;
    width: 100%;
    height: 100%;
    /* 修改：使容器占满父元素高度 */
    box-sizing: border-box;
    padding: 20px;
    overflow: hidden;
    /* 修改：禁止溢出滚动 */
}

.left-panel {
    flex: 2.8;
    display: flex;
    flex-direction: column;
    gap: 20px;
    overflow-y: auto;
    /* 修改：允许左侧面板内容滚动 */
    padding-right: 10px;
    height: 100%;
    /* 使左侧面板占满容器高度 */
}

.right-panel {
    flex: 1.2;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
    height: 100%;
    /* 修改：使右侧面板占满容器高度 */
    position: relative;
    /* 修改：不再使用sticky定位 */
    top: 0;
}

.detail-card {
    background: white;
    border-radius: 12px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
    overflow: hidden;
    transition: box-shadow 0.3s;
    width: 96%;
    margin: 0 auto;
}

.detail-card:hover {
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px 20px;
    border-bottom: 1px solid #ebeef5;
    background: linear-gradient(135deg, #ffffff, #f8fafd);
}

.card-title {
    display: flex;
    align-items: center;
    gap: 8px;
}

.card-title h3 {
    margin: 0;
    font-size: 16px;
    font-weight: 600;
    color: #303133;
}

.info-content {
    padding: 12px 16px;
}

/* 新增的两栏布局样式 */
.info-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
}

.info-column {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.info-item {
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.info-label {
    font-weight: 500;
    color: #606266;
    font-size: 13px;
}

.info-value {
    color: #303133;
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 14px;
}

.md5-value {
    font-family: monospace;
    word-break: break-all;
}

/* 卡片主体区域 */
.card-body {
    padding: 16px;
    overflow-y: auto;
    /* 允许卡片内容滚动 */
}

/* 卡片类型样式 */
.transcription-card {
    flex-shrink: 0;
}

.content-card {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    /* 确保内容不溢出 */
}

.content-card .card-body {
    flex: 1;
    display: flex;
    flex-direction: column;
    padding: 16px;
    overflow: hidden;
    /* 确保内容不溢出 */
}

/* 音频转文字内容 */
.text-content {
    white-space: pre-wrap;
    line-height: 1.6;
    font-size: 13px;
    color: #4a5568;
    padding: 12px 16px;
    border: 1px solid #edf2f7;
    border-radius: 12px;
    background: #f8f9fa;
    max-height: 120px;
    overflow-y: auto;
    text-align: left;
}

/* 生成图文区域 */
.markdown-content {
    line-height: 1.6;
    font-size: 13px;
    color: #303133;
    padding: 12px 16px;
    border: 1px solid #edf2f7;
    border-radius: 12px;
    background: #f8f9fa;
    height: auto;
    /* 移除固定最小高度 */
    min-height: 200px;
    /* 减小最小高度 */
    max-height: calc(100% - 10px);
    /* 动态计算高度，减去内边距 */
    overflow-y: auto;
    text-align: left;
    flex: 1;
    box-sizing: border-box;
    /* 确保padding包含在高度内 */
    margin-bottom: 0;
    /* 移除底部外边距 */
}

/* 思维导图容器 */
.mind-map-container {
    width: 100%;
    height: calc(100% - 32px);
    /* 动态计算高度，减去内边距 */
    background: #f9fafc;
    border-radius: 12px;
    position: relative;
    overflow: hidden;
    border: 1px solid #ebeef5;
    flex: 1;
    box-sizing: border-box;
    /* 确保border包含在高度内 */
    margin-bottom: 0;
    /* 移除底部外边距 */
}

.embedded-chat {
    height: 100%;
    border-radius: 12px;
}

/* 滚动条样式 - 与ChatPanel保持一致 */
.left-panel::-webkit-scrollbar,
.text-content::-webkit-scrollbar,
.markdown-content::-webkit-scrollbar {
    width: 5px;
}

.left-panel::-webkit-scrollbar-thumb,
.text-content::-webkit-scrollbar-thumb,
.markdown-content::-webkit-scrollbar-thumb {
    background: #dcdfe6;
    border-radius: 10px;
}

.left-panel::-webkit-scrollbar-track,
.text-content::-webkit-scrollbar-track,
.markdown-content::-webkit-scrollbar-track {
    background: transparent;
}

/* 响应式设计 */
@media screen and (max-width: 1600px) {
    .task-detail-page {
        width: 100%;
    }
}

@media screen and (max-width: 1400px) {
    .info-grid {
        grid-template-columns: 1fr;
        /* 在中等屏幕上切换为单列 */
    }

    .info-column:first-child {
        margin-bottom: 0;
    }
}

@media screen and (max-width: 1200px) {
    .detail-container {
        flex-direction: column;
        height: auto;
    }

    .left-panel,
    .right-panel {
        width: 100%;
        height: 45vh;
        /* 在小屏幕上，左右各占45vh */
    }

    .right-panel {
        position: relative;
        top: 0;
    }
}

/* 内容区域标题样式调整 - 确保与卡片左侧对齐 */
.section-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 12px;
    padding-left: 0;
    /* 移除任何左内边距 */
    margin-left: 0;
    /* 移除任何左外边距 */
    text-align: left;
}

.transcription-section .section-header,
.content-section .section-header {
    margin-left: 0;
    /* 确保与卡片左侧对齐 */
}

/* 区域内容容器调整 */
.text-content,
.markdown-content,
.mind-map-container {
    margin-left: 0;
    /* 确保内容左对齐 */
    width: 100%;
    /* 确保内容宽度充满父容器 */
}

/* 思维导图提示文本样式 */
.mindmap-tip {
    font-size: 12px;
    color: #909399;
    margin-top: 8px;
    padding-left: 4px;
    line-height: 1.4;
    text-align: left;
}

.mindmap-tip a {
    color: #409EFF;
    text-decoration: none;
}

.mindmap-tip a:hover {
    text-decoration: underline;
}
</style>
