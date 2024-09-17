from sqlalchemy.ext.asyncio import AsyncSession

import api.models.task.index as task_model


async def change_is_done_of_task(
    db: AsyncSession, is_done: bool, target_task: task_model.Task
) -> task_model.Task:
    """
    タスクの完了フラグ更新

    Args:
        db (Session): SQLAlchemyのデータベースセッションオブジェクト。
        is_done (bool): タスクの完了状態。
        target_task (task_schema.Task): 更新対象のタスクのオブジェクト。

    Returns:
        task_model.Task: 更新したタスクのオブジェクト。
    """
    target_task.is_done = is_done
    db.add(target_task)
    await db.commit()
    await db.refresh(target_task)
    return target_task
