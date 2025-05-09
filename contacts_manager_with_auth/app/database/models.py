from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER
from app.database.config import Base
from sqlalchemy.sql import func


class Users(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    creation_date = Column(DateTime(timezone=True), server_default=func.now())
    account_updated = Column(DateTime(timezone=True), onupdate=func.now())


class Contacts(Base):
    __tablename__ = "contacts"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    contact_number = Column(INTEGER(10), nullable=False)
    country_code = Column(String, nullable=False)
    description = Column(String, nullable=True)
    creation_datetime = Column(DateTime(timezone=True), server_default=func.now())
    update_datetime = Column(DateTime(timezone=True), onupdate=func.now())
