# src/models/chunk_metadata.py
from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime

class ChunkMetadata(BaseModel):
    article_id: int
    chunk_id: int
    title: Optional[str] = None
    source: Optional[str] = None
    url: Optional[HttpUrl] = None
    created_at: Optional[datetime] = None
    text: str

