from fastapi import FastAPI
from app.service.library_service import router as library_route
from app.service.student_service import router as student_route
from app.service.book_issue_service import router as issue_route
from app.utiles.logger import get_logger


logger = get_logger(__name__)

app = FastAPI (title = "Library Mangement API", version="1.0.0")

app.include_router(library_route,prefix="/api/books", tags=["LibraryMangement"])
app.include_router(student_route,prefix="/api/students", tags=["LibraryMangement"])
app.include_router(issue_route,prefix="/api/issue", tags=["LibraryMangement"])

