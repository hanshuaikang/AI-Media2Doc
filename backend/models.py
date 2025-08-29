from pydantic import BaseModel
from typing import List, Optional


class MessageModel(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[MessageModel]
    model: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None


class FileNameRequest(BaseModel):
    filename: str
