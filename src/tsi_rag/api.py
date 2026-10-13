from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse

from .config import Settings
from .models import AskRequest, AskResponse, SearchRequest
from .service import RAGService


@lru_cache(maxsize=1)
def get_service() -> RAGService:
    return RAGService(Settings())


app = FastAPI(title="TSI RAG Azure MVP", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    settings = Settings()
    return {
        "status": "ok",
        "retriever_backend": settings.retriever_backend,
        "embedding_provider": settings.embedding_provider,
        "generator_provider": settings.generator_provider,
    }


@app.post("/search")
def search(request: SearchRequest) -> dict:
    hits = get_service().search(request.query, request.mode, request.top_k)
    return {
        "query": request.query,
        "mode": request.mode,
        "hits": [
            {
                "source": h.source,
                "title": h.title,
                "chunk_id": h.chunk_id,
                "score": round(h.score, 5),
                "content": h.content,
            }
            for h in hits
        ],
    }


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest) -> AskResponse:
    return get_service().ask(request.query, request.mode, request.top_k)


@app.get("/")
def ui() -> FileResponse:
    return FileResponse(Path("web/index.html"))
