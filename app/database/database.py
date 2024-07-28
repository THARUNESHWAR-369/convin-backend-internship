from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config.config import settings

engine : create_engine = create_engine(settings.SQLALCHEMY_DATABASE_URL.value, connect_args={"check_same_thread": False})
SessionLocal : sessionmaker = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
