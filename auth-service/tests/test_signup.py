# auth-service/tests/test_signup.py

from fastapi.testclient import TestClient
from app import app  # adjust if your app is under another module

client = TestClient(app)

def test_signup_new_user():
    response = client.post("/api/signup", json={
        "email": "testuser@example.com",
        "password": "password123"
    })
    assert response.status_code == 200 or response.status_code == 201

def test_signup_existing_user():
    # Sign up once
    client.post("/api/signup", json={
        "email": "testuser@example.com",
        "password": "password123"
    })

    # Try to sign up again
    response = client.post("/api/signup", json={
        "email": "testuser@example.com",
        "password": "password123"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"
