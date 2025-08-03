<template>
    <div class="other-settings">
        <h3 class="other-title">其他设置</h3>
        <div class="other-form-list">
            <div class="other-form-row">
                <div class="form-content">
                    <label class="other-label" for="max-records">前端允许保存记录的最大数量：</label>
                    <el-input-number id="max-records" v-model="maxRecords" :min="1" :max="100" :step="1"
                        class="max-records-input" controls-position="right" />
                </div>
                <div class="form-tip">
                    <span class="other-tip">默认为 10，范围 1~100。</span>
                </div>
            </div>
            <div class="other-form-row upload-size-row">
                <div class="form-content">
                    <label class="other-label" for="max-upload-size">前端允许最大上传文件大小：</label>
                    <el-input-number id="max-upload-size" v-model="maxUploadSize" :min="10" :max="1024" :step="10"
                        class="max-upload-size-input" controls-position="right" />
                </div>
                <div class="form-tip">
                    <span class="other-tip">单位：MB，默认 200，范围 10~1024。</span>
                </div>
            </div>
            <div class="other-form-row polling-row">
                <div class="form-content">
                    <label class="other-label" for="max-polling-attempts">最大轮询次数：</label>
                    <el-input-number id="max-polling-attempts" v-model="maxPollingAttempts" :min="10" :max="1000"
                        :step="10" class="max-polling-attempts-input" controls-position="right" />
                </div>
                <div class="form-tip">
                    <span class="other-tip">默认 60，范围 10~1000。用于音频转文字任务轮询。</span>
                </div>
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
        </div>
        <div class="save-btn-row other-save-btn-row">
            <el-button type="primary" @click="saveOtherSettings">保存</el-button>
            <span v-if="otherSaveSuccess" class="save-success-msg">已保存！</span>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElInputNumber, ElButton, ElMessage } from 'element-plus'

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
function getLocalMaxPollingAttempts() {
    try {
        const v = localStorage.getItem('maxPollingAttempts')
        if (v) {
            const n = parseInt(v)
            if (!isNaN(n) && n >= 10) return n
        }
    } catch { }
    return 60
}
function setLocalMaxPollingAttempts(val) {
    localStorage.setItem('maxPollingAttempts', String(val))
}
const maxRecords = ref(getLocalMaxRecords())
const maxUploadSize = ref(getLocalMaxUploadSize())
const maxPollingAttempts = ref(getLocalMaxPollingAttempts())
const otherSaveSuccess = ref(false)

function saveOtherSettings() {
    setLocalMaxRecords(maxRecords.value)
    setLocalMaxUploadSize(maxUploadSize.value)
    setLocalMaxPollingAttempts(maxPollingAttempts.value)
    otherSaveSuccess.value = true
    ElMessage.success('已保存到本地')
    setTimeout(() => {
        otherSaveSuccess.value = false
    }, 2000)
}
</script>

<style scoped>
.other-settings {
    width: 100%;
    max-width: 700px;
    margin: 0;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: flex-start;
    background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
    border-radius: 12px;
    padding: 24px 32px 24px 32px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    min-height: 120px;
    box-sizing: border-box;
    border: 1px solid #e2e8f0;
}

.other-title {
    font-size: 18px;
    font-weight: 700;
    margin: 0 0 20px 0;
    color: #1e293b;
    letter-spacing: 0.2px;
    align-self: flex-start;
    display: flex;
    align-items: center;
    gap: 8px;
}

.other-title::before {
    content: '';
    width: 4px;
    height: 18px;
    background: linear-gradient(135deg, #3b82f6, #8b5cf6);
    border-radius: 2px;
}

.other-form-list {
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 0;
}

.other-form-row {
    display: flex;
    flex-direction: column;
    width: 100%;
    min-height: 80px;
    margin-bottom: 12px;
    background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #e2e8f0;
    transition: all 0.2s ease;
}

.other-form-row:hover {
    background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
    border-color: #3b82f6;
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.1);
}

.other-form-row.upload-size-row {
    margin-bottom: 12px;
}

.other-form-row.polling-row {
    margin-bottom: 0;
}

.other-form-row:last-child {
    margin-bottom: 0;
}

.form-content {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 8px;
}

.form-tip {
    margin-top: 4px;
}

.other-label {
    font-size: 15px;
    font-weight: 600;
    color: #1e293b;
    text-align: left;
    margin-bottom: 0;
    letter-spacing: 0.1px;
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: flex-start;
    min-width: 200px;
}

.max-records-input,
.max-upload-size-input,
.max-polling-attempts-input {
    width: 120px;
    margin-right: 8px;
    border-radius: 8px;
    background: white;
    border: 2px solid #e2e8f0;
    font-size: 14px;
    transition: all 0.2s ease;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.max-records-input:focus-within,
.max-upload-size-input:focus-within,
.max-polling-attempts-input:focus-within {
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.other-tip {
    color: #64748b;
    font-size: 13px;
    text-align: left;
    line-height: 1.5;
    display: flex;
    align-items: flex-start;
    background: rgba(148, 163, 184, 0.1);
    padding: 8px 12px;
    border-radius: 6px;
    border-left: 3px solid #94a3b8;
    word-break: break-word;
    white-space: normal;
}

.align-tip {
    align-items: flex-start;
}

.warn-tip-row {
    display: flex;
    align-items: center;
    margin-top: 8px;
    margin-bottom: 8px;
    font-size: 13px;
    color: #d97706;
    background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
    border-left: 4px solid #f59e0b;
    border-radius: 8px;
    padding: 12px 16px;
    font-weight: 500;
    box-shadow: 0 2px 8px rgba(245, 158, 11, 0.1);
    animation: fadeIn 0.3s;
}

.warn-tip-text b {
    color: #d97706;
    font-weight: 700;
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
