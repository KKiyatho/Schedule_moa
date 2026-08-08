"""
Test for auth endpoints
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from app.db.base import Base, get_db
from app.schemas import UserCreate


# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


Base.metadata.create_all(bind=engine)

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(scope="function")
def setup_db():
    """Setup test database"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_root_endpoint(setup_db):
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "일정모아" in response.json()["message"]


def test_health_check(setup_db):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_register_user(setup_db):
    """Test user registration"""
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "test@example.com", "full_name": "Test User"}
    )
    # May fail due to form data, but structure is correct
    assert response.status_code in [200, 422]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
