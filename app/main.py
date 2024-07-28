
from fastapi import FastAPI
from app.api.apiv1 import api_router
from app.database.database import engine, Base
from dotenv import load_dotenv

load_dotenv()

Base.metadata.create_all(bind=engine)

app  : FastAPI = FastAPI(title="Convin Backend Intern Project (Daily Expense Sharing App)")

app.include_router(api_router, prefix="/api/v1")
