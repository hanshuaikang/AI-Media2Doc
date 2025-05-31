<script setup>
import { ref, onMounted, watch, onBeforeUnmount } from 'vue'
import { ElMenu, ElMenuItem, ElAvatar, ElTag, ElIcon, ElEmpty, ElMessage, ElMessageBox } from 'element-plus'
import { VideoCameraFilled, Tickets, Document, Plus, ArrowRight, Delete } from '@element-plus/icons-vue'
import { getAllTasks, deleteTask } from '../utils/db'
import { eventBus } from '../utils/eventBus'
import Settings from './Settings/Settings.vue'

const props = defineProps({
    activeMenu: {
        type: String,
        default: 'new-task'
    }
})

const emit = defineEmits(['menu-select', 'view-task', 'chat'])

const handleSelect = (key) => {
    if (key === 'settings') {
        showSettingsDialog.value = true
        return
    }
    if (key.startsWith('task-')) {
        const taskId = parseInt(key.replace('task-', ''))
        const task = recentTasks.value.find(t => t.id === taskId)
        if (task) {
            emit('view-task', task)
        }
        return
    }

    emit('menu-select', key)
}

const recentTasks = ref([])
const isTasksLoading = ref(false)
const showHistoryTasks = ref(true)
const isInitialLoad = ref(true)
const showSettingsDialog = ref(false)

const styleMap = {
    note: { name: '知识笔记', color: '#409EFF' }, // 蓝色
    summary: { name: '内容总结', color: '#67C23A' }, // 绿色
    xiaohongshu: { name: '小红书风格', color: '#FE2C55' }, // 红色
    wechat: { name: '公众号风格', color: '#07C160' }, // 微信绿
    mind: { name: '思维导图', color: '#8E93F2' } // 紫色
}

const getStyleInfo = (style) => {
    return styleMap[style] || { name: style || '未知类型', color: '#909399' }
}

const loadRecentTasks = async () => {
    // 防止重复加载或循环加载
    if (isTasksLoading.value) return

    isTasksLoading.value = true
    try {
        const allTasks = await getAllTasks()
        console.log('所有任务:', allTasks)
        // 按创建时间倒序排序并获取前5条
        recentTasks.value = allTasks
            .sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt))
            .slice(0, 10)

    } catch (error) {
        console.error('加载历史任务失败:', error)
        ElMessage.error('加载历史任务失败')
    } finally {
        isTasksLoading.value = false
        console.log('加载历史任务完成')
    }
}

const toggleHistoryTasks = () => {
    showHistoryTasks.value = !showHistoryTasks.value
}

onMounted(() => {
    loadRecentTasks()
    isInitialLoad.value = false
})

watch(showHistoryTasks, (newVal, oldVal) => {
    if (newVal === true && oldVal === false && !isInitialLoad.value) {
        loadRecentTasks()
    }
}, { flush: 'post' })

const refreshTasksOnUpdate = () => {
    console.log('检测到新任务，刷新历史列表')
    loadRecentTasks()
}

onMounted(() => {
    loadRecentTasks()
    isInitialLoad.value = false

    eventBus.on('task-updated', refreshTasksOnUpdate)
})

onBeforeUnmount(() => {
    eventBus.off('task-updated', refreshTasksOnUpdate)
})

const handleDeleteTask = async (event, task) => {
    event.stopPropagation();

    try {
        await ElMessageBox.confirm(
            '确定要删除此任务记录吗？此操作不可撤销。',
            '删除确认',
            {
                confirmButtonText: '确定删除',
                cancelButtonText: '取消',
                type: 'warning',
                // confirmButtonClass: 'el-button--danger el-button--borderless'
            }
        );

        await deleteTask(task.id);

        recentTasks.value = recentTasks.value.filter(t => t.id !== task.id);

        ElMessage.success('已删除任务记录');

        eventBus.emit('task-updated');
    } catch (error) {
        if (error !== 'cancel') {
            console.error('删除任务失败:', error);
            ElMessage.error('删除失败，请重试');
        }
    }
};
</script>

<template>
    <div class="app-sidebar">
        <!-- 头像和应用名称区域 -->
        <div class="app-logo">
            <div class="logo-container">
                <!-- 纯白色 logo 区域 -->
                <img src="/src/assets/logo.png" alt="Logo" class="app-logo-img" />
            </div>
            <div class="app-title">
                <h3>AI-Media2Doc</h3>
                <div class="app-subtitle">一键音视频转文档</div>
            </div>
        </div>

        <!-- 导航菜单 -->
        <el-menu :default-active="activeMenu" class="sidebar-menu" @select="handleSelect">
            <el-menu-item index="new-task" class="menu-item">
                <div class="menu-item-content">
                    <el-icon class="menu-icon-new">
                        <Plus />
                    </el-icon>
                    <span>新建任务</span>
                </div>
            </el-menu-item>

            <!-- 历史任务菜单项 -->
            <div class="history-section">
                <div class="history-header" @click="toggleHistoryTasks">
                    <div class="menu-item-content">
                        <el-icon class="menu-icon">
                            <Tickets />
                        </el-icon>
                        <span id="historyTaskText">历史任务</span>
                    </div>
                    <el-icon class="expand-icon" :class="{ 'is-expanded': showHistoryTasks }">
                        <ArrowRight />
                    </el-icon>
                </div>

                <!-- 历史任务子菜单 -->
                <div class="history-submenu" :class="{ 'is-expanded': showHistoryTasks }">
                    <div v-if="isTasksLoading" class="history-loading">
                        <span>加载中...</span>
                    </div>
                    <div v-else-if="recentTasks.length === 0" class="history-empty">
                        <span>暂无历史任务</span>
                    </div>
                    <div v-else class="history-list">
                        <div v-for="task in recentTasks" :key="task.id" class="history-item"
                            @click="handleSelect(`task-${task.id}`)">
                            <el-icon class="history-icon">
                                <Document />
                            </el-icon>
                            <div class="history-info">
                                <div class="history-title">{{ task.fileName || '未命名文件' }}</div>
                                <div class="history-meta">
                                    <el-tag size="small" effect="plain" :style="{
                                        background: getStyleInfo(task.contentStyle).color + '15' + ' !important',
                                        color: getStyleInfo(task.contentStyle).color + ' !important',
                                        border: '1px solid ' + getStyleInfo(task.contentStyle).color + '30' + ' !important'
                                    }">
                                        {{ getStyleInfo(task.contentStyle).name }}
                                    </el-tag>
                                </div>
                            </div>
                            <!-- 添加删除按钮 -->
                            <div class="history-actions" @click.stop>
                                <el-icon class="delete-icon" @click="handleDeleteTask($event, task)">
                                    <Delete />
                                </el-icon>
                            </div>
                        </div>
                        <!-- 移除查看全部历史链接 -->
                    </div>
                </div>
            </div>
        </el-menu>

        <!-- 设置按钮放在底部版权信息上方，脱离 el-menu -->
        <div class="sidebar-settings">
            <div class="settings-menu-item" @click="showSettingsDialog = true">
                <div class="settings-btn-content">
                    <el-icon class="menu-icon-settings">
                        <el-icon>
                            <svg viewBox="0 0 1024 1024" width="1em" height="1em">
                                <path
                                    d="M512 320a192 192 0 1 0 0 384 192 192 0 0 0 0-384zm0 320a128 128 0 1 1 0-256 128 128 0 0 1 0 256z"
                                    fill="#0057ff" />
                                <path
                                    d="M952 544h-56.8a376.8 376.8 0 0 0-16.8-64.8l40.8-40.8a40 40 0 0 0 0-56.8l-79.2-79.2a40 40 0 0 0-56.8 0l-40.8 40.8A376.8 376.8 0 0 0 544 128V71.6A39.6 39.6 0 0 0 504.4 32h-112.8A39.6 39.6 0 0 0 352 71.6V128a376.8 376.8 0 0 0-64.8 16.8l-40.8-40.8a40 40 0 0 0-56.8 0l-79.2 79.2a40 40 0 0 0 0 56.8l40.8 40.8A376.8 376.8 0 0 0 128 480H71.6A39.6 39.6 0 0 0 32 519.6v112.8A39.6 39.6 0 0 0 71.6 672H128a376.8 376.8 0 0 0 16.8 64.8l-40.8 40.8a40 40 0 0 0 0 56.8l79.2 79.2a40 40 0 0 0 56.8 0l40.8-40.8A376.8 376.8 0 0 0 480 896v56.4A39.6 39.6 0 0 0 519.6 992h112.8A39.6 39.6 0 0 0 672 952.4V896a376.8 376.8 0 0 0 64.8-16.8l40.8 40.8a40 40 0 0 0 56.8 0l79.2-79.2a40 40 0 0 0 0-56.8l-40.8-40.8A376.8 376.8 0 0 0 896 544h56.4A39.6 39.6 0 0 0 992 504.4v-112.8A39.6 39.6 0 0 0 952 544z"
                                    fill="#0057ff" />
                            </svg>
                        </el-icon>
                    </el-icon>
                    <span>自定义配置</span>
                </div>
            </div>
            <Settings v-model:visible="showSettingsDialog" />
        </div>

        <!-- 底部版权信息 -->
        <div class="sidebar-footer">
            <div class="footer-content">
                <p>© 2025 AI 视频图文创作助手</p>
            </div>
        </div>
    </div>
</template>

<style scoped>
.app-sidebar {
    height: 100vh;
    width: 260px;
    display: flex;
    flex-direction: column;
    position: fixed;
    left: 0;
    top: 0;
    z-index: 1000;
    background-color: #f7f8fa;
    /* 修改阴影为四周都明显 */
    box-shadow: 0 1px 8px 0px rgba(0, 0, 0, 0.06);
    overflow: hidden;
    transition: all 0.3s ease;
    border-right: 1.5px solid #f2f3f5;
}

.app-logo {
    padding: 28px 20px 18px 20px;
    display: flex;
    align-items: center;
    gap: 12px;
    border-bottom: 1.5px solid #f2f3f5;
    background: linear-gradient(to bottom, #fff 80%, #f7f8fa 100%);
}


.logo-container {
    width: 44px;
    height: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 12px;
    background: #fff;
    /* 纯白色背景 */
    box-shadow: none;
    /* 去除阴影 */
    overflow: hidden;
    position: relative;
    border: 1.5px solid #f2f3f5;
    /* 可选：加淡灰色边框以区分背景 */
}

/* 移除 logo-container::after 伪元素 */
.logo-container::after {
    display: none;
}

.app-logo-img {
    width: 32px;
    height: 32px;
    object-fit: contain;
    display: block;
    margin: auto;
    background: transparent;
    border-radius: 8px;
}

.sidebar-menu {
    flex: 1 1 auto;
    border-right: none;
    background-color: transparent;
    padding: 18px 0 0 0;
    overflow-y: auto;

}

.menu-icon-new {
    color: #0057ff;
}

.menu-item {
    height: auto !important;
    line-height: normal !important;
    padding: 0 !important;
    margin: 6px 14px !important;
    border-radius: 10px;
    transition: all 0.2s ease;
    overflow: hidden;
    background: #fff;
    border: 1px solid #f2f3f5;
    box-shadow: 0 1px 4px rgba(60, 80, 120, 0.04);

}

.menu-item-content {
    display: flex;
    align-items: center;
    padding: 13px 14px;
    gap: 10px;
    border-radius: 10px;
    transition: all 0.2s ease;
}

.menu-item-content span {
    font-size: 15px;
    font-weight: 600;
    color: #0057ff;
    letter-spacing: 0.1px;
}

.menu-icon {
    font-size: 19px;
    color: #444950;
    transition: all 0.2s ease;
}

.sidebar-menu :deep(.el-menu-item) {
    /* transition: all 0.2s ease; */
    min-height: auto;
    height: auto;
    background: transparent;
    border-radius: 10px;
    border: none;
    box-shadow: none;
    border: 1px solid #0057ff;
}

.sidebar-menu :deep(.el-menu-item.is-active) {
    background: rgba(0, 87, 255, 0.06);
    color: #0057ff;
    border-radius: 10px;
    /* font-weight: 700; */
    border: 1px solid #0057ff;
}

.sidebar-menu :deep(.el-menu-item.is-active) .menu-icon {
    color: #0057ff;
}

.sidebar-menu :deep(.el-menu-item:hover) {
    background-color: #d9e5f8;
    /* color: #e1681d; */
    /* transform: translateY(-1px); */
    /* box-shadow: 0 2px 8px rgba(60, 80, 120, 0.08); */
}

.sidebar-menu :deep(.el-menu-item:hover) .menu-icon {
    transform: scale(1.08);
}

.sidebar-menu :deep(.el-menu-item .el-icon) {
    margin-right: 0;
}

/* 历史任务区域样式 */
.history-section {
    margin: 10px 14px;
    border-radius: 10px;
    background-color: #fff;
    overflow: hidden;
    box-shadow: 0 1px 4px rgba(60, 80, 120, 0.04);
    border: 1px solid #f2f3f5;
}

.history-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-right: 12px;
    cursor: pointer;
    transition: all 0.2s ease;
    border-radius: 10px 10px 0 0;
    border-bottom: 1px solid #f2f3f5;
    /* background-color: #f7f8fa; */
}

.history-header:hover {
    background-color: #e9eaec;
}

.expand-icon {
    font-size: 15px;
    color: #909399;
    transition: transform 0.3s ease;
}

.expand-icon.is-expanded {
    transform: rotate(90deg);
}

.history-submenu {
    max-height: 0;
    overflow: hidden;
    transition: max-height 0.3s ease, opacity 0.3s ease;
    opacity: 0;
    margin-top: 0;
    background-color: #fff;
}

.history-submenu.is-expanded {
    max-height: 750px;
    overflow-y: auto;
    opacity: 1;
    padding: 5px 0;
    border-radius: 0 0 10px 10px;
    box-shadow: inset 0 1px 2px rgba(60, 80, 120, 0.02);
}

.history-loading,
.history-empty {
    padding: 15px;
    text-align: center;
    color: #909399;
    font-size: 13px;
    background-color: #f5f6fa;
    border-radius: 8px;
    margin: 8px;
}

.history-list {
    padding: 4px;
}

.history-item {
    display: flex;
    align-items: flex-start;
    padding: 10px 12px;
    cursor: pointer;
    border-radius: 8px;
    margin: 2px 4px;
    gap: 10px;
    transition: all 0.2s ease;
    background-color: #f7f8fa;
    border-left: 2px solid transparent;
    position: relative;
}

.history-item:hover {
    background-color: #f3f4f6;
    transform: translateX(2px);
    border-left: 2px solid #23272f;
}

.history-icon {
    font-size: 15px;
    color: #909399;
    margin-top: 2px;
    transition: all 0.2s ease;
}

.history-item:hover .history-icon {
    color: #23272f;
}

.history-info {
    flex: 1;
    min-width: 0;
    display: flex;
    flex-direction: column;
    gap: 6px;
    align-items: flex-start;
}

.history-title {
    font-size: 13px;
    color: #23272f;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    width: 100%;
    text-align: left;
    font-weight: 600;
}

.history-meta {
    display: flex;
    gap: 4px;
    width: 100%;
    justify-content: flex-start;
}

.history-meta :deep(.el-tag) {
    height: 20px;
    line-height: 18px;
    padding: 0 8px;
    font-size: 11px;
    font-weight: 500;
    border-radius: 4px;
    text-align: left;
    box-shadow: 0 1px 2px rgba(60, 80, 120, 0.04);
    background: #f5f6fa !important;
    border: 1px solid #e0e3e8 !important;
    color: #23272f !important;
}

.sidebar-footer {
    padding: 14px 16px;
    border-top: 1.5px solid #f2f3f5;
    background-color: #f7f8fa;
    text-align: center;
}

.footer-content {
    text-align: center;
}

.footer-content p {
    margin: 0;
    font-size: 11px;
    color: #909399;
    letter-spacing: 0.1px;
}

.app-title h3 {
    margin: 0;
    font-size: 17px;
    font-weight: 800;
    color: #23272f;
    letter-spacing: 0.5px;
    text-shadow: 0 1px 1px rgba(255, 255, 255, 0.7);
}

.app-subtitle {
    font-size: 12px;
    color: #909399;
    margin-top: 2px;
    font-weight: 00;
    letter-spacing: 0.2px;
    line-height: 1.2;
    text-align: left;
}

@media screen and (max-width: 768px) {
    .app-sidebar {
        width: 60px;
    }

    .app-title {
        display: none;
    }

    .menu-item-content span {
        display: none;
    }

    .expand-icon {
        display: none;
    }

    .history-header {
        padding-right: 0;
        justify-content: center;
    }

    .history-submenu {
        display: none;
    }

    .sidebar-footer {
        display: none;
    }

    .settings-menu-item {
        margin: 0 !important;
    }
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(5px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.history-item {
    animation: fadeIn 0.2s ease forwards;
}

.history-item:nth-child(2) {
    animation-delay: 0.05s;
}

.history-item:nth-child(3) {
    animation-delay: 0.1s;
}

.history-item:nth-child(4) {
    animation-delay: 0.15s;
}

.history-item:nth-child(5) {
    animation-delay: 0.2s;
}

.history-item:nth-child(6) {
    animation-delay: 0.25s;
}

.history-item:nth-child(7) {
    animation-delay: 0.3s;
}

.history-item:nth-child(8) {
    animation-delay: 0.35s;
}

.history-item:nth-child(9) {
    animation-delay: 0.4s;
}

.history-item:nth-child(10) {
    animation-delay: 0.45s;
}

.history-actions {
    opacity: 0;
    position: absolute;
    right: 8px;
    top: 50%;
    transform: translateY(-50%);
    transition: all 0.2s ease;
    background: rgba(250, 250, 250, 0.9);
    border-radius: 4px;
    padding: 3px;
}

.history-item:hover .history-actions {
    opacity: 1;
}

#historyTaskText {
    color: #23272f !important;
}

.delete-icon {
    color: #f56c6c;
    font-size: 14px;
    cursor: pointer;
    padding: 3px;
    border-radius: 4px;
    transition: all 0.2s ease;
}

.delete-icon:hover {
    color: #ff4d4f;
    background-color: rgba(245, 108, 108, 0.1);
    transform: scale(1.1);
}

.sidebar-settings {
    width: 100%;
    padding: 0 0 12px 0;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.settings-menu-item {
    width: 92%;
    margin: 0 auto 10px auto !important;
    background: #fff;
    border: 1.5px solid #f2f3f5;
    border-radius: 10px;
    box-shadow: 0 1px 4px rgba(60, 80, 120, 0.04);
    cursor: pointer;
    transition: all 0.18s;
    padding: 0;
    display: flex;
    align-items: center;
    justify-content: center;
}

.settings-menu-item:hover {
    background: #f0f6ff;
    border-color: #0057ff;
    box-shadow: 0 2px 8px rgba(0, 87, 255, 0.07);
}

.settings-btn-content {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 9px;
    padding: 13px 0;
    border-radius: 10px;
}

.settings-btn-content span {
    font-size: 15px;
    font-weight: 700;
    color: #0057ff;
    letter-spacing: 0.1px;
}

.menu-icon-settings {
    color: #0057ff;
    font-size: 18px;
    display: flex;
    align-items: center;
}
</style>

<style>
/* 删除确认按钮移除边框 */
.el-message-box__btns .el-button--danger {
    border-color: transparent !important;
}
</style>
