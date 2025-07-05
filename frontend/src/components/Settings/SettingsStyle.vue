<template>
    <div class="style-settings">
        <div class="style-selector-row">
            <div v-for="item in styleList" :key="item.label" class="style-card"
                :class="{ active: selectedStyle === item.label }" @click="selectedStyle = item.label">
                <img :src="item.icon" :alt="item.name" class="style-card-icon" />
                <span class="style-card-name">{{ item.name }}</span>
            </div>
        </div>
        <div class="prompt-editor-row">
            <div class="prompt-tip">
                请勿修改 <code>{content}</code> 以及思维导图的 json 内容，不然可能会导致生成失败。
            </div>
            <div class="prompt-label-row">
                <label class="prompt-label">Prompt：</label>
            </div>
            <div class="prompt-action-row">
                <el-button class="refresh-prompt-btn" size="small" type="info" plain @click="refreshPrompt"
                    title="刷新最新默认配置">
                    <el-icon style="vertical-align: middle; margin-right: 3px;">
                        <svg viewBox="0 0 1024 1024" width="16" height="16">
                            <path fill="currentColor"
                                d="M512 128a384 384 0 1 1-271.6 112.4l-60.8-60.8A448 448 0 1 0 960 512h-64a384 384 0 0 1-384 384A384 384 0 0 1 128 512c0-106.1 41.4-205.8 116.6-281l-60.8-60.8A448 448 0 1 0 960 512h-64A384 384 0 0 1 512 128z" />
                        </svg>
                    </el-icon>
                    刷新最新默认配置
                </el-button>
            </div>
            <el-input v-model="currentPrompt" type="textarea" :rows="8" resize="vertical" class="prompt-textarea" />
        </div>
        <div class="save-btn-row">
            <el-button type="primary" @click="savePrompt">保存</el-button>
            <span v-if="saveSuccess" class="save-success-msg">已保存！</span>
        </div>
    </div>
</template>

<script setup>
import { ref, reactive, watch } from 'vue'
import { ElButton, ElInput, ElMessage } from 'element-plus'
import { DEFAULT_PROMPTS } from '../../constants'

const styleList = [
    { label: 'note', name: '知识笔记', icon: new URL('../../assets/笔记.svg', import.meta.url).href },
    { label: 'xiaohongshu', name: '小红书', icon: new URL('../../assets/小红书.svg', import.meta.url).href },
    { label: 'wechat', name: '公众号', icon: new URL('../../assets/微信公众号.svg', import.meta.url).href },
    { label: 'summary', name: '内容总结', icon: new URL('../../assets/汇总.svg', import.meta.url).href },
    { label: 'mind', name: '思维导图', icon: new URL('../../assets/思维导图.svg', import.meta.url).href },
]

function getLocalPrompts() {
    try {
        const str = localStorage.getItem('customPrompts')
        if (str) return JSON.parse(str)
    } catch { }
    return {}
}
function setLocalPrompts(obj) {
    localStorage.setItem('customPrompts', JSON.stringify(obj))
}
const prompts = reactive({ ...DEFAULT_PROMPTS, ...getLocalPrompts() })

const selectedStyle = ref(styleList[0].label)
const currentPrompt = ref(prompts[selectedStyle.value])
const saveSuccess = ref(false)

watch(selectedStyle, (val) => {
    currentPrompt.value = prompts[val] || ''
    saveSuccess.value = false
})

function savePrompt() {
    prompts[selectedStyle.value] = currentPrompt.value
    setLocalPrompts(prompts)
    saveSuccess.value = true
    ElMessage.success('已保存到本地')
}

function refreshPrompt() {
    const style = selectedStyle.value
    if (DEFAULT_PROMPTS[style]) {
        currentPrompt.value = DEFAULT_PROMPTS[style]
        prompts[style] = DEFAULT_PROMPTS[style]
        setLocalPrompts(prompts)
        saveSuccess.value = false
        ElMessage.success('已刷新为最新默认配置')
    } else {
        ElMessage.warning('未找到该风格的默认配置')
    }
}
</script>

<style scoped>
.style-settings {
    width: 100%;
    max-width: 700px;
    margin: 0;
}

.style-selector-row {
    margin-bottom: 18px;
    display: flex;
    flex-wrap: wrap;
    gap: 18px;
    justify-content: flex-start;
    align-items: center;
    overflow-x: auto;
}

.style-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: #fff;
    border: 2px solid #e5e6eb;
    border-radius: 12px;
    padding: 14px 18px 10px 18px;
    min-width: 90px;
    min-height: 74px;
    cursor: pointer;
    transition: border-color 0.18s, box-shadow 0.18s, background 0.18s, color 0.18s;
    font-size: 1.01rem;
    color: #23272f;
    box-shadow: 0 1px 4px 0 rgba(60, 80, 120, 0.04);
    user-select: none;
}

.style-card:hover {
    border-color: #357aff;
    box-shadow: 0 4px 16px 0 rgba(53, 122, 255, 0.08);
    background: #f0f6ff;
}

.style-card.active {
    border-color: #357aff;
    background: #eaf2ff;
    color: #357aff;
    box-shadow: 0 4px 16px 0 rgba(53, 122, 255, 0.10);
}

.style-card-icon {
    width: 28px;
    height: 28px;
    margin-bottom: 7px;
    vertical-align: middle;
}

.style-card-name {
    font-size: 1.01rem;
    font-weight: 600;
    letter-spacing: 0.1px;
}

.prompt-editor-row {
    margin-bottom: 14px;
    margin-top: 0;
    display: flex;
    flex-direction: column;
    gap: 6px;
    position: relative;
}

.prompt-tip {
    color: #e67e22;
    font-size: 0.96rem;
    margin-bottom: 6px;
    line-height: 1.6;
    text-align: left;
    background: #fffbe6;
    border-left: 4px solid #ffd666;
    padding: 6px 12px;
    border-radius: 4px;
}

.prompt-label-row {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 2px;
}

.prompt-label {
    font-size: 1.01rem;
    font-weight: 600;
    color: #23272f;
    margin-bottom: 0;
    margin-top: 0;
    text-align: left;
    padding-right: 0;
    line-height: 1.8;
}

.prompt-action-row {
    position: absolute;
    top: 38px;
    right: 0;
    z-index: 2;
    display: flex;
    align-items: center;
}

.refresh-prompt-btn {
    padding: 0 10px;
    height: 26px;
    font-size: 0.97rem;
    border-radius: 4px;
    border: 1px solid #dbeafe;
    background: #f7faff;
    color: #357aff;
    transition: background 0.15s, border-color 0.15s;
}

.refresh-prompt-btn:hover {
    background: #eaf2ff;
    border-color: #357aff;
    color: #357aff;
}

.prompt-textarea {
    width: 100%;
    font-size: 0.98rem;
    border-radius: 6px;
    background: #f7f8fa;
    border: 1.5px solid #e3e6ef;
    transition: border-color 0.18s;
    padding-top: 32px !important;
}

.prompt-textarea:focus-within {
    border-color: #357aff;
}

.save-btn-row {
    margin-top: 8px;
    display: flex;
    align-items: center;
    gap: 14px;
}

.save-success-msg {
    color: #67C23A;
    font-size: 0.97rem;
}
</style>
