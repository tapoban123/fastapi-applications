# Connects business logic with api routes


from fastapi import APIRouter, status, Header
from .model import (
    CreateNewUserModel,
    LoginUserModel,
    GetUserInfo,
    UpdateUserDetails,
    ChangeUserPassword,
)
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
def update_user_details(
    new_user: UpdateUserDetails, token: Annotated[str, Header()], db: db_dependency
):
    user = update_user(
        new_email=new_user.email,
        new_name=new_user.name,
        token=token,
        db=db,
    )

    new_user = GetUserInfo(
        id=user.id,
        name=user.name,
        email=user.email,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )

    return {"status": "user_updated", "details": new_user.model_dump()}


@router.put("/change-password")
def change_user_password(
    new_creds: ChangeUserPassword, token: Annotated[str, Header()], db: db_dependency
):
    return change_password(
        token=token,
        new_password=new_creds.new_password,
        old_password=new_creds.old_password,
        db=db,
    )


@router.delete("/delete-user")
def delete_user_account(
    token: Annotated[str, Header()], password: str, db: db_dependency
):
    return delete_user(db=db, password=password, token=token)
