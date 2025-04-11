# Contain all database configurations

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.engine import create_engine
from fastapi import Depends
from dotenv import load_dotenv
from typing import Annotated
import os


DATABASE_URL = "sqlite:///users.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


Base = declarative_base()


def get_db():
    with Session(engine) as session:
        yield session


db_dependency = Annotated[Session, Depends(get_db)]
