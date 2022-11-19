from fastapi.testclient import TestClient
from app import main
from tests.test_base import fake_db

dummy_user = {
    "username": "codestronomer",
    "first_name": "John",
    "last_name": "Rumide",
    "email": "johnrumide6@gmail.com",
    "password": "password123",
    "account_balance": 10,
    "role": "developer",
    "image_url": "image url"
}

client = TestClient(main.app)


def test_read_users():
    """Tests for getting users by client"""
    response = client.get("/users")
    assert response.status_code == 200
    # assert response.json() == {"success": True, "data": fake_db}


def test_write_user():
    """Test if create user by client is successful"""
    response = client.post("/users", json={dummy_user})
    assert response.status_code == 200
    assert isinstance(response.json(), dict) == True


def test_nonexistent_user():
    """Test if client is trying to get an inexistent user"""
    response = client.get("/users/2000", headers={"X-Token": "asilentplace"})
    assert response.status_code == 404
    assert response.json() == {
        "detail": "user with user_id : 2000 not found"
    }


# def test_create_user_with_bad_token():
#     """Tests if client is creating a user with bad token"""
#     response = client.get("/users", headers={"X-Token": "corusant"})
#     assert response.status_code == 400
#     assert response.json() == {"detail": "Invalid X-Token header"}


def test_creating_existing_user():
    """Tests if client is creating an existing user"""
    response = client.get("/users", json={dummy_user})
    assert response.status_code == 400
    assert response.json() == {"detail": "User already exists"}


def test_update_existing_user():
    """Tests for updating a user"""
    dummy_user["username"] == "Skywalker10"
    dummy_user["first_name"] == "Luke"
    dummy_user["last_name"] == "Skywalker"
    response = client.patch("/users/2", "/users", json=dummy_user)
    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "message": "Profile Updated",
        "data": dummy_user
    }


def test_update_nonexistent_user():
    """Tests if the client is trying to update an invalid user"""
    dummy_user["username"] == "Skywalker20"
    dummy_user["first_name"] == "Anakin"
    dummy_user["last_name"] == "Skywalker"
    response = client.patch('/users/2000',
                            json=dummy_user)
    assert response.status_code == 404
    assert response.json() == {"detail": "Not found"}


def test_update_user_with_bad_token():
    """Tests if the client uses a invalid token while updating"""
    dummy_user["username"] == "Skywalker10"
    dummy_user["first_name"] == "Luke"
    dummy_user["last_name"] == "Skywalker"
    response = client.post("/users/2", json=dummy_user)
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}
