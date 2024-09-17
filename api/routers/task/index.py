from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException

# from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

import api.cruds.task.index as task_crud
import api.schemas.task.index as task_schema
from api.db import get_db
from api.routers.task import done

router = APIRouter()


# タスク一覧の取得
@router.get("/tasks", tags=["task"], response_model=List[task_schema.Task])
async def list_tasks(is_done: Optional[bool] = None, db: AsyncSession = Depends(get_db)):
    return await task_crud.get_tasks(db, is_done)


# タスクの新規作成
@router.post("/tasks", tags=["task"], response_model=task_schema.Task)
async def create_task(task_body: task_schema.TaskOfOnlyTitle, db: AsyncSession = Depends(get_db)):
    return await task_crud.create_task(db, new_task=task_body)


# タスクの取得
@router.get("/tasks/{task_id}", tags=["task"], response_model=task_schema.Task)
async def get_task(task_id: int, db: AsyncSession = Depends(get_db)):
    task = await task_crud.get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


# タスクの更新
@router.put("/tasks/{task_id}", tags=["task"], response_model=task_schema.Task)
async def update_task(
    task_id: int,
    task_body: task_schema.TaskOfOnlyTitle,
    db: AsyncSession = Depends(get_db),
):
    task = await task_crud.get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return await task_crud.update_task(db, update_task=task_body, target_task=task)


# タスクの削除
@router.delete("/tasks/{task_id}", tags=["task"], response_model=None)
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    task = await task_crud.get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return await task_crud.delete_task(db, delete_task=task)


router.include_router(done.router)
