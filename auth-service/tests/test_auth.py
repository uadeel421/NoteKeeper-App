import pytest
from fastapi.testclient import TestClient
from auth-service.app import app  # Change the import path

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_login_validation():
    response = client.post(
        "/api/login",
        json={"email": "", "password": ""}
    )
    assert response.status_code == 422  # Validation error
