from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from starlette.status import HTTP_204_NO_CONTENT, HTTP_201_CREATED

from src.db import get_db
from src.crud.task import (
    get_tasks,
    create_task,
    update_task,
    complete_tasks,
    delete_tasks,
    restore_tasks,
    validated_task,
)
from src.schemas.tasks import (
    TaskResponse,
    TaskCreate,
    TaskUpdate,
)

router = APIRouter(prefix='/users', tags=['tasks'])


@router.get('/{user_id}/tasks', response_model=List[TaskResponse])
async def read_tasks(user_id: int, db: Session = Depends(get_db)):
    return get_tasks(db, user_id)

@router.get('/{user_id}/tasks/{task_id}', response_model=TaskResponse)
async def read_specific_task(user_id: int, task_id: int, db: Session = Depends(get_db)):
    return validated_task(db, user_id, task_id)

@router.post('/{user_id}/tasks/', response_model=TaskResponse, status_code=HTTP_201_CREATED)
async def add_task(user_id: int, task: TaskCreate, db: Session = Depends(get_db)):
    return create_task(db, user_id, task)


@router.post('/{user_id}/tasks/delete', status_code=HTTP_204_NO_CONTENT)
async def remove_task(user_id: int, task_ids: List[int], db: Session = Depends(get_db)):
    delete_tasks(db, user_id, task_ids)
    return {'message': 'Task deleted successfully'}

@router.post('/{user_id}/tasks/permanentDelete', status_code=HTTP_204_NO_CONTENT)
async def permanent_remove_task(user_id: int, task_ids: List[int], db: Session = Depends(get_db)):
    delete_tasks(db, user_id, task_ids, permanent=True)
    return {'message': 'Task deleted successfully'}

@router.patch('/{user_id}/tasks/complete', response_model=List[TaskResponse])
async def set_complete_task(user_id: int, task_ids: List[int], db: Session = Depends(get_db)):
    return complete_tasks(db, user_id, task_ids)

@router.patch('/{user_id}/tasks/uncomplete', response_model=List[TaskResponse])
async def set_uncomplete_task(user_id: int, task_ids: List[int], db: Session = Depends(get_db)):
    return complete_tasks(db, user_id, task_ids, completed=False)

@router.patch('/{user_id}/tasks/restore')
async def undelete_task(user_id: int, task_ids: List[int], db: Session = Depends(get_db)):
    return restore_tasks(db, user_id, task_ids)

@router.patch('/{user_id}/tasks/{task_id}', response_model=TaskResponse)
async def modify_task(
        user_id: int,
        task_id: int,
        task: TaskUpdate,
        db: Session = Depends(get_db)
):
    return update_task(db, user_id, task_id, task)
