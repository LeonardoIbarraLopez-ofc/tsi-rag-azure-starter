from __future__ import annotations

import json
import time
from pathlib import Path

from .config import Settings
from .embeddings import get_embedder
from .generation import get_generator
from .models import AskResponse, SearchHit, SourceItem
from .retrieval import Retriever


class RAGService:
    def __init__(self, settings: Settings | None = None):
        self.settings = settings or Settings()
        self.embedder = get_embedder(self.settings)
        self.retriever = Retriever(self.settings, self.embedder)
        self.generator = get_generator(self.settings)

    def search(self, query: str, mode: str = "hybrid", top_k: int | None = None) -> list[SearchHit]:
        return self.retriever.search(query, mode, top_k or self.settings.top_k)

    def _has_evidence(self, hits: list[SearchHit]) -> bool:
        if not hits:
            return False
        if self.settings.retriever_backend == "local":
            # In hash mode a non-overlapping query can show small random cosine collisions.
            if self.settings.embedding_provider == "hash" and all(
                int(h.metadata.get("lexical_overlap", 0)) == 0 for h in hits
            ):
                return False
            return hits[0].score >= self.settings.min_relevance
        # Azure Search scores are not normalized to 0..1; existence of retrieved evidence
        # is used as the first gate and the generator must still refuse unsupported answers.
        return True

    def ask(self, query: str, mode: str = "hybrid", top_k: int | None = None) -> AskResponse:
        total_start = time.perf_counter()
        retrieval_start = time.perf_counter()
        hits = self.search(query, mode, top_k)
        retrieval_ms = (time.perf_counter() - retrieval_start) * 1000

        generation_start = time.perf_counter()
        if not self._has_evidence(hits):
            answer = "No encuentro esa informacion en las fuentes disponibles."
            flags: list[str] = []
            used_hits: list[SearchHit] = []
        else:
            answer, flags = self.generator.generate(query, hits)
            used_hits = hits
        generation_ms = (time.perf_counter() - generation_start) * 1000
        total_ms = (time.perf_counter() - total_start) * 1000

        response = AskResponse(
            answer=answer,
            sources=[
                SourceItem(
                    source=h.source,
                    title=h.title,
                    chunk_id=h.chunk_id,
                    score=round(h.score, 5),
                )
                for h in used_hits
            ],
            mode=mode,
            retrieval_ms=round(retrieval_ms, 2),
            generation_ms=round(generation_ms, 2),
            total_ms=round(total_ms, 2),
            security_flags=flags,
            generator=self.generator.name,
        )
        self._log(query, response)
        return response

    def _log(self, query: str, response: AskResponse) -> None:
        path: Path = self.settings.query_log_path
        path.parent.mkdir(parents=True, exist_ok=True)
        record = {
            "ts_unix": time.time(),
            "query": query,
            "mode": response.mode,
            "sources": [s.model_dump() for s in response.sources],
            "retrieval_ms": response.retrieval_ms,
            "generation_ms": response.generation_ms,
            "total_ms": response.total_ms,
            "security_flags": response.security_flags,
            "generator": response.generator,
        }
        with path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")
