# -*- coding: UTF-8 -*-

import enum


class VolcengineASRResponseStatusCode(enum.Enum):
    """火山语音新版接口状态码（响应头 X-Api-Status-Code）"""

    SUCCESS = "20000000"
    RUNNING = "20000001"
    PENDING = "20000002"


class AsrTaskStatus(enum.Enum):
    RUNNING = "running"
    FINISHED = "finished"
    FAILED = "failed"
