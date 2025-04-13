# Connects business logic with api routes


from fastapi import APIRouter, status, Header
from .model import CreateNewUserModel, LoginUserModel, GetUserInfo
from ..database.core import db_dependency
from .services import *
from typing import Annotated


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


@router.get("/user-info", response_model=GetUserInfo)
def get_user_details(token: Annotated[str, Header()], db: db_dependency):
    return authenticate_user(token=token, db=db)


@router.put("/update-user")
def update_user_details():
    pass


@router.put("/change-password")
def change_user_password():
    pass


@router.delete("/delete-user")
def delete_user_account():
    pass
