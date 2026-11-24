from sqlalchemy import select
from sqlalchemy.orm import Session

from pm_hook.models.project import Project
from pm_hook.schemas.project import CreateProjectRequest


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
