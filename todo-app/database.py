from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

USERNAME = os.environ.get("DB_USERNAME")
PASSWORD = os.environ.get("DB_PASSWORD")
DATABASE_NAME = os.environ.get("DATABASE_NAME")

print(USERNAME, PASSWORD, DATABASE_NAME)

DATEBASE_URL = (
    f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@localhost:5432/{DATABASE_NAME}"
)

engine = create_engine(DATEBASE_URL)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
