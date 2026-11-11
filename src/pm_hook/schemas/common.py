from typing import Any, Literal

from pydantic import BaseModel


class ErrorDetail(BaseModel):
    code: str
    message: str


class ErrorResponse(BaseModel):
    success: Literal[False] = False
    error: ErrorDetail
    details: list[dict[str, Any]] | None = None