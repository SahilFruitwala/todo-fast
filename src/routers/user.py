from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from src.crud.user import (
    get_users,
    validated_user,
    create_user,
    update_user,
    delete_user,
)
from src.db import get_db
from src.schemas.users import UserResponse, UserCreate, UserUpdate

router = APIRouter(prefix='/users', tags=['users'])


@router.get('/', response_model=List[UserResponse])
async def read_users(db: Session = Depends(get_db)):
    return get_users(db)


@router.get('/{user_id}', response_model=UserResponse)
async def read_specific_user(user_id: int, db: Session = Depends(get_db)):
    return validated_user(db, user_id)


@router.post('/', response_model=UserResponse)
async def write_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)


@router.patch('/{user_id}', response_model=UserResponse)
async def modify_task(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    return update_user(db, user_id, user)


@router.post('/delete/{user_id}')
async def remove_task(user_id: int, db: Session = Depends(get_db)):
    return delete_user(db, user_id)
