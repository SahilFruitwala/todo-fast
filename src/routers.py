from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.db import get_db
from src.crud import (
    get_task,
    get_tasks,
    create_task,
    update_task,
    delete_task,
    set_complete_task,
    set_delete_task,
)
from src.schemas import TaskResponse, TaskCreate, TaskUpdate, TaskComplete, TaskDelete

router = APIRouter(prefix="/tasks", tags=['tasks'])


@router.get("/", response_model=List[TaskResponse])
async def read_tasks(db: Session = Depends(get_db)):
    return get_tasks(db)


@router.get("/{task_id}", response_model=TaskResponse)
async def read_specific_task(task_id: int, db: Session = Depends(get_db)):
    db_task = get_task(db, task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@router.post("/", response_model=TaskResponse)
async def write_task(task: TaskCreate, db: Session = Depends(get_db)):
    return create_task(db, task)


@router.patch("/complete", response_model=List[TaskResponse])
async def set_complete_multiple_task(
    tasks: TaskComplete, db: Session = Depends(get_db)
):
    return set_complete_task(db, tasks)


@router.patch("/delete", response_model=List[TaskResponse])
async def set_delete_multiple_task(
    tasks: TaskDelete, db: Session = Depends(get_db)
):
    return set_delete_task(db, tasks)


@router.patch("/{task_id}", response_model=TaskResponse)
async def modify_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    return update_task(db, task_id, task)


@router.delete("/{task_id}")
async def remove_task(task_id: int, db: Session = Depends(get_db)):
    return delete_task(db, task_id)
