"""
General testing module for app
"""
import unittest
from app import main
from fastapi.testclient import TestClient
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

client = TestClient(main.app)

fake_db = {
    "1": {
        "user_id": 1, "username": "codestronomer",
        "first_name": "John", "last_name": "Rumide",
        "email": "johnrumide6@gmail.com", "password": "testpassword",
        "account_balance": 10, "role": "user",
        "image_url": "https://github.com/codestronomer"},
    "2": {
        "user_id": 2, "username": "codestronomer",
        "first_name": "John", "last_name": "Rumide",
        "email": "johnrumide6@gmail.com", "password": "testpassword",
        "account_balance": 10, "role": "user",
        "image_url": "https://github.com/codestronomer"
    },
    "3": {
        "user_id": 1, "username": "codestronomer",
        "first_name": "John", "last_name": "Rumide",
        "email": "johnrumide6@gmail.com", "password": "testpassword",
        "account_balance": 10, "role": "user",
        "image_url": "https://github.com/codestronomer"
    }
}


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    print(response.json())
    assert response.json() == {"msg": ""}


def test_bad_token():
    response = client.get("/", headers={"X-Token": "therepublic"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}
