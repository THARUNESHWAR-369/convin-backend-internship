import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database.database import Base
from app.models import models
from app.utils.security import hash_password
from app.config.config import settings
from app.utils.dependencies import get_db
from dotenv import load_dotenv

load_dotenv()

# Set the correct path for the app

# Create the test database engine
engine = create_engine(
    os.environ.get('SQLALCHEMY_DATABASE_URL'), connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Fixture for the database
@pytest.fixture(scope="module")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


# Fixture for the test client
@pytest.fixture(scope="module")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client


# Fixture for a test user
@pytest.fixture(scope="module")
def test_user(db):
    user = models.User(
        email="test@example.com",
        name="Test User",
        mobile="1234567890",
        hashed_password=hash_password("testpassword"),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# Test for creating a user
def test_create_user(client):
    response = client.post(
        "/api/v1/users/",
        json={
            "email": "newuser@example.com",
            "name": "New User",
            "mobile": "0987654321",
            "password": "newpassword",
        },
    )
    assert response.status_code == 200
    assert response.json()["email"] == "newuser@example.com"


# Test for duplicate email during user creation
def test_create_user_duplicate_email(client, test_user):
    response = client.post(
        "/api/v1/users/",
        json={
            "email": "test@example.com",
            "name": "Duplicate User",
            "mobile": "0987654321",
            "password": "newpassword",
        },
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Email already registered"}


# Test for user login
def test_login(client, test_user):
    response = client.post(
        "/api/v1/auth/token", params={"email": "test@example.com", "password": "testpassword"},
                headers={"Content-Type": "application/json"} 
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


# Test for getting the current user
def test_get_current_user(client, test_user):
    login_response = client.post(
        "/api/v1/auth/token", params={"email": "test@example.com", "password": "testpassword"}
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/v1/users/current_user", headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"


# Test for creating an expense
def test_create_expense(client, test_user):
    login_response = client.post(
        "/api/v1/auth/token", params={"email": "test@example.com", "password": "testpassword"}
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    expense_data = {
        "amount": 100.0,
        "description": "Test Expense",
        "split_method": "equal",
        "splits": [{"user_id": test_user.id}],
    }
    response = client.post("/api/v1/expenses/create_expense", headers=headers, json=expense_data)
    assert response.status_code == 200
    assert response.json()["description"] == "Test Expense"


# Test for getting current user's expenses
def test_get_current_user_expenses(client, test_user):
    login_response = client.post(
        "/api/v1/auth/token", params={"email": "test@example.com", "password": "testpassword"}
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/v1/expenses/current_user_expenses/", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) >= 1
