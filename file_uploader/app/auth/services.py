# Contains all the business logic

from passlib.context import CryptContext
from ..database.core import db_dependency
from ..entities.user import Users
from ..exceptions import AccountNotFoundError, InvalidCredentialsError
import uuid
from dotenv import load_dotenv
import os
from jose import JWTError, jwt
from datetime import datetime, timedelta

load_dotenv()

JWT_SECRET_KEY = os.environ.get("SECRET_KEY")
JWT_ALGORITHM = os.environ.get("ALGORITHM")


bycrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(name: str, email: str, password: str, db: db_dependency):
    new_user = Users(
        id=uuid.uuid4().hex,
        name=name,
        email=email,
        hashed_password=bycrypt_context.hash(password),
    )

    db.add(new_user)
    db.commit()

    return {"details": "success"}


def user_login(email: str, password: str, db: db_dependency):
    existing_user = db.query(Users).filter(Users.email == email).first()

    if not existing_user:
        raise AccountNotFoundError()

    if not bycrypt_context.verify(password, existing_user.hashed_password):
        raise InvalidCredentialsError()

    token = generate_token(uid=existing_user.id, email=existing_user.email)

    return {"token": token, "valid_for": "30 days"}


def generate_token(uid: str, email: str):
    payload = {"email": email, "uid": uid}
    exp_claim = datetime.now() + timedelta(days=30)
    payload.update({"exp": exp_claim})

    token = jwt.encode(payload, algorithm=JWT_ALGORITHM, key=JWT_SECRET_KEY)
    return token
