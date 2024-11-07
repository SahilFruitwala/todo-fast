from src.schemas.users import UserCreate, UserUpdate
from src.utils import utc_time, get_hashed_password, check_password
from sqlalchemy.orm import Session
from src.models import User
from fastapi import HTTPException


def validated_user(db: Session, user_id: int) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=404, detail=f"User with id '{user_id}' not found"
        )
    return user


def create_user(db: Session, user: UserCreate) -> User:
    user_data = user.model_dump(exclude_none=True)
    user_data['password'] = get_hashed_password(user_data['password'])
    del user_data['confirm_password']
    db_user = User(**user_data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user: UserUpdate) -> User:
    user_data = user.model_dump(exclude_none=True)
    db_user = validated_user(db, user_id)

    if check_password(user_data['password'], db_user.password):
        user_data['password'] = get_hashed_password(user_data['new_password'])
        del user_data['new_password']

    for key, value in user_data.items():
        setattr(db_user, key, value)

    db_user.updated_at = utc_time()
    db.commit()
    db.refresh(db_user)

    return db_user


def delete_user(db: Session, user_id: int):
    db_user = validated_user(db, user_id)
    db_user.is_active = False
    db_user.updated_at = utc_time()
    db.commit()
