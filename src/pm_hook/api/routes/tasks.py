    
from pm_hook.services.task_service import create_task, get_tasks_by_project, get_task_by_id, update_task, delete_task

from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session

from pm_hook.db.session import get_db
from pm_hook.schemas.task import CreateTaskRequest, TaskResponse, UpdateTaskRequest, TaskStatus, TaskListResponse


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
    response_model=TaskListResponse,
    status_code=status.HTTP_200_OK,
)
def get_tasks_by_project_route(
    project_id: int,
    task_status: TaskStatus | None = Query(
        default=None, # Remember: default=None makes it optional; 
        alias="status" # alias changes the external parameter name.
        ),
    limit: int = Query(
            default=10,
            ge=1,
            le=100,
        ),
    offset: int = Query(
            default=0,
            ge=0,
        ),
    db: Session = Depends(get_db),
) -> TaskListResponse:
    tasks = get_tasks_by_project(db, project_id, task_status, limit=limit, offset=offset)
    
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


@router.patch(
    "/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
)
def update_task_route(
    project_id: int,
    task_id: int,
    task_data: UpdateTaskRequest,
    db: Session = Depends(get_db),
) -> TaskResponse:
    task = update_task(
        db,
        project_id,
        task_id,
        task_data,
    )

    return task


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_task_route(
    project_id: int,
    task_id: int,
    db: Session = Depends(get_db),
) -> None:
    delete_task(db, project_id, task_id)
