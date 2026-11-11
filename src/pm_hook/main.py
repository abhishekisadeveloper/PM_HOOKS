# from fastapi import FastAPI

# from pm_hook.api.routes import chat


# app = FastAPI(
#     title="PM Hooks API",
#     description="Backend API for PM Hooks",
#     version="0.1.0"
# )


# app.include_router(chat.router)


from fastapi import FastAPI

from pm_hook.api.routes import chat
from pm_hook.api.exception_handlers import register_exception_handlers
from pm_hook.core.config import get_settings
from pm_hook.core.logging_config import configure_logging


def create_app() -> FastAPI:
    settings = get_settings()

    configure_logging(settings.debug)

    application = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug
    )

    application.include_router(chat.router)

    register_exception_handlers(application)

    return application


app = create_app()