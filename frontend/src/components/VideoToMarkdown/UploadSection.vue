<script setup>
import { ElUpload, ElIcon, ElMessage } from 'element-plus'
import { UploadFilled, VideoCamera } from '@element-plus/icons-vue'

defineProps({
  ffmpegLoading: {
    type: Boolean,
    default: false
  },
  isProcessing: {
    type: Boolean,
    default: false
  },
  acceptHint: {
    type: String,
    default: '上传视频或Mp3音频'
  }
})

const emit = defineEmits(['file-selected'])

const allowedTypes = [
  'video/mp4',
  'video/quicktime',  // .mov
  'video/x-msvideo',  // .avi
  'video/x-matroska', // .mkv
  'video/webm',       // .webm
  'audio/mpeg'        // .mp3 - 添加支持MP3格式
]

const handleFileChange = (file) => {
  // 检查文件类型是否为允许的类型或MP3文件
  const isAllowedType = allowedTypes.includes(file.raw.type) ||
    file.raw.name.toLowerCase().endsWith('.mp3');

  if (!isAllowedType) {
    ElMessage.error('只支持上传视频文件（MP4、MOV、AVI、MKV、WebM）或MP3音频文件')
    return false
  }

  // 修改文件大小限制为100MB
  const maxSize = 100 * 1024 * 1024
  if (file.raw.size > maxSize) {
    ElMessage.error('文件大小不能超过 100MB')
    return false
  }

  emit('file-selected', file.raw)
}
</script>

<template>
  <div class="upload-section" :class="{ 'loading-state': ffmpegLoading }">
    <h3 class="section-title">
      <el-icon>
        <VideoCamera />
      </el-icon>
      {{ acceptHint }}
    </h3>
    <el-upload class="uploader" drag action="" :auto-upload="false" :on-change="handleFileChange"
      :disabled="ffmpegLoading || isProcessing" :accept="allowedTypes.join(',') + ',.mp3'">
      <div class="upload-content">
        <div class="upload-icon-wrapper">
          <el-icon class="upload-icon">
            <UploadFilled />
          </el-icon>
        </div>
        <h3 class="upload-title">
          {{ ffmpegLoading ? '正在加载 ffmpeg，请稍候...' : '开始上传' }}
        </h3>
        <p class="upload-desc" v-if="!ffmpegLoading">
          支持拖放或点击上传视频或MP3文件<br>
          <span class="upload-formats">支持格式：MP4、MOV、AVI、MKV、WebM、MP3，最大 100MB</span>
        </p>
      </div>
    </el-upload>
  </div>
</template>

<style scoped>
.upload-section {
  width: 100%;
  background-color: #ffffff;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
  border: 1px solid #ebeef5;
  box-sizing: border-box;
  margin: 0;
  height: auto;
}

.section-title {
  font-size: 1.1rem;
  color: #303133;
  margin-bottom: 0.8rem;
  font-weight: 600;
  text-align: left;
  display: flex;
  align-items: center;
  gap: 8px;
}

.section-title .el-icon {
  font-size: 1.2rem;
  color: var(--el-color-primary);
}

.uploader {
  width: 100%;
}

.upload-content {
  text-align: center;
  padding: 1rem;
}

.upload-icon-wrapper {
  width: 48px;
  height: 48px;
  background: #ecf5ff;
  border-radius: 50%;
  margin: 0 auto 0.5rem;
  /* 减小下方边距 */
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #d9ecff;
}

.upload-icon {
  font-size: 1.4rem;
  /* 减小图标字体大小 */
  color: #409EFF;
}

.upload-title {
  font-size: 1.1rem;
  /* 减小标题字体大小 */
  color: #303133;
  margin: 0.5rem 0;
  /* 减小标题上下边距 */
  font-weight: 500;
}

.upload-desc {
  color: #606266;
  line-height: 1.5;
  font-size: 0.9rem;
  /* 减小描述字体大小 */
}

.upload-formats {
  font-size: 0.8rem;
  /* 减小格式文字大小 */
  color: #909399;
}

.loading-state {
  background-color: #f8f9fa;
  pointer-events: none;
  opacity: 0.8;
}

/* 添加小屏幕优化 */
@media screen and (max-height: 800px) {
  .upload-section {
    padding: 1.2rem;
  }

  .upload-icon-wrapper {
    width: 42px;
    height: 42px;
    margin: 0 auto 0.3rem;
  }

  .upload-title {
    font-size: 1rem;
    margin: 0.3rem 0;
  }

  .upload-desc {
    font-size: 0.85rem;
    line-height: 1.4;
  }

  .section-title {
    font-size: 1rem;
    margin-bottom: 0.6rem;
    gap: 6px;
  }

  .section-title .el-icon {
    font-size: 1.1rem;
  }
}

@media screen and (max-height: 700px) {
  .section-title {
    font-size: 1rem;
    margin-bottom: 0.6rem;
  }

  .upload-content {
    padding: 0.7rem;
  }

  .upload-icon-wrapper {
    width: 36px;
    height: 36px;
  }

  .upload-formats {
    font-size: 0.75rem;
  }
}
</style>
