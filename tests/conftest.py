import os
import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(scope="session")
def client():
    # Set test environment variables
    os.environ.setdefault("ADMIN_TOKEN", "test-admin")
    os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")
    os.environ.setdefault("ZOHO_CLIENT_ID", "test")
    os.environ.setdefault("ZOHO_CLIENT_SECRET", "test")
    os.environ.setdefault("ENCRYPTION_KEY", "test_key_32_chars_long_exactly!!")
    os.environ.setdefault("APP_BASE_URL", "http://localhost:8000")

    return TestClient(app)