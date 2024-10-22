from typing import List
from sqlalchemy.orm import Session
from src.models import Task
from src.schemas import TaskCreate, TaskUpdate, TaskComplete, TaskDelete
from fastapi import HTTPException
from datetime import datetime

def get_task(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()

def get_tasks(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Task).filter(Task.is_active == True).offset(skip).limit(limit).all()  # noqa: E712


def create_task(db: Session, task: TaskCreate):
    task_data = task.dict(exclude_unset=True)
    db_task = Task(**task_data)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(db: Session, task_id: int, task: TaskUpdate):
    task_data = task.dict(exclude_unset=True)
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in task_data.items():
        setattr(db_task, key, value)

    db_task.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_task)

    return db_task


def set_delete_task(db: Session, tasks: TaskDelete):
    db.query(Task).filter(Task.id.in_(tasks.ids), Task.is_active == True).update(
        {Task.is_active: False},
        synchronize_session=False,
    )
    db.commit()
    return db.query(Task).filter(Task.id.in_(tasks.ids), Task.is_active == True).all()


def set_complete_task(db: Session, tasks: TaskComplete):
    db.query(Task).filter(Task.id.in_(tasks.ids), Task.is_active == True).update(
        {Task.completed: tasks.completed},
        synchronize_session=False,
    )
    db.commit()
    return db.query(Task).filter(Task.id.in_(tasks.ids), Task.is_active == True).all()


def delete_task(db: Session, task_id: int):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    if db_task.is_active:  # send to trash
        db_task.updated_at = datetime.utcnow()
        db_task.is_active = False
    else:  # permanently delete
        db.delete(db_task)
    
    db.commit()
