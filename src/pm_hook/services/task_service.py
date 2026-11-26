from sqlalchemy.orm import Session
from pm_hook.schemas.task import CreateTaskRequest, UpdateTaskRequest
from pm_hook.models.project import Project
from pm_hook.core.exceptions import AppError
from fastapi import status
from sqlalchemy import select

from pm_hook.models.task import Task


def create_task(
    db: Session,
    project_id: int,
    task_data: CreateTaskRequest
) -> Task:
    project = db.get(Project, project_id)

    if project is None:
        raise AppError(
            message='Project not found',
            code='PROJECT_NOT_FOUND',
            status_code=status.HTTP_404_NOT_FOUND,
        )

    task = Task(
        project_id=project_id,
        title=task_data.title,
        description=task_data.description,
        status=task_data.status,
        due_date=task_data.due_date,
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def get_tasks_by_project(
    db: Session,
    project_id: int,
) -> list[Task]:
    project = db.get(Project, project_id)

    if project is None:
        raise AppError(
            message="Project not found",
            code="PROJECT_NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    statement = select(Task).where(
        Task.project_id == project_id
    )

    tasks = db.scalars(statement).all()

    return list(tasks)


def get_task_by_id(
    db: Session,
    project_id: int,
    task_id: int,
) -> Task:
    project = db.get(Project, project_id)

    if project is None:
        raise AppError(
            message="Project not found",
            code="PROJECT_NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    statement = select(Task).where(
        Task.id == task_id,
        Task.project_id == project_id,
    )

    task = db.scalar(statement)

    if task is None:
        raise AppError(
            message="Task not found",
            code="TASK_NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return task


def update_task(
    db: Session,
    project_id: int,
    task_id: int,
    task_data: UpdateTaskRequest,
) -> Task:
    project = db.get(Project, project_id)

    if project is None:
        raise AppError(
            message="Project not found",
            code="PROJECT_NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    statement = select(Task).where(
        Task.id == task_id,
        Task.project_id == project_id,
    )

    task = db.scalar(statement)

    if task is None:
        raise AppError(
            message="Task not found",
            code="TASK_NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    update_data = task_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        if field == "status" and value is not None:
            value = value.value

        setattr(task, field, value)

    db.commit()
    db.refresh(task)

    return task


def delete_task(
    db: Session,
    project_id: int,
    task_id: int,
) -> None:
    project = db.get(Project, project_id)

    if project is None:
        raise AppError(
            message="Project not found",
            code="PROJECT_NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    statement = select(Task).where(
        Task.id == task_id,
        Task.project_id == project_id,
    )

    task = db.scalar(statement)

    if task is None:
        raise AppError(
            message="Task not found",
            code="TASK_NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    db.delete(task)
    db.commit()