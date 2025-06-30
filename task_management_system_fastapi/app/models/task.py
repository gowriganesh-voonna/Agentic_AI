from pydantic import BaseModel, Field, validator
from typing import Optional, Literal
from datetime import datetime

# Allowed status and priority values
StatusType = Literal["Pending", "In Progress", "Completed"]
PriorityType = Literal["Low", "Medium", "High"]

class TaskBase(BaseModel):
   
    title: str = Field(..., example="Submit report")
    description: Optional[str] = Field(None, example="Weekly report for client John")
    status: StatusType = Field(..., example="Pending")
    priority: PriorityType = Field(..., example="High")
    deadline: datetime = Field(..., example="2025-07-10T18:00:00")
    assigned_to: Optional[str] = Field(None, example="john_doe")
    # Validator to ensure deadline is in the future
    @validator("deadline")
    def validate_deadline(cls, v: datetime):
        if v < datetime.now():
            raise ValueError("Deadline must be a future date/time.")
        return v


class TaskCreate(TaskBase):
    pass  # Used for creating new tasks


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[StatusType] = None
    priority: Optional[PriorityType] = None
    deadline: Optional[datetime] = None
    assigned_to: Optional[str] = None
    # Deadline validator: only if deadline is provided
    @validator("deadline")
    def validate_deadline(cls, v: datetime):
        if v and v < datetime.now():
            raise ValueError("Deadline must be a future date/time.")
        return v

class Task(TaskBase):
    id : int
    created_at : datetime


class DeleteTask(BaseModel):
    title : str