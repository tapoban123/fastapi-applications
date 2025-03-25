from pydantic import BaseModel
from datetime import datetime


class _BaseTaskBase:
    title: str
    description: str


class TaskBase(BaseModel, _BaseTaskBase):
    created_at: datetime = datetime.now()
    updated_at: None
    completed_at: None


class EditTaskBase(BaseModel, _BaseTaskBase):
    updated_at: datetime = datetime.now()
