from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from typing import Annotated
from dotenv import load_dotenv
import os

DATEBASE_URL = f"postgresql+psycopg2://postgres:tapoban@localhost:5432/to-do_appDB"

engine = create_engine(DATEBASE_URL)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
