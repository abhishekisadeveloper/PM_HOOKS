from sqlalchemy import select
from sqlalchemy.orm import Session
from pm_hook.core.exceptions import AppError
from fastapi import status

from pm_hook.models.project import Project
from pm_hook.schemas.project import CreateProjectRequest, UpdateProjectRequest


def create_project(
    db: Session,
    project_data: CreateProjectRequest,
) -> Project:
    # 1. Create SQLAlchemy model object
    project = Project(
        name=project_data.name,
        description=project_data.description,
    )

    # 2. Add the object to the session
    db.add(project)

    db.commit()
    db.refresh(project)

    # 5. Return the created project
    return project


def update_project(
    db: Session,
    project_id: int,
    update_data: UpdateProjectRequest,
) -> Project:
    project = db.get(Project, project_id)

    if project is None:
        # Raise existing AppError here
        raise AppError(
            message='Project not found',
            code='PROJECT_NOT_FOUND',
            status_code=status.HTTP_404_NOT_FOUND,
        )

    updated_fields = update_data.model_dump(exclude_unset=True)
    
    # print('new test for the data:', updated_fields)

    for field, value in updated_fields.items(): # <- e.g. {"description": "New text"}
        setattr(project, field, value)

    db.commit()
    db.refresh(project)

    return project


def get_projects(db: Session) -> list[Project]:
    statement = select(Project)

    projects = db.scalars(statement).all()

    return list(projects)


def get_project_by_id(
    db: Session,
    project_id: int,
) -> Project | None:
    statement = select(Project).where(Project.id == project_id)

    project = db.scalar(statement)

    return project
