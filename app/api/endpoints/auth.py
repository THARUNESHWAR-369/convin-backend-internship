from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta
from app.database.schemas.token_schema import Token
from app.database.schemas.auth_schema import AuthUser
from app.database.schemas.user_schema import User
from app.utils import security
from app.utils.curd import get_user_by_email
from app.utils.dependencies import get_db
from app.config.config import settings
from typing import Dict
import os
from app.utils.status import status_codes as sac

router: APIRouter = APIRouter()


@router.post("/token", response_model=Token)
def login(
    db: Session = Depends(get_db), form_data: AuthUser = Depends()
) -> Dict[str, str]:
    """
    Authenticate the user and return an access token.

    This function is called when the user tries to log in. It verifies the
    user's credentials and returns a JWT access token if the credentials are valid.

    Args:
        db (Session): Database session dependency.
        form_data (AuthUser): Dependency that extracts the user's login credentials from the request.

    Returns:
        Dict[str, str]: A dictionary containing the access token and token type.

    Raises:
        HTTPException: If the email or password is incorrect, raises a 401 Unauthorized error.
    """
    user: User | None = get_user_by_email(db, email=form_data.email)
    if not user or not security.verify_password(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(status_code=sac.HTTP_UNAUTHORIZED, detail="Incorrect email or password")
    access_token_expires: timedelta = timedelta(
        minutes=float(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"))
    )
    access_token: str = security.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
