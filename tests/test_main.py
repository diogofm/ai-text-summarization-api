import sys
import os

from fastapi.testclient import TestClient
from starlette.status import HTTP_403_FORBIDDEN, HTTP_200_OK

from app.main import app

from decouple import config

API_KEY = config("API_KEY")
API_KEY_NAME = config("API_KEY_NAME")

client = TestClient(app)


def test_read_main():
    response = client.get("/", headers={API_KEY_NAME: API_KEY})
    assert response.status_code == HTTP_200_OK
    assert response.json() == {"message": "Welcome to the AI Text Summarization!"}


def test_read_main_no_auth():
    response = client.get("/")
    assert response.status_code == HTTP_403_FORBIDDEN
