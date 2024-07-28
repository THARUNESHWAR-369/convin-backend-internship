from fastapi import APIRouter
from app.api.endpoints import user, expense, auth

api_router : APIRouter = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(user.router, prefix="/users", tags=["Users"])
api_router.include_router(expense.router, prefix="/expenses", tags=["Expenses"])
