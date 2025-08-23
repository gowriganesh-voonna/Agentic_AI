from fastapi import APIRouter
from app.models.vehicle import VehicleCreate, VehicleUpdate, VehicleDelete
from app.services.vehicle_service import (
    add_vehicle_service,
    update_vehicle_service,
    delete_vehicle_service,
    search_vehicle_service,
    dispatch_vehicle_service
)

router = APIRouter(prefix="/vehicles", tags=["Vehicle Management"])

@router.post("/register_vehicle", response_model=dict)
async def Register_vehicle(vehicle: VehicleCreate):
    return await add_vehicle_service(vehicle)

@router.put("/update_vehicle", response_model=dict)
async def update_vehicle(update: VehicleUpdate):
    return await update_vehicle_service(update)

@router.delete("/delete_vehicle", response_model=dict)
async def delete_vehicle(req: VehicleDelete):
    return await delete_vehicle_service(req)

@router.get("/search_vehicle", response_model=dict)
async def search_vehicle(Vehicle_ID: str = None, Vehicle_Number: str = None, Status: str = None):
    return await search_vehicle_service(Vehicle_ID, Vehicle_Number, Status)

@router.get("/dispatch_vehicle", response_model=dict)
async def dispatch_vehicle():
    return await dispatch_vehicle_service()
