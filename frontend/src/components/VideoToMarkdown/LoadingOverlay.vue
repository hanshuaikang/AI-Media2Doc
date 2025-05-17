<template>
    <div class="loading-overlay">
        <div class="lottie-container">
            <LottieAnimation :animationData="lottieSrc" :width="150" :height="150" :loop="true" :autoplay="true" />
        </div>
        <div class="main-text">正在智能处理您的内容</div>
        <div class="progress-bar-outer" v-if="percent !== undefined && percent !== null">
            <div class="progress-bar-inner" :style="{ width: percent + '%' }"></div>
        </div>
        <div class="step-row">
            <span class="step-text">{{ stepText }}</span>
            <span class="percent-text" v-if="percent !== undefined && percent !== null">{{ percent }}%</span>
        </div>
        <div class="sub-text">
            请勿关闭或者离开此页面
        </div>
    </div>
</template>

<script setup>
import { computed } from 'vue'
import { LottieAnimation } from 'lottie-web-vue'
import lottieSrc from '../../assets/lottie/loading.json'

const props = defineProps({
    stepText: {
        type: String,
        default: ''
    },
    percent: {
        type: [Number, String],
        default: null
    }
})
</script>

<style scoped>
.loading-overlay {
    position: absolute;
    left: 260px;
    right: 0;
    top: 0;
    bottom: 0;
    z-index: 9999;
    background: rgba(255, 255, 255, 0.96);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    transition: opacity 0.2s;
}

.lottie-container {
    /* 控制整体缩放和最大尺寸 */
    max-width: 500px;
    max-height: 500px;
    transform: scale(0.5);
    margin-bottom: 0.5em;
    opacity: 0.96;
    display: flex;
    align-items: center;
    justify-content: center;
    animation: floatY 2.2s ease-in-out infinite alternate;
}

@keyframes floatY {
    0% {
        transform: translateY(0);
    }

    100% {
        transform: translateY(-18px);
    }
}

.main-text {
    font-size: 1.08rem;
    font-weight: 800;
    color: #23272f;
    letter-spacing: 0.5px;
    margin-bottom: 0.7em;
    text-shadow: 0 2px 16px #fff, 0 1px 2px #e5e7eb;
    text-align: center;
}

.progress-bar-outer {
    width: 220px;
    height: 8px;
    background: #f3f4f6;
    border-radius: 6px;
    margin-bottom: 0.7em;
    overflow: hidden;
    box-shadow: 0 1px 4px 0 rgba(60, 80, 120, 0.07);
    position: relative;
}

.progress-bar-inner {
    height: 100%;
    background: linear-gradient(90deg, #409EFF 60%, #67C23A 100%);
    border-radius: 6px;
    transition: width 0.3s cubic-bezier(.4, 0, .2, 1);
}

.step-row {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5em;
    margin-bottom: 0.6em;
}

.step-text {
    color: #409EFF;
    font-weight: 700;
    font-size: 1.08em;
    opacity: 0.92;
    letter-spacing: 0.1px;
    background: linear-gradient(90deg, #409EFF 60%, #67C23A 100%);
    background-clip: text;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.percent-text {
    color: #888;
    font-size: 1.07em;
    margin-left: 0.2em;
    opacity: 0.7;
    font-weight: 600;
    letter-spacing: 0.1px;
}

.sub-text {
    font-size: 0.89rem;
    color: #6b7280;
    font-weight: 500;
    margin-top: 0.5em;
    opacity: 0.85;
    letter-spacing: 0.1px;
    text-align: center;
}

.loading-text {
    display: none;
}
</style>
