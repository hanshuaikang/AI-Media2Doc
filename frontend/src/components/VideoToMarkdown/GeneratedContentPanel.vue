<template>
    <div class="text-card full-height">
        <div class="section-header with-bar">
            <h2>{{ getContentTypeTitle() }}</h2>
            <!-- 大纲弹出框与按钮 -->
            <el-popover
                v-model:visible="outlineVisible"
                placement="bottom-start"
                trigger="click"
                :width="340"
                popper-class="outline-popover"
                :hide-on-click="false"
            >
                <template #reference>
                    <el-button
                        type="primary"
                        :icon="List"
                        circle
                        size="small"
                        class="outline-btn"
                        title="大纲"
                    />
                </template>
                <div class="outline-content" @click.stop>
                    <div v-if="outlineLoading" class="outline-loading">
                        <el-icon class="loading-icon"><Loading /></el-icon>
                        <span class="loading-text">正在生成大纲…</span>
                        <el-skeleton animated :rows="6" style="margin-top:8px;" />
                    </div>
                    <div v-else>
                        <div v-if="outlineItems.length === 0" class="outline-empty">当前内容暂无标题</div>
                        <ul v-else class="outline-list">
                            <li
                                v-for="item in outlineItems"
                                :key="item.id"
                                class="outline-item"
                                :style="{ paddingLeft: (item.level - 1) * 16 + 'px' }"
                                @click="scrollToHeading(item)"
                                :title="item.text"
                            >
                                <span :class="'level-' + item.level">{{ item.text }}</span>
                            </li>
                        </ul>
                    </div>
                </div>
            </el-popover>
            <el-button type="primary" :icon="Download" circle size="small" title="下载内容" @click="downloadContent"
                class="copy-btn" />
        </div>
        <div class="original-text-content markdown-content-area">
            <template v-if="isContentMindMap">
                <MindMapViewer :content="content" />
            </template>
            <template v-else>
                <div v-html="renderedContent" class="markdown-content" />
            </template>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, nextTick, watch } from 'vue'
import { ElButton } from 'element-plus'
import { Download, List, Loading } from '@element-plus/icons-vue'
import MarkdownIt from 'markdown-it'
import MindMapViewer from './MindMapViewer.vue'

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

// 生成标题锚点的简易 slugify（与 taskId 结合保证唯一）
const slugify = (s) => {
    return String(s || '')
        .toLowerCase()
        .trim()
        .replace(/<[^>]*>/g, '') // 去除可能的 HTML
        .replace(/[^a-z0-9\u4e00-\u9fa5\s-]/g, '') // 允许中文、空格、连字符
        .replace(/\s+/g, '-')
        .slice(0, 64)
}

// 在渲染阶段为所有标题添加 id，避免后续 DOM 读写带来的卡顿
const originalHeadingOpen = md.renderer.rules.heading_open || function (tokens, idx, options, env, self) {
    return self.renderToken(tokens, idx, options)
}
md.renderer.rules.heading_open = function (tokens, idx, options, env, self) {
    const next = tokens[idx + 1]
    let text = ''
    if (next && next.type === 'inline') {
        text = (next.content || '').trim()
    }
    const id = slugify(text) + '-' + String(env?.taskId ?? '')
    // 设置/覆盖 id 属性
    const existing = tokens[idx].attrIndex('id')
    if (existing < 0) {
        tokens[idx].attrPush(['id', id])
    } else {
        tokens[idx].attrs[existing][1] = id
    }
    return originalHeadingOpen(tokens, idx, options, env, self)
}

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
    // 通过 env 传入 taskId，确保渲染时标题带唯一 id
    return md.render(props.content, { taskId: props.taskId })
})

// 大纲相关状态
const outlineVisible = ref(false)
const outlineLoading = ref(false)
const outlineItems = ref([])
let generateTimer = null

// 生成大纲（首次点击时进行）
const generateOutline = async () => {
    outlineLoading.value = true
    await nextTick()
    // 让弹出层先渲染帧，避免首次打开卡顿
    await new Promise((resolve) => requestAnimationFrame(resolve))
    // 直接使用 markdown-it 的 token 列表解析标题，避免 DOM 查询开销
    const tokens = md.parse(props.content, { taskId: props.taskId })
    const items = []
    for (let i = 0; i < tokens.length; i++) {
        const t = tokens[i]
        if (t.type === 'heading_open') {
            const level = Number(t.tag.slice(1))
            const inline = tokens[i + 1]
            const text = inline && inline.type === 'inline' ? (inline.content || '').trim() : ''
            const id = t.attrGet('id') || slugify(text) + '-' + String(props.taskId)
            items.push({ id, level, text })
        }
    }
    outlineItems.value = items
    outlineLoading.value = false
}

// 当弹出框打开时，进行防抖解析（每次点击都生成）
watch(outlineVisible, (visible) => {
    if (visible) {
        if (generateTimer) clearTimeout(generateTimer)
        generateTimer = setTimeout(() => {
            if (outlineVisible.value) {
                generateOutline()
            }
        }, 100)
    }
})

// 滚动到对应标题（容器内平滑滚动）
const scrollToHeading = (item) => {
    const container = document.querySelector('.original-text-content.markdown-content-area')
    const target = document.getElementById(item.id)
    if (!container || !target) return
    const top = target.offsetTop
    container.scrollTo({ top, behavior: 'smooth' })
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

.outline-btn {
    margin-left: auto;
    margin-right: 8px;
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

/* 大纲弹出框与列表样式 */
.outline-popover {
    padding: 8px 0;
    border: 1px solid #e9ecef;
    border-radius: 10px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
}

.outline-content {
    max-height: 300px;
    overflow-y: auto;
    background: #fff;
}

.outline-loading {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px 12px 6px 12px;
    color: #555;
}

.loading-icon {
    animation: spin 1s linear infinite;
}

@keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

.outline-empty {
    padding: 10px 12px;
    color: #888;
    font-size: 13px;
}

.outline-list {
    list-style: none;
    margin: 0;
    padding: 4px 0;
}

.outline-item {
    padding: 6px 12px;
    cursor: pointer;
    border-top: 1px solid #f2f3f5;
    color: #333;
}

.outline-item:hover {
    background: #f8f9fa;
}

.outline-item .level-1 { font-weight: 700; font-size: 14px; color: #222; }
.outline-item .level-2 { font-weight: 600; font-size: 13px; color: #333; }
.outline-item .level-3 { font-weight: 600; font-size: 12px; color: #444; }
.outline-item .level-4 { font-weight: 500; font-size: 12px; color: #555; }
.outline-item .level-5 { font-weight: 500; font-size: 12px; color: #666; }
.outline-item .level-6 { font-weight: 500; font-size: 12px; color: #777; }
</style>
