from datetime import datetime
from src.utils import utc_time
from sqlalchemy import String, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from src.db import Base


class Task(Base):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(primary_key=True)
    todo: Mapped[str] = mapped_column(String(120))
    description: Mapped[str] = mapped_column(String(480))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_time)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utc_time)
    completed: Mapped[bool] =  mapped_column(Boolean, default=False)
    deleted: Mapped[bool] =  mapped_column(Boolean, default=False)
    is_active: Mapped[bool] =  mapped_column(Boolean, default=True)
