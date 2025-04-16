<h1 align="center">
  <p>
  <img src="docs/images/logo.jpeg" alt="logo" width="50" height="50" style="border-radius: 50%;">
 </p>
  AI 视频图文创作助手
</h1>
<p align="center">
    <em> AI 图文创作助手基于AI大模型, 支持将基于任意视频/音频转换成各种风格的文档, 目前支持内容总结/小红书/知识笔记/微信公众号和思维导图 </em>
</p>

<p align="center">
    <img src="docs/images/index.png" alt="index">
</p>

[English Document](./README_EN.md)

**可基于视频内容二次对话**
<p align="center">
<img src="docs/images/task_details.png" alt="task details">
</p>

**支持生成思维导图**
生成的思维导图可以导出到第三方免费的平台进行编辑和调整
<p align="center">
<img src="docs/images/mindmap.png" alt="mindmap">
</p>

#### 开发者的话
AI 视频创作助手源于我年初的一个想法, 作为一个喜欢阅读的人, 我更希望将一些视频内容转化为文字, 方便我进行二次阅读思考和总结记录笔记, 但市面上并没有一个好的工具来实现这个想法, 大多数工具都需要登录和付费, 我不太想在互联网上注册过多的账号, 同时也不想将自己想要总结的内容上传至除了云厂商之外的第三方平台，因此我开发了这个小应用，MIT 协议, 任何人都可以以极低的成本去体验音视频转文本。


### 功能特点:
- 完全开源, 支持本地部署, 无需登录注册, 任务记录保存在本地。
- 音视频纯前端处理方案, 使用(ffmpeg wasm), 无需本地安装 ffmpeg。
- 支持视频/音频文件, 支持输出多种风格的文档, 包括小红书/知识笔记/微信公众号和思维导图。
- 支持针对视频内容进行AI二次对话。

### 未来计划:
- 支持智能截取视频关键帧, 实现真正的图文并茂。
- 音频识别支持使用 fast-whisper 本地大模型处理, 更进一步降低成本。
- 我前端有点菜, 我会努力把页面做的再好看些。
- 支持 docker 一键部署。

### 处理流程
<p align="center">
<img src="docs/images/process_flow.png" alt="architecture">
</p>

### 本地环境安装
- [后端本地部署](./backend/README.md)
- [前端本地部署](./frontend/README.md)


### 📄 License
- [MIT](./LICENSE)

### Links
- [volcengine-ai-app-lab](https://github.com/volcengine/ai-app-lab)

