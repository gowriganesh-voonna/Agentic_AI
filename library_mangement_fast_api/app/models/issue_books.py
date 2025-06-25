from pydantic import BaseModel
from typing import Optional

class IssueBook(BaseModel):
    student_id : str
    book_id : str

class ReturnBook(BaseModel):
    student_id : str
    book_id : str