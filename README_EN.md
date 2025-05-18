<h1 align="center">
  <p>
  <img src="docs/images/logo.jpeg" alt="logo" width="50" height="50" style="border-radius: 50%;">
 </p>
  AI Media2Doc Assistant
</h1>

<p align="center">
    <em>Based on AI large models, convert videos and audios to various document styles like Xiaohongshu/WeChat Official Account/Knowledge Notes/Mind Maps with one click.</em>
</p>

<p align="center">
  <a href="./LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="MIT License"></a>
  <img src="https://img.shields.io/badge/Platform-Web-orange" alt="Web Platform">
</p>

<p align="center">
    <img src="docs/images/index.png" alt="index" width="80%">
</p>

[中文文档](./README.md)

### 📖 Introduction

AI Media2Doc Assistant is a web tool based on AI large models that converts videos and audios to various document styles with one click. No login or registration required, with both frontend and backend supporting local deployment. Experience AI video/audio to styled document conversion services at an extremely low cost - I spent just five dollars for a month of development and testing.

### ✨ Core Features

- ✅ **Fully Open Source**: Licensed under MIT, supports local deployment.
- 🔒 **Privacy Protection**: No login or registration required, task records saved locally.
- 💻 **Frontend Processing**: Uses ffmpeg wasm technology, no need to install ffmpeg locally.
- 🎯 **Multiple Style Support**: Supports various document styles like Xiaohongshu/WeChat Official Account/Knowledge Notes/Mind Maps/Content Summaries.
- 🤖 **AI Conversation**: Supports secondary Q&A based on video content.
- 🤖 **Local Deployment Friendly**: With basic development knowledge, you can get it running in no time.
- 🐳 **One-Click Deployment**: Supports one-click deployment with Docker.

### 🔜 Future Plans

- 📷 Support intelligent extraction of video key frames, achieving true integration of text and images
- 🎙️ Support audio recognition using fast-whisper local large model processing to further reduce costs
- 🎨 Completely rebuild the frontend page using React for a smoother experience

### 📦 Installation Guide

1) Image Build:

```shell
$ make docker-image
```

2) Please refer to the [Backend Deployment Guide / Configuration Instructions](https://github.com/hanshuaikang/AI-Media2Doc/blob/main/backend/README.md#%E5%9C%A8%E7%81%AB%E5%B1%B1%E5%BC%95%E6%93%8E%E8%8E%B7%E5%8F%96%E5%AF%B9%E5%BA%94%E7%9A%84%E7%8E%AF%E5%A2%83%E5%8F%98%E9%87%8F%E7%9A%84%E5%80%BC) to complete the `variables.env` file in the root directory.

3) Run the Project:

```shell
$ make run
```

### 👾 Developer's Note

The AI Media2Doc Assistant originated from an idea I had at the beginning of the year. As someone who enjoys reading, I prefer to convert video content into text for easier re-reading, thinking, and note-taking. However, I couldn't find a good tool to achieve this - most tools required login and payment. I didn't want to register too many accounts on the internet, nor did I want to upload my content to third-party platforms other than cloud providers. Therefore, I developed this small application under the MIT license, allowing anyone to experience audio/video to text conversion at a minimal cost.

### Project Screenshots

#### Support AI Q&A based on video content
<p align="center">
<img src="docs/images/task_details.png" alt="task details" width="80%">
</p>

#### Support mind map generation

Generated mind maps can be exported to third-party platforms for editing and optimization
<p align="center">
<img src="docs/images/mindmap.png" alt="mindmap" width="80%">
</p>

### 🔄 Processing Flow

<p align="center">
<img src="docs/images/process_flow.png" alt="architecture" width="80%">
</p>

### 🔧 Local Development Guide

- [Backend Local Deployment](./backend/README.md)
- [Frontend Local Deployment](./frontend/README.md)

### 📄 License

This project is licensed under the [MIT License](./LICENSE)

### 🔗 Related Links

- [volcengine-ai-app-lab](https://github.com/volcengine/ai-app-lab)
- [throttled-py](https://github.com/ZhuoZhuoCrayon/throttled-py): ✨Python rate-limiting library, reasonably limits and smooths cloud resource usage.


[韩数的开发笔记： 致力于分享 Github 上那些好玩、有趣、免费、实用的高质量项目](https://www.xiaohongshu.com/user/profile/5e2992b000000000010064a4)

### 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=hanshuaikang/AI-Media2Doc&type=Date)](https://www.star-history.com/#hanshuaikang/AI-Media2Doc&Date)