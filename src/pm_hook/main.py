from fastapi import FastAPI

from pm_hook.api.routes import chat


app = FastAPI(
    title="PM Hooks API",
    description="Backend API for PM Hooks",
    version="0.1.0"
)


app.include_router(chat.router)