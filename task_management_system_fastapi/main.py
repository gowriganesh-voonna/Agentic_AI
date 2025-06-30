from fastapi import FastAPI
from app.service.services import router

app = FastAPI(
    title="Task Management System – PoC",
    description="FastAPI app with JSON persistence, logging, and custom error handling",
    version="1.0.0"
)

app.include_router(router,prefix="/api/task")