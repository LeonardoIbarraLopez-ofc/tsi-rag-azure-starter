from __future__ import annotations

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "TSI - RAG minimo viable"
    retriever_backend: str = "local"
    embedding_provider: str = "hash"
    generator_provider: str = "extractive"

    top_k: int = Field(default=5, ge=1, le=20)
    min_relevance: float = Field(default=0.12, ge=0.0, le=1.0)
    chunk_size: int = Field(default=900, ge=200, le=4000)
    chunk_overlap: int = Field(default=120, ge=0, le=1000)
    corpus_dir: Path = Path("data/docs")
    query_log_path: Path = Path("logs/queries.jsonl")

    azure_search_endpoint: str | None = None
    azure_search_admin_key: str | None = None
    azure_search_index: str = "tsi-rag-lab"
    azure_search_api_version: str = "2025-09-01"

    sentence_transformer_model: str = (
        "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )

    azure_openai_endpoint: str | None = None
    azure_openai_api_key: str | None = None
    azure_openai_api_version: str = "2024-10-21"
    azure_openai_embedding_deployment: str | None = None
    azure_openai_embedding_dimensions: int = 1536
    azure_openai_chat_deployment: str | None = None

    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.2:3b"

    @property
    def has_azure_search(self) -> bool:
        return bool(self.azure_search_endpoint and self.azure_search_admin_key)

    @property
    def has_azure_openai(self) -> bool:
        return bool(self.azure_openai_endpoint and self.azure_openai_api_key)
