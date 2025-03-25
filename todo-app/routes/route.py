from fastapi import APIRouter, Depends, status, HTTPException
from database import get_db
from sqlalchemy.orm import Session
from typing import Annotated
from models.request_models import TaskBase, EditTaskBase
from datetime import datetime
import models.db_models as db_models

db_dependency = Annotated[Session, Depends(get_db)]


router = APIRouter(
    prefix="/tasks",
    tags=["Task"],
)


@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_task(task: TaskBase, db: db_dependency):
    try:
        db_task = db_models.Tasks(**task.model_dump())
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create task"
        )

    return {"detail": "success"}


@router.put("/update-task/{task_id}")
def edit_task(task_id: int, new_task: EditTaskBase, db: db_dependency):
    task_model = db.query(db_models.Tasks).filter(db_models.Tasks.id == task_id).first()
    if task_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No task exists at id {task_id}.",
        )

    task_model.title = new_task.title
    task_model.description = new_task.description
    task_model.updated_at = new_task.updated_at

    db.add(task_model)
    db.commit()

    return {"detail": task_model}


@router.get("/get-tasks")
def get_all_tasks(db: db_dependency):
    tasks = db.query(db_models.Tasks).all()
    return {"details": {"tasks": tasks}}


@router.delete("/delete-task/{task_id}")
def delete_task(task_id: int, db: db_dependency):
    task_model = db.query(db_models.Tasks).filter(db_models.Tasks.id == task_id).first()
    if task_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No task exists by id: {task_id}",
        )

    db.query(db_models.Tasks).filter(db_models.Tasks.id == task_id).delete()
    db.commit()

    return {"deleted": task_model}
