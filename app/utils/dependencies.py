from app.database.database import SessionLocal
from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.utils.security import decode_jwt
from app.database.schemas.user_schema import User
from sqlalchemy.orm import Session
from app.models import models
from typing import Any
from app.utils.status import status_codes as sac

def get_db() -> Any:
    """
    Provide a database session to the request context.

    Yields:
        Any: The database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class JWTBearer(HTTPBearer):
    """
    JWT Bearer authentication class that inherits from FastAPI's HTTPBearer.
    """

    def __init__(self, auto_error: bool = True) -> None:
        """
        Initialize the JWTBearer instance.

        Args:
            auto_error (bool): Whether to automatically raise an HTTPException if an error occurs.
        """
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> dict:
        """
        Handle the request and extract the JWT token.

        Args:
            request (Request): The incoming request.

        Returns:
            dict: The decoded JWT token payload.

        Raises:
            HTTPException: If the authentication scheme is invalid or the token is invalid/expired.
        """
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=sac.HTTP_FORBIDDEN, detail="Invalid authentication scheme.")
            token: (dict | None) = self.verify_jwt(credentials.credentials)
            if not token:
                raise HTTPException(status_code=sac.HTTP_FORBIDDEN, detail="Invalid token or expired token.")
            return token
        else:
            raise HTTPException(status_code=sac.HTTP_FORBIDDEN, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> (dict | None):
        """
        Verify the JWT token.

        Args:
            jwtoken (str): The JWT token to verify.

        Returns:
            dict | None: The decoded token payload if the token is valid, otherwise None.
        """
        try:
            payload: dict = decode_jwt(jwtoken)
            return payload if payload else None
        except:
            return None

def get_current_user(token: dict = Depends(JWTBearer()), db: Session = Depends(get_db)) -> User:
    """
    Get the current user from the JWT token.

    Args:
        token (dict): The decoded JWT token payload.
        db (Session): The database session.

    Returns:
        User: The current user.

    Raises:
        HTTPException: If the token does not contain an email or the user is not found.
    """
    email: (Any | None) = token.get("sub")
    if email is None:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    user: (User | None) = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user
