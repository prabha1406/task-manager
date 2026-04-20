from fastapi.testclient import TestClient
from backend.main import app   # 🔥 IMPORTANT FIX

client = TestClient(app)

def test_register():
    response = client.post("/register", json={
        "username": "testuser123",
        "password": "1234"
    })
    assert response.status_code == 200