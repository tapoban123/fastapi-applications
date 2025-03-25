from database import Base
from sqlalchemy import Column, String, Integer, DateTime


class Tasks(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    completed_at = Column(DateTime, nullable=True)
