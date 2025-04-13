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
    id: str
    name: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime | None


class UpdateUserDetails(BaseModel):
    name: str | None
    email: str | None


class ChangeUserPassword(BaseModel):
    old_password: str
    new_password: str
