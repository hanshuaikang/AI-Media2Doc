<script setup>
import { ElInput, ElPopover, ElInputNumber, ElIcon, ElTooltip } from 'element-plus'
import { Operation, QuestionFilled } from '@element-plus/icons-vue'
import { ref, watch } from 'vue'

const props = defineProps({
    modelValue: {
        type: String,
        default: ''
    },
    placeholder: {
        type: String,
        default: '你可以添加备注在默认提示词的基础上实现更加个性化的输出, 例如: 输出更详细一些'
    },
    disabled: {
        type: Boolean,
        default: false
    },
    rows: {
        type: Number,
        default: 3
    },
    timeout: {
        type: Number,
        default: 120
    },
    maxTokens: {
        type: Number,
        default: 8192
    }
})

const emit = defineEmits(['update:modelValue', 'update:timeout', 'update:maxTokens'])

// 从 localStorage 获取存储的值，如果没有则使用 props 的默认值
const getStoredValue = (key, defaultValue) => {
    try {
        const stored = localStorage.getItem(key)
        return stored ? JSON.parse(stored) : defaultValue
    } catch {
        return defaultValue
    }
}

// 存储值到 localStorage
const setStoredValue = (key, value) => {
    try {
        localStorage.setItem(key, JSON.stringify(value))
    } catch (error) {
        console.warn('Failed to save to localStorage:', error)
    }
}

const localValue = ref(props.modelValue || '')
const localTimeout = ref(getStoredValue('llm.timeout', props.timeout))
const localMaxTokens = ref(getStoredValue('llm.max_tokens', props.maxTokens))
const showSettings = ref(false)

watch(() => props.modelValue, (newVal) => {
    localValue.value = newVal
})

watch(() => props.timeout, (newVal) => {
    localTimeout.value = newVal
})

watch(() => props.maxTokens, (newVal) => {
    localMaxTokens.value = newVal
})

const handleInput = (val) => {
    emit('update:modelValue', val)
}

const handleTimeoutChange = (val) => {
    setStoredValue('llm.timeout', val)
    emit('update:timeout', val)
}

const handleMaxTokensChange = (val) => {
    setStoredValue('llm.max_tokens', val)
    emit('update:maxTokens', val)
}
</script>

<template>
    <div class="remarks-wrapper">
        <div class="textarea-container">
            <el-input v-model="localValue" type="textarea" :placeholder="placeholder" :rows="rows" :disabled="disabled"
                @input="handleInput" class="remarks-input" resize="none" />

            <!-- 内嵌在文本框左下角的设置按钮 -->
            <el-popover placement="bottom-start" :width="300" trigger="click" v-model:visible="showSettings"
                :disabled="disabled" popper-class="settings-popover" :offset="8" :teleported="false" :popper-options="{
                    strategy: 'absolute',
                    modifiers: [
                        {
                            name: 'flip',
                            enabled: false
                        }
                    ]
                }">
                <template #reference>
                    <div class="settings-trigger" :class="{ disabled: disabled }">
                        <el-icon class="settings-icon">
                            <Operation />
                        </el-icon>
                        <span class="settings-text">生成设置</span>
                    </div>
                </template>

                <div class="settings-popover-content">
                    <div class="settings-title-header">生成参数配置</div>

                    <div class="setting-row">
                        <label class="setting-label">超时时间 (s):</label>
                        <el-input-number v-model="localTimeout" :min="30" :max="600" :step="10"
                            @change="handleTimeoutChange" size="small" />
                    </div>

                    <div class="setting-row">
                        <div class="setting-label-with-tooltip">
                            <label class="setting-label">Max Tokens
                                <el-tooltip content="Max Tokens 表示模型输出的丰富度, 越大表示内容越丰富 具体的值请参考对应的模型服务商说明。"
                                    placement="top" :show-after="300">
                                    <el-icon class="tooltip-icon">
                                        <QuestionFilled />
                                    </el-icon>
                                </el-tooltip>:
                            </label>
                        </div>
                        <el-input-number v-model="localMaxTokens" :min="1024" :max="32768" :step="4096"
                            @change="handleMaxTokensChange" size="small" />
                    </div>
                </div>
            </el-popover>
        </div>
    </div>
</template>

<style scoped>
.remarks-wrapper {
    width: 93%;
    margin-bottom: 3rem;
    margin-top: 0;
    position: relative;
    overflow: visible;
}

.textarea-container {
    position: relative;
    width: 100%;
}

.remarks-input {
    width: 100%;
}

.settings-trigger {
    position: absolute;
    bottom: 8px;
    left: 12px;
    display: flex;
    align-items: center;
    gap: 4px;
    color: #9ca3af;
    font-size: 0.85rem;
    cursor: pointer;
    padding: 4px 8px;
    border-radius: 6px;
    transition: all 0.18s;
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(4px);
    z-index: 10;
    border: 1px solid transparent;
}

.settings-trigger:hover:not(.disabled) {
    color: #6b7280;
    background: rgba(255, 255, 255, 1);
    border-color: #e5e7eb;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.settings-trigger.disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.settings-icon {
    font-size: 0.9em;
}

.settings-text {
    font-weight: 500;
    letter-spacing: 0.1px;
}

:deep(.remarks-input .el-textarea__inner) {
    background: #f7f8fa !important;
    border: 1.5px solid #f2f3f5 !important;
    border-radius: 14px !important;
    padding: 16px 20px 32px 20px !important;
    font-size: 1.01rem !important;
    color: #23272f !important;
    transition: border-color 0.18s, box-shadow 0.18s !important;
    resize: none !important;
    font-family: inherit !important;
    line-height: 1.5 !important;
    box-shadow: 0 2px 10px 0 rgba(60, 80, 120, 0.04) !important;
}

:deep(.remarks-input .el-textarea__inner:focus) {
    border-color: #23272f !important;
    box-shadow: 0 0 0 2px rgba(35, 39, 47, 0.1), 0 2px 10px 0 rgba(60, 80, 120, 0.04) !important;
    outline: none !important;
}

:deep(.remarks-input .el-textarea__inner::placeholder) {
    color: #9ca3af !important;
    font-size: 0.98rem !important;
    line-height: 1.5 !important;
}

:deep(.remarks-input .el-textarea__inner:disabled) {
    background: #f3f4f6 !important;
    color: #9ca3af !important;
    cursor: not-allowed !important;
    border-color: #e5e7eb !important;
}
</style>

<!-- 全局样式，用于自定义 popover -->
<style>
.settings-popover {
    padding: 0 !important;
    border: 1px solid #e5e7eb !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 24px rgba(0, 0, 0, 0.12) !important;
    background: #fff !important;
}

.settings-popover-content {
    padding: 20px;
}

.settings-title-header {
    font-size: 1rem;
    font-weight: 600;
    color: #1f2937;
    margin-bottom: 16px;
    padding-bottom: 8px;
    border-bottom: 1px solid #f3f4f6;
}

.setting-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    margin-bottom: 16px;
}

.setting-row:last-child {
    margin-bottom: 0;
}

.setting-label {
    font-size: 0.9rem;
    color: #4b5563;
    font-weight: 500;
    min-width: 120px;
    text-align: left;
    white-space: nowrap;
}

.setting-label-with-tooltip {
    display: flex;
    align-items: center;
    gap: 4px;
}

.tooltip-icon {
    font-size: 0.8rem;
    color: #9ca3af;
    cursor: pointer;
    transition: color 0.2s;
}

.tooltip-icon:hover {
    color: #6b7280;
}
</style>
