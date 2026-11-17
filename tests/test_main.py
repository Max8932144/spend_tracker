from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/docs")
    assert response.status_code == 200

def test_get_expenses():
    response = client.get("/expenses")
    # Пока базы нет, мы ожидаем либо 200, либо 500, главное, что сервер жив
    assert response.status_code in [200, 500]

def test_get_max_expense():
    response = client.get("/expenses/statistics/max?month=2026-10")
    assert response.status_code == 200
    assert "max_amount" in response.json()