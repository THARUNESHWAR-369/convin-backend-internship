from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.utils.curd import get_user_by_email, create_user as cu, get_user
from app.database.schemas.user_schema import User, UserCreate
from app.utils.dependencies import get_db, JWTBearer, get_current_user
from typing import List
from app.utils.status import status_codes as sac
from app.models.models import User as model_user

router: APIRouter = APIRouter()

@router.post("/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)) -> User:
    """
    Create a new user.

    This function registers a new user if the email is not already registered.

    Args:
        user (UserCreate): The user details to be created.
        db (Session): Database session dependency.

    Returns:
        User: The created user object.

    Raises:
        HTTPException: If the email is already registered.
    """
    db_user: User | None = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=sac.HTTP_BAD_REQUEST, detail="Email already registered")
    return cu(db=db, user=user)

@router.get("/current_user", response_model=User, dependencies=[Depends(JWTBearer())])
def current_users(current_user: User = Depends(get_current_user)) -> User:
    """
    Retrieve the current authenticated user.

    This function returns the details of the current authenticated user.

    Args:
        current_user (User): The current authenticated user.

    Returns:
        User: The current user object.
    """
    return current_user

@router.get("/all", response_model=List[User], dependencies=[Depends(JWTBearer())])
def all_users(db: Session = Depends(get_db)) -> List[User]:
    """
    Retrieve all users.

    This function returns a list of all users in the database.

    Args:
        db (Session): Database session dependency.

    Returns:
        List[User]: A list of all user objects.
    """
    return db.query(model_user).all()

@router.get("/{user_id}", response_model=User, dependencies=[Depends(JWTBearer())])
def read_user(user_id: int, db: Session = Depends(get_db)) -> User:
    """
    Retrieve a user by ID.

    This function returns the details of a user specified by the user ID.

    Args:
        user_id (int): The ID of the user to retrieve.
        db (Session): Database session dependency.

    Returns:
        User: The user object corresponding to the given ID.

    Raises:
        HTTPException: If the user is not found.
    """
    db_user: User | None = get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=sac.HTTP_NOT_FOUND, detail="User not found")
    return db_user
