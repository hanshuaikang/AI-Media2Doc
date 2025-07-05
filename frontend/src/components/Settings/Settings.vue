<template>
    <el-dialog v-model="visible" title="自定义配置" width="50vw" class="settings-dialog" :close-on-click-modal="false"
        :close-on-press-escape="true" :show-close="true" @close="handleClose">
        <div class="settings-dialog-body">
            <div class="settings-sidebar">
                <ul>
                    <li :class="{ active: activeMenu === 'style' }" @click="activeMenu = 'style'">风格设置</li>
                    <li :class="{ active: activeMenu === 'password' }" @click="activeMenu = 'password'">访问密码</li>
                    <li :class="{ active: activeMenu === 'screenshot' }" @click="activeMenu = 'screenshot'">智能截图</li>
                    <li :class="{ active: activeMenu === 'other' }" @click="activeMenu = 'other'">其他设置</li>
                    <li :class="{ active: activeMenu === 'about' }" @click="activeMenu = 'about'">关于</li>
                </ul>
            </div>
            <div class="settings-content">
                <SettingsStyle v-if="activeMenu === 'style'" />
                <SettingsPassword v-if="activeMenu === 'password'" />
                <SettingsScreenshot v-if="activeMenu === 'screenshot'" />
                <SettingsOther v-if="activeMenu === 'other'" />
                <SettingsAbout v-if="activeMenu === 'about'" />
            </div>
        </div>
    </el-dialog>
</template>

<script setup>
import { ref, watch, defineProps, defineEmits } from 'vue'
import SettingsStyle from './SettingsStyle.vue'
import SettingsPassword from './SettingsPassword.vue'
import SettingsScreenshot from './SettingsScreenshot.vue'
import SettingsOther from './SettingsOther.vue'
import SettingsAbout from './SettingsAbout.vue'

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

const activeMenu = ref('style')
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
    justify-content: flex-start;
}
</style>
