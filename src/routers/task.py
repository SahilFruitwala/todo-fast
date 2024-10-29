from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from src.db import get_db
from src.crud.task import (
    get_tasks,
    create_task,
    update_task,
    complete_tasks,
    delete_tasks,
    restore_tasks,
    validated_tasks,
    validated_task,
)
from src.schemas.tasks import (
    TaskResponse,
    TaskCreate,
    TaskUpdate,
    TaskComplete,
    TaskDeleteRestore,
)

router = APIRouter(prefix='/tasks', tags=['tasks'])


@router.get('/', response_model=List[TaskResponse])
async def read_tasks(db: Session = Depends(get_db)):
    return get_tasks(db)


@router.get('/{task_id}', response_model=TaskResponse)
async def read_specific_task(task_id: int, db: Session = Depends(get_db)):
    return validated_task(db, task_id)


@router.post('/', response_model=TaskResponse)
async def write_task(task: TaskCreate, db: Session = Depends(get_db)):
    return create_task(db, task)


@router.patch('/complete')
async def set_complete_multiple_task(
    tasks: TaskComplete, db: Session = Depends(get_db)
):
    await validated_tasks(db, tasks.ids)
    return complete_tasks(db, tasks)


@router.patch('/restore')
async def restore_multiple_task(
    tasks: TaskDeleteRestore, db: Session = Depends(get_db)
):
    return restore_tasks(db, tasks)


@router.patch('/{task_id}', response_model=TaskResponse)
async def modify_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    return update_task(db, task_id, task)


@router.post('/delete')
async def remove_task(tasks: TaskDeleteRestore, db: Session = Depends(get_db)):
    return delete_tasks(db, tasks)


@router.post('/permanentDelete')
async def remove_permanent_task(
    tasks: TaskDeleteRestore, db: Session = Depends(get_db)
):
    return delete_tasks(db, tasks, permanent=True)