from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime


class IngestRequest(BaseModel):
    type: str  # "note" or "url"
    content: str
    title: Optional[str] = None

    @field_validator("type")
    @classmethod
    def validate_type(cls, v: str) -> str:
        if v not in ("note", "url"):
            raise ValueError("type must be 'note' or 'url'")
        return v

    @field_validator("content")
    @classmethod
    def validate_content(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("content cannot be empty")
        return v.strip()


class IngestResponse(BaseModel):
    id: str
    title: str
    chunk_count: int
    type: str


class ItemSummary(BaseModel):
    id: str
    title: str
    type: str
    preview: str
    created_at: str
    chunk_count: int


class ItemsResponse(BaseModel):
    items: list[ItemSummary]


class QueryRequest(BaseModel):
    question: str

    @field_validator("question")
    @classmethod
    def validate_question(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("question cannot be empty")
        return v.strip()


class SourceInfo(BaseModel):
    item_id: str
    title: str
    snippet: str
    relevance_score: float


class QueryResponse(BaseModel):
    answer: str
    sources: list[SourceInfo]
