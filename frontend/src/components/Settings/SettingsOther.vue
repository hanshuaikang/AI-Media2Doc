<template>
    <div class="other-settings">
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
                <el-input-number id="max-upload-size" v-model="maxUploadSize" :min="10" :max="1024" :step="10"
                    class="max-upload-size-input" controls-position="right" />
                <span class="other-tip align-tip">
                    单位：MB，默认 200，范围 10~1024。
                </span>
            </div>
            <div class="other-form-row polling-row">
                <label class="other-label" for="max-polling-attempts">最大轮询次数：</label>
                <el-input-number id="max-polling-attempts" v-model="maxPollingAttempts" :min="10" :max="1000" :step="10"
                    class="max-polling-attempts-input" controls-position="right" />
                <span class="other-tip align-tip">
                    默认 60，范围 10~1000。用于音频转文字任务轮询。
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
    border-bottom: 1px solid #f0f1f3;
    margin-bottom: 0;
    padding-bottom: 8px;
}

.other-form-row.polling-row {
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
.max-upload-size-input,
.max-polling-attempts-input {
    width: 120px;
    margin-right: 8px;
    border-radius: 6px;
    background: #f7f8fa;
    border: 1.5px solid #e3e6ef;
    font-size: 1.01rem;
    transition: border-color 0.18s;
}

.max-records-input:focus-within,
.max-upload-size-input:focus-within,
.max-polling-attempts-input:focus-within {
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
