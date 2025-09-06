<template>
    <div class="connectivity-settings">
        <h3 class="conn-title">后端连通性测试</h3>
        <div class="conn-tip">
            <el-icon style="margin-right:6px;color:#3b82f6;">
                <svg viewBox="0 0 1024 1024" width="16" height="16">
                    <path fill="currentColor"
                        d="M512 128a384 384 0 1 0 384 384A384 384 0 0 0 512 128zm0 704a320 320 0 1 1 320-320 320 320 0 0 1-320 320z" />
                </svg>
            </el-icon>
            用于检测前端后端的网络是否正常
        </div>

        <div class="conn-status-card">
            <div class="status-line">
                <span class="status-label">当前状态：</span>
                <span class="status-indicator" :class="indicatorClass"></span>
                <span class="status-text">{{ statusText }}</span>
            </div>
            <div class="meta-line">
                <span>最近检测：{{ lastCheckDisplay }}</span>
                <span v-if="health && health.timestamp" class="split-dot">|</span>
                <span v-if="health && health.timestamp">服务时间戳：{{ health.timestamp }}</span>
            </div>
            <div class="action-line">
                <el-button size="small" type="primary" :loading="loading" @click="runCheck">重新检测</el-button>
            </div>
        </div>

        <transition name="fade-slide">
            <div v-if="isHealthy" class="env-card">
                <div class="env-card-header">
                    <div class="env-card-title">
                        环境变量
                        <span class="env-subtip" v-if="secretsLoading">加载中...</span>
                        <span class="env-subtip error" v-else-if="secretsError">{{ secretsError }}</span>
                        <span class="env-subtip" v-else>共 {{ secretPairs.length }} 项</span>
                    </div>
                    <div class="env-card-actions">
                        <el-button size="small" link type="primary" @click="reloadSecrets" :disabled="secretsLoading">
                            刷新
                        </el-button>
                        <el-button size="small" link type="info" @click="toggleExpanded">
                            {{ isExpanded ? '收起' : '展开' }}
                        </el-button>
                    </div>
                </div>
                <transition name="fade-slide">
                    <div v-if="!secretsError && isExpanded" class="env-grid">
                        <div v-for="(item, idx) in secretPairs" :key="item.key" class="env-item">
                            <div class="env-key">
                                {{ idx + 1 }}. {{ item.key }}
                            </div>
                            <div class="env-value" :title="item.raw ?? '(未配置)'">
                                <span v-if="item.raw === null" class="env-null">(未配置)</span>
                                <span v-else>{{ item.raw }}</span>
                            </div>
                        </div>
                    </div>
                </transition>
            </div>
        </transition>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { checkHealth, getSecrets } from '../../apis'
import type { HealthCheckResponse, SecretsData } from '../../apis/types'
import { ElMessage } from 'element-plus'

const loading = ref(false)
const health = ref<HealthCheckResponse | null>(null)
const error = ref<string | null>(null)
const lastCheckAt = ref<number | null>(null)

const secrets = ref<SecretsData | null>(null)
const secretsLoading = ref(false)
const secretsError = ref<string | null>(null)
const showFull = ref(false)
const isExpanded = ref(false)

async function runCheck() {
    loading.value = true
    error.value = null
    try {
        const data = await checkHealth()
        health.value = data
        lastCheckAt.value = Date.now()
        ElMessage.success('健康检查成功')
        // 健康后拉取 secrets
        loadSecrets()
    } catch (e: any) {
        error.value = e?.message || '检查失败'
        health.value = null
        lastCheckAt.value = Date.now()
        ElMessage.error(error.value)
    } finally {
        loading.value = false
    }
}

async function loadSecrets() {
    secretsLoading.value = true
    secretsError.value = null
    try {
        secrets.value = await getSecrets()
    } catch (e: any) {
        secretsError.value = e?.message || '获取环境变量失败'
    } finally {
        secretsLoading.value = false
    }
}

function reloadSecrets() {
    loadSecrets()
}

function toggleExpanded() {
    isExpanded.value = !isExpanded.value
}

function maskValue(s: string): string {
    if (!s || typeof s !== 'string') return s || ''
    if (s.length <= 6) return '*'.repeat(s.length)
    const head = s.slice(0, 4)
    const tail = s.slice(-4)
    return `${head}${'*'.repeat(Math.max(4, s.length - 8))}${tail}`
}

function displayValue(raw: string | null) {
    if (raw === null || raw === undefined) return '(未配置)'
    return showFull.value ? raw : maskValue(raw)
}

onMounted(runCheck)

const isHealthy = computed(() => !!health.value && !error.value && health.value.status?.toLowerCase().includes('healthy'))
const indicatorClass = computed(() => {
    if (loading.value) return 'pending'
    if (isHealthy.value) return 'ok'
    if (error.value) return 'error'
    return 'unknown'
})
const statusText = computed(() => {
    if (loading.value) return '检测中...'
    if (isHealthy.value) return '正常'
    if (error.value) return '异常'
    return '未知'
})
const lastCheckDisplay = computed(() => {
    if (!lastCheckAt.value) return '—'
    return new Date(lastCheckAt.value).toLocaleString()
})

const secretPairs = computed(() => {
    if (!secrets.value) return []
    return Object.entries(secrets.value).map(([key, val]) => ({ key, raw: val }))
})
</script>

<style scoped>
.connectivity-settings {
    width: 100%;
    max-width: 600px;
    margin: 0;
    display: flex;
    flex-direction: column;
    background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
    border-radius: 12px;
    padding: 24px 32px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    border: 1px solid #e2e8f0;
}

.conn-title {
    font-size: 18px;
    font-weight: 700;
    margin: 0 0 16px 0;
    color: #1e293b;
    letter-spacing: 0.2px;
    position: relative;
}

.conn-title::before {
    content: '';
    width: 4px;
    height: 18px;
    background: linear-gradient(135deg, #3b82f6, #8b5cf6);
    border-radius: 2px;
    position: absolute;
    left: -12px;
    top: 2px;
}

.conn-tip {
    color: #64748b;
    font-size: 14px;
    line-height: 1.5;
    text-align: left;
    background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
    border-left: 4px solid #94a3b8;
    padding: 12px 16px;
    border-radius: 8px;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    /* 原: flex-start，改为垂直居中 */
    gap: 4px;
}

.conn-status-card {
    display: flex;
    flex-direction: column;
    gap: 14px;
    background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 20px 22px;
    position: relative;
    overflow: hidden;
}

.conn-status-card::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, #3b82f6, #8b5cf6);
    opacity: .8;
}

.status-line {
    display: flex;
    align-items: center;
    gap: 10px;
    font-weight: 600;
    color: #1e293b;
    font-size: 15px;
    line-height: 1.2;
    /* 降低行高避免基线偏差 */
}

.status-label {
    color: #475569;
    font-weight: 600;
}

.status-indicator {
    width: 14px;
    height: 14px;
    border-radius: 50%;
    box-shadow: 0 0 0 3px rgba(0, 0, 0, 0.04);
    position: relative;
    display: inline-block;
    vertical-align: middle;
    transform: translateY(1px);
    /* 微调向下 1px 对齐文字基线 */
}

.status-indicator.ok {
    background: #10b981;
    box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.15);
    animation: pulseOk 1.8s infinite;
}

.status-indicator.error {
    background: #ef4444;
    box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.18);
    animation: pulseErr 1.8s infinite;
}

.status-indicator.pending {
    background: #f59e0b;
    box-shadow: 0 0 0 3px rgba(245, 158, 11, 0.18);
    animation: pulsePend 1.4s infinite;
}

.status-indicator.unknown {
    background: #94a3b8;
    box-shadow: 0 0 0 3px rgba(148, 163, 184, 0.18);
}

.status-text {
    font-size: 15px;
    letter-spacing: 0.5px;
}

.meta-line {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    font-size: 13px;
    color: #64748b;
    line-height: 1.4;
}

.split-dot {
    color: #cbd5e1;
}

.action-line {
    display: flex;
    gap: 12px;
    align-items: center;
}

.fade-slide-enter-active,
.fade-slide-leave-active {
    transition: all .25s cubic-bezier(.55, 0, .1, 1);
}

.fade-slide-enter-from,
.fade-slide-leave-to {
    opacity: 0;
    transform: translateY(-8px);
}

.env-card {
    margin-top: 22px;
    background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 18px 22px 22px;
    position: relative;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    gap: 16px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
    transition: padding .25s ease, gap .25s ease;
}

.env-card-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    flex-wrap: wrap;
    gap: 12px;
}

.env-card-title {
    font-size: 15px;
    font-weight: 600;
    color: #1e293b;
    display: flex;
    align-items: center;
    gap: 10px;
}

.env-subtip {
    font-size: 12px;
    font-weight: 500;
    color: #64748b;
    background: rgba(148, 163, 184, 0.15);
    padding: 4px 8px;
    border-radius: 6px;
    line-height: 1.2;
}

.env-subtip.error {
    color: #b91c1c;
    background: rgba(239, 68, 68, 0.15);
}

.env-card-actions {
    display: flex;
    gap: 8px;
    align-items: center;
}

.env-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 12px;
}

.env-item {
    background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 10px 12px 12px;
    display: flex;
    flex-direction: column;
    gap: 6px;
    position: relative;
    transition: all .2s ease;
}

.env-item:hover {
    border-color: #3b82f6;
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
    background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
}

.env-key {
    font-size: 12px;
    font-weight: 600;
    letter-spacing: .3px;
    color: #334155;
    text-transform: none;
    word-break: break-all;
}

.env-value {
    font-size: 13px;
    font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
    color: #1e293b;
    word-break: break-all;
    line-height: 1.4;
}

.env-null {
    color: #94a3b8;
    font-style: italic;
}

.env-error-row {
    display: flex;
    gap: 12px;
    align-items: center;
    font-size: 13px;
    color: #b91c1c;
    background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
    padding: 12px 14px;
    border-radius: 10px;
    border: 1px solid #fca5a5;
}

/* 可选: 收起时鼠标悬浮头部增加指示(按需) */
/* .env-card.collapsed .env-card-header { cursor: pointer; } */

@keyframes pulseOk {
    0% {
        box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.25);
    }

    70% {
        box-shadow: 0 0 0 8px rgba(16, 185, 129, 0);
    }

    100% {
        box-shadow: 0 0 0 3px rgba(16, 185, 129, 0);
    }
}

@keyframes pulseErr {
    0% {
        box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.3);
    }

    70% {
        box-shadow: 0 0 0 8px rgba(239, 68, 68, 0);
    }

    100% {
        box-shadow: 0 0 0 3px rgba(239, 68, 68, 0);
    }
}

@keyframes pulsePend {
    0% {
        box-shadow: 0 0 0 3px rgba(245, 158, 11, 0.35);
    }

    70% {
        box-shadow: 0 0 0 8px rgba(245, 158, 11, 0);
    }

    100% {
        box-shadow: 0 0 0 3px rgba(245, 158, 11, 0);
    }
}
</style>
