# -*- coding: UTF-8 -*-

from pydantic import BaseModel
from typing import List, Optional, Any


class MessageModel(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[MessageModel]
    model: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int]
    timeout: Optional[int]


class FileNameRequest(BaseModel):
    filename: str


class EnvResponse(BaseModel):
    code: int = 200
    success: bool = True
    message: str = "operation successful"
    data: Optional[Any] = None
