# app/models/schemas.py
from pydantic import BaseModel
from typing import Optional

class QueryRequest(BaseModel):
    prompt: Optional[str] = None

class TextResponse(BaseModel):
    response: str
    detected_language: str

class AudioResponse(BaseModel):
    audio_content: bytes
    detected_language: str
    question: Optional[str] = None
    llm_response: Optional[str] = None