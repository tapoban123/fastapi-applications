# Contains pydantic data validation schemas.

from pydantic import BaseModel, EmailStr
from datetime import datetime


class AuthModelBase:
    email: EmailStr
    password: str


class CreateNewUserModel(BaseModel, AuthModelBase):
    name: str


class LoginUserModel(BaseModel, AuthModelBase):
    pass


class GetUserInfo(BaseModel):
    token: str
    id: str
    name: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime | None
