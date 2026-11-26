from pydantic import BaseModel, Field, field_validator
from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field

class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"

class CreateTaskRequest(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = None
    status: TaskStatus = TaskStatus.pending
    due_date: date | None = None

class UpdateTaskRequest(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )
    description: str | None = None
    status: TaskStatus | None = None
    due_date: date | None = None

    @field_validator("title")
    @classmethod
    def title_cannot_be_null(cls, value: str | None) -> str:
        if value is None:
            raise ValueError("Task title cannot be null")
        return value

    @field_validator("status")
    @classmethod
    def status_cannot_be_null(
        cls,
        value: TaskStatus | None,
    ) -> TaskStatus:
        if value is None:
            raise ValueError("Task status cannot be null")
        return value

class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    project_id: int
    title: str
    description: str | None
    status: TaskStatus
    due_date: date | None
    created_at: datetime


class TaskListResponse(BaseModel):
    items: list[TaskResponse]
    total: int
    limit: int
    offset: int
