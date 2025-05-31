<template>
    <el-dialog v-model="visible" title="自定义配置" width="50vw" class="settings-dialog" :close-on-click-modal="false"
        :close-on-press-escape="true" :show-close="true" @close="handleClose">
        <div class="settings-dialog-body">
            <div class="settings-sidebar">
                <ul>
                    <li :class="{ active: activeMenu === 'style' }" @click="activeMenu = 'style'">风格设置</li>
                    <li :class="{ active: activeMenu === 'about' }" @click="activeMenu = 'about'">关于</li>
                    <!-- 可扩展更多菜单 -->
                </ul>
            </div>
            <div class="settings-content">
                <div v-if="activeMenu === 'style'" class="style-settings">
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
                        <label class="prompt-label">Prompt：</label>
                        <el-input v-model="currentPrompt" type="textarea" :rows="8" resize="vertical"
                            class="prompt-textarea" />
                    </div>
                    <div class="save-btn-row">
                        <el-button type="primary" @click="savePrompt">保存</el-button>
                        <span v-if="saveSuccess" class="save-success-msg">已保存！</span>
                    </div>
                </div>
                <div v-if="activeMenu === 'about'" class="about-settings">
                    <h2 style="margin-top:0;">AI 视频图文创作助手</h2>
                    <p style="font-size:1.05rem;line-height:1.7;">
                        AI 视频图文创作助手是一款 Web 工具, 基于 AI 大模型, 一键将视频和音频转化为各种风格的文档, 无需登录注册, 前后端本地部署，以极低的成本体验 AI 视频/音频转风格文档服务。
                    </p>
                    <div style="margin: 12px 0;">
                        项目地址：
                        <a href="https://github.com/hanshuaikang/AI-Media2Doc" target="_blank" style="color:#357aff;">
                            https://github.com/hanshuaikang/AI-Media2Doc
                        </a>
                    </div>
                    <div style="margin: 18px 0 0 0;">
                        <span>赞助作者：</span>
                        <a href="https://afdian.com/a/hanshu-github" target="_blank"
                            style="color:#e67e22;font-weight:600;">
                            我的爱发电主页
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </el-dialog>
</template>

<script setup>
import { ref, reactive, watch, defineProps, defineEmits } from 'vue'
import { ElRadioGroup, ElRadioButton, ElInput, ElButton, ElMessage, ElDialog } from 'element-plus'
import { DEFAULT_PROMPTS } from '../../constants'

const props = defineProps({
    visible: {
        type: Boolean,
        default: false
    }
})
const emit = defineEmits(['update:visible'])

const visible = ref(props.visible)
watch(() => props.visible, v => visible.value = v)
watch(visible, v => emit('update:visible', v))

function handleClose() {
    visible.value = false
}

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

const activeMenu = ref('style')
const selectedStyle = ref(styleList[0].label)
const currentPrompt = ref(prompts[selectedStyle.value])
const saveSuccess = ref(false)

watch(selectedStyle, (val) => {
    currentPrompt.value = prompts[val] || ''
    saveSuccess.value = false
})

function onStyleChange(val) {
    currentPrompt.value = prompts[val] || ''
    saveSuccess.value = false
}

function savePrompt() {
    prompts[selectedStyle.value] = currentPrompt.value
    setLocalPrompts(prompts)
    saveSuccess.value = true
    ElMessage.success('已保存到本地')
}
</script>

<style scoped>
.settings-dialog :deep(.el-dialog__body) {
    padding: 0;
}

.settings-dialog-body {
    display: flex;
    min-height: 380px;
    background: #f7f8fa;
    border-radius: 12px;
    overflow: hidden;
}

.settings-sidebar {
    width: 110px;
    background: #f5f7fa;
    border-right: 1px solid #e5e6eb;
    padding: 28px 0 0 0;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
}

.settings-sidebar ul {
    width: 100%;
    padding: 0;
    margin: 0;
    list-style: none;
}

.settings-sidebar li {
    width: 100%;
    padding: 10px 12px;
    font-size: 0.98rem;
    color: #6b7280;
    cursor: pointer;
    border-left: 3px solid transparent;
    background: none;
    transition: background 0.18s, border-color 0.18s, color 0.18s;
    border-radius: 0 8px 8px 0;
    margin-bottom: 2px;
    font-weight: 500;
    letter-spacing: 0.1px;
    text-align: left;
}

.settings-sidebar li.active,
.settings-sidebar li:hover {
    background: #eaf2ff;
    border-left: 3px solid #357aff;
    color: #357aff;
    font-weight: 700;
}

.settings-content {
    flex: 1;
    padding: 32px 28px 32px 28px;
    display: flex;
    align-items: flex-start;
    /* 顶部对齐 */
    /* justify-content: center; */
    /* 移除居中 */
    min-width: 260px;
    min-height: 320px;
    background: #fff;
    border-radius: 0 12px 12px 0;
}

.style-settings {
    width: 100%;
    max-width: 700px;
    /* margin: 0 auto; */
    /* 移除居中 */
    margin: 0;
    /* 靠左 */
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
    /* 保证与顶部对齐 */
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

.prompt-label {
    font-size: 1.01rem;
    font-weight: 600;
    color: #23272f;
    margin-bottom: 6px;
    display: block;
    margin-top: 0;
    text-align: left;
    /* 左对齐 */
    /* 保证与顶部对齐 */
}

.prompt-textarea {
    width: 100%;
    font-size: 0.98rem;
    border-radius: 6px;
    background: #f7f8fa;
    border: 1.5px solid #e3e6ef;
    transition: border-color 0.18s;
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

.about-settings {
    width: 100%;
    max-width: 700px;
    margin: 0;
    color: #23272f;
    font-size: 1.01rem;
    line-height: 1.7;
    background: #fff;
    border-radius: 8px;
    padding: 8px 4px 8px 0;
    text-align: left;
    /* 新增：左对齐 */

}

.about-settings a {
    text-decoration: underline;
    word-break: break-all;
}
</style>
