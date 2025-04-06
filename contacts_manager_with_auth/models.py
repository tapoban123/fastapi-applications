from pydantic import BaseModel
import datetime


class BaseUserCredentialRequest:
    email: str
    password: str


class CreateUser(BaseUserCredentialRequest, BaseModel):
    name: str


class LoginUser(BaseUserCredentialRequest, BaseModel):
    pass


class DeleteUser(BaseUserCredentialRequest, BaseModel):
    pass


class Token(BaseModel):
    access_token: str
    token_type: str
