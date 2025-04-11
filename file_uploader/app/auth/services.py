# Contains all the business logic

from fastapi import APIRouter
from .model import CreateNewUserModel, LoginUserModel

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/create-user")
def create_new_user(user_details: CreateNewUserModel):
    return [user_details.name, user_details.email, user_details.password]
