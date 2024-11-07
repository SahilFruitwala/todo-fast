from datetime import datetime
from typing import List

from src.utils import utc_time
from sqlalchemy import String, DateTime, Boolean, ForeignKey, TypeDecorator, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db import Base

# class HexByteString(TypeDecorator):
#     """Convert Python bytestring to string with hexadecimal digits and back for storage."""
#
#     impl = String
#
#     def process_bind_param(self, value, dialect):
#         if not isinstance(value, bytes):
#             raise TypeError("HexByteString columns support only bytes values.")
#         return value.hex()
#
#     def process_result_value(self, value, dialect):
#         return bytes.fromhex(value) if value else None


class Task(Base):
    __tablename__ = 'task'

    id: Mapped[int] = mapped_column(primary_key=True)
    todo: Mapped[str] = mapped_column(String(120))
    description: Mapped[str] = mapped_column(String(480))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_time)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utc_time)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped['User'] = relationship(back_populates='tasks')


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(120), nullable=True)
    last_name: Mapped[str] = mapped_column(String(120), nullable=True)
    email: Mapped[str] = mapped_column(String(120), unique=True)
    password: Mapped[str] = mapped_column(LargeBinary, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_time)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utc_time)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    tasks: Mapped[List['Task']] = relationship(
        back_populates='user', cascade='all, delete'
    )
