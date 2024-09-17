from typing import List, Optional, Tuple

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

import api.models.task.index as task_model
import api.schemas.task.index as task_schema


async def create_task(db: AsyncSession, new_task: task_schema.TaskOfOnlyTitle) -> task_model.Task:
    """
    タスクの新規作成

    Args:
        db (Session): SQLAlchemyのデータベースセッションオブジェクト。
        new_task (task_schema.TaskOfOnlyTitle): 新規作成するタスクのオブジェクト。

    Returns:
        task_model.Task: 新規作成したタスクのオブジェクト。
    """
    task = task_model.Task(**new_task.dict())
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


async def get_task(db: AsyncSession, task_id: int) -> Optional[task_model.Task]:
    """
    タスクの取得

    Args:
        db (Session): SQLAlchemyのデータベースセッションオブジェクト。
        task_id (int): 取得したいタスクのID。

    Returns:
        Optional[task_model.Task]: 指定されたIDのタスクのオブジェクト。存在しない場合はNone。
    """
    result: Result = await db.execute(select(task_model.Task).filter(task_model.Task.id == task_id))
    task: Optional[Tuple[task_model.Task]] = result.first()
    return task[0] if task is not None else None


async def get_tasks(db: AsyncSession, is_done: Optional[bool]) -> List[task_model.Task]:
    """
    タスク一覧の取得

    Args:
        db (Session): SQLAlchemyのデータベースセッションオブジェクト。
        is_done (Optional[bool]): フィルタリング条件となるタスクの完了状態。

    Returns:
        List[task_model.Task]: タスクのオブジェクトのリスト
    """
    result: Result = await db.execute(
        select(
            task_model.Task.id,
            task_model.Task.title,
            task_model.Task.is_done,
        ).filter(task_model.Task.is_done == is_done if is_done is not None else True)
    )
    return result.all()


async def update_task(
    db: AsyncSession,
    update_task: task_schema.TaskOfOnlyTitle,
    target_task: task_model.Task,
) -> task_model.Task:
    """
    タスクの更新

    Args:
        db (Session): SQLAlchemyのデータベースセッションオブジェクト。
        update_task (task_schema.TaskOfOnlyTitle): 更新するタスクのオブジェクト。
        target_task (task_schema.Task): 更新対象のタスクのオブジェクト。

    Returns:
        task_model.Task: 更新したタスクのオブジェクト。
    """
    target_task.title = update_task.title
    db.add(target_task)
    await db.commit()
    await db.refresh(target_task)
    return target_task


async def delete_task(db: AsyncSession, delete_task: task_model.Task) -> None:
    """
    タスクの削除

    Args:
        db (Session): SQLAlchemyのデータベースセッションオブジェクト。
        delete_task (task_model.Task): 削除するタスクのオブジェクト。

    Returns:
        None: この関数は値を返しません。
    """
    await db.delete(delete_task)
    await db.commit()
