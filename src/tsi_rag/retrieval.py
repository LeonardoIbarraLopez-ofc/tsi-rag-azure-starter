from __future__ import annotations

from .azure_search import AzureSearchClient
from .config import Settings
from .embeddings import Embedder
from .local_store import LocalRetriever
from .models import SearchHit


class Retriever:
    def __init__(self, settings: Settings, embedder: Embedder):
        self.settings = settings
        self.embedder = embedder
        backend = settings.retriever_backend.lower().strip()
        self.backend = backend
        if backend == "local":
            self.local = LocalRetriever(settings, embedder)
            self.azure = None
        elif backend == "azure":
            self.azure = AzureSearchClient(settings)
            self.local = None
        else:
            raise ValueError(f"RETRIEVER_BACKEND no soportado: {backend}")

    def search(self, query: str, mode: str, top_k: int) -> list[SearchHit]:
        if self.backend == "local":
            return self.local.search(query, mode, top_k)
        vector = self.embedder.embed(query)
        return self.azure.search(query, vector, mode, top_k)
