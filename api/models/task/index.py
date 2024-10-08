from sqlalchemy import Boolean, Column, Date, Integer, String

from api.db import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String(1024))
    due_date = Column(Date)
    is_done = Column(Boolean, default=False, nullable=False)
