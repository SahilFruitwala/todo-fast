from typing import Type, List

import itertools as it

from src.crud.user import validated_user
from src.utils import utc_time
from sqlalchemy.orm import Session
from src.models import Task
from src.schemas.tasks import TaskCreate, TaskUpdate, TaskComplete, TaskDeleteRestore
from fastapi import HTTPException

from typing import Annotated
from src.db import get_db
from fastapi import Depends

db_dep = Annotated[Session, Depends(get_db)]


# Dependency to check if multiple tasks exist
async def validated_tasks(db: Session, task_ids: List[int]) -> List[Task]:
    incoming_ids = set(task_ids)
    tasks = db.query(Task).filter(Task.id.in_(incoming_ids)).all()
    existing_ids = set(task.id for task in tasks)
    if error_ids := incoming_ids - existing_ids:
        raise HTTPException(
            status_code=404,
            detail=f"Task with ids '{', '.join(str(_id) for _id in error_ids)}' not found",
        )
    return tasks


def validated_task(db: Session, task_id: int) -> Task:
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(
            status_code=404, detail=f"Task with id '{task_id}' not found"
        )
    return task


def get_tasks(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Task).filter(Task.is_active == True).offset(skip).limit(limit).all()


def create_task(db: Session, task: TaskCreate):
    validated_user(db, user_id=task.user_id)
    task_data = task.model_dump(exclude_none=True)
    db_task = Task(**task_data)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(db: Session, task_id: int, task: TaskUpdate):
    task_data = task.model_dump(exclude_none=True)
    db_task = validated_task(db, task_id)
    for key, value in task_data.items():
        setattr(db_task, key, value)

    db_task.updated_at = utc_time()
    db.commit()
    db.refresh(db_task)

    return db_task


def delete_tasks(db: Session, tasks: TaskDeleteRestore, permanent=False):
    if not permanent:
        db.query(Task).filter(Task.id.in_(tasks.ids), Task.is_active == True).update(
            {Task.deleted: True, Task.updated_at: utc_time()},
            synchronize_session=False,
        )
    else:
        db.query(Task).filter(Task.id.in_(tasks.ids), Task.is_active == True).update(
            {Task.is_active: False, Task.updated_at: utc_time()},
            synchronize_session=False,
        )
    db.commit()


def restore_tasks(db: Session, tasks: TaskDeleteRestore):
    db.query(Task).filter(Task.id.in_(tasks.ids), Task.is_active == True).update(
        {Task.deleted: False, Task.updated_at: utc_time()},
        synchronize_session=False,
    )
    db.commit()


def complete_tasks(db: Session, tasks: TaskComplete):
    db.query(Task).filter(Task.id.in_(tasks.ids), Task.is_active == True).update(
        {Task.completed: tasks.completed, Task.updated_at: utc_time()},
        synchronize_session=False,
    )
    db.commit()
    return db.query(Task).filter(Task.id.in_(tasks.ids), Task.is_active == True).all()
