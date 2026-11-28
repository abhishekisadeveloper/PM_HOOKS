
from pydantic import Field
from typing import Any
from sqlalchemy.orm import Session
from pm_hook.schemas.task import (
    CreateTaskRequest,
    TaskResponse,
)
from pm_hook.services.task_service import create_task
from pm_hook.tools.registry import ToolDefinition


class CreateTaskToolArgs(CreateTaskRequest):
    project_id: int = Field(
        gt=0,
        description="ID of the project that will contain the task",
    )


def execute_create_task(
    arguments: dict[str, Any],
    db: Session,
) -> dict[str, Any]:
    validated = CreateTaskToolArgs.model_validate(arguments)

    project_id = validated.project_id

    task_data = CreateTaskRequest.model_validate(
        validated.model_dump(exclude={"project_id"})
    )

    task = create_task(
        db=db,
        project_id=project_id,
        task_data=task_data,
    )

    response = TaskResponse.model_validate(task)

    return response.model_dump(mode="json")


def register_task_tools(registry) -> None:
    registry.register(
        ToolDefinition(
            name="create_task",
            description=(
                "Create a task in an existing project. "
                "Requires project_id and title. "
                "Can optionally include description, status, and due_date."
            ),
            arguments_schema=CreateTaskToolArgs.model_json_schema(),
            execute=execute_create_task,
        )
    )
