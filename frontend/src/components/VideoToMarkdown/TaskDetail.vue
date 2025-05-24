<script setup>
import { ref, computed } from 'vue'
import ChatPanel from './ChatPanel.vue'
import TranscriptionPanel from './TranscriptionPanel.vue'
import GeneratedContentPanel from './GeneratedContentPanel.vue'
import { ChatDotRound } from '@element-plus/icons-vue'

const props = defineProps({
    task: {
        type: Object,
        required: true
    }
})

const emit = defineEmits(['back'])


const chatPanelKey = computed(() => `chat-panel-${props.task.id}`)

const showChatPanel = ref(false)
const openChatPanel = () => { showChatPanel.value = true }
const closeChatPanel = () => { showChatPanel.value = false }
</script>

<template>
    <div class="task-detail-page">
        <div class="detail-container">
            <!-- 左侧：生成图文 -->
            <div class="left-panel">
                <GeneratedContentPanel :content="task.markdownContent" :taskId="task.id" />
            </div>
            <!-- 右侧：会议对话 -->
            <div class="right-panel">
                <TranscriptionPanel :transcription="task.transcriptionText" />
            </div>
        </div>

        <!-- 悬浮AI助手按钮 -->
        <div class="floating-ai-btn">
            <el-button type="primary" :icon="ChatDotRound" circle size="medium" @click="openChatPanel" title="AI智能助手" />
        </div>
        <!-- AI助手抽屉/侧边栏 -->
        <div v-if="showChatPanel" class="chat-panel-overlay" @click.self="closeChatPanel">
            <ChatPanel :task="task" :embedded="false" :key="chatPanelKey" @close="closeChatPanel" />
        </div>
    </div>
</template>

<style>
#mindMapContainer * {
    margin: 0;
    padding: 0;
}

/* 确保Markdown内容左对齐 */
.markdown-content * {
    text-align: left !important;
}

.markdown-content ul,
.markdown-content ol {
    padding-left: 2em;
    margin: 0.5em 0;
}

.markdown-content p,
.markdown-content h1,
.markdown-content h2,
.markdown-content h3,
.markdown-content h4 {
    margin: 0.5em 0;
}
</style>

<style scoped>
.task-detail-page {
    width: 80%;
    margin: 0 auto;
    height: 96vh;
    display: flex;
    flex-direction: column;
    box-sizing: border-box;
    overflow: hidden;
}

.detail-container {
    display: flex;
    gap: 20px;
    width: 100%;
    height: 100%;
    box-sizing: border-box;
    padding: 20px 0;
    overflow: hidden;
}

.left-panel {
    flex: 7;
    /* 占据 70% 宽度 */
    height: 100%;
    display: flex;
    flex-direction: column;
    overflow: hidden;
}

.right-panel {
    flex: 3;
    /* 占据 30% 宽度 */
    height: 100%;
    display: flex;
    flex-direction: column;
    overflow: hidden;
}

.text-card.full-height {
    height: 100%;
    display: flex;
    flex-direction: column;
}

.text-card.full-height .original-text-content.markdown-content-area {
    flex: 1;
    overflow-y: auto;
    padding: 8px 16px 16px 16px;
}

/* 悬浮AI助手按钮 */
.floating-ai-btn {
    position: fixed;
    right: 40px;
    bottom: 40px;
    z-index: 3000;
}

.floating-ai-btn .el-button {
    width: 48px;
    height: 48px;
    font-size: 22px;
    box-shadow: 0 4px 20px rgba(64, 158, 255, 0.25);
    background: linear-gradient(135deg, #409EFF, #64b5f6);
    border: none;
}

.floating-ai-btn .el-button:hover {
    background: linear-gradient(135deg, #337ecc, #5ba3e8);
}

/* AI助手抽屉/侧边栏 */
.chat-panel-overlay {
    position: fixed;
    top: 0;
    right: 0;
    width: 420px;
    height: 100vh;
    background: rgba(0, 0, 0, 0.08);
    /* 原为 0.18，改为 0.08 */
    z-index: 4000;
    display: flex;
    align-items: stretch;
    animation: fadeIn 0.2s;
}

@keyframes fadeIn {
    from {
        opacity: 0;
    }

    to {
        opacity: 1;
    }
}

/* 响应式 */
@media screen and (max-width: 1200px) {
    .task-detail-page {
        width: 100%;
    }

    .detail-container {
        flex-direction: column;
        gap: 20px;
        padding: 10px 0;
    }

    .left-panel,
    .right-panel {
        width: 100%;
        margin: 0;
    }

    .chat-panel-overlay {
        width: 100vw;
    }
}
</style>
