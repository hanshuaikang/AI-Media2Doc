<template>
    <el-dialog v-model="visible" title="自定义配置" width="50vw" class="settings-dialog" :close-on-click-modal="false"
        :close-on-press-escape="true" :show-close="true" @close="handleClose">
        <div class="settings-dialog-body">
            <div class="settings-sidebar">
                <ul>
                    <li :class="{ active: activeMenu === 'style' }" @click="activeMenu = 'style'">风格设置</li>
                    <li :class="{ active: activeMenu === 'password' }" @click="activeMenu = 'password'">访问密码</li>
                    <li :class="{ active: activeMenu === 'other' }" @click="activeMenu = 'other'">其他设置</li>
                    <li :class="{ active: activeMenu === 'about' }" @click="activeMenu = 'about'">关于</li>
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
                <div v-if="activeMenu === 'password'" class="password-settings">
                    <h3 class="password-title">Web 访问密码</h3>
                    <div class="password-tip">
                        如果服务端配置了访问密码，请在此输入。留空表示不使用密码。
                    </div>
                    <div class="password-form-row">
                        <label class="password-label" for="web-access-password">访问密码：</label>
                        <el-input id="web-access-password" v-model="webAccessPassword" type="password"
                            placeholder="请输入 Web 访问密码" class="password-input" show-password clearable />
                    </div>
                    <div class="save-btn-row password-save-btn-row">
                        <el-button type="primary" @click="savePassword">保存</el-button>
                        <span v-if="passwordSaveSuccess" class="save-success-msg">已保存！</span>
                    </div>
                </div>
                <div v-if="activeMenu === 'other'" class="other-settings">
                    <h3 class="other-title">其他设置</h3>
                    <div class="other-form-list">
                        <div class="other-form-row">
                            <label class="other-label" for="max-records">前端允许保存记录的最大数量：</label>
                            <el-input-number id="max-records" v-model="maxRecords" :min="1" :max="100" :step="1"
                                class="max-records-input" controls-position="right" />
                            <span class="other-tip align-tip">默认为 10，范围 1~100。</span>
                        </div>
                        <div class="other-form-row upload-size-row">
                            <label class="other-label" for="max-upload-size">前端允许最大上传文件大小：</label>
                            <el-input-number id="max-upload-size" v-model="maxUploadSize" :min="10" :max="1024"
                                :step="10" class="max-upload-size-input" controls-position="right" />
                            <span class="other-tip align-tip">
                                单位：MB，默认 200，范围 10~1024。
                            </span>
                        </div>
                        <transition name="fade-slide">
                            <div v-if="maxUploadSize > 200" class="warn-tip-row">
                                <el-icon style="margin-right: 6px; color: #e67e22;">
                                    <svg viewBox="0 0 1024 1024" width="18" height="18">
                                        <path fill="currentColor"
                                            d="M512 64C264.6 64 64 264.6 64 512s200.6 448 448 448 448-200.6 448-448S759.4 64 512 64zm0 820c-205.3 0-372-166.7-372-372S306.7 140 512 140s372 166.7 372 372-166.7 372-372 372zm-36-236h72v72h-72v-72zm0-360h72v288h-72V288z">
                                        </path>
                                    </svg>
                                </el-icon>
                                <span class="warn-tip-text">超过 <b>200M</b> 可能导致处理卡顿！</span>
                            </div>
                        </transition>
                        <!-- 未来可在此添加更多设置项 -->
                    </div>
                    <div class="save-btn-row other-save-btn-row">
                        <el-button type="primary" @click="saveOtherSettings">保存</el-button>
                        <span v-if="otherSaveSuccess" class="save-success-msg">已保存！</span>
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
import { ElRadioGroup, ElRadioButton, ElInput, ElButton, ElMessage, ElDialog, ElInputNumber } from 'element-plus'
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


function savePrompt() {
    prompts[selectedStyle.value] = currentPrompt.value
    setLocalPrompts(prompts)
    saveSuccess.value = true
    ElMessage.success('已保存到本地')
}

function getLocalPassword() {
    try {
        return localStorage.getItem('webAccessPassword') || ''
    } catch {
        return ''
    }
}

function setLocalPassword(password) {
    if (password) {
        localStorage.setItem('webAccessPassword', password)
    } else {
        localStorage.removeItem('webAccessPassword')
    }
}

const webAccessPassword = ref(getLocalPassword())
const passwordSaveSuccess = ref(false)

function savePassword() {
    setLocalPassword(webAccessPassword.value)
    passwordSaveSuccess.value = true
    ElMessage.success('密码已保存到本地')

    // 清除成功提示
    setTimeout(() => {
        passwordSaveSuccess.value = false
    }, 2000)
}

// 其他设置：前端保存记录最大数量
function getLocalMaxRecords() {
    try {
        const v = localStorage.getItem('maxRecords')
        if (v) {
            const n = parseInt(v)
            if (!isNaN(n) && n > 0) return n
        }
    } catch { }
    return 10
}
function setLocalMaxRecords(val) {
    localStorage.setItem('maxRecords', String(val))
}

// 新增：前端允许最大上传文件大小
function getLocalMaxUploadSize() {
    try {
        const v = localStorage.getItem('maxUploadSize')
        if (v) {
            const n = parseInt(v)
            if (!isNaN(n) && n >= 10) return n
        }
    } catch { }
    return 200
}
function setLocalMaxUploadSize(val) {
    localStorage.setItem('maxUploadSize', String(val))
}

const maxRecords = ref(getLocalMaxRecords())
const maxUploadSize = ref(getLocalMaxUploadSize())
const maxRecordsSaveSuccess = ref(false)
const otherSaveSuccess = ref(false)

function saveMaxRecords() {
    setLocalMaxRecords(maxRecords.value)
    maxRecordsSaveSuccess.value = true
    ElMessage.success('已保存到本地')
    setTimeout(() => {
        maxRecordsSaveSuccess.value = false
    }, 2000)
}

// 新增：保存所有“其他设置”
function saveOtherSettings() {
    setLocalMaxRecords(maxRecords.value)
    setLocalMaxUploadSize(maxUploadSize.value)
    otherSaveSuccess.value = true
    ElMessage.success('已保存到本地')
    setTimeout(() => {
        otherSaveSuccess.value = false
    }, 2000)
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
    min-width: 260px;
    min-height: 320px;
    background: #fff;
    border-radius: 0 12px 12px 0;
    /* 新增：让内容靠左显示 */
    justify-content: flex-start;
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

.password-settings {
    width: 420px;
    /* 固定宽度，左侧展示 */
    margin: 0;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: flex-start;
    background: #fff;
    border-radius: 8px;
    padding: 24px 32px 18px 32px;
    box-shadow: 0 2px 8px 0 rgba(60, 80, 120, 0.04);
    min-height: 220px;
}

.password-title {
    font-size: 1.18rem;
    font-weight: 700;
    margin: 0 0 12px 0;
    color: #23272f;
    letter-spacing: 0.2px;
    align-self: flex-start;
    /* 左对齐 */
}

.password-tip {
    color: #6b7280;
    font-size: 0.97rem;
    margin-bottom: 22px;
    line-height: 1.7;
    text-align: left;
    background: #f8f9fa;
    border-left: 4px solid #d1d5db;
    padding: 8px 14px;
    border-radius: 4px;
    width: 100%;
    align-self: flex-start;
    /* 左对齐 */
}

.password-form-row {
    display: flex;
    align-items: center;
    width: 100%;
    margin-bottom: 18px;
    gap: 12px;
    justify-content: flex-start;
    /* 左对齐 */
}

.password-label {
    font-size: 1.03rem;
    font-weight: 600;
    color: #23272f;
    min-width: 84px;
    text-align: right;
    margin-bottom: 0;
    letter-spacing: 0.1px;
}

.password-input {
    flex: 1;
    max-width: 240px;
    min-width: 120px;
}

.password-save-btn-row {
    margin-top: 6px;
    display: flex;
    align-items: center;
    gap: 14px;
    align-self: flex-start;
    /* 左对齐 */
}

.other-settings {
    width: 100%;
    max-width: 900px;
    margin: 0;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: flex-start;
    background: #fff;
    border-radius: 8px;
    padding: 32px 40px 24px 40px;
    box-shadow: 0 2px 8px 0 rgba(60, 80, 120, 0.04);
    min-height: 120px;
    box-sizing: border-box;
}

.other-title {
    font-size: 1.18rem;
    font-weight: 700;
    margin: 0 0 18px 0;
    color: #23272f;
    letter-spacing: 0.2px;
    align-self: flex-start;
}

.other-form-list {
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 0;
}

.other-form-row {
    display: flex;
    align-items: center;
    width: 100%;
    min-height: 48px;
    margin-bottom: 0;
    gap: 18px;
    border-bottom: 1px solid #f0f1f3;
    padding: 8px 0;
    background: transparent;
    transition: background 0.18s;
}

.other-form-row.upload-size-row {
    border-bottom: none;
    margin-bottom: 0;
    padding-bottom: 0;
}

.other-form-row:last-child {
    border-bottom: none;
}

.other-label {
    font-size: 1.03rem;
    font-weight: 600;
    color: #23272f;
    text-align: right;
    margin-bottom: 0;
    letter-spacing: 0.1px;
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: flex-end;
}

.max-records-input,
.max-upload-size-input {
    width: 120px;
    margin-right: 8px;
    border-radius: 6px;
    background: #f7f8fa;
    border: 1.5px solid #e3e6ef;
    font-size: 1.01rem;
    transition: border-color 0.18s;
}

.max-records-input:focus-within,
.max-upload-size-input:focus-within {
    border-color: #357aff;
}

.other-tip {
    color: #6b7280;
    font-size: 0.97rem;
    flex: 1;
    text-align: left;
    min-width: 160px;
    white-space: nowrap;
    display: flex;
    align-items: center;
    background: transparent;
}

.align-tip {
    align-items: center;
}

.warn-tip-row {
    display: flex;
    align-items: center;
    margin-left: 228px;
    margin-top: 2px;
    margin-bottom: 8px;
    font-size: 1.01rem;
    color: #e67e22;
    background: #fffbe6;
    border-left: 4px solid #ffd666;
    border-radius: 4px;
    padding: 6px 16px;
    font-weight: 600;
    box-shadow: 0 1px 4px 0 rgba(60, 80, 120, 0.04);
    max-width: 420px;
    animation: fadeIn 0.3s;
}

.warn-tip-text b {
    color: #e67e22;
    font-weight: 700;
}

.fade-slide-enter-active,
.fade-slide-leave-active {
    transition: all 0.25s cubic-bezier(.55, 0, .1, 1);
}

.fade-slide-enter-from,
.fade-slide-leave-to {
    opacity: 0;
    transform: translateY(-8px);
}

.fade-slide-enter-to,
.fade-slide-leave-from {
    opacity: 1;
    transform: translateY(0);
}
</style>
