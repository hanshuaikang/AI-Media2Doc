<script setup>
import { ElRadioGroup, ElRadio } from 'element-plus'
import { PictureFilled } from '@element-plus/icons-vue'

const props = defineProps({
  modelValue: {
    type: String,
    default: 'note'
  },
  disabled: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue'])
</script>

<template>
  <div class="style-section" :class="{ 'disabled': disabled }">
    <h3 class="section-title">
      <el-icon>
        <PictureFilled />
      </el-icon>
      选择图文风格
    </h3>
    <div class="style-selector">
      <el-radio-group :modelValue="modelValue" @update:modelValue="val => emit('update:modelValue', val)"
        class="style-options" :disabled="disabled">
        <el-radio label="note" class="style-option">
          <img src="../../assets/笔记.svg" class="style-icon" />
          知识笔记
        </el-radio>
        <el-radio label="summary" class="style-option">
          <img src="../../assets/汇总.svg" class="style-icon" />
          内容总结
        </el-radio>
        <el-radio label="xiaohongshu" class="style-option">
          <img src="../../assets/小红书.svg" class="style-icon" />
          小红书风格
        </el-radio>
        <el-radio label="wechat" class="style-option">
          <img src="../../assets/微信公众号.svg" class="style-icon" />
          公众号风格
        </el-radio>
        <el-radio label="mind" class="style-option">
          <img src="../../assets/思维导图.svg" class="style-icon" />
          思维导图
        </el-radio>
      </el-radio-group>
    </div>
  </div>
</template>

<style scoped>
.style-section {
  width: 100%;
  box-sizing: border-box;
  margin: 0;
  margin-top: 20px;
  position: relative;
}

.style-section.disabled::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  pointer-events: none;
  z-index: 1;
}

.style-selector {
  background-color: #ffffff;
  border-radius: 12px;
  padding: 1.2rem 1.5rem;
  /* 调整内部填充，因为没有标题了 */
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
  border: 1px solid #ebeef5;
  box-sizing: border-box;
}

.section-title {
  font-size: 1.1rem;
  color: #303133;
  margin-bottom: 0.7rem;
  font-weight: 600;
  text-align: left;
  display: flex;
  align-items: center;
  gap: 8px;
  padding-left: 0.2rem;
}

.section-title .el-icon {
  font-size: 1.2rem;
  color: var(--el-color-primary);
}

.style-options {
  display: flex;
  justify-content: space-between;
  flex-wrap: nowrap;
  width: 100%;
  overflow-x: auto;
  padding-bottom: 4px;
}

.style-option {
  display: flex;
  align-items: center;
  gap: 0.3rem;
  padding: 0.6rem 0.8rem;
  border-radius: 8px;
  transition: all 0.3s ease;
  margin: 0;
  border: 1px solid transparent;
  flex: 1;
  min-width: auto;
  justify-content: center;
  white-space: nowrap;
}

.style-option:hover {
  background-color: #f5f7fa;
}

.style-icon {
  width: 20px;
  height: 20px;
  vertical-align: middle;
}

.style-option :deep(.el-radio__label) {
  display: flex;
  align-items: center;
  gap: 0.3rem;
  font-size: 0.9rem;
  color: #303133;
}

.style-option :deep(.el-radio__input.is-checked + .el-radio__label) {
  color: var(--el-color-primary);
  font-weight: 500;
}

.style-option :deep(.el-radio__input.is-checked)~.el-radio__label {
  color: var(--el-color-primary);
}

/* 自定义滚动条，使其更美观 */
.style-options::-webkit-scrollbar {
  height: 4px;
}

.style-options::-webkit-scrollbar-thumb {
  background-color: rgba(0, 0, 0, 0.15);
  border-radius: 2px;
}

.style-options::-webkit-scrollbar-track {
  background-color: rgba(0, 0, 0, 0.05);
}

/* 禁用状态提示信息 */
.disabled-message {
  margin-top: 1rem;
  text-align: center;
  color: #909399;
  font-size: 0.9rem;
  padding: 0.5rem;
  background-color: #f9f9f9;
  border-radius: 6px;
  z-index: 2;
  position: relative;
}

/* 响应式调整 - 在非常小的屏幕上允许滚动 */
@media screen and (max-width: 768px) {
  .style-selector {
    padding: 1rem;
  }

  .style-option {
    padding: 0.5rem 0.6rem;
  }

  .style-option :deep(.el-radio__label) {
    font-size: 0.8rem;
  }

  .style-icon {
    width: 18px;
    height: 18px;
  }
}

/* 添加屏幕高度相关的媒体查询 */
@media screen and (max-height: 800px) {
  .style-section {
    margin-top: 15px;
  }

  .section-title {
    font-size: 1rem;
    margin-bottom: 0.6rem;
    /* 减小外部标题和卡片之间的距离 */
    gap: 6px;
  }

  .style-selector {
    padding: 1rem 1.2rem;
    /* 调整内部填充 */
  }
}

@media screen and (max-height: 700px) {
  .style-section {
    margin-top: 12px;
  }

  .style-selector {
    padding: 0.8rem 1rem;
    /* 调整内部填充 */
  }

  .section-title {
    margin-bottom: 0.5rem;
    /* 减小标题和卡片之间的距离 */
  }

  .style-options {
    padding-bottom: 2px;
  }
}
</style>
