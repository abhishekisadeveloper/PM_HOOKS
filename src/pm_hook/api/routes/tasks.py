    
from pm_hook.services.task_service import create_task, get_tasks_by_project, get_task_by_id

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from pm_hook.db.session import get_db
from pm_hook.schemas.task import CreateTaskRequest, TaskResponse


router = APIRouter(
    prefix="/projects/{project_id}/tasks",
    tags=["tasks"],
)

@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_task_route(
    project_id: int,
    task_data: CreateTaskRequest,
    db: Session = Depends(get_db),
) -> TaskResponse:
    task = create_task(db, project_id, task_data)
    return task 


@router.get(
    "/",
    response_model=list[TaskResponse],
    status_code=status.HTTP_200_OK,
)
def get_tasks_by_project_route(
    project_id: int,
    db: Session = Depends(get_db),
) -> list[TaskResponse]:
    tasks = get_tasks_by_project(db, project_id)
    
    return tasks


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
)
def get_task_by_id_route(
    project_id: int,
    task_id: int,
    db: Session = Depends(get_db),
) -> TaskResponse:
    task = get_task_by_id(db, project_id, task_id)

    return task
