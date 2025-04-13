# SQL Table for file data

from ..database.core import Base
from sqlalchemy import Column, String, DateTime, func, ForeignKey


class UserFiles(Base):
    __tablename__ = "user_files"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    name = Column(String, nullable=True)
    description = Column(String, nullable=True)
    url = Column(String, nullable=False)
    file_type = Column(String, nullable=True)
    size = Column(String, nullable=True)
    uploaded_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
