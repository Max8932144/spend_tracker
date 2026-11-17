from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch, AsyncMock

client = TestClient(app)

@patch("app.main.expenses_collection.insert_one")
def test_create_expense(mock_insert):
    mock_insert.return_value.inserted_id = "123"
    response = client.post("/expenses", json={
        "category": "Еда",
        "amount": 500,
        "date": "2026-10-27"
    })
    assert response.status_code == 201
    assert response.json()["id"] == "123"

@patch("app.main.expenses_collection.find")
def test_get_expenses(mock_find):
    mock_cursor = AsyncMock()
    mock_cursor.__aiter__.return_value = [{"_id": "123", "category": "Еда", "amount": 500, "date": "2026-10-27"}]
    mock_find.return_value = mock_cursor
    response = client.get("/expenses")
    assert response.status_code == 200
    assert len(response.json()) == 1