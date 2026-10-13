from fastapi.testclient import TestClient

from tsi_rag.api import app, get_service


client = TestClient(app)


def setup_function():
    get_service.cache_clear()


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_search_endpoint():
    response = client.post(
        "/search",
        json={"query": "busqueda hibrida", "mode": "hybrid", "top_k": 3},
    )
    assert response.status_code == 200
    assert len(response.json()["hits"]) == 3


def test_ask_endpoint():
    response = client.post(
        "/ask",
        json={"query": "¿Como se protegen los secretos?", "mode": "hybrid", "top_k": 5},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["answer"]
    assert body["sources"]
