# SQL Table for file data

from ..database import core
from sqlalchemy import Column, String, DateTime, func


class FileData(core.Base):
    __tablename__ = "users"

    id = Column(String, index=True, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now)
    updated_at = Column(DateTime, nullable=False, onupdate=func.now)
