from pydantic import BaseModel

class Student(BaseModel):
    student_id: str
    name: str
    branch: str
    year: int