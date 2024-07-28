from pydantic import BaseModel, EmailStr

class AuthUser(BaseModel):
    email: EmailStr
    password: str