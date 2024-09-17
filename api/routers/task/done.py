from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import api.cruds.task.done as done_crud
import api.cruds.task.index as task_crud
import api.schemas.task.index as task_schema
from api.db import get_db

router = APIRouter()


# タスクの完了状態の更新
@router.put("/tasks/{task_id}/done", tags=["task"], response_model=task_schema.Task)
async def change_is_done_of_task(task_id: int, db: AsyncSession = Depends(get_db)):
    task = await task_crud.get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return await done_crud.change_is_done_of_task(db, is_done=(not task.is_done), target_task=task)
