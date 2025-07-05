<template>
    <div class="password-settings">
        <h3 class="password-title">Web 访问密码</h3>
        <div class="password-tip">
            如果服务端配置了访问密码，请在此输入。留空表示不使用密码。
        </div>
        <div class="password-form-row">
            <label class="password-label" for="web-access-password">访问密码：</label>
            <el-input id="web-access-password" v-model="webAccessPassword" type="password" placeholder="请输入 Web 访问密码"
                class="password-input" show-password clearable />
        </div>
        <div class="save-btn-row password-save-btn-row">
            <el-button type="primary" @click="savePassword">保存</el-button>
            <span v-if="passwordSaveSuccess" class="save-success-msg">已保存！</span>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElInput, ElButton, ElMessage } from 'element-plus'

function getLocalPassword() {
    try {
        return localStorage.getItem('webAccessPassword') || ''
    } catch {
        return ''
    }
}
function setLocalPassword(password) {
    if (password) {
        localStorage.setItem('webAccessPassword', password)
    } else {
        localStorage.removeItem('webAccessPassword')
    }
}
const webAccessPassword = ref(getLocalPassword())
const passwordSaveSuccess = ref(false)

function savePassword() {
    setLocalPassword(webAccessPassword.value)
    passwordSaveSuccess.value = true
    ElMessage.success('密码已保存到本地')
    setTimeout(() => {
        passwordSaveSuccess.value = false
    }, 2000)
}
</script>

<style scoped>
.password-settings {
    width: 420px;
    margin: 0;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: flex-start;
    background: #fff;
    border-radius: 8px;
    padding: 24px 32px 18px 32px;
    box-shadow: 0 2px 8px 0 rgba(60, 80, 120, 0.04);
    min-height: 220px;
}

.password-title {
    font-size: 1.18rem;
    font-weight: 700;
    margin: 0 0 12px 0;
    color: #23272f;
    letter-spacing: 0.2px;
    align-self: flex-start;
}

.password-tip {
    color: #6b7280;
    font-size: 0.97rem;
    margin-bottom: 22px;
    line-height: 1.7;
    text-align: left;
    background: #f8f9fa;
    border-left: 4px solid #d1d5db;
    padding: 8px 14px;
    border-radius: 4px;
    width: 100%;
    align-self: flex-start;
}

.password-form-row {
    display: flex;
    align-items: center;
    width: 100%;
    margin-bottom: 18px;
    gap: 12px;
    justify-content: flex-start;
}

.password-label {
    font-size: 1.03rem;
    font-weight: 600;
    color: #23272f;
    min-width: 84px;
    text-align: right;
    margin-bottom: 0;
    letter-spacing: 0.1px;
}

.password-input {
    flex: 1;
    max-width: 240px;
    min-width: 120px;
}

.password-save-btn-row {
    margin-top: 6px;
    display: flex;
    align-items: center;
    gap: 14px;
    align-self: flex-start;
}

.save-btn-row {
    margin-top: 8px;
    display: flex;
    align-items: center;
    gap: 14px;
}

.save-success-msg {
    color: #67C23A;
    font-size: 0.97rem;
}
</style>
