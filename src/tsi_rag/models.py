from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

from pydantic import BaseModel, Field


@dataclass(slots=True)
class Chunk:
    id: str
    title: str
    source: str
    chunk_id: int
    content: str
    vector: list[float] = field(default_factory=list)


@dataclass(slots=True)
class SearchHit:
    id: str
    title: str
    source: str
    chunk_id: int
    content: str
    score: float
    metadata: dict[str, Any] = field(default_factory=dict)


class SearchRequest(BaseModel):
    query: str = Field(min_length=2, max_length=1000)
    mode: Literal["keyword", "vector", "hybrid"] = "hybrid"
    top_k: int = Field(default=5, ge=1, le=20)


class AskRequest(BaseModel):
    query: str = Field(min_length=2, max_length=1000)
    mode: Literal["keyword", "vector", "hybrid"] = "hybrid"
    top_k: int = Field(default=5, ge=1, le=20)


class SourceItem(BaseModel):
    source: str
    title: str
    chunk_id: int
    score: float


class AskResponse(BaseModel):
    answer: str
    sources: list[SourceItem]
    mode: str
    retrieval_ms: float
    generation_ms: float
    total_ms: float
    security_flags: list[str] = []
    generator: str
