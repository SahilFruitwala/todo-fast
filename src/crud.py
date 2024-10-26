from typing import Type, List

from src.utils import utc_time
from sqlalchemy.orm import Session
from src.models import Task
from src.schemas import TaskCreate, TaskUpdate, TaskComplete, TaskDeleteRestore
from fastapi import HTTPException

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

    db_task.updated_at = utc_time()
    db.commit()
    db.refresh(db_task)

    return db_task


def delete_tasks(db: Session, tasks: TaskDeleteRestore, permanent=False):
    if not permanent:
        db.query(Task).filter(Task.id.in_(tasks.ids), Task.is_active == True).update(
            {Task.deleted: True},
            synchronize_session=False,
        )
    else:
        db.query(Task).filter(Task.id.in_(tasks.ids), Task.is_active == True).update(
            {Task.is_active: False},
            synchronize_session=False,
        )
    db.commit()


def restore_tasks(db: Session, tasks: TaskDeleteRestore):
    db.query(Task).filter(Task.id.in_(tasks.ids), Task.is_active == True).update(
        {Task.deleted: False},
        synchronize_session=False,
    )
    db.commit()


def complete_tasks(db: Session, tasks: TaskComplete):
    db.query(Task).filter(Task.id.in_(tasks.ids), Task.is_active == True).update(
        {Task.completed: tasks.completed},
        synchronize_session=False,
    )
    db.commit()
    return db.query(Task).filter(Task.id.in_(tasks.ids), Task.is_active == True).all()
