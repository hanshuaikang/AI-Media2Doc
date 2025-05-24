<template>
    <div class="text-card half-height">
        <div class="section-header with-bar">
            <h2>文本转录信息</h2>
            <el-button type="primary" :icon="CopyDocument" circle size="small" title="复制文本" @click="copyText"
                class="copy-btn" />
            <el-button type="primary" :icon="Download" size="small" title="导出为字幕文件" @click="exportSRT"
                class="export-btn rounded-btn" style="margin-left: 8px;">
                导出字幕
            </el-button>
        </div>
        <div class="original-text-content">
            <template v-if="isSegmentArray">
                <div v-for="(seg, idx) in transcription" :key="idx" class="text-item">
                    <div class="text-time text-time-blue">{{ formatTime(seg.start_time) }}</div>
                    <div class="text-content">{{ seg.text }}</div>
                </div>
            </template>
            <template v-else>
                <div class="text-item">
                    <div class="text-content" style="margin-left:0;">{{ transcription }}</div>
                </div>
            </template>
        </div>
    </div>
</template>

<script setup>
import { computed } from 'vue'
import { ElButton, ElMessage } from 'element-plus'
import { CopyDocument, Download } from '@element-plus/icons-vue'

const props = defineProps({
    transcription: {
        type: [Array, String],
        required: true
    }
})

const isSegmentArray = computed(() => {
    const t = props.transcription
    return Array.isArray(t) && t.length > 0 && typeof t[0] === 'object' && 'start_time' in t[0] && 'text' in t[0]
})

// 时间格式化 mm:ss
const formatTime = (ms) => {
    if (typeof ms !== 'number') return ''
    const totalSeconds = Math.floor(ms / 1000)
    const min = Math.floor(totalSeconds / 60)
    const sec = totalSeconds % 60
    return `${min.toString().padStart(2, '0')}:${sec.toString().padStart(2, '0')}`
}

const copyText = () => {
    let textToCopy = props.transcription
    if (isSegmentArray.value && Array.isArray(props.transcription)) {
        textToCopy = props.transcription.map(seg => seg.text).join('\n')
    }
    if (!textToCopy) {
        ElMessage.warning('没有可复制的文本')
        return
    }
    navigator.clipboard.writeText(textToCopy)
        .then(() => {
            ElMessage.success('文本已复制到剪贴板')
        })
        .catch(() => {
            ElMessage.error('复制失败')
        })
}

// 导出 SRT 字幕文件
const exportSRT = () => {
    if (!isSegmentArray.value || !Array.isArray(props.transcription)) {
        ElMessage.warning('当前内容无法导出为字幕文件')
        return
    }
    // SRT 文件头注释
    const header = `1\n00:00:00,000 --> 00:00:00,000\n字幕由 AI-Media2Doc 生成\nhttps://github.com/hanshuaikang/AI-Media2Doc\n\n`
    // 生成 SRT 正文
    const srtContent = props.transcription.map((seg, idx) => {
        const start = msToSrtTime(seg.start_time)
        // 结束时间为下一个片段的开始时间，最后一条+2秒
        const end = msToSrtTime(
            idx < props.transcription.length - 1
                ? props.transcription[idx + 1].start_time
                : seg.start_time + 2000
        )
        return `${idx + 1}\n${start} --> ${end}\n${seg.text}\n`
    }).join('\n')

    const fullSrt = header + srtContent

    // 下载
    const blob = new Blob([fullSrt], { type: 'text/plain;charset=utf-8' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'transcription.srt'
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
    ElMessage.success('字幕文件已导出')
}

// 毫秒转 SRT 时间格式
function msToSrtTime(ms) {
    const h = String(Math.floor(ms / 3600000)).padStart(2, '0')
    const m = String(Math.floor((ms % 3600000) / 60000)).padStart(2, '0')
    const s = String(Math.floor((ms % 60000) / 1000)).padStart(2, '0')
    const msStr = String(ms % 1000).padStart(3, '0')
    return `${h}:${m}:${s},${msStr}`
}
</script>

<style scoped>
.text-card {
    box-shadow: 0 4px 16px 0 rgba(0, 42, 102, 0.08);
    /* 更柔和的阴影 */
    border-radius: 8px;
    background: #fff;
    padding: 0 0 12px 0;
    margin-bottom: 0;
    height: 100%;
    display: flex;
    flex-direction: column;
}

.text-card.half-height {
    /* 移除固定高度限制，改为自适应 */
    height: 100%;
    min-height: 120px;
    display: flex;
    flex-direction: column;
}

.section-header {
    padding: 0 16px;
    margin-bottom: 0;
    border-bottom: none;
    display: flex;
    align-items: center;
    justify-content: flex-start;
    position: relative;
    min-height: 48px;
}

.section-header h2 {
    font-size: 16px;
    margin: 0;
    color: #333;
    font-weight: 500;
    text-align: left;
    line-height: 48px;
}

.section-header.with-bar {
    padding-left: 16px;
}

.section-header.with-bar::before {
    content: '';
    display: block;
    width: 4px;
    height: 22px;
    background: #1890ff;
    border-radius: 2px;
    position: absolute;
    left: 0;
    top: 50%;
    transform: translateY(-50%);
}

.copy-btn {
    margin-left: auto;
}

.export-btn {
    /* 可根据需要自定义样式 */
}

.rounded-btn {
    border-radius: 6px !important;
}

.original-text-content {
    /* 改为自适应高度 */
    flex: 1;
    overflow-y: auto;
    padding: 8px 16px 0 16px;
    scrollbar-width: none;
    /* Firefox */
}

.original-text-content::-webkit-scrollbar {
    display: none;
    /* Chrome/Safari */
}

.text-item {
    display: flex;
    align-items: flex-start;
    margin-bottom: 10px;
    padding: 8px;
    border-radius: 8px;
    background-color: #f9f9f9;
    transition: background-color 0.2s;
}

.text-item:hover {
    background-color: #f0f7ff;
}

.text-time {
    width: 60px;
    color: #999;
    font-family: monospace;
    font-size: 13px;
    flex-shrink: 0;
    margin-right: 12px;
    text-align: right;
    line-height: 1.6;
}

.text-time-blue {
    color: #1890ff;
}

.text-content {
    flex: 1;
    line-height: 1.6;
    font-size: 14px;
    color: #444;
    text-align: left;
    word-break: break-all;
}

/* 兼容单条文本无时间的情况 */
.text-item .text-content {
    margin-left: 0;
}
</style>
