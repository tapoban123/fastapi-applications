from sqlalchemy import Column, String, Integer, DateTime
from database.config import Base
from sqlalchemy.sql import func
import uuid


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    creation_date = Column(DateTime(timezone=True), server_default=func.now())
    account_updated = Column(DateTime(timezone=True), onupdate=func.now())


class Contacts(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    contact_id = Column(unique=True, nullable=False, server_default=uuid.uuid1())
    name = Column(String, nullable=False)
    contact_number = Column(Integer, nullable=False)
    country_code = Column(String, nullable=False)
    description = Column(String, nullable=True)
    creation_datetime = Column(DateTime(timezone=True), server_default=func.now())
    update_datetime = Column(DateTime(timezone=True), onupdate=func.now())
