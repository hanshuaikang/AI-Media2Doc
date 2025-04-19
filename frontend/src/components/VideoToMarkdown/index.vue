<script setup>
import { ref, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import UploadSection from './UploadSection.vue'
import StyleSelector from './StyleSelector.vue'
import ProcessSteps from './ProcessSteps.vue'
import ResultsArea from './ResultsArea.vue'
import { loadFFmpeg, extractAudio } from '../../utils/ffmpeg'
import { submitAudioTask, pollAudioTask } from '../../apis/audioService'
import { generateMarkdownText } from '../../apis/markdownService'
import { calculateMD5 } from '../../utils/md5'
import { getAudioUploadUrl, uploadFile } from '../../apis'
import { saveTask, checkTaskExistsByMd5AndStyle, getAnyTaskByMd5 } from '../../utils/db'
import { Document, Promotion } from '@element-plus/icons-vue'
import { eventBus } from '../../utils/eventBus'

// FFmpeg 相关状态
const ffmpegLoaded = ref(false)
const ffmpegLoading = ref(false)

// 步骤状态
const steps = ref([
  {
    title: '初始化 FFmpeg',
    icon: 'Promotion',
    status: 'wait'
  },
  {
    title: '提取音频',
    icon: 'Headset',
    status: 'wait'
  },
  {
    title: '上传文件',
    icon: 'Upload',
    status: 'wait'
  },
  {
    title: '音频转文字',
    icon: 'Document',
    status: 'wait'
  },
  {
    title: '生成图文',
    icon: 'Document',
    status: 'wait'
  },
])
const activeStep = ref(0)

const isProcessing = ref(false)
const audioUrl = ref('')
const audioData = ref(null)
const audioExtracted = ref(false)
const textTranscribed = ref(false)
const audioFilename = ref('')
const transcriptionText = ref('')
const markdownContent = ref('')
const contentStyle = ref('note')

const currentFileName = ref('')

// 添加加载状态
const processingAudio = ref(false)

// 添加状态来控制是否显示开始生成按钮
const showStartButton = ref(false)
const videoFile = ref(null)

// 添加风格映射
const styleMap = {
  note: {
    name: '知识笔记',
    color: '#409EFF' // 蓝色
  },
  summary: {
    name: '内容总结',
    color: '#67C23A' // 绿色
  },
  xiaohongshu: {
    name: '小红书风格',
    color: '#FE2C55' // 红色
  },
  wechat: {
    name: '公众号风格',
    color: '#07C160' // 微信绿
  },
  mind: {
    name: '思维导图',
    color: '#8E93F2' // 紫色
  }
}

// 计算当前风格的中文名称和颜色
const currentStyleInfo = computed(() => {
  return styleMap[contentStyle.value] || { name: contentStyle.value, color: '#409EFF' }
})

// 步骤状态修改部分 - 请在相关处理代码中应用这些颜色设置
const updateStepStatus = (stepIndex, status) => {
  if (stepIndex >= 0 && stepIndex < steps.value.length) {
    steps.value[stepIndex].status = status;
    // 确保"上传文件"和"音频转文字"步骤的文字显示为黑色
    if ((stepIndex === 2 || stepIndex === 3) && status === 'success') {
      // 这里不需要额外代码，因为我们已经在CSS中设置了所有状态为黑色
    }
  }
}

const handleFile = async (file) => {
  if (!file) return;

  currentFileName.value = file.name;
  videoFile.value = file;

  // 显示开始按钮
  showStartButton.value = true;

  // 确保其他状态复位
  audioData.value = null;
  audioUrl.value = '';
  audioExtracted.value = false;
  textTranscribed.value = false;
  audioFilename.value = '';
  transcriptionText.value = '';
  markdownContent.value = '';
  processingAudio.value = false;
  isProcessing.value = false;
}

// 检查文件是否为MP3
const isMP3File = (file) => {
  return file && (file.type === 'audio/mpeg' || file.name.toLowerCase().endsWith('.mp3'));
}

// 开始处理按钮的点击事件处理
const startProcessing = async () => {
  if (!videoFile.value) {
    ElMessage.error('请先上传视频文件');
    return;
  }

  // 开始处理，设置状态
  isProcessing.value = true;
  processingAudio.value = true;

  try {
    // 检查是否为MP3文件
    const isMp3 = isMP3File(videoFile.value);

    // 提取音频或直接使用MP3文件
    if (isMp3) {
      // 如果是MP3文件，直接跳过音频提取步骤
      updateStepStatus(1, 'success');
      ElMessage.success('检测到MP3文件，将直接跳过音频提取步骤');

      // 直接读取MP3文件
      audioData.value = new Uint8Array(await videoFile.value.arrayBuffer());
      const blob = new Blob([audioData.value], { type: 'audio/mpeg' });
      audioUrl.value = URL.createObjectURL(blob);
      audioExtracted.value = true;
    } else {
      // 如果不是MP3文件，正常提取音频
      activeStep.value = 1;
      updateStepStatus(1, 'processing');

      const videoData = new Uint8Array(await videoFile.value.arrayBuffer());
      const extractedAudio = await extractAudio(videoData);

      audioData.value = extractedAudio;
      const blob = new Blob([extractedAudio], { type: 'audio/mpeg' });
      audioUrl.value = URL.createObjectURL(blob);
      audioExtracted.value = true;
      updateStepStatus(1, 'success');
    }

    // 使用音频文件计算 MD5
    const audioMd5 = await calculateMD5(audioData.value);

    // 检查是否存在相同的 MD5 和内容类型
    const exists = await checkTaskExistsByMd5AndStyle(audioMd5, contentStyle.value);
    if (exists) {
      ElMessage.warning('该音频已经以相同风格处理过，请在历史记录中查看或选择其他风格');
      updateStepStatus(1, 'warning');
      processingAudio.value = false;
      isProcessing.value = false;
      return;
    }

    audioFilename.value = `${audioMd5}.mp3`;

    // 检查是否有任何风格的相同音频已完成处理
    const existingTask = await getAnyTaskByMd5(audioMd5);

    if (existingTask && existingTask.transcriptionText) {
      // 有相同MD5的任务，直接复用其转写文本
      ElMessage.success('检测到相同音频，直接复用已有转写结果');

      // 标记上传和识别步骤为成功
      updateStepStatus(2, 'success');
      activeStep.value = 3;
      updateStepStatus(3, 'success');

      // 直接使用已存在的转写文本
      transcriptionText.value = existingTask.transcriptionText;
      textTranscribed.value = true;

      // 跳到第四步：生成 Markdown
      activeStep.value = 4;
      updateStepStatus(4, 'processing');

      const markdown = await generateMarkdownText(transcriptionText.value, contentStyle.value);
      markdownContent.value = markdown;
      updateStepStatus(4, 'success');

      // 保存新风格的任务记录
      await saveTask({
        fileName: currentFileName.value,
        md5: audioMd5,
        transcriptionText: transcriptionText.value,
        markdownContent: markdown,
        contentStyle: contentStyle.value,
        createdAt: new Date().toISOString()
      });

      // 发送任务更新事件，通知历史列表刷新
      eventBus.emit('task-updated');

      ElMessage.success('图文内容生成完成');
    } else {
      // 没有相同MD5的任务，正常执行流程

      // 上传音频文件
      updateStepStatus(2, 'processing');
      activeStep.value = 2;

      const uploadUrl = await getAudioUploadUrl(audioFilename.value);
      const audioBlob = new Blob([audioData.value], { type: 'audio/mpeg' });
      await uploadFile(uploadUrl, audioBlob);

      updateStepStatus(2, 'success');
      ElMessage.success('音频上传成功');

      // 音频识别
      updateStepStatus(3, 'processing');
      activeStep.value = 3;

      const taskId = await submitAudioTask(audioFilename.value);
      const text = await pollAudioTask(
        taskId,
        (status) => {
          if (status === 'processing') {
            ElMessage.info('正在识别音频...');
          }
        }
      );

      transcriptionText.value = text;
      textTranscribed.value = true;
      updateStepStatus(3, 'success');
      ElMessage.success('音频识别完成');

      // 生成 Markdown
      updateStepStatus(4, 'processing');
      activeStep.value = 4;

      const markdown = await generateMarkdownText(text, contentStyle.value);
      markdownContent.value = markdown;
      updateStepStatus(4, 'success');

      // 保存任务记录
      await saveTask({
        fileName: currentFileName.value,
        md5: audioMd5,
        transcriptionText: text,
        markdownContent: markdown,
        contentStyle: contentStyle.value,
        createdAt: new Date().toISOString()
      });

      eventBus.emit('task-updated');

      ElMessage.success('图文内容生成完成');
    }

  } catch (error) {
    // 设置当前步骤为错误状态
    if (activeStep.value >= 0 && activeStep.value < steps.value.length) {
      updateStepStatus(activeStep.value, 'error');
    }
    ElMessage.error(`处理失败: ${error.message}`);
  } finally {
    processingAudio.value = false;
    isProcessing.value = false;
    showStartButton.value = false;
  }
};

// 下载处理函数
const downloadAudio = () => {
  const a = document.createElement('a')
  a.href = audioUrl.value
  a.download = audioFilename.value || 'extracted_audio.mp3'
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
}

const downloadText = () => {
  const blob = new Blob([transcriptionText.value], { type: 'text/plain' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = 'transcript.txt'
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}

const downloadMarkdown = () => {
  const blob = new Blob([markdownContent.value], { type: 'text/markdown' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = 'content.md'
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}

onMounted(() => {
  ffmpegLoading.value = true;
  loadFFmpeg()
    .then(() => {
      ffmpegLoaded.value = true;
      updateStepStatus(0, 'success');
    })
    .catch(err => {
      console.error('FFmpeg 预加载失败:', err);
      updateStepStatus(0, 'error');
    })
    .finally(() => {
      ffmpegLoading.value = false;
    });
})


</script>

<template>
  <div class="video-markdown-container">
    <div class="main-content">
      <div class="component-wrapper">
        <ProcessSteps :steps="steps" :active-step="activeStep" class="process-steps" />
      </div>

      <div class="component-wrapper">
        <StyleSelector v-model="contentStyle" class="style-selector"
          :disabled="processingAudio || isProcessing || showStartButton" />
      </div>

      <!-- 上传区域只在未上传文件且未完成处理时显示 -->
      <div v-if="!showStartButton && !audioExtracted && !textTranscribed && !markdownContent" class="component-wrapper">
        <UploadSection :ffmpeg-loading="ffmpegLoading" :is-processing="isProcessing" @file-selected="handleFile"
          class="upload-section" />
      </div>

      <!-- 开始处理按钮区域 - 动态色条和左对齐文件名 -->
      <div v-if="showStartButton && !processingAudio" class="component-wrapper start-button-container"
        :style="{ '--top-gradient-color': currentStyleInfo.color }">
        <div class="start-button-content">
          <!-- 文件预览信息 - 左对齐 -->
          <div class="file-info-section">
            <div class="file-preview">
              <div class="file-icon-wrapper" :style="{ background: `${currentStyleInfo.color}15` }">
                <el-icon class="file-icon" :style="{ color: currentStyleInfo.color }">
                  <Document />
                </el-icon>
              </div>
              <div class="file-details">
                <div class="file-name text-left">{{ currentFileName }}</div>
                <div class="file-status">
                  <span class="status-dot"></span>
                  <span>文件已选择</span>
                </div>
              </div>
            </div>

            <!-- 风格选择信息 - 左对齐并使用中文名称和对应颜色 -->
            <div class="style-info">
              <span class="style-label">输出风格:</span>
              <span class="style-chip"
                :style="{ backgroundColor: `${currentStyleInfo.color}10`, color: currentStyleInfo.color, borderColor: `${currentStyleInfo.color}30` }">
                {{ currentStyleInfo.name }}
              </span>
            </div>
          </div>

          <!-- 按钮区域 - 居中 -->
          <div class="button-section">
            <el-button type="danger" size="large" @click="startProcessing" class="start-button"
              :style="{ backgroundColor: currentStyleInfo.color + ' !important', borderColor: currentStyleInfo.color + ' !important' }">
              <div class="button-content">
                <el-icon class="plane-icon">
                  <Promotion />
                </el-icon>
                <span>开始生成</span>
              </div>
            </el-button>
          </div>

          <div class="reset-option">
            <a href="#" @click.prevent="showStartButton = false">重新选择文件</a>
          </div>
        </div>
      </div>

      <!-- 结果展示区域 -->
      <div class="component-wrapper" v-if="audioExtracted || textTranscribed || markdownContent">
        <ResultsArea :audio-extracted="audioExtracted" :text-transcribed="textTranscribed" :audio-url="audioUrl"
          :audio-filename="audioFilename" :transcription-text="transcriptionText" :markdown-content="markdownContent"
          :content-style="contentStyle" @download-audio="downloadAudio" @download-text="downloadText"
          @download-markdown="downloadMarkdown" class="results-area" />
      </div>
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
  overflow-y: visible;
  /* 修改为visible，允许内容溢出 */
  min-height: auto;
  /* 修改：移除最小高度限制 */
  height: auto;
  /* 自适应高度 */
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto 40px;
  padding: 20px 20px;
  box-sizing: border-box;
  height: auto;
  overflow-y: visible;
  position: relative;
}

/* 确保组件包装器不受高度限制 */
.component-wrapper {
  width: 100%;
  box-sizing: border-box;
  border-radius: 12px;
  overflow: visible;
  /* 修改：允许内容溢出 */
  margin-bottom: 20px;
  /* 添加：组件间距，确保视觉分离 */
}

/* 移除各组件内的冲突边距 */
.process-steps,
.upload-section,
.style-selector,
.results-area {
  margin: 0;
  width: 100%;
}

/* 媒体查询 */
@media screen and (max-width: 1300px) {
  .main-content {
    max-width: 95%;
    padding: 0 15px;
  }
}

@media screen and (max-width: 768px) {
  .main-content {
    gap: 16px;
    margin: 10px auto;
    padding: 0 10px;
    transform: scale(0.9);
    /* 添加：整体缩放到90% */
    transform-origin: top center;
    /* 添加：从顶部中心开始缩放 */
    width: 111.11%;
    /* 添加：补偿缩放带来的宽度减少 (100/0.9=111.11) */
    margin-left: -5.55%;
    /* 添加：水平居中调整 */
  }

  /* 调整组件间距以适应缩放 */
  .component-wrapper {
    margin-bottom: 15px;
  }
}

/* 添加更小屏幕的额外优化 */
@media screen and (max-width: 480px) {
  .main-content {
    transform: scale(0.85);
    /* 进一步缩小 */
    width: 117.65%;
    /* 补偿缩放 (100/0.85=117.65) */
    margin-left: -8.825%;
    /* 水平居中调整 */
  }
}

/* 重新设计的开始按钮容器样式 - 支持动态色条 */
.start-button-container {
  background-color: #ffffff;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
  border: 1px solid #f0f0f0;
  position: relative;
  overflow: hidden;
  --top-gradient-color: #fe2c55;
  /* 默认颜色，将被动态覆盖 */
}

.start-button-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, var(--top-gradient-color), var(--top-gradient-color, #fe2c55));
}

.start-button-content {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  /* 减小间距 */
  padding-bottom: 1rem;
  /* 为底部链接留出空间 */
}

/* 文件信息区域 - 左对齐布局 */
.file-info-section {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
  align-items: flex-start;
}

.file-preview {
  display: flex;
  align-items: center;
  gap: 16px;
  background: #f9f9f9;
  padding: 1rem 1.5rem;
  border-radius: 10px;
  border: 1px solid #eee;
  width: 100%;
}

.file-icon-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: #e6f1ff;
  border-radius: 50%;
  flex-shrink: 0;
}

.file-icon {
  color: #409EFF;
  font-size: 1.2rem;
}

.file-details {
  flex: 1;
  min-width: 0;
  /* 确保弹性项目可以缩小到小于其内容大小 */
}

.file-name {
  font-size: 1rem;
  font-weight: 500;
  color: #303133;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  text-align: left;
  width: 100%;
}

.text-left {
  text-align: left;
}

.file-status {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.85rem;
  color: #67c23a;
  margin-top: 4px;
}

.status-dot {
  display: inline-block;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background-color: #67c23a;
}



.style-chip {
  font-weight: 500;
  font-size: 0.9rem;
  padding: 0.3rem 0.8rem;
  border-radius: 16px;
  border-width: 1px;
  border-style: solid;
  transition: all 0.2s ease;
}

/* 按钮区域 - 居中 */
.button-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding-top: 0.5rem;
  border-top: 1px dashed #eee;
  margin-top: 0.5rem;
}

/* 开始按钮样式 */
.start-button {
  padding: 0 !important;
  height: auto !important;
  transition: all 0.3s ease;
  border-radius: 30px !important;
  width: 140px;
}

.button-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 10px 0;
  width: 100%;
  position: relative;
  overflow: hidden;
  font-size: 0.95rem;
  font-weight: 500;
}

.start-button:hover {
  transform: translateY(-2px);
  filter: brightness(1.1);
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
}

.start-button:active {
  transform: translateY(0);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.plane-icon {
  font-size: 1rem;
  transform: rotate(45deg);
}

/* 重新定位的"重新选择文件"链接 */
.reset-option {
  position: absolute;
  bottom: 1rem;
  right: 1.5rem;
  margin-top: 0;
}

.reset-option a {
  color: #409EFF;
  /* 使用蓝色 */
  font-size: 0.85rem;
  text-decoration: none;
  transition: all 0.2s;
  padding: 0.3rem 0.8rem;
  border-radius: 4px;
  font-weight: 500;
}

.reset-option a:hover {
  color: #337ecc;
  /* 深蓝色悬停效果 */
  background-color: #ecf5ff;
}
</style>
