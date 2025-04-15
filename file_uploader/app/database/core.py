# Contain all database configurations

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.engine import create_engine
from fastapi import Depends
from typing import Annotated
from ..enums import ENV_VALUES

DATABASE_URL = ENV_VALUES.POSTGRES_DATABASE_URL.value

# engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
engine = create_engine(DATABASE_URL)

Base = declarative_base()


def get_db():
    with Session(engine) as session:
        yield session


db_dependency = Annotated[Session, Depends(get_db)]
