import pytest
from fastapi.testclient import TestClient
import sys
import os
from pathlib import Path

# Add the project root to Python path
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.append(str(ROOT_DIR))

from auth-service.app import app

client = TestClient(app)

def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_login_with_valid_credentials(valid_user_credentials):
    """Test login with valid credentials"""
    response = client.post("/api/login", json=valid_user_credentials)
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_with_invalid_credentials(invalid_user_credentials):
    """Test login with invalid credentials"""
    response = client.post("/api/login", json=invalid_user_credentials)
    assert response.status_code == 401

def test_login_with_empty_credentials():
    """Test login with empty credentials"""
    response = client.post("/api/login", json={"email": "", "password": ""})
    assert response.status_code == 422

def test_login_with_invalid_email_format():
    """Test login with invalid email format"""
    response = client.post(
        "/api/login", 
        json={"email": "invalid-email", "password": "password123"}
    )
    assert response.status_code == 422