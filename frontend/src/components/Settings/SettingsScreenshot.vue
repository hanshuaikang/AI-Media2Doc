<template>
    <div class="screenshot-settings">
        <h3 class="screenshot-title">智能截图设置</h3>
        <div class="screenshot-tip">
            智能截图功能可以自动为生成的内容添加相关图片，提升视觉效果。
        </div>
        <div class="screenshot-form-row">
            <label class="screenshot-label">启用智能截图：</label>
            <el-switch v-model="smartScreenshotEnabled" size="default" active-text="开启" inactive-text="关闭"
                class="screenshot-switch" />
        </div>
        <transition name="fade-slide">
            <div v-if="smartScreenshotEnabled" class="screenshot-warn-tip-row">
                <el-icon style="margin-right: 6px; color: #e67e22;">
                    <svg viewBox="0 0 1024 1024" width="18" height="18">
                        <path fill="currentColor"
                            d="M512 64C264.6 64 64 264.6 64 512s200.6 448 448 448 448-200.6 448-448S759.4 64 512 64zm0 820c-205.3 0-372-166.7-372-372S306.7 140 512 140s372 166.7 372 372-166.7 372-372 372zm-36-236h72v72h-72v-72zm0-360h72v288h-72V288z">
                        </path>
                    </svg>
                </el-icon>
                <span class="screenshot-warn-tip-text">开启之后生成图文等待时间会变长，仅支持一小时内的视频, 请谨慎开启</span>
            </div>
        </transition>
        <div class="save-btn-row screenshot-save-btn-row">
            <el-button type="primary" @click="saveScreenshotSettings">保存</el-button>
            <span v-if="screenshotSaveSuccess" class="save-success-msg">已保存！</span>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElSwitch, ElButton, ElMessage } from 'element-plus'

function getLocalSmartScreenshot() {
    try {
        const v = localStorage.getItem('smartScreenshotEnabled')
        return v === 'true'
    } catch {
        return false
    }
}
function setLocalSmartScreenshot(enabled) {
    localStorage.setItem('smartScreenshotEnabled', String(enabled))
}
const smartScreenshotEnabled = ref(getLocalSmartScreenshot())
const screenshotSaveSuccess = ref(false)

function saveScreenshotSettings() {
    setLocalSmartScreenshot(smartScreenshotEnabled.value)
    screenshotSaveSuccess.value = true
    ElMessage.success('智能截图设置已保存到本地')
    setTimeout(() => {
        screenshotSaveSuccess.value = false
    }, 2000)
}
</script>

<style scoped>
.screenshot-settings {
    width: 480px;
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

.screenshot-title {
    font-size: 1.18rem;
    font-weight: 700;
    margin: 0 0 12px 0;
    color: #23272f;
    letter-spacing: 0.2px;
    align-self: flex-start;
}

.screenshot-tip {
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
}

.screenshot-form-row {
    display: flex;
    align-items: center;
    width: 100%;
    margin-bottom: 18px;
    gap: 12px;
    justify-content: flex-start;
}

.screenshot-label {
    font-size: 1.03rem;
    font-weight: 600;
    color: #23272f;
    min-width: 120px;
    text-align: right;
    margin-bottom: 0;
    letter-spacing: 0.1px;
}

.screenshot-switch {
    margin-left: 8px;
}

.screenshot-warn-tip-row {
    display: flex;
    align-items: center;
    margin-top: 2px;
    margin-bottom: 8px;
    font-size: 1.01rem;
    color: #e67e22;
    background: #fffbe6;
    border-left: 4px solid #ffd666;
    border-radius: 4px;
    padding: 8px 16px;
    font-weight: 600;
    box-shadow: 0 1px 4px 0 rgba(60, 80, 120, 0.04);
    width: 100%;
    align-self: flex-start;
    text-align: left;
    /* 新增：左对齐 */
}

.screenshot-warn-tip-text {
    color: #e67e22;
    font-weight: 600;
    text-align: left;
    /* 新增：左对齐 */
}

.screenshot-save-btn-row {
    margin-top: 6px;
    display: flex;
    align-items: center;
    gap: 14px;
    align-self: flex-start;
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
