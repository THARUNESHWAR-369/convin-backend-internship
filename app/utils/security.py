from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from app.config.config import settings
import time
from typing import Any, Dict

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.

    Args:
        password (str): The plaintext password to be hashed.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)
    
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plaintext password against a hashed password.

    Args:
        plain_password (str): The plaintext password.
        hashed_password (str): The hashed password.

    Returns:
        bool: True if the password matches, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    Create a JWT access token.

    Args:
        data (dict): The data to encode in the token.
        expires_delta (timedelta, optional): The time delta after which the token expires. Defaults to 15 minutes.

    Returns:
        str: The encoded JWT token.
    """
    if expires_delta:
        expire: datetime = datetime.utcnow() + expires_delta
    else:
        expire: datetime = datetime.utcnow() + timedelta(minutes=15)
    data.update({"exp": expire})
    encoded_jwt: str = jwt.encode(data, settings.SECRET_KEY.value, algorithm=settings.ALGORITHM.value)
    return encoded_jwt

def decode_jwt(token: str) -> dict:
    """
    Decode a JWT token.

    Args:
        token (str): The JWT token to decode.

    Returns:
        dict: The decoded token data if the token is valid and not expired, otherwise an empty dictionary.
    """
    try:
        decoded_token: Dict[str, Any] = jwt.decode(token, settings.SECRET_KEY.value, algorithms=[settings.ALGORITHM.value])
        return decoded_token if decoded_token["exp"] >= time.time() else None
    except:
        return {}
