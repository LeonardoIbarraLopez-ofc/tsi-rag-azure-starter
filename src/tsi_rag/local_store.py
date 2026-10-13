from __future__ import annotations

import math
import re
from collections import Counter

from .chunking import load_corpus
from .config import Settings
from .embeddings import Embedder
from .models import Chunk, SearchHit


WORD_RE = re.compile(r"[a-zA-ZáéíóúüñÁÉÍÓÚÜÑ0-9]+", re.UNICODE)
STOPWORDS = {
    "a", "al", "algo", "como", "con", "cual", "cuando", "de", "del", "el", "en", "es",
    "esta", "este", "la", "las", "lo", "los", "para", "por", "que", "se", "sin", "su",
    "sus", "un", "una", "unos", "unas", "y", "o", "qué", "cómo", "cuál", "cuándo",
}


def _tokens(text: str) -> list[str]:
    return [x.lower() for x in WORD_RE.findall(text) if x.lower() not in STOPWORDS]


def _cosine(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b, strict=True))


class LocalRetriever:
    def __init__(self, settings: Settings, embedder: Embedder):
        self.settings = settings
        self.embedder = embedder
        self.chunks: list[Chunk] = load_corpus(
            settings.corpus_dir, settings.chunk_size, settings.chunk_overlap
        )
        vectors = embedder.embed_many([c.content for c in self.chunks])
        for chunk, vector in zip(self.chunks, vectors, strict=True):
            chunk.vector = vector
        self.doc_freq: Counter[str] = Counter()
        for chunk in self.chunks:
            self.doc_freq.update(set(_tokens(chunk.content)))

    def _keyword_score(self, query: str, content: str) -> tuple[float, int]:
        q_tokens = _tokens(query)
        c_counts = Counter(_tokens(content))
        if not q_tokens:
            return 0.0, 0
        n_docs = max(1, len(self.chunks))
        raw = 0.0
        overlap = 0
        for token in set(q_tokens):
            if c_counts[token] <= 0:
                continue
            overlap += 1
            idf = math.log((n_docs + 1) / (1 + self.doc_freq[token])) + 1.0
            raw += (1.0 + math.log(c_counts[token])) * idf
        score = raw / max(1.0, len(set(q_tokens)) * 3.0)
        return min(score, 1.0), overlap

    def search(self, query: str, mode: str = "hybrid", top_k: int = 5) -> list[SearchHit]:
        q_vec = self.embedder.embed(query)
        hits: list[SearchHit] = []
        for chunk in self.chunks:
            keyword, overlap = self._keyword_score(query, chunk.content)
            vector = max(0.0, _cosine(q_vec, chunk.vector))
            if mode == "keyword":
                score = keyword
            elif mode == "vector":
                score = vector
            elif mode == "hybrid":
                score = 0.55 * vector + 0.45 * keyword
            else:
                raise ValueError(f"Modo no soportado: {mode}")
            hits.append(
                SearchHit(
                    id=chunk.id,
                    title=chunk.title,
                    source=chunk.source,
                    chunk_id=chunk.chunk_id,
                    content=chunk.content,
                    score=float(score),
                    metadata={
                        "keyword_score": keyword,
                        "vector_score": vector,
                        "lexical_overlap": overlap,
                    },
                )
            )
        return sorted(hits, key=lambda x: x.score, reverse=True)[:top_k]
