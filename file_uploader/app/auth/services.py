# Contains all the business logic

from passlib.context import CryptContext
from ..database.core import db_dependency
from ..entities.user import Users
from ..exceptions import (
    AccountNotFoundError,
    InvalidCredentialsError,
    UserValidationFailedError,
    UserAlreadyExistsError
)
import uuid
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.enums import ENV_VALUES

JWT_SECRET_KEY = ENV_VALUES.JWT_SECRET_KEY.value
JWT_ALGORITHM = ENV_VALUES.JWT_ALGORITHM.value

bycrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(name: str, email: str, password: str, db: db_dependency):
    is_user_exists = db.query(Users).filter(Users.email == email).first()
    if is_user_exists:
        raise UserAlreadyExistsError()

    new_user = Users(
        id=uuid.uuid4().hex,
        name=name,
        email=email,
        hashed_password=bycrypt_context.hash(password),
    )

    db.add(new_user)
    db.commit()

    token = generate_token(new_user.id)

    return {"details": "success", "token": token, "valid_for": "30 days"}


def user_login(email: str, password: str, db: db_dependency):
    existing_user = db.query(Users).filter(Users.email == email).first()

    if not existing_user:
        raise AccountNotFoundError()

    if not bycrypt_context.verify(password, existing_user.hashed_password):
        raise InvalidCredentialsError()

    token = generate_token(uid=existing_user.id)

    return {"token": token, "valid_for": "30 days"}


def generate_token(uid: str):
    payload = {"uid": uid}
    exp_claim = datetime.now() + timedelta(days=30)
    payload.update({"exp": exp_claim})

    token = jwt.encode(payload, algorithm=JWT_ALGORITHM, key=JWT_SECRET_KEY)
    return token


def is_token_valid(token: str, db: db_dependency):
    try:
        payload = jwt.decode(token, algorithms=[JWT_ALGORITHM], key=JWT_SECRET_KEY)

        uid = payload.get("uid")

        if uid is None:
            return False

        user = db.query(Users).filter(Users.id == uid).first()

        if not user:
            return False

        return user
    except JWTError:
        return False


def authenticate_user(token: str, db: db_dependency):
    user = is_token_valid(token, db)

    if not user:
        raise UserValidationFailedError()

    return user


def update_user(
        token: str, new_name: str | None, new_email: str | None, db: db_dependency
):
    user = is_token_valid(token, db)
    if not user:
        raise UserValidationFailedError()

    # updating user
    user.name = new_name if new_name is not None else user.name
    user.email = new_email if new_email is not None else user.email

    db.add(user)
    db.commit()

    return user


def change_password(
        token: str, old_password: str, new_password: str, db: db_dependency
):
    user = is_token_valid(token, db)
    if not user:
        raise UserValidationFailedError()

    if not bycrypt_context.verify(old_password, user.hashed_password):
        raise InvalidCredentialsError()

    # updating old password
    user.hashed_password = bycrypt_context.hash(new_password)
    db.add(user)
    db.commit()

    return {"details": "success", "status": "password_changed"}


def delete_user(token: str, password: str, db: db_dependency):
    user = is_token_valid(token, db)

    if not user:
        raise UserValidationFailedError()

    if not bycrypt_context.verify(password, user.hashed_password):
        raise InvalidCredentialsError()

    db.query(Users).filter(Users.id == user.id).delete()
    db.commit()

    return {"details": "success", "status": "account_deleted"}
