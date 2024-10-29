from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: str


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None


class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        json_encoders={datetime: lambda v: v.strftime("%Y-%m-%d %H-%M-%S")},
        from_attributes=True,
    )
