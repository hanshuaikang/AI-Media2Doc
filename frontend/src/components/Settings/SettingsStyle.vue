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
    max-width: 800px;
    margin: 0;
}

.style-selector-row {
    margin-bottom: 24px;
    display: flex;
    flex-wrap: wrap;
    gap: 16px;
    justify-content: flex-start;
    align-items: center;
    overflow-x: auto;
}

.style-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
    border: 2px solid #e2e8f0;
    border-radius: 16px;
    padding: 20px 16px 16px;
    min-width: 100px;
    min-height: 80px;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    font-size: 14px;
    color: #475569;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    user-select: none;
    position: relative;
    overflow: hidden;
}

.style-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, #3b82f6, #8b5cf6);
    transform: scaleX(0);
    transition: transform 0.3s ease;
}

.style-card:hover {
    border-color: #3b82f6;
    box-shadow: 0 8px 25px rgba(59, 130, 246, 0.15);
    background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
    transform: translateY(-2px);
}

.style-card:hover::before {
    transform: scaleX(1);
}

.style-card.active {
    border-color: #3b82f6;
    background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
    color: #1d4ed8;
    box-shadow: 0 8px 25px rgba(59, 130, 246, 0.2);
    transform: translateY(-2px);
}

.style-card.active::before {
    transform: scaleX(1);
}

.style-card-icon {
    width: 32px;
    height: 32px;
    margin-bottom: 8px;
    vertical-align: middle;
    filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
}

.style-card-name {
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 0.2px;
    text-align: center;
    line-height: 1.2;
}

.prompt-editor-row {
    margin-bottom: 20px;
    margin-top: 0;
    display: flex;
    flex-direction: column;
    gap: 8px;
    position: relative;
}

.prompt-tip {
    color: #d97706;
    font-size: 13px;
    margin-bottom: 8px;
    line-height: 1.6;
    text-align: left;
    background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
    border-left: 4px solid #f59e0b;
    padding: 12px 16px;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(245, 158, 11, 0.1);
}

.prompt-label-row {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 2px;
}

.prompt-label {
    font-size: 15px;
    font-weight: 600;
    color: #1e293b;
    margin-bottom: 0;
    margin-top: 0;
    text-align: left;
    padding-right: 0;
    line-height: 1.8;
}

.prompt-action-row {
    position: absolute;
    top: 42px;
    right: 0;
    z-index: 2;
    display: flex;
    align-items: center;
}

.refresh-prompt-btn {
    padding: 0 12px;
    height: 28px;
    font-size: 13px;
    border-radius: 6px;
    border: 1px solid #dbeafe;
    background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
    color: #3b82f6;
    transition: all 0.2s ease;
    box-shadow: 0 2px 4px rgba(59, 130, 246, 0.1);
}

.refresh-prompt-btn:hover {
    background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
    border-color: #3b82f6;
    color: #1d4ed8;
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(59, 130, 246, 0.2);
}

.prompt-textarea {
    width: 100%;
    font-size: 14px;
    border-radius: 8px;
    background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
    border: 2px solid #e2e8f0;
    transition: all 0.3s ease;
    padding-top: 36px !important;
    font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
    line-height: 1.6;
}

.prompt-textarea:focus-within {
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    background: white;
}

.save-btn-row {
    margin-top: 16px;
    display: flex;
    align-items: center;
    gap: 16px;
}

.save-success-msg {
    color: #059669;
    font-size: 14px;
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 6px;
}

.save-success-msg::before {
    content: '✓';
    font-weight: bold;
}
</style>
