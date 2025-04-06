from fastapi import APIRouter, status, Depends, HTTPException
from models import CreateUser, Token, LoginUser, DeleteUser
from passlib.context import CryptContext
from database.models import Users, Contacts
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from database.config import get_db, Session
from typing import Annotated
from jose import jwt, JWTError
from datetime import datetime, timedelta

router = APIRouter(prefix="/auth", tags=["auth"])

SECRET_KEY = "2b949df779171e3bf29d67809044172c1ecb14c0a730ea7837e4afb00a8cacf0a7c795e9dcb9b6c888b5d484e2bebc3740d20fb2c94e5d674bc16114278c09ef534e1c46eaddd3731ca515e30102cae8e96d1ad99585f478ad122e235361d5dad5fc49fb2770c577df704b83275a213a2a15811fec8c39e423559f15d96fefb3e43b04ba4bac25fecb7da1c8110e59ee4a60cf6f679eb353f741f34cd74000f0cf91b5ba932f1e58a6be2f05295e67710b20c92e13e6e091eeb4e32177d06347a8abf002ab9b815caf42cbf678a7ceb2b39d243cf6a0e11b775f9465cd7893f003556ae9d55525941cec4754bd3eb5a8850625c90407accfeae76952fa9e14dfeba97b1ce7ced99f46ed7a4d05ede37d56c68b7ab37a41cf2f28f07ba789c310"
ALGORITHM = "HS256"

bcrypt_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

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
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency
):
    user = authenticate_user(form_data.email, form_data.password, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Failed to validate user."
        )

    token = create_token_for_user(user.email, db)
    return {"token_type": "Bearer", "access_token": token}


@router.delete("/delete-user")
def delete_user(user: DeleteUser, db: db_dependency):
    user = authenticate_user(user.email, user.password)

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


def create_token(email: str, creation_date: str, id: int):
    payload = {"email": email, "creation_date": creation_date, "id": id}
    exp_claim = datetime.now() + timedelta(minutes=20)
    payload.update({"exp": exp_claim})

    token = jwt.encode(payload, algorithm=ALGORITHM, key=SECRET_KEY)

    return token
