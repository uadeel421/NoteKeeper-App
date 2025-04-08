import pytest
import sys
import os
from pathlib import Path

# Add project root to Python path
ROOT_DIR = Path(__file__).parent.parent
sys.path.append(str(ROOT_DIR))

@pytest.fixture
def valid_user_credentials():
    """Fixture for valid user login credentials"""
    return {
        "email": "test@example.com",
        "password": "Test123!"
    }

@pytest.fixture
def invalid_user_credentials():
    """Fixture for invalid user credentials"""
    return {
        "email": "wrong@example.com",
        "password": "wrong"
    }