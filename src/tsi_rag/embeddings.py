from __future__ import annotations

import hashlib
import math
import re
from abc import ABC, abstractmethod

import httpx

from .config import Settings


TOKEN_RE = re.compile(r"[a-zA-ZáéíóúüñÁÉÍÓÚÜÑ0-9]+", re.UNICODE)


class Embedder(ABC):
    @property
    @abstractmethod
    def dimensions(self) -> int: ...

    @abstractmethod
    def embed(self, text: str) -> list[float]: ...

    def embed_many(self, texts: list[str]) -> list[list[float]]:
        return [self.embed(text) for text in texts]


class HashEmbedder(Embedder):
    """Deterministic zero-download embedding.

    It is intentionally simple and useful as a didactic fallback. It is not a replacement
    for a production semantic embedding model.
    """

    def __init__(self, dimensions: int = 128):
        self._dimensions = dimensions

    @property
    def dimensions(self) -> int:
        return self._dimensions

    def embed(self, text: str) -> list[float]:
        vector = [0.0] * self._dimensions
        tokens = [token.lower() for token in TOKEN_RE.findall(text)]
        for token in tokens:
            digest = hashlib.sha256(token.encode("utf-8")).digest()
            idx = int.from_bytes(digest[:4], "big") % self._dimensions
            sign = 1.0 if digest[4] % 2 == 0 else -1.0
            vector[idx] += sign
        norm = math.sqrt(sum(x * x for x in vector)) or 1.0
        return [x / norm for x in vector]


class SentenceTransformerEmbedder(Embedder):
    def __init__(self, model_name: str):
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as exc:
            raise RuntimeError(
                "Instale el extra semantico: uv sync --extra semantic"
            ) from exc
        self.model = SentenceTransformer(model_name)
        sample = self.model.encode(["dimension"], normalize_embeddings=True)[0]
        self._dimensions = int(len(sample))

    @property
    def dimensions(self) -> int:
        return self._dimensions

    def embed(self, text: str) -> list[float]:
        arr = self.model.encode([text], normalize_embeddings=True)[0]
        return [float(x) for x in arr]

    def embed_many(self, texts: list[str]) -> list[list[float]]:
        arr = self.model.encode(texts, normalize_embeddings=True)
        return [[float(x) for x in row] for row in arr]


class AzureOpenAIEmbedder(Embedder):
    def __init__(self, settings: Settings):
        if not settings.has_azure_openai or not settings.azure_openai_embedding_deployment:
            raise RuntimeError("Falta configurar Azure OpenAI para embeddings")
        self.endpoint = settings.azure_openai_endpoint.rstrip("/")
        self.key = settings.azure_openai_api_key
        self.version = settings.azure_openai_api_version
        self.deployment = settings.azure_openai_embedding_deployment
        self._dimensions = settings.azure_openai_embedding_dimensions

    @property
    def dimensions(self) -> int:
        return self._dimensions

    def embed_many(self, texts: list[str]) -> list[list[float]]:
        url = (
            f"{self.endpoint}/openai/deployments/{self.deployment}/embeddings"
            f"?api-version={self.version}"
        )
        response = httpx.post(
            url,
            headers={"api-key": self.key, "Content-Type": "application/json"},
            json={"input": texts},
            timeout=60,
        )
        response.raise_for_status()
        data = response.json()["data"]
        return [[float(x) for x in item["embedding"]] for item in data]

    def embed(self, text: str) -> list[float]:
        return self.embed_many([text])[0]


def get_embedder(settings: Settings) -> Embedder:
    provider = settings.embedding_provider.lower().strip()
    if provider == "hash":
        return HashEmbedder()
    if provider == "sentence_transformers":
        return SentenceTransformerEmbedder(settings.sentence_transformer_model)
    if provider == "azure_openai":
        return AzureOpenAIEmbedder(settings)
    raise ValueError(f"EMBEDDING_PROVIDER no soportado: {provider}")
