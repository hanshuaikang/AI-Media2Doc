<template>
    <div class="text-card full-height">
        <div class="section-header with-bar">
            <h2>{{ isContentMindMap ? '思维导图' : '图文信息' }}</h2>
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
                <div v-html="md.render(content)" class="markdown-content" />
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

const md = new MarkdownIt()
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
    const filename = isContentMindMap.value ? `mindmap_${props.taskId}.json` : `markdown_${props.taskId}.md`
    const type = isContentMindMap.value ? 'application/json' : 'text/markdown'
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
.markdown-content ol ol {
    padding-left: 1.2em;
    margin-top: 0;
    margin-bottom: 0;
}

.markdown-content li {
    margin: 0.2em 0;
    padding-left: 0;
}

.mindmap-tip {
    margin-top: 16px;
    font-size: 14px;
    color: #888;
}
</style>
