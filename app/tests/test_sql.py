from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..database import Base
from ..main import app
from ..database import get_db

SQLALCHEMY_DATABASE_URL = "f'postgresql://{settings.test_database_username}:{settings.test_database_password}@{settings.test_database_hostname}:{settings.test_database_port}/{settings.test_database_name}'"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

dummy_user = {
    "username": "codestronomer",
    "first_name": "Dead",
    "last_name": "Pool",
    "email": "deadpool@example.com",
    "password": "password123",
    "account_balance": 10,
    "role": "developer",
    "image_url": "image url"
}


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_user():
    response = client.post(
        "/users/",
        json=dummy_user
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "deadpool@example.com"
    assert "id" in data
    user_id = data["id"]

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "deadpool@example.com"
    assert data["id"] == user_id
