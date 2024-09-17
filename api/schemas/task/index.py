import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Task(BaseModel):
    id: int
    title: Optional[str] = Field(None, example="ラジオ体操", description="タスク名")
    due_date: Optional[datetime.date] = Field(None, example="2024-09-01", description="期日")
    is_done: bool = Field(False, description="完了状態の真偽値")

    class Config:
        orm_mode = True


class TaskOfOnlyTitle(BaseModel):
    title: Optional[str] = Field(None, example="ラジオ体操", description="タスク名")
