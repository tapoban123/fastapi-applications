from sqlalchemy import Column, String, Integer, DateTime
from database.config import Base
from sqlalchemy.sql import func


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    creation_date = Column(DateTime(timezone=True), server_default=func.now())
    account_updated = Column(DateTime(timezone=True), server_default=func.now())


class Contacts(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    number = Column(String, nullable=False, unique=True)
