from tsi_rag.config import Settings
from tsi_rag.service import RAGService


def _service() -> RAGService:
    return RAGService(
        Settings(
            retriever_backend="local",
            embedding_provider="hash",
            generator_provider="extractive",
            corpus_dir="data/docs",
        )
    )


def test_secret_query_retrieves_expected_document():
    hits = _service().search("como proteger secretos y claves de API", "hybrid", 5)
    assert "08_gestion_secretos.md" in [h.source for h in hits]


def test_hybrid_search_returns_ranked_hits():
    hits = _service().search("busqueda hibrida vectorial y textual", "hybrid", 5)
    assert len(hits) == 5
    assert hits[0].score >= hits[-1].score
