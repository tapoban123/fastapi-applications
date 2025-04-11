# Contains pydantic data validation schemas.

from pydantic import BaseModel, EmailStr

class AuthModelBase:
    email: EmailStr
    password: str
    
class CreateNewUserModel(BaseModel, AuthModelBase):
    name: str

class LoginUserModel(BaseModel, AuthModelBase):
    pass