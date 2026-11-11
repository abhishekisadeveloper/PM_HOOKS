import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from pm_hook.core.exceptions import AppError
from pm_hook.schemas.common import ErrorResponse, ErrorDetail


logger = logging.getLogger(__name__)


async def app_error_handler(
    request: Request,
    exc: AppError
) -> JSONResponse:

    response = ErrorResponse(
        error=ErrorDetail(
            code=exc.code,
            message=exc.message
        )
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=response.model_dump()
    )


async def validation_error_handler(
    request: Request,
    exc: RequestValidationError
) -> JSONResponse:

    logger.warning(
        "Request validation failed: %s %s",
        request.method,
        request.url.path
    )

    details = [
        {
            "location": list(error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        }
        for error in exc.errors()
    ]

    response = ErrorResponse(
        error=ErrorDetail(
            code="VALIDATION_ERROR",
            message="Request validation failed"
        ),
        details=details
    )

    return JSONResponse(
        status_code=422,
        content=response.model_dump()
    )


async def http_error_handler(
    request: Request,
    exc: StarletteHTTPException
) -> JSONResponse:

    response = ErrorResponse(
        error=ErrorDetail(
            code="HTTP_ERROR",
            message=str(exc.detail)
        )
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=response.model_dump(),
        headers=exc.headers
    )


async def unexpected_error_handler(
    request: Request,
    exc: Exception
) -> JSONResponse:

    logger.exception(
        "Unhandled error during %s %s",
        request.method,
        request.url.path
    )

    response = ErrorResponse(
        error=ErrorDetail(
            code="INTERNAL_SERVER_ERROR",
            message="An unexpected error occurred"
        )
    )

    return JSONResponse(
        status_code=500,
        content=response.model_dump()
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppError, app_error_handler)
    app.add_exception_handler(
        RequestValidationError,
        validation_error_handler
    )
    app.add_exception_handler(
        StarletteHTTPException,
        http_error_handler
    )
    app.add_exception_handler(
        Exception,
        unexpected_error_handler
    )