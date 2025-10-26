<template>
    <div class="mindmap-fullscreen">
        <div id="mindMapContainerFull" ref="containerRef" class="mind-map-container-full"></div>

        <div class="fullscreen-toolbar">
            <el-button type="primary" :icon="Close" circle size="small" title="退出全屏" @click="handleClose" />
            <div class="toolbar-divider"></div>
            <el-button type="default" :icon="ZoomIn" circle size="small" title="放大" @click="handleZoomIn" />
            <el-button type="default" :icon="ZoomOut" circle size="small" title="缩小" @click="handleZoomOut" />
            <el-button type="default" :icon="Aim" circle size="small" title="适应画布" @click="handleFit" />
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue'
import { ElMessage, ElButton } from 'element-plus'
import { Close, ZoomIn, ZoomOut, Aim } from '@element-plus/icons-vue'
import MindMap from 'simple-mind-map'

const props = defineProps({
    content: { type: String, required: true }
})

const emit = defineEmits(['close'])

const containerRef = ref(null)
const mindMapInstance = ref(null)

const convertToMindMapFormat = (jsonData) => {
    try {
        const data = typeof jsonData === 'object' ? jsonData : JSON.parse(jsonData)
        return data.data && (data.data.text || data.data.title)
            ? data
            : { data: { text: data.text || data.title || "思维导图" }, children: data.children || [] }
    } catch {
        return { data: { text: "解析失败的思维导图" }, children: [] }
    }
}

const adjustView = () => {
    const mm = mindMapInstance.value
    if (!mm) return
    mm.command?.executeCommand('fit')
    requestAnimationFrame(() => {
        if (mm.view?.translateToCenter) {
            mm.view.translateToCenter()
        } else {
            mm.command?.executeCommand('TO_CENTER')
        }
    })
}

const initMindMap = async () => {
    try {
        if (!containerRef.value) return
        if (mindMapInstance.value) mindMapInstance.value.destroy()
        await nextTick()

        const container = containerRef.value
        const mindMapData = convertToMindMapFormat(props.content)

        mindMapInstance.value = new MindMap({
            el: container,
            data: mindMapData,
            theme: 'primary',
            layout: 'logicalStructure',
            enableNodeDragging: true,
            height: window.innerHeight,
            width: window.innerWidth,
            keypress: true,
            contextMenu: false,
            fit: true,
            scale: 0.9,
            textAutoWrap: true,
            nodeTextEdit: false,
            mousewheelAction: 'zoom',
            enableMouseWheel: true
        })

        mindMapInstance.value.render()
        setTimeout(() => adjustView(), 120)
    } catch {
        ElMessage.error('思维导图初始化失败')
    }
}

const handleZoomIn = () => {
    mindMapInstance.value?.view?.enlarge()
}

const handleZoomOut = () => {
    mindMapInstance.value?.view?.narrow()
}

const handleFit = () => {
    adjustView()
}

const handleClose = () => {
    emit('close')
}

let resizeRaf = 0
const handleResize = () => {
    cancelAnimationFrame(resizeRaf)
    resizeRaf = requestAnimationFrame(() => {
        if (mindMapInstance.value) {
            mindMapInstance.value.resize()
            adjustView()
        }
    })
}

const handleKeydown = (e) => {
    if (e.key === 'Escape') {
        handleClose()
    }
}

onMounted(() => {
    initMindMap()
    window.addEventListener('keydown', handleKeydown)
    window.addEventListener('resize', handleResize)
})

onBeforeUnmount(() => {
    mindMapInstance.value?.destroy()
    window.removeEventListener('keydown', handleKeydown)
    window.removeEventListener('resize', handleResize)
    cancelAnimationFrame(resizeRaf)
})
</script>

<style scoped>
.mindmap-fullscreen {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    width: 100vw;
    height: 100vh;
    background: #fff;
    z-index: 9999;
}

#mindMapContainerFull * {
    margin: 0;
    padding: 0;
}

.mind-map-container-full {
    width: 100%;
    height: 100%;
    background: #fff;
}

.fullscreen-toolbar {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 10000;
    display: flex;
    align-items: center;
    gap: 8px;
    background: rgba(255, 255, 255, 0.95);
    padding: 8px 12px;
    border-radius: 8px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.toolbar-divider {
    width: 1px;
    height: 24px;
    background: #e5e7eb;
    margin: 0 4px;
}
</style>
