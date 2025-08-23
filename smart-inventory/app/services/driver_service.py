# services/driver_service.py
from pymongo import ReturnDocument
from datetime import datetime,UTC
from uuid import uuid4
from typing import List, Optional
from app.models.driver import DriverCreate, DriverUpdate, DriverOut
from app.db.mongodb import db  # your MongoDB/Motor async client
import uuid


# ------------------------
# Create Driver
# ------------------------
async def create_driver(driver: DriverCreate) -> DriverOut:
    driver_id = str(uuid4())
    driver_doc = {
        "driver_id": driver_id,
        "name": driver.name,
        "license_number": driver.license_number,
        "age": driver.age,
        "status": "active",
        "hub_id": driver.hub_id,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "retired_reason": None
    }
    await db.drivers.insert_one(driver_doc)
    return DriverOut(**driver_doc)


# ------------------------
# Get Driver by ID
# ------------------------
async def get_driver_by_id(driver_id: str) -> Optional[DriverOut]:
    doc = await db.drivers.find_one({"driver_id": str(driver_id), "status": {"$ne": "deleted"}})
    if doc:
        return DriverOut(**doc)
    return None


# ------------------------
# Search Drivers
# ------------------------
async def search_drivers(
    name: Optional[str] = None,
    license_number: Optional[str] = None,
    status: Optional[str] = None,
    hub_id: Optional[str] = None,
    limit: int = 10,
    skip: int = 0
) -> List[DriverOut]:
    query = {"status": {"$ne": "deleted"}}
    if name:
        query["name"] = {"$regex": name, "$options": "i"}
    if license_number:
        query["license_number"] = license_number
    if status:
        query["status"] = status
    if hub_id:
        query["hub_id"] = hub_id

    cursor = db.drivers.find(query).skip(skip).limit(limit)
    results = [DriverOut(**doc) async for doc in cursor]
    return results


# ------------------------
# Update Driver
# ------------------------
async def update_driver(driver_update: DriverUpdate) -> Optional[DriverOut]:
    # Convert dict and force UUID → str
    update_data = {}
    for k, v in driver_update.dict(exclude_unset=True).items():
        if isinstance(v, uuid.UUID):  # convert any UUID fields to str
            update_data[k] = str(v)
        else:
            update_data[k] = v
    update_data["updated_at"] = datetime.utcnow()
    driver_id_str = str(driver_update.driver_id)

    result = await db.drivers.find_one_and_update(
        {"driver_id": driver_id_str, "status": {"$ne": "deleted"}},
        {"$set": update_data},
        return_document=ReturnDocument.AFTER
    )
    if result:
        return DriverOut(**result)
    return None


# ------------------------
# Delete Driver (Soft Delete)
# ------------------------
async def delete_driver(driver_id: str) -> bool:
    result = await db.drivers.update_one(
        {"driver_id": str(driver_id), "status": {"$ne": "deleted"}},
        {"$set": {"status": "deleted", "retired_reason": "Deleted", "updated_at": datetime.utcnow()}}
    )
    return result.modified_count > 0


# ------------------------
# Retire Drivers (Batch Audit)
# ------------------------
async def retire_old_drivers() -> int:
    result = await db.drivers.update_many(
        {"age": {"$gt": 50}, "status": "active"},
        {"$set": {"status": "retired", "retired_reason": "Age > 50", "updated_at": datetime.utcnow()}}
    )
    return result.modified_count
