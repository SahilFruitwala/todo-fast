from typing import Optional, Any
from datetime import datetime
from typing_extensions import Self

from pydantic import BaseModel, ConfigDict, field_validator, model_validator


class UserBase(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: str


class UserCreate(UserBase):
    password: str
    confirm_password: str

    @model_validator(mode='after')
    def check_passwords_match(self) -> Self:
        pw1 = self.password
        pw2 = self.confirm_password
        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValueError('Passwords do not match!')
        return self


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    new_password: Optional[str] = None

    @model_validator(mode='after')
    def check_passwords_match(self) -> Self:
        password = self.password
        new_password = self.new_password
        if (password is not None and new_password is None) or (password is None and new_password is not None):
            raise ValueError('Both password fields are required!')
        if password is not None and password == new_password:
            raise ValueError('Password fields cannot be same!')
        return self


class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        json_encoders={datetime: lambda v: v.strftime('%Y-%m-%d %H-%M-%S')},
        from_attributes=True,
    )
