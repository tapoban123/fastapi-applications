# Connects business logic with api routes


from fastapi import APIRouter, status, HTTPException
from .model import CreateNewUserModel, LoginUserModel, GetUserInfo
from passlib.context import CryptContext
from ..database.core import db_dependency
from ..entities.user import Users
import uuid
from .services import *
from dotenv import load_dotenv
import os


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/create-user", status_code=status.HTTP_201_CREATED)
def create_new_user(user_details: CreateNewUserModel, db: db_dependency):
    return create_user(
        db=db,
        email=user_details.email,
        name=user_details.name,
        password=user_details.password,
    )


@router.post("/login-user")
def login_user(user_details: LoginUserModel, db: db_dependency):
    return user_login(db=db, email=user_details.email, password=user_details.password)
