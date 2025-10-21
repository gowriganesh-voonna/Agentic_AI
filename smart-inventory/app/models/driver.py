from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import date,datetime
from uuid import uuid4,UUID

# ---------------------------
# Driver Base Schema
# ---------------------------
class DriverBase(BaseModel):
    name: str = Field(..., description="Full name of the driver")
    age: int = Field(..., ge=18, le=70, description="Driver age")
    license_number: str = Field(..., description="Unique driver license number")
    hub_id: str = Field(..., description="Assigned Hub ID")
    # Allow transient states used by dispatch assignment
    status: Literal["active", "retired", "deleted", "Inactive", "Assigned"] = "active"
    retirement_reason: Optional[str] = None

# ---------------------------
# Create Schema
# ---------------------------
class DriverCreate(DriverBase):
    driver_id: str = Field(default_factory=lambda: str(uuid4()))

class DriverIdRequest(BaseModel):
    driver_id: UUID

# ---------------------------
# Update Schema
# ---------------------------
class DriverUpdate(BaseModel):
    driver_id: str  # Changed from UUID to str to match frontend
    name: Optional[str] = None
    age: Optional[int] = None
    license_number: Optional[str] = None
    hub_id: Optional[str] = None
    # Keep allowed set in sync with DriverBase.status
    status: Optional[Literal["active", "retired", "deleted", "Inactive", "Assigned"]] = None
    retirement_reason: Optional[str] = None
 
# ---------------------------
# DB Schema
# ---------------------------
class DriverInDB(DriverCreate):
    created_at: date = Field(default_factory=date.today)

# Output schema
class DriverOut(BaseModel):
    driver_id: str  # Changed from UUID to str to match database
    name: str
    license_number: str
    age: int
    hub_id: str
    status: str
    reason: Optional[str] = None
    created_at: datetime
    updated_at: datetime
