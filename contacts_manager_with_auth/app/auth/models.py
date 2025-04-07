from pydantic import BaseModel, EmailStr, UUID4
from datetime import datetime


class BaseUserCredentialRequest:
    email: EmailStr
    password: str


class CreateUser(BaseUserCredentialRequest, BaseModel):
    name: str


class FetchUserInfo(BaseModel):
    id: UUID4
    name: str
    email: EmailStr
    creation_date: datetime
    account_updated: datetime | None


class Token(BaseModel):
    access_token: str
    token_type: str
