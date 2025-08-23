# endpoints/driver_endpoints.py

from fastapi import APIRouter, HTTPException
from typing import List, Optional
from app.models.driver import DriverCreate, DriverUpdate, DriverOut, DriverIdRequest
from app.services import driver_service

router = APIRouter(prefix="/drivers", tags=["Drivers"])


# Create
@router.post("/register_driver", response_model=DriverOut)
async def create_driver(driver: DriverCreate):
    return await driver_service.create_driver(driver)


# Get by ID
@router.get("/get_driver_by_id", response_model=DriverOut)
async def get_driver(payload : DriverIdRequest):
    driver = await driver_service.get_driver_by_id(payload.driver_id)
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    return driver


# Search
@router.get("/search_driver", response_model=List[DriverOut])
async def search_drivers(
    name: Optional[str] = None,
    license_number: Optional[str] = None,
    status: Optional[str] = None,
    hub_id: Optional[str] = None,
    limit: int = 10,
    skip: int = 0
):
    return await driver_service.search_drivers(name, license_number, status, hub_id, limit, skip)


# Update
@router.put("/update_driver", response_model=DriverOut)
async def update_driver(driver: DriverUpdate):
    updated = await driver_service.update_driver(driver)
    if not updated:
        raise HTTPException(status_code=404, detail="Driver not found or deleted")
    return updated


# Delete
@router.delete("/delete_driver")
async def delete_driver(payload : DriverIdRequest):
    success = await driver_service.delete_driver(payload.driver_id)
    if not success:
        raise HTTPException(status_code=404, detail="Driver not found or already deleted")
    return {"message": "Driver deleted successfully"}


# Retirement Audit
@router.post("/retire-audit")
async def retire_audit():
    count = await driver_service.retire_old_drivers()
    return {"retired_count": count}
