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
    width: 100%;
    max-width: 500px;
    margin: 0;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: flex-start;
    background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
    border-radius: 12px;
    padding: 24px 32px 24px 32px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    min-height: 220px;
    border: 1px solid #e2e8f0;
}

.password-title {
    font-size: 18px;
    font-weight: 700;
    margin: 0 0 16px 0;
    color: #1e293b;
    letter-spacing: 0.2px;
    align-self: flex-start;
    display: flex;
    align-items: center;
    gap: 8px;
}

.password-title::before {
    content: '';
    width: 4px;
    height: 18px;
    background: linear-gradient(135deg, #3b82f6, #8b5cf6);
    border-radius: 2px;
}

.password-tip {
    color: #64748b;
    font-size: 14px;
    margin-bottom: 24px;
    line-height: 1.7;
    text-align: left;
    background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
    border-left: 4px solid #94a3b8;
    padding: 12px 16px;
    border-radius: 8px;
    width: 100%;
    align-self: flex-start;
    box-shadow: 0 2px 8px rgba(148, 163, 184, 0.1);
}

.password-form-row {
    display: flex;
    align-items: center;
    width: 100%;
    margin-bottom: 20px;
    gap: 16px;
    justify-content: flex-start;
    background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
    padding: 16px 20px;
    border-radius: 10px;
    border: 1px solid #e2e8f0;
}

.password-label {
    font-size: 15px;
    font-weight: 600;
    color: #1e293b;
    min-width: 100px;
    text-align: left;
    margin-bottom: 0;
    letter-spacing: 0.1px;
}

.password-input {
    flex: 1;
    max-width: 280px;
    min-width: 160px;
}

.password-save-btn-row {
    margin-top: 12px;
    display: flex;
    align-items: center;
    gap: 16px;
    align-self: flex-start;
}

.save-btn-row {
    margin-top: 12px;
    display: flex;
    align-items: center;
    gap: 16px;
}

.save-success-msg {
    color: #059669;
    font-size: 14px;
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 6px;
}

.save-success-msg::before {
    content: '✓';
    font-weight: bold;
}
</style>
