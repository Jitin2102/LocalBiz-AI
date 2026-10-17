import json
import os
from pathlib import Path

os.environ["LOCALBIZ_DB"] = str(Path(__file__).parent / "test_localbiz.db")

from fastapi.testclient import TestClient
from app import main

client = TestClient(main.app)


def test_health_is_available():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_generate_falls_back_when_ollama_is_unavailable(monkeypatch):
    def fail(_data):
        raise OSError("Ollama not running")
    monkeypatch.setattr(main, "call_ollama", fail)
    response = client.post("/api/generate", json={
        "business_name": "Test Bakery",
        "product": "Chocolate cake",
        "price": "₹499",
        "audience": "families",
        "tone": "Friendly",
        "language": "Hinglish",
        "platform": "Instagram",
        "details": "Eggless, 500g"
    })
    assert response.status_code == 200
    body = response.json()
    assert body["mode"] == "offline-template"
    assert "Chocolate cake" in body["content"]["instagram_caption"]
    assert body["id"] > 0


def test_history_contains_saved_generation():
    response = client.get("/api/history")
    assert response.status_code == 200
    assert isinstance(response.json()["items"], list)
    assert any(item["product"] == "Chocolate cake" for item in response.json()["items"])


def test_generate_validates_product():
    response = client.post("/api/generate", json={"product": "x"})
    assert response.status_code == 422


def test_delete_history_item():
    response = client.post("/api/generate", json={"product": "Test item"})
    generation_id = response.json()["id"]
    deleted = client.delete(f"/api/history/{generation_id}")
    assert deleted.status_code == 200
    assert deleted.json()["deleted"] is True
