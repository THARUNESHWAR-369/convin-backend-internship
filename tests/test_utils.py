import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))


import pytest
from app.utils.security import hash_password, verify_password, create_access_token, decode_jwt
from datetime import timedelta
from app.config.config import settings

def test_hash_password():
    password = "test_user_pass"
    hashed = hash_password(password)
    assert hashed != password
    assert verify_password(password, hashed)

def test_verify_password():
    password = "test_user_pass"
    wrong_password = "wrong_user_password"
    hashed = hash_password(password)
    assert verify_password(password, hashed)
    assert not verify_password(wrong_password, hashed)

def test_create_access_token():
    data = {"sub": "test@example.com"}
    expires = timedelta(minutes=5)
    token = create_access_token(data, expires)
    assert token is not None

def test_decode_jwt():
    data = {"sub": "test@example.com"}
    expires = timedelta(minutes=5)
    token = create_access_token(data, expires)
    decoded = decode_jwt(token)
    assert decoded["sub"] == data["sub"]
