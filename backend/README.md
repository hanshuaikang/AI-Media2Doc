# 后端部署教程

后端依赖于字节跳动火山引擎高代码 SDK Arkitect [高代码 SDK Arkitect](https://github.com/volcengine/ai-app-lab/blob/main/arkitect/README.md)。 
在启动后端服务之前, 需要先安装好 Arkitect 的依赖, 并且申请字节 Tos 对象存储服务 以及 对应大模型的 API 调用权限

## 1. 安装依赖
```bash
pip install -r requirements.txt
```

## 2. 配置环境变量

```bash
export ENDPOINT_ID=xxxx
export ARK_API_KEY=xxxx
export TOS_ACCESS_KEY=xxxx
export TOS_SECRET_KEY=xxxx
export TOS_ENDPOINT=xxxx
export TOS_REGION=xxxx
export TOS_BUCKET=xxxx
export AUC_APP_ID=xxxx
export AUC_ACCESS_TOKEN=xxxx
```


## 3. 启动服务
```bash
python app.py
```

## 在火山引擎获取对应的环境变量的值
主要分为三部分, 火山方舟/字节Tos/音频识别大模型

### 火山方舟
#### ENDPOINT_ID
登录[方舟控制台](https://console.volcengine.com/ark/region:ark+cn-beijing/endpoint?projectName=default)，创建一个推理接入点（Endpoint），推荐使用Doubao-pro-32k [参考文档](https://www.volcengine.com/docs/82379/1399008#_2-%E5%88%9B%E5%BB%BA%E5%9C%A8%E7%BA%BF%E6%8E%A8%E7%90%86%E6%8E%A5%E5%85%A5%E7%82%B9%EF%BC%88endpoint%EF%BC%89) 你就得到了 `ENDPOINT_ID` 的 值。
#### ARK_API_KEY
在 API Key 管理中创建一个 API Key [参考文档](https://www.volcengine.com/docs/82379/1399008#_3-%E5%88%9B%E5%BB%BAAPIKey) 你就得到了 `ARK_API_KEY` 的值。

### 火山引擎对象存储服务
#### 创建 bucket 设置跨域规则
登录[对象存储控制台](https://console.volcengine.com/tos) 创建一个 bucket, 创建完毕之后进入该 bucket。点击右侧权限管理, 找到跨域访问设置, 新建一条跨域访问规则。
<p>
<img src="../docs/images/cors.png" alt="tos access key">
</p>
当然你也可以根据实际情况灵活选择。

#### TOS_BUCKET
`TOS_BUCKET` 的值就是你创建的 bucket 的名称。

#### TOS_REGION
`TOS_REGION` 的值就是你创建的 bucket 的区域, 例如 `cn-beijing`。


#### TOS_ACCESS_KEY 和 TOS_SECRET_KEY
进入 [IAM控制台](https://console.volcengine.com/iam/keymanage) 创建一个访问密钥,
你就得到了 `TOS_ACCESS_KEY` 和 `TOS_SECRET_KEY` 的值。


### 音频识别大模型
登录录音文件识别大模型控制台(https://console.volcengine.com/speech/service), 点击右侧录音文件识别大模型， 创建一个应用, 你就得到了 `AUC_APP_ID` 和 `AUC_ACCESS_TOKEN` 的值。
#### AUC_APP_ID
`AUC_APP_ID` 的值就是你创建的应用的 ID。

#### AUC_ACCESS_TOKEN
`AUC_ACCESS_TOKEN` 的值就是你创建的应用的 Access Token。







