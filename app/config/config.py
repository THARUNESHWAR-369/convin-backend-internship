from enum import Enum
import os

class Settings(Enum):
    SECRET_KEY: str = os.environ.get("SECRET_KEY")
    ALGORITHM: str = os.environ.get("HASH_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")
    SQLALCHEMY_DATABASE_URL : str = os.environ.get("SQLALCHEMY_DATABASE_URL")
    SQLALCHEMY_DATABASE_URL_TESTING_DB : str = os.environ.get("SQLALCHEMY_DATABASE_URL_TESTING_DB")

settings = Settings
