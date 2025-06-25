from pydantic import BaseModel
from typing import Optional

class Student(BaseModel):
    student_id: str
    name: str
    branch: str
    year: int

class UpdateStudent(BaseModel):
    student_id: str
    name : Optional[str] = None
    branch : Optional[str] = None
    year : Optional[int] = None

class SearchStudent(BaseModel):
    query : str

class RemoveStudent(BaseModel):
    student_id: str
    name: str