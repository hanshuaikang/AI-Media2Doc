<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import AppSidebar from './components/AppSidebar.vue'
import VideoToMarkdown from './components/VideoToMarkdown/index.vue'
import TaskDetail from './components/VideoToMarkdown/TaskDetail.vue'
import { eventBus } from './utils/eventBus'

const activeMenu = ref('new-task')
const isChatOpen = ref(false)
const selectedTask = ref(null)

const isTaskDetailOpen = ref(false)
const currentTask = ref(null)

const previousMenu = ref('new-task')

const handleMenuSelect = (key) => {
  if (key.startsWith('task-')) {
    const taskId = parseInt(key.replace('task-', ''))
    return;
  }

  isTaskDetailOpen.value = false
  currentTask.value = null
  activeMenu.value = key
}


const handleViewTask = (task) => {
  currentTask.value = task
  isTaskDetailOpen.value = true
  previousMenu.value = activeMenu.value
  activeMenu.value = 'task-detail'
}

onMounted(() => {
  eventBus.on('view-task', handleViewTask)
})
onBeforeUnmount(() => {
  eventBus.off('view-task', handleViewTask)
})
</script>

<template>
  <div class="app-container">
    <AppSidebar :active-menu="activeMenu" @menu-select="handleMenuSelect" @view-task="handleViewTask" />

    <div class="content-area">
      <div class="content-wrapper">
        <template v-if="isTaskDetailOpen && currentTask">
          <TaskDetail :task="currentTask" />
        </template>
        <template v-else-if="activeMenu === 'new-task'">
          <VideoToMarkdown />
        </template>
        <template v-else>
        </template>
      </div>
    </div>

  </div>
</template>

<style>
.app-container {
  display: flex;
  min-height: 100vh;
  width: 100vw;
  max-width: 100%;
  position: relative;
  overflow-x: hidden;
  overflow-y: auto;
}

.content-area {
  flex: 1;
  margin-left: 260px;
  width: calc(100vw - 260px);
  min-height: auto;
  display: flex;
  flex-direction: column;
  padding: 0 20px;
  box-sizing: border-box;
  overflow-y: auto;
  overflow-x: hidden;
}

.content-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 1800px;
  margin: 0 auto;
  box-sizing: border-box;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 20px 0;
  height: auto;
}

body {
  margin: 0;
  padding: 0;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  background-color: #ffffff;
  width: 100%;
  height: auto;
  overflow-y: auto;
  overflow-x: hidden;
}

html {
  width: 100%;
  height: auto;
  background-color: #ffffff;
  overflow-y: auto;
  overflow-x: hidden;
}

#app {
  width: 100vw;
  min-height: auto;
  position: relative;
  background-color: #ffffff;
  margin: 0;
  padding: 0;
  max-width: 100%;
  overflow-y: auto;
  overflow-x: hidden;
}

/* 媒体查询 */
@media screen and (max-width: 768px) {
  .content-area {
    margin-left: 60px;
    width: calc(100vw - 60px);
    padding: 0 5px;
    /* 减少水平内边距 */
    overflow-y: auto;
    /* 确保垂直滚动可用 */
  }

  .content-wrapper {
    padding: 10px 0;
    /* 减少垂直内边距 */
    overflow-y: visible;
    /* 确保内容可见 */
  }
}

/* 添加更小屏幕的优化 */
@media screen and (max-width: 480px) {
  .content-area {
    padding: 0 2px;
  }

  .content-wrapper {
    padding: 5px 0;
  }
}

/* 确保所有滚动容器都继承背景色 */
::-webkit-scrollbar-track {
  background-color: #f5f7fa;
}

/* 修改滚动条样式 */
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-thumb {
  background-color: #c0c4cc;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background-color: #909399;
}
</style>
