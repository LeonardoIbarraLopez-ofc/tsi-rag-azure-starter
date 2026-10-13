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


def test_answer_includes_sources_when_evidence_exists():
    response = _service().ask("¿Como se gestionan los secretos?", "hybrid", 5)
    assert response.sources
    assert "Fuentes:" in response.answer


def test_unknown_question_returns_no_evidence_message():
    response = _service().ask("¿Cual es el precio de una licencia de Photoshop?", "hybrid", 5)
    assert response.answer.startswith("No encuentro esa informacion")
    assert response.sources == []
