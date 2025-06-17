# -*- coding: UTF-8 -*-
import os

LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://ark.cn-beijing.volces.com/api/v3")
LLM_MODEL_ID = os.getenv("MODEL_ID")
LLM_API_KEY = os.getenv("ARK_API_KEY") or os.getenv("LLM_API_KEY")
TOS_ACCESS_KEY = os.getenv("TOS_ACCESS_KEY")
TOS_SECRET_KEY = os.getenv("TOS_SECRET_KEY")
TOS_ENDPOINT = os.getenv("TOS_ENDPOINT")
TOS_REGION = os.getenv("TOS_REGION")
TOS_BUCKET = os.getenv("TOS_BUCKET")
AUC_APP_ID = os.getenv("AUC_APP_ID")
AUC_ACCESS_TOKEN = os.getenv("AUC_ACCESS_TOKEN")
AUC_CLUSTER_ID = os.getenv("AUC_CLUSTER_ID", None)  # 选填, 填这个可以试用
WEB_ACCESS_PASSWORD = os.getenv("WEB_ACCESS_PASSWORD", None)  # 选填, 填这个可以开启 Web 端访问密码
