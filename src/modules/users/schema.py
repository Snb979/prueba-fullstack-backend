from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):

    username: str = Field(
        min_length=3,
        max_length=50,
        description="Nombre de usuario"
    )

    email: EmailStr

    password: str = Field(
        min_length=6,
        max_length=100,
        description="Contraseña segura"
    )

    role: str = Field(
        default="user"
    )


class UserResponse(BaseModel):

    id: int
    username: str
    email: EmailStr
    role: str
    created_at: Optional[datetime]

    class Config:
        from_attributes = True