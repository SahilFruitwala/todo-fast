from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class TaskBase(BaseModel):
    todo: str
    description: str


class TaskCreate(TaskBase):
    user_id: int


class TaskUpdate(BaseModel):
    todo: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class TaskComplete(BaseModel):
    ids: List[int] = []
    completed: Optional[bool] = None


class TaskDeleteRestore(BaseModel):
    ids: List[int] = []


class TaskResponse(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime
    completed: bool

    model_config = ConfigDict(
        json_encoders={datetime: lambda v: v.strftime("%Y-%m-%d %H-%M-%S")},
        from_attributes=True,
    )
