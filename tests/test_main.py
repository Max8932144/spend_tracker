from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_docs():
    # Проверяем, что сервер вообще запускается и отдает документацию
    response = client.get("/docs")
    assert response.status_code == 200

def test_max_expense():
    # Проверяем эндпоинт, который не требует БД
    response = client.get("/expenses/statistics/max?month=2026-10")
    assert response.status_code == 200
    assert response.json()["max_amount"] == 1000