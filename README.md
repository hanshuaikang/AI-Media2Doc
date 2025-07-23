<h1 align="center">
  <p>
  <img src="docs/images/readme_header.jpg" alt="logo">
    </p>
</h1>

<p align="center">
    <a href="https://hellogithub.com/repository/d869461d98d245d388b50e25b6a80dae" target="_blank"><img src="https://abroad.hellogithub.com/v1/widgets/recommend.svg?rid=d869461d98d245d388b50e25b6a80dae&claim_uid=uT2Sc8Xli4PUA76" alt="Featured｜HelloGitHub" style="width: 250px; height: 54px;" width="250" height="54" /></a>
</p>

<p align="center">
  <a href="./LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="MIT License"></a>
  <img src="https://img.shields.io/badge/Platform-Web-orange" alt="Web Platform">
  <img src="https://img.shields.io/badge/Docker-Support-blue?logo=docker" alt="Docker Support">
</p>


### 📖 简介

AI 视频图文创作助手是一款 Web 工具, 基于 AI 大模型, 一键将视频和音频转化为各种风格的文档, 无需登录注册, 前后端本地部署，以极低的成本体验 AI 视频/音频转风格文档服务。

### ✨ 核心功能

- ✅ **完全开源**：MIT 协议授权，支持本地部署。
- 🔒 **隐私保护**：无需登录注册，任务记录保存在本地
- 💻 **前端处理**：采用 ffmpeg wasm 技术，无需本地安装 ffmpeg
- 🎯 **多种风格支持**：支持小红书/公众号/知识笔记/思维导图/内容总结等多种文档风格支持。
- 🤖 **AI 对话**：支持针对视频内容进行 AI 二次问答。
- 🎬 **支持字幕导出**: 结果一键导出为字幕文件。
- 🖼️ **智能截图**: 基于字幕信息智能截图并插入文章, 无需视觉大模型, 实现真正的图文并茂。
- 🎨 **支持自定义 Prompt**：支持在前端自定义配置 prompt。
- 🐳 **一键部署**：支持 Docker 一键部署。
- 🔒 **支持设置访问密码**: 后端设置访问密码之后, 前端用户需要填写该密码才可以正常使用。


### 🔜 未来计划
- 🎙️ 音频识别支持使用 fast-whisper 本地大模型处理，进一步降低成本

### 💬 哪里可以找到我
公众号(韩数同学)
<p align="left">
    <img src="docs/images/wxgzh/hstx.jpg" alt="index" width="20%">
</p>

或者首页置顶 issue 加入微信交流群. 如果部署遇到问题，我下班之后看到后一般会回复。


### 项目截图

#### 全新设计的首页, 尽力之作

<p align="center">
    <img src="docs/images/index.jpg" alt="index" width="80%">
</p>

#### 更加简洁的加载页
<p align="center">
<img src="docs/images/loading.png" alt="task details" width="80%">
</p>

#### 全新功能: 支持智能截图并插入到文中对应位置(本地方案, 无需视觉大模型, 0成本)

开启方式, 点击自定义设置->智能截图 选择打开。


<p align="center">
<img src="docs/images/screenshot.png" alt="task details" width="80%">
</p>

#### 全新设计的结果页, 支持一键导出为字幕。
<p align="center">
<img src="docs/images/details.png" alt="task details" width="80%">
</p>

#### 支持自定义 prompt
<p align="center">
<img src="docs/images/custom_prompt.png" alt="task details" width="80%">
</p>


#### 可基于视频内容进行 AI 二次对话

<p align="center">
<img src="docs/images/ai_talk.png" alt="mindmap" width="80%">
</p>


### 📦 docker 本地一键部署
0️⃣：安装 `docker`, 这个网上有教程

1️⃣：镜像构建, 在项目根目录下执行:
```shell
$ make docker-image
```
2️⃣：请根据 [后端部署指引 / 配置项说明](https://github.com/hanshuaikang/AI-Media2Doc/blob/main/backend/README.md#%E5%9C%A8%E7%81%AB%E5%B1%B1%E5%BC%95%E6%93%8E%E8%8E%B7%E5%8F%96%E5%AF%B9%E5%BA%94%E7%9A%84%E7%8E%AF%E5%A2%83%E5%8F%98%E9%87%8F%E7%9A%84%E5%80%BC) 完善根目录下的 `variables.env` 文件。 

3️⃣：运行项目,在项目根目录下执行:

```shell
$ make run
```

### 👾 开发者的废话

AI 视频创作助手源于我年初的一个想法, 作为一个喜欢阅读的人, 我更希望将一些视频内容转化为文字, 方便我进行二次阅读思考和总结记录笔记, 但市面上并没有一个好的工具来实现这个想法, 大多数工具都需要登录和付费, 我不太想在互联网上注册过多的账号, 同时也不想将自己想要总结的内容上传至除了云厂商之外的第三方平台，因此我开发了这个小应用，MIT 协议, 任何人都可以以极低的成本去体验音视频转文本。


### 🔄 处理流程

<p align="center">
<img src="docs/images/process_flow.jpg" alt="architecture" width="80%">
</p>

### 🔧 本地开发指南

- [后端本地部署](./backend/README.md)
- [前端本地部署](./frontend/README.md)

### 📄 许可证

本项目采用 [MIT 许可证](./LICENSE)

### 🔗 相关链接

- [volcengine-ai-app-lab](https://github.com/volcengine/ai-app-lab)

- [throttled-py](https://github.com/ZhuoZhuoCrayon/throttled-py)：✨Python 限流库，合理限制、平滑云资源用量。

### 🌵 支持开发者
你可以关注我的小红书:

[韩数同学： 致力于分享 Github 上那些好玩、有趣、免费、实用的高质量项目](https://www.xiaohongshu.com/user/profile/5e2992b000000000010064a4)

微信公众号: **韩数同学**

**或者请我吃一包辣条** , 作为一个超级喜欢吃辣条的人, 很多晚上维护开源项目都是边吃辣条边写代码的 🤪。如果你有很喜欢吃的辣条, 你可以投喂我吃一包辣条, 5毛一包的也可以, 我将直接开启代码狂暴模式(化身八爪鱼: 🐙)。

请留下你要赞助作者的辣条名称 (🤩❤️‍🔥): 支持卫龙/麻辣王子/博士牛筋/臭干子，禁止投喂(🥵😵😵‍💫🤧🥴): **缺牙齿**/**霸王丝**等有损本人生命值的辣条。

同时请备注你的 github 名称, 方便我整理展示在项目主页。🙌

<p align="left">
 赞助作者: <a href="https://afdian.com/a/hanshu-github">我的爱发电主页</a>
</p>

**赞助名单**

| 赞助者          | 渠道  | 金额    | 备注                             |
|--------------|-----|-------|--------------------------------|
| LMseventeen  | 爱发电 | 9.9元  | 请作者吃包辣条(买了卫龙)                  |
| 甄选网创云        | 爱发电 | 19.8元 | 开源正能量, 请作者吃辣条哈哈哈，超好用，完美解决了我的困扰 |
| 小红书博主: 摸鱼的小李 | 爱发电 | 59.4元 | 大家都去关注的他的小红书哇，很好的一个账号          |


### 🙌 致谢
感谢这些朋友对本项目做出的贡献:

|  |  |                                                                                                                        |
|:-:|:-:|:----------------------------------------------------------------------------------------------------------------------:|
| <a href="https://github.com/ZhuoZhuoCrayon"><img src="https://github.com/ZhuoZhuoCrayon.png" width="50" height="50"/><br/>crayon</a> | <a href="https://github.com/cjx929"><img src="https://github.com/cjx929.png" width="50" height="50"/><br/>chen_jx</a> | <a href="https://github.com/LMseventeen"><img src="https://github.com/LMseventeen.png" width="50" height="50"/><br/>LMseventeen</a>  |

感谢以下自媒体对本项目的关注和转发(以下排名不分先后), 大家感兴趣的话可以关注下他们 ～

| [HelloGithub](https://hellogithub.com)   |                           开源AI项目落地                            |                               [阮一峰的网络日志](https://www.ruanyifeng.com/blog/weekly/)                               |                               一飞开源                               |                             胖氪笔记                              |                          逛逛Github                            |                    小红书: 摸鱼的小李                            |
|:----:|:-------------------------------------------------------------:|:---------------------------------------------------------------------------------------------------------------:|:------------------------------------------------------------:|:-------------------------------------------------------------:|:------------------------------------------------------------:|:------------------------------------------------------------:|
|<img src="docs/images/wxgzh/hellogithub.png" width="80" height="80"/>|<img src="docs/images/wxgzh/aild.png" width="80" height="80"/> |<img src="docs/images/wxgzh/ryf.png" width="80" height="80"/> | <img src="docs/images/wxgzh/yf.png" width="80" height="80"/> | <img src="docs/images/wxgzh/pk.png" width="80" height="80"/>  | <img src="docs/images/wxgzh/gg.png" width="80" height="80"/> | <img src="docs/images/wxgzh/myxl.png" width="80" height="80"/> 

小红书:
[AI-GitHub](https://www.xiaohongshu.com/user/profile/65c44d1200000000090254fc) | [逛逛Github](https://www.xiaohongshu.com/user/profile/65e05165000000000500b059)


推特:
| [Geek](https://x.com/geekbb) | [AIGCLINK](https://x.com/aigclink) | [ilovelife](https://x.com/ilovek8s) | [ahhhhfs](https://x.com/abskoop)

### 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=hanshuaikang/AI-Media2Doc&type=Date)](https://www.star-history.com/#hanshuaikang/AI-Media2Doc&Date)

