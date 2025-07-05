<template>
    <div class="about-settings">
        <div class="about-highlight-tip">
            🎉 感谢支持！关注下方公众号或小红书，获取最新版本更新以及反馈您的建议
        </div>
        <h2 style="margin-top:0;">AI 视频图文创作助手</h2>
        <p style="font-size:1.05rem;line-height:1.7;">
            AI 视频图文创作助手是一款 Web 工具, 基于 AI 大模型, 一键将视频和音频转化为各种风格的文档, 无需登录注册, 前后端本地部署，以极低的成本体验 AI 视频/音频转风格文档服务。
        </p>
        <div style="margin: 12px 0;">
            项目地址：
            <a href="https://github.com/hanshuaikang/AI-Media2Doc" target="_blank" style="color:#357aff;">
                https://github.com/hanshuaikang/AI-Media2Doc
            </a>
        </div>
        <div style="margin: 18px 0 0 0;">
            <span>赞助作者：</span>
            <a href="https://afdian.com/a/hanshu-github" target="_blank" style="color:#e67e22;font-weight:600;">
                我的爱发电主页
            </a>
        </div>
        <span style="color:#6b7280;font-size:0.95rem;">或者关注我的公众号或者小红书, 你的关注同样是我继续维护下去的动力!</span>
        <div class="about-qrcodes">
            <div class="about-qrcode-item">
                <div class="about-qrcode-title">公众号</div>
                <img :src="wechatQr" alt="公众号二维码" class="about-qrcode-img" />
            </div>
            <div class="about-qrcode-item">
                <div class="about-qrcode-title">小红书</div>
                <img :src="xiaohongshuQr" alt="小红书二维码" class="about-qrcode-img" />
            </div>
        </div>
    </div>
</template>
<script setup>
const wechatQr = new URL('../../assets/wechat-qr.jpg', import.meta.url).href
const xiaohongshuQr = new URL('../../assets/xiaohongshu-qr.png', import.meta.url).href
</script>
<style scoped>
.about-settings {
    width: 100%;
    max-width: 700px;
    margin: 0;
    color: #23272f;
    font-size: 1.01rem;
    line-height: 1.7;
    background: #fff;
    border-radius: 8px;
    padding: 8px 4px 8px 0;
    text-align: left;
}

.about-highlight-tip {
    background: linear-gradient(90deg, #eaf2ff 0%, #fffbe6 100%);
    color: #d35400;
    font-size: 1.09rem;
    font-weight: 700;
    border-left: 5px solid #ffd666;
    border-radius: 7px;
    padding: 10px 18px;
    margin-bottom: 18px;
    margin-top: 2px;
    letter-spacing: 0.2px;
    box-shadow: 0 2px 8px 0 rgba(53, 122, 255, 0.06);
    text-align: left;
}

.about-settings a {
    text-decoration: underline;
    word-break: break-all;
}

.about-qrcodes {
    display: flex;
    gap: 36px;
    margin-top: 18px;
    margin-bottom: 8px;
    justify-content: flex-start;
    align-items: flex-end;
}

.about-qrcode-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    background: #fff;
    border-radius: 10px;
    box-shadow: 0 2px 12px 0 rgba(53, 122, 255, 0.06);
    border: 1.5px solid #eaf2ff;
    padding: 10px 18px 12px 18px;
}

.about-qrcode-title {
    font-size: 1.01rem;
    font-weight: 600;
    color: #357aff;
    margin-bottom: 7px;
    letter-spacing: 0.5px;
}

.about-qrcode-img {
    width: 110px;
    height: 110px;
    border-radius: 14px;
    border: 2px solid #ffd6e0;
    background: #fff;
    object-fit: contain;
    box-shadow: 0 2px 8px 0 rgba(255, 99, 132, 0.08);
}
</style>
