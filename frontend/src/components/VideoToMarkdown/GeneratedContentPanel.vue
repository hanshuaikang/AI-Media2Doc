<template>
    <div class="text-card full-height">
        <div class="section-header with-bar">
            <h2>{{ getContentTypeTitle() }}</h2>
            <el-button type="primary" :icon="Download" circle size="small" title="下载内容" @click="downloadContent"
                class="copy-btn" />
        </div>
        <div class="original-text-content markdown-content-area">
            <template v-if="isContentMindMap">
                <div id="mindMapContainer" class="mind-map-container"></div>
                <div class="mindmap-tip">
                    点击下载思维导图, 导入到 <a href="https://wanglin2.github.io/mind-map/#/"
                        target="_blank">https://wanglin2.github.io/mind-map/#/</a> 即可在线编辑
                </div>
            </template>
            <template v-else>
                <div v-html="renderedContent" class="markdown-content" />
            </template>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, watch, nextTick } from 'vue'
import { ElButton, ElMessage } from 'element-plus'
import { Download } from '@element-plus/icons-vue'
import MarkdownIt from 'markdown-it'
import MindMap from 'simple-mind-map'

const props = defineProps({
    content: {
        type: String,
        required: true
    },
    taskId: {
        type: [String, Number],
        required: true
    }
})

// 配置 markdown-it 支持表格
const md = new MarkdownIt({
    html: true,
    breaks: true,
    linkify: true
})

// 启用表格插件
md.enable('table')

const mindMapInstance = ref(null)

// 判断内容是否为JSON格式
const isJsonString = (str) => {
    if (typeof str !== 'string') return false
    try {
        const result = JSON.parse(str)
        return typeof result === 'object' && result !== null
    } catch (e) {
        return false
    }
}

// 判断内容是否应该显示为思维导图
const isContentMindMap = computed(() => isJsonString(props.content))

// 获取内容类型标题
const getContentTypeTitle = () => {
    if (isContentMindMap.value) return '思维导图'
    return '图文信息'
}

// 渲染后的内容
const renderedContent = computed(() => {
    return md.render(props.content)
})

// 转换思维导图数据格式
const convertToMindMapFormat = (jsonData) => {
    try {
        const data = typeof jsonData === 'object' ? jsonData : JSON.parse(jsonData)
        return data.data && (data.data.text || data.data.title)
            ? data
            : { data: { text: data.text || data.title || "思维导图" }, children: data.children || [] }
    } catch {
        return { data: { text: "解析失败的思维导图" }, children: [] }
    }
}

// 初始化思维导图
const initMindMap = async () => {
    try {
        if (mindMapInstance.value) mindMapInstance.value.destroy()
        await nextTick()
        const container = document.getElementById('mindMapContainer')
        if (!container) return
        container.style.width = '100%'
        container.style.height = '500px'
        const mindMapData = convertToMindMapFormat(props.content)
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
            nodeTextEdit: false
        })
        mindMapInstance.value.render()
        setTimeout(() => mindMapInstance.value?.command?.executeCommand('fit'), 300)
    } catch {
        ElMessage.error('思维导图初始化失败')
    }
}

// 下载内容
const downloadContent = () => {
    let filename, type
    if (isContentMindMap.value) {
        filename = `mindmap_${props.taskId}.json`
        type = 'application/json'
    } else {
        filename = `markdown_${props.taskId}.md`
        type = 'text/markdown'
    }

    const blob = new Blob([props.content], { type })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = filename
    document.body.appendChild(a)
    a.click()
    URL.revokeObjectURL(url)
    document.body.removeChild(a)
}

// 组件生命周期
onMounted(() => isContentMindMap.value && initMindMap())
onBeforeUnmount(() => mindMapInstance.value?.destroy())
watch(() => props.content, () => isContentMindMap.value && initMindMap())
</script>

<style scoped>
.text-card.full-height {
    background: #fff;
    border-radius: 16px;
    box-shadow: 0 4px 16px 0 rgba(0, 42, 102, 0.08);
    height: 100%;
    display: flex;
    flex-direction: column;
    padding: 0;
    border: none;
}

.section-header {
    padding: 0 24px;
    margin-bottom: 0;
    border-bottom: none;
    display: flex;
    align-items: center;
    justify-content: flex-start;
    position: relative;
    min-height: 56px;
    background: transparent;
}

.section-header.with-bar {
    padding-left: 28px;
}

.section-header.with-bar::before {
    content: '';
    display: block;
    width: 4px;
    height: 24px;
    background: #409eff;
    border-radius: 2px;
    position: absolute;
    left: 16px;
    top: 50%;
    transform: translateY(-50%);
}

.section-header h2 {
    font-size: 17px;
    font-weight: 600;
    color: #222;
    margin: 0;
    line-height: 56px;
    letter-spacing: 0.5px;
}

.copy-btn {
    margin-left: auto;
    box-shadow: none;
}

.original-text-content.markdown-content-area {
    flex: 1;
    overflow-y: auto;
    padding: 24px 32px 32px 32px;
    border-radius: 0 0 16px 16px;
    background: transparent;
    scrollbar-width: none;
    /* Firefox */
}

.original-text-content.markdown-content-area::-webkit-scrollbar {
    display: none;
    /* Chrome/Safari */
}

/* Mind map 容器内元素归零 */
#mindMapContainer * {
    margin: 0;
    padding: 0;
}

/* Markdown 内容样式优化 */
.markdown-content {
    font-size: 15px;
    color: #222;
    line-height: 2;
    word-break: break-word;
    background: transparent;
}

.markdown-content * {
    text-align: left !important;
    box-sizing: border-box;
}

.markdown-content h1,
.markdown-content h2,
.markdown-content h3,
.markdown-content h4 {
    font-weight: 600;
    color: #222;
    margin: 0.5em 0;
    line-height: 1.5;
}

.markdown-content h1 {
    font-size: 1.3em;
}

.markdown-content h2 {
    font-size: 1.1em;
}

.markdown-content h3 {
    font-size: 1em;
}

.markdown-content h4 {
    font-size: 0.95em;
}

.markdown-content p {
    margin: 0.5em 0;
    color: #222;
    font-size: 15px;
}

.markdown-content ul,
.markdown-content ol {
    padding-left: 2em;
    margin: 0.5em 0;
    font-size: 15px;
    list-style-position: outside;
}

.markdown-content ul ul,
.markdown-content ol ul,
.markdown-content ul ol,
.markdown-content.ol ol {
    padding-left: 1.2em;
    margin-top: 0;
    margin-bottom: 0;
}

.markdown-content li {
    margin: 0.2em 0;
    padding-left: 0;
}

/* 表格响应式处理 */
@media (max-width: 768px) {
    .markdown-content table {
        font-size: 12px;
    }

    .markdown-content table th,
    .markdown-content table td {
        padding: 8px 12px;
        font-size: 12px;
    }
}

.mindmap-tip {
    margin-top: 16px;
    font-size: 14px;
    color: #888;
}
</style>

<style>
/* 全局表格样式，确保应用到动态渲染的内容 */
.markdown-content table {
    width: 100% !important;
    border-collapse: collapse !important;
    margin: 1em 0 !important;
    font-size: 14px !important;
    background: #fff !important;
    border-radius: 8px !important;
    overflow: hidden !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
    border: 1px solid #e9ecef !important;
}

.markdown-content table th {
    background: #f8f9fa !important;
    color: #333 !important;
    font-weight: 600 !important;
    padding: 12px 16px !important;
    text-align: left !important;
    border: 1px solid #e9ecef !important;
    font-size: 14px !important;
}

.markdown-content table td {
    padding: 12px 16px !important;
    border: 1px solid #e9ecef !important;
    color: #555 !important;
    font-size: 14px !important;
    line-height: 1.4 !important;
}

.markdown-content table tr:hover {
    background-color: #f8f9fa !important;
}

.markdown-content table tr:last-child td {
    border-bottom: 1px solid #e9ecef !important;
}
</style>
