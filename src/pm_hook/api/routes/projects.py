
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from pm_hook.db.session import get_db
from pm_hook.schemas.project import CreateProjectRequest, ProjectResponse
from pm_hook.services.project_service import create_project, get_projects, get_project_by_id


router = APIRouter(
    prefix="/projects",
    tags=["projects"],
)


@router.post(
    "/",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_project_route(
    project_data: CreateProjectRequest,
    db: Session = Depends(get_db),
) -> ProjectResponse:
    project = create_project(db, project_data)
    return project


@router.get(
    "/",
    response_model=list[ProjectResponse],
    status_code=status.HTTP_200_OK,
)
def get_projects_route(
    db: Session = Depends(get_db),
) -> list[ProjectResponse]:
    projects = get_projects(db)
    return projects



@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
    status_code=status.HTTP_200_OK,
)
def get_project_by_id_route(
    project_id: int,
    db: Session = Depends(get_db),
) -> ProjectResponse:
    project = get_project_by_id(db, project_id)

    if project is None:
        
        # When error expected use AppError, When unexpected use intentional HTTP error like here we used. 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    return project
