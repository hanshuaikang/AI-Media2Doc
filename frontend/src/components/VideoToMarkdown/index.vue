<script setup>
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import UploadSection from './UploadSection.vue'
import LoadingOverlay from './LoadingOverlay.vue'
import { loadFFmpeg, extractAudio, captureVideoFrame, frameToBase64 } from '../../utils/ffmpeg'
import { submitAsrTask, pollAsrTask } from '../../apis/asrService'
import { generateMarkdownText } from '../../apis/markdownService'
import { calculateMD5 } from '../../utils/md5'
import { getAudioUploadUrl, uploadFile } from '../../apis'
import { saveTask, checkTaskExistsByMd5AndStyle, getAnyTaskByMd5, getTaskByID } from '../../utils/db'
import { eventBus } from '../../utils/eventBus'

const stepDefs = [
  { title: '初始化 FFmpeg', icon: 'Promotion', status: 'wait' },
  { title: '提取音频', icon: 'Headset', status: 'wait' },
  { title: '上传文件', icon: 'Upload', status: 'wait' },
  { title: '音频转文字', icon: 'Document', status: 'wait' },
  { title: '生成图文', icon: 'Document', status: 'wait' }
]

const steps = ref(stepDefs.map(s => ({ ...s })))
const activeStep = ref(0)

const ffmpegLoading = ref(false)
const ffmpegLoaded = ref(false)
const isProcessing = ref(false)

const file = ref(null)
const fileName = ref('')
const showStyleSelector = ref(false)
const style = ref('')
const showStartButton = ref(false)

const audioData = ref(null)
const audioUrl = ref('')
const audioFilename = ref('')
const audioExtracted = ref(false)
const textTranscribed = ref(false)
const transcriptionText = ref('')
const markdownContent = ref('')

const fileMd5 = ref('')
const fileSize = ref(0)
const md5Calculating = ref(false)

const smartScreenshot = ref(false)
const imageCount = ref(0)
const imageTotal = ref(0)

const resetAll = () => {
  steps.value = stepDefs.map(s => ({ ...s }))
  activeStep.value = 0
  isProcessing.value = false
  file.value = null
  fileName.value = ''
  showStyleSelector.value = false
  style.value = ''
  showStartButton.value = false
  audioData.value = null
  audioUrl.value = ''
  audioFilename.value = ''
  audioExtracted.value = false
  textTranscribed.value = false
  transcriptionText.value = ''
  markdownContent.value = ''
}

const handleFileSelected = async (f) => {
  resetAll()
  file.value = f
  fileName.value = f.name
  fileSize.value = f.size
  md5Calculating.value = true
  // 计算MD5
  fileMd5.value = await calculateMD5(new Uint8Array(await f.arrayBuffer()))
  md5Calculating.value = false
  showStyleSelector.value = true
}

const handleStyleSelected = (val) => {
  style.value = val
  showStartButton.value = true
}

const updateStepStatus = (idx, status) => {
  steps.value[idx].status = status
  activeStep.value = idx
}

const isMP3File = (f) => f && (f.type === 'audio/mpeg' || f.name.toLowerCase().endsWith('.mp3'))

const startProcessing = async () => {
  if (!file.value || !style.value) return
  isProcessing.value = true
  steps.value = stepDefs.map(s => ({ ...s }))
  try {
    // 0. 初始化FFmpeg
    updateStepStatus(0, 'processing')
    ffmpegLoading.value = true
    await loadFFmpeg()
    ffmpegLoaded.value = true
    updateStepStatus(0, 'success')
    ffmpegLoading.value = false

    // 1. 提取音频
    updateStepStatus(1, 'processing')
    let audioBuf
    if (isMP3File(file.value)) {
      audioBuf = new Uint8Array(await file.value.arrayBuffer())
      ElMessage.success('检测到MP3文件，跳过音频提取')
    } else {
      audioBuf = await extractAudio(new Uint8Array(await file.value.arrayBuffer()))
    }
    audioExtracted.value = true
    updateStepStatus(1, 'success')

    // 2. 检查MD5和历史
    const audioMd5 = await calculateMD5(audioBuf)
    audioFilename.value = `${audioMd5}.mp3`
    const exists = await checkTaskExistsByMd5AndStyle(audioMd5, style.value)
    if (exists) {
      updateStepStatus(2, 'error')
      isProcessing.value = false
      ElMessage.warning('该音频已以相同风格处理过，请在历史记录中查看')
      return
    }

    // 4. 识别
    updateStepStatus(3, 'processing')
    const existingTask = await getAnyTaskByMd5(audioMd5)
    if (existingTask && existingTask.transcriptionText) {
      transcriptionText.value = existingTask.transcriptionText
      textTranscribed.value = true
      updateStepStatus(3, 'success')
    } else {
      // 全新的任务才需要上传和识别
      updateStepStatus(2, 'processing')
      const uploadUrl = await getAudioUploadUrl(audioFilename.value)
      await uploadFile(uploadUrl, new Blob([audioBuf], { type: 'audio/mpeg' }))
      updateStepStatus(2, 'success')

      updateStepStatus(3, 'processing')
      const taskId = await submitAsrTask(audioFilename.value)
      const text = await pollAsrTask(taskId)
      transcriptionText.value = text
      textTranscribed.value = true
      updateStepStatus(3, 'success')
    }

    // 5. 生成内容
    updateStepStatus(4, 'processing')
    // 处理转录文本，支持字幕格式
    let processedText
    if (Array.isArray(transcriptionText.value) && transcriptionText.value.length > 0 && typeof transcriptionText.value[0] === 'object' && 'text' in transcriptionText.value[0]) {
      // 转换为字幕格式，包含时间戳信息
      processedText = transcriptionText.value.map(seg => {
        const startMin = Math.floor(seg.start_time / 60000)
        const startSec = Math.floor((seg.start_time % 60000) / 1000)
        const startMs = seg.start_time % 1000
        const endMin = Math.floor(seg.end_time / 60000)
        const endSec = Math.floor((seg.end_time % 60000) / 1000)
        const endMs = seg.end_time % 1000
        const startTime = `${startMin.toString().padStart(2, '0')}:${startSec.toString().padStart(2, '0')}.${startMs.toString().padStart(3, '0')}`
        const endTime = `${endMin.toString().padStart(2, '0')}:${endSec.toString().padStart(2, '0')}.${endMs.toString().padStart(3, '0')}`
        return `[${startTime} - ${endTime}] ${seg.text}`
      }).join('\n')
    } else {
      processedText = transcriptionText.value
    }
    const md = await generateMarkdownText(processedText, style.value)
    // 提取所有时间戳标记 #image[20] 格式（整数秒数）
    const imageTimeRegex = /#image\[(\d+)\]/g
    const imageTimeMarkers = md.match(imageTimeRegex) || []
    console.log('提取到的时间戳标记:', imageTimeMarkers)
    // 新逻辑：根据开关处理截图
    markdownContent.value = await processImageMarkers(md, file.value, imageTimeMarkers)

    updateStepStatus(4, 'success')

    // 保存
    const task = {
      fileName: fileName.value,
      md5: audioMd5,
      transcriptionText: transcriptionText.value,
      markdownContent: markdownContent.value, // 使用处理后的markdown内容
      contentStyle: style.value,
      createdAt: new Date().toISOString()
    }
    const taskId = await saveTask(task)
    eventBus.emit('task-updated')
    ElMessage.success('图文内容生成完成')
    // 用 taskId 查询完整任务对象并跳转
    const savedTask = await getTaskByID(taskId)
    if (savedTask) {
      eventBus.emit('view-task', savedTask)
    }
  } catch (e) {
    updateStepStatus(activeStep.value, 'error')
    ElMessage.error(e.message || '处理失败')
  } finally {
    isProcessing.value = false
    showStartButton.value = false
  }
}

// 智能截图开关读取
function isSmartScreenshotEnabled() {
  try {
    return localStorage.getItem('smartScreenshotEnabled') === 'true'
  } catch {
    return false
  }
}

// 抽离截图处理逻辑
async function processImageMarkers(md, file, imageTimeMarkers) {
  // 去除掉 md 开头的 ```markdown 和 结尾的 ```
  if (md.startsWith('```markdown')) {
    md = md.replace(/^```markdown\s*/, '').replace(/```$/, '').trim()
  } else if (md.startsWith('```')) {
    md = md.replace(/^```/, '').replace(/```$/, '').trim()
  }
  smartScreenshot.value = isSmartScreenshotEnabled()
  imageCount.value = 0
  imageTotal.value = imageTimeMarkers.length
  if (!smartScreenshot.value) {
    // 未开启，全部替换为空
    let result = md
    for (const marker of imageTimeMarkers) {
      result = result.replaceAll(marker, '')
    }
    imageCount.value = 0
    imageTotal.value = 0
    return result
  }
  // 已开启，执行截图逻辑
  if (imageTimeMarkers.length > 0 && !isMP3File(file)) {
    const videoData = new Uint8Array(await file.arrayBuffer())
    let result = md
    let imageIdx = 1 // 新增编号计数器
    for (const marker of imageTimeMarkers) {
      try {
        // 匹配 #image[20] 形式
        const timeMatch = marker.match(/#image\[(\d+)\]/)
        if (timeMatch) {
          const totalSeconds = parseInt(timeMatch[1])
          console.log(`正在截图: ${marker} (时间: ${totalSeconds}秒) 当前进度 ${imageIdx}/${imageTimeMarkers.length}`)
          // 捕获视频帧
          const frameData = await captureVideoFrame(videoData, totalSeconds)
          const base64Image = frameToBase64(frameData)
          // 使用 HTML img 标签并加编号，设置最大宽度自适应
          const imageTag = `<div style="text-align:center;"><span style="font-size:0.98em;color:#888;">截图${imageIdx}</span><br><img src="${base64Image}" alt="截图${imageIdx}" style="max-width:100%;height:auto;border-radius:8px;box-shadow:0 2px 8px #0001;margin:8px 0;" /></div>`
          result = result.replace(marker, imageTag)
          imageCount.value = imageIdx // 实时更新进度
          imageIdx++
        }
      } catch (error) {
        console.error(`处理标记 ${marker} 时出错:`, error)
        ElMessage.error(`处理标记 ${marker} 时出错: ${error.message}`)
      }
    }
    imageCount.value = imageTotal.value // 处理完成
    return result
  } else if (imageTimeMarkers.length > 0 && isMP3File(file)) {
    imageCount.value = 0
    imageTotal.value = 0
    return md
  }
  imageCount.value = 0
  imageTotal.value = 0
  return md
}

// 步骤百分比辅助
const stepPercents = [10, 30, 50, 80, 100]
const percent = computed(() => stepPercents[activeStep.value] || 0)
const stepText = computed(() => steps.value[activeStep.value]?.title || '')

</script>

<template>
  <div class="video-markdown-container">
    <div class="main-content">
      <!-- 步骤1：上传/风格选择/文件信息，始终显示，除非正在处理或有结果 -->
      <div v-if="!isProcessing && !markdownContent" class="component-wrapper">
        <UploadSection :ffmpeg-loading="ffmpegLoading" :is-processing="isProcessing" :file="file" :file-name="fileName"
          :file-size="fileSize" :file-md5="fileMd5" :md5-calculating="md5Calculating" :style="style"
          @file-selected="handleFileSelected" @update:style="handleStyleSelected" @start-process="startProcessing"
          @reset="resetAll" />
      </div>
      <!-- 步骤3：处理进度（全屏loading） -->
      <LoadingOverlay v-if="isProcessing" :step-text="stepText" :percent="percent" :smart-screenshot="smartScreenshot"
        :image-count="imageCount" :image-total="imageTotal" />
    </div>
  </div>
</template>

<style scoped>
.video-markdown-container {
  width: 100%;
  flex: 1;
  margin-top: 0;
  display: flex;
  flex-direction: column;
  background-color: transparent;
  padding: 0;
  min-height: auto;
  height: auto;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: row;
  width: 100%;
  /* 只占父容器宽度 */
  max-width: 100%;
  /* 只占父容器宽度 */
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  height: 100vh;
  align-items: center;
  justify-content: center;
  min-height: 0;
}

.component-wrapper {
  width: auto;
  max-width: 900px;
  box-sizing: border-box;
  border-radius: 12px;
  overflow: visible;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 24px 0;
  /* 新增，防止极小屏幕时贴边 */
}

/* 文件信息卡片和风格选择区域样式与 UploadSection.vue 保持一致 */
.file-info-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2.2rem;
  background: transparent;
  box-shadow: none;
  border: none;
}

.file-info-card {
  width: 100%;
  max-width: 520px;
  background: #fff;
  /* 纯白色 */
  border-radius: 14px;
  padding: 1.5rem 2rem 1.2rem 2rem;
  box-shadow: 0 2px 10px 0 rgba(60, 80, 120, 0.04);
  border: 1px solid #23272f22;
  /* 淡黑色边框 */
  margin-bottom: 0.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.7rem;
}

.file-info-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.03rem;
  color: #23272f;
  font-weight: 500;
  word-break: break-all;
}

.file-info-label {
  color: #6b7280;
  font-size: 1.01rem;
  font-weight: 500;
  min-width: 70px;
}

.file-info-value {
  color: #23272f;
  font-size: 1.03rem;
  font-weight: 600;
}

.file-info-md5 {
  font-family: monospace;
  font-size: 0.98rem;
  color: #888;
  background: #f3f4f6;
  border-radius: 4px;
  padding: 2px 6px;
}

.style-selector-wrapper {
  width: 100%;
  max-width: 520px;
}

.file-action-row {
  width: 100%;
  max-width: 520px;
  display: flex;
  align-items: center;
  gap: 1.2rem;
  margin-top: 0.5rem;
  justify-content: flex-start;
}

.start-process-btn {
  background: #23272f !important;
  color: #fff !important;
  border: none !important;
  border-radius: 8px !important;
  font-size: 1.08rem;
  font-weight: 700;
  padding: 0.7rem 2.2rem;
  transition: background 0.18s;
  box-shadow: 0 2px 8px 0 rgba(60, 80, 120, 0.06);
}

.start-process-btn:disabled {
  background: #e5e7eb !important;
  color: #b0b3b8 !important;
  cursor: not-allowed !important;
  box-shadow: none;
}

.start-process-btn:hover:not(:disabled) {
  background: #444950 !important;
}

.reset-link {
  color: #888;
  font-size: 0.98rem;
  text-decoration: underline;
  cursor: pointer;
  margin-left: 0.5rem;
  transition: color 0.18s;
}

.reset-link:hover {
  color: #23272f;
}
</style>
