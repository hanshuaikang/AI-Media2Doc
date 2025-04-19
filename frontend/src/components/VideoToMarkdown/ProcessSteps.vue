<script setup>
import { Check, CircleCloseFilled, Promotion, Headset, Upload, Document, Connection } from '@element-plus/icons-vue'

defineProps({
  steps: {
    type: Array,
    required: true
  },
  activeStep: {
    type: Number,
    required: true
  }
})

const iconMap = {
  'Promotion': Promotion,
  'Headset': Headset,
  'Upload': Upload,
  'Document': Document
}
</script>

<template>
  <div class="steps-container">
    <h3 class="section-title">
      <el-icon>
        <Connection />
      </el-icon>
      处理进度
    </h3>
    <el-steps :active="activeStep" finish-status="success" class="custom-steps" align-center>
      <el-step v-for="(step, index) in steps" :key="index" :title="step.title">
        <template #icon>
          <div class="step-icon-wrapper" :class="{
            'processing': step.status === 'processing',
            'success': step.status === 'success',
            'error': step.status === 'error'
          }">
            <el-icon>
              <component :is="step.status === 'success' ? Check :
                step.status === 'error' ? CircleCloseFilled :
                  iconMap[step.icon]
                " />
            </el-icon>
          </div>
        </template>
      </el-step>
    </el-steps>
  </div>
</template>

<style scoped>
.steps-container {
  width: 100%;
  box-sizing: border-box;
  background-color: #ffffff;
  border-radius: 12px;
  padding: 1.8rem;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
  border: 1px solid #ebeef5;
}

.section-title {
  font-size: 1.1rem;
  color: #303133;
  margin-bottom: 1.2rem;
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

.custom-steps {
  width: 100%;
  box-sizing: border-box;
}

.step-icon-wrapper {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: #f5f7fa;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  margin: 0 auto;
  position: relative;
  overflow: hidden;
  border: 1px solid #dcdfe6;
  color: #909399;
}

.step-icon-wrapper.success {
  background: #ecf5ff;
  color: #409EFF;
  border: 2px solid #409EFF;
  box-shadow: 0 0 8px rgba(64, 158, 255, 0.2);
}

.step-icon-wrapper.processing {
  background: var(--el-color-primary);
  color: #fff;
  border: 2px solid var(--el-color-primary);
  box-shadow: 0 0 0 0 rgba(64, 158, 255, 0.7);
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(64, 158, 255, 0.7);
  }

  70% {
    box-shadow: 0 0 0 10px rgba(64, 158, 255, 0);
  }

  100% {
    box-shadow: 0 0 0 0 rgba(64, 158, 255, 0);
  }
}

.step-icon-wrapper.error {
  background: var(--el-color-danger-light-9);
  color: var(--el-color-danger);
  border: 2px solid var(--el-color-danger);
}

:deep(.el-step__icon.is-icon) {
  background: transparent !important;
  border: none;
}

:deep(.el-step__line) {
  background-color: #dcdfe6;
  /* 默认线条为灰色 */
  height: 2px;
}

:deep(.el-step.is-success) {

  .el-step__title,
  .el-step__description {
    color: #303133;
    font-weight: 600;
  }

  .el-step__line {
    background-color: #409EFF !important;
    /* 修改为蓝色，添加!important */
  }
}

:deep(.el-step.is-success + .el-step .el-step__line) {
  background-color: #409EFF !important;
  /* 确保下一个步骤的线条也是蓝色 */
}

:deep(.el-step__head.is-success .el-step__line) {
  background-color: #409EFF !important;
  /* 成功步骤头部的线条 */
}

:deep(.el-step__head.is-success + .el-step__main .el-step__line) {
  background-color: #409EFF !important;
  /* 成功步骤后的主体线条 */
}

:deep(.el-step.is-process) {

  .el-step__title,
  .el-step__description {
    color: #303133;
    font-weight: 600;
  }

  /* 处理中状态线条保持默认灰色 */
}

:deep(.el-step.is-error) {

  .el-step__title,
  .el-step__description {
    color: #303133;
    font-weight: 600;
  }

  .el-step__line {
    background-color: var(--el-color-danger);
    /* 错误状态线条为红色 */
  }
}

/* 全面覆盖所有边框和文本颜色，确保成功状态的所有颜色都是蓝色 */
:deep(.el-step.is-success .el-step__icon),
:deep(.el-step__head.is-success),
:deep(.el-step__head.is-success .el-step__icon),
:deep(.el-step__head.is-success .el-step__icon.is-text),
:deep(.el-step__head.is-success .el-step__icon-inner) {
  color: #409EFF !important;
}


@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(64, 158, 255, 0.7);
  }

  70% {
    box-shadow: 0 0 0 10px rgba(64, 158, 255, 0);
  }

  100% {
    box-shadow: 0 0 0 0 rgba(64, 158, 255, 0);
  }
}

/* 设置所有步骤文字的基础样式 */
:deep(.el-step__title) {
  font-size: 14px !important;
  /* 固定文字大小为12px */
  color: #303133 !important;
  /* 设置为黑色 */
  margin-top: 8px;
  /* 增加与图标的间距 */
  transition: none;
  /* 禁用颜色过渡效果 */
}

/* 确保等待状态的文字也是12px黑色 */
:deep(.el-step.is-wait) .el-step__title,
:deep(.el-step__title.is-wait) {
  font-size: 12px !important;
  color: #303133 !important;
  font-weight: normal;
}

:deep(.el-step__title:not(.is-wait)) {
  font-weight: 600;
  /* 保持非等待状态标题加粗 */
}

/* 添加屏幕高度相关的媒体查询 */
@media screen and (max-height: 800px) {
  .steps-container {
    padding: 1.4rem;
  }

  .section-title {
    font-size: 1rem;
    margin-bottom: 1rem;
    gap: 6px;
  }

  .section-title .el-icon {
    font-size: 1.1rem;
  }

  .step-icon-wrapper {
    width: 32px;
    height: 32px;
  }
}

@media screen and (max-height: 700px) {
  .steps-container {
    padding: 1.2rem 1rem;
  }

  .section-title {
    margin-bottom: 0.8rem;
  }

  .step-icon-wrapper {
    width: 28px;
    height: 28px;
  }

  :deep(.el-step__title) {
    font-size: 12px !important;
  }
}
</style>
