from pydantic import BaseModel
from datetime import datetime


class BaseUserCredentialRequest:
    email: str
    password: str


class CreateUser(BaseUserCredentialRequest, BaseModel):
    name: str


class FetchUserInfo(BaseModel):
    id: int
    name: str
    email: str
    creation_date: datetime
    account_updated: datetime | None


class Token(BaseModel):
    access_token: str
    token_type: str
