from fastapi import APIRouter, status, Depends, HTTPException
from routers.auth.models import CreateUser, Token, FetchUserInfo
from passlib.context import CryptContext
from database.models import Users, Contacts
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from database.config import get_db, Session
from typing import Annotated
from jose import jwt, JWTError
from datetime import datetime, timedelta
from dotenv import load_dotenv
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

db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/create-user", status_code=status.HTTP_201_CREATED, response_model=Token)
def create_user(credentials: CreateUser, db: db_dependency):
    user_model = Users(
        name=credentials.name,
        email=credentials.email,
        password=bcrypt_context.hash(credentials.password),
    )

    db.add(user_model)
    db.commit()

    token = create_token_for_user(email=credentials.email, db=db)

    return {"token_type": "Bearer", "access_token": token}


@router.post("/login", response_model=Token)
def login(formdata: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(formdata.username, formdata.password, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Failed to validate user."
        )

    token = create_token_for_user(user.email, db)
    return {"token_type": "Bearer", "access_token": token}


@router.post("/authenticate-user", response_model=FetchUserInfo)
async def authenticate_user_by_token(token: str, db: db_dependency):
    try:
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])

        email: str = payload.get("email")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user.",
            )
        user_in_db = db.query(Users).filter(email == Users.email).first()

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


def create_token(email: str, creation_date: datetime, id: int):
    payload = {"email": email, "creation_date": creation_date.isoformat(), "id": id}
    exp_claim = datetime.now() + timedelta(minutes=20)
    payload.update({"exp": exp_claim})

    token = jwt.encode(payload, algorithm=ALGORITHM, key=SECRET_KEY)

    return token
