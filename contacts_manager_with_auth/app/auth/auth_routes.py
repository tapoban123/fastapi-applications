from fastapi import APIRouter, status, Depends, HTTPException
from .models import CreateUser, Token, FetchUserInfo
from passlib.context import CryptContext
from ..database.models import Users
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from ..database.config import db_dependency
from typing import Annotated
from jose import jwt, JWTError
from datetime import datetime, timedelta
from dotenv import load_dotenv
import uuid
import os

load_dotenv()

router = APIRouter(prefix="/auth", tags=["auth"])

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")

bcrypt_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


# oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


@router.post("/create-user", status_code=status.HTTP_201_CREATED, response_model=Token)
def create_user(credentials: CreateUser, db: db_dependency):
    is_user_exists = db.query(Users).filter(Users.email == credentials.email).first()
    if is_user_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists.")
    user_model = Users(
        id=uuid.uuid4().hex,
        name=credentials.name,
        email=credentials.email,
        password=bcrypt_context.hash(credentials.password),
    )

    db.add(user_model)
    db.commit()

    token = create_token_for_user(email=credentials.email, db=db)

    return {"token_type": "Bearer", "access_token": token}


@router.post("/login", response_model=Token)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Failed to validate user."
        )

    token = create_token_for_user(user.email, db)
    return {"token_type": "Bearer", "access_token": token}


@router.get("/authenticate-user", response_model=FetchUserInfo)
async def authenticate_user_by_token(token: str, db: db_dependency):
    try:
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])

        user_id: str = payload.get("id")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user.",
            )
        user_in_db = db.query(Users).filter(user_id == Users.id).first()

        if not user_in_db:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found."
            )
        return user_in_db
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token. Could not validate user.",
        )


@router.delete("/delete-user")
def delete_user(
        user: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency
):
    user = authenticate_user(user.username, user.password, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Failed to validate user."
        )

    db.query(Users).filter(user.email == Users.email).delete()
    db.commit()

    return {"details": "success"}


def authenticate_user(email: str, password: str, db: db_dependency):
    user_in_db = db.query(Users).filter(Users.email == email).first()

    if not user_in_db:
        return False
    if not bcrypt_context.verify(password, user_in_db.password):
        return False

    return user_in_db


def create_token_for_user(email: str, db: db_dependency):
    user = db.query(Users).filter(Users.email == email).first()
    return create_token(user.email, user.creation_date, user.id)


def create_token(email: str, creation_date: datetime, user_id: str):
    payload = {"email": email, "creation_date": creation_date.isoformat(), "id": user_id}
    exp_claim = datetime.now() + timedelta(minutes=20)
    payload.update({"exp": exp_claim})

    token = jwt.encode(payload, algorithm=ALGORITHM, key=SECRET_KEY)

    return token


def validate_token(token: str, db: db_dependency):
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("id")

        if user_id is None:
            return False

        user = db.query(Users).filter(Users.id == user_id).first()

        if not user:
            return False

        return user_id
    except JWTError:
        return False
