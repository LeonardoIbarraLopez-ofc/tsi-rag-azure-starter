from __future__ import annotations

from typing import Any

import httpx

from .config import Settings
from .models import Chunk, SearchHit


class AzureSearchClient:
    """Small REST client intentionally kept explicit for teaching Azure AI Search."""

    def __init__(self, settings: Settings):
        if not settings.has_azure_search:
            raise RuntimeError("Configure AZURE_SEARCH_ENDPOINT y AZURE_SEARCH_ADMIN_KEY")
        self.endpoint = settings.azure_search_endpoint.rstrip("/")
        self.key = settings.azure_search_admin_key
        self.index = settings.azure_search_index
        self.api_version = settings.azure_search_api_version

    @property
    def headers(self) -> dict[str, str]:
        return {"api-key": self.key, "Content-Type": "application/json"}

    def _url(self, path: str) -> str:
        return f"{self.endpoint}{path}?api-version={self.api_version}"

    def create_or_update_index(self, dimensions: int) -> dict[str, Any]:
        schema = {
            "name": self.index,
            "fields": [
                {"name": "id", "type": "Edm.String", "key": True, "filterable": True},
                {"name": "title", "type": "Edm.String", "searchable": True, "retrievable": True},
                {"name": "source", "type": "Edm.String", "searchable": True, "filterable": True, "retrievable": True},
                {"name": "chunk_id", "type": "Edm.Int32", "filterable": True, "sortable": True, "retrievable": True},
                {"name": "content", "type": "Edm.String", "searchable": True, "retrievable": True, "analyzer": "es.microsoft"},
                {
                    "name": "content_vector",
                    "type": "Collection(Edm.Single)",
                    "searchable": True,
                    "retrievable": False,
                    "dimensions": dimensions,
                    "vectorSearchProfile": "vector-profile",
                },
            ],
            "vectorSearch": {
                "algorithms": [
                    {
                        "name": "hnsw-config",
                        "kind": "hnsw",
                        "hnswParameters": {
                            "metric": "cosine",
                            "m": 4,
                            "efConstruction": 400,
                            "efSearch": 500,
                        },
                    }
                ],
                "profiles": [{"name": "vector-profile", "algorithm": "hnsw-config"}],
            },
        }
        response = httpx.put(
            self._url(f"/indexes('{self.index}')"),
            headers=self.headers,
            json=schema,
            timeout=60,
        )
        response.raise_for_status()
        return response.json()

    def upload_chunks(self, chunks: list[Chunk], batch_size: int = 100) -> int:
        uploaded = 0
        for start in range(0, len(chunks), batch_size):
            batch = chunks[start : start + batch_size]
            payload = {
                "value": [
                    {
                        "@search.action": "mergeOrUpload",
                        "id": c.id,
                        "title": c.title,
                        "source": c.source,
                        "chunk_id": c.chunk_id,
                        "content": c.content,
                        "content_vector": c.vector,
                    }
                    for c in batch
                ]
            }
            response = httpx.post(
                self._url(f"/indexes('{self.index}')/docs/search.index"),
                headers=self.headers,
                json=payload,
                timeout=60,
            )
            response.raise_for_status()
            uploaded += len(batch)
        return uploaded

    def search(
        self,
        query: str,
        query_vector: list[float],
        mode: str = "hybrid",
        top_k: int = 5,
    ) -> list[SearchHit]:
        body: dict[str, Any] = {
            "count": True,
            "select": "id,title,source,chunk_id,content",
            "top": top_k,
        }
        if mode in {"keyword", "hybrid"}:
            body["search"] = query
        if mode in {"vector", "hybrid"}:
            body["vectorQueries"] = [
                {
                    "kind": "vector",
                    "vector": query_vector,
                    "fields": "content_vector",
                    "k": top_k,
                    "exhaustive": True,
                }
            ]
        response = httpx.post(
            self._url(f"/indexes/{self.index}/docs/search"),
            headers=self.headers,
            json=body,
            timeout=60,
        )
        response.raise_for_status()
        items = response.json().get("value", [])
        return [
            SearchHit(
                id=item["id"],
                title=item.get("title", ""),
                source=item.get("source", ""),
                chunk_id=int(item.get("chunk_id", 0)),
                content=item.get("content", ""),
                score=float(item.get("@search.score", 0.0)),
                metadata={},
            )
            for item in items
        ]

    def list_indexes(self) -> list[str]:
        response = httpx.get(self._url("/indexes"), headers=self.headers, timeout=30)
        response.raise_for_status()
        return [item["name"] for item in response.json().get("value", [])]
