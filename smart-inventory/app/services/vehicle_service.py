from datetime import datetime
from fastapi import HTTPException
from app.db.mongodb import db
from app.models.vehicle import VehicleCreate, VehicleUpdate, VehicleDelete

# Allowed statuses
VALID_STATUSES = ["Available", "Unavailable", "In-Transit", "Under-Maintenance"]

# ---------------- Service: Add Vehicle ----------------
async def add_vehicle_service(vehicle: VehicleCreate):
    exists = await db["vehicles"].find_one({
        "$or": [
            {"Vehicle_ID": vehicle.Vehicle_ID},
            {"Vehicle_Number": vehicle.Vehicle_Number}
        ]
    })
    if exists:
        raise HTTPException(status_code=409, detail="Vehicle_ID or Vehicle_Number already exists")

    doc = vehicle.dict()
    doc["created_at"] = datetime.utcnow()
    doc["updated_at"] = datetime.utcnow()
    await db["vehicles"].insert_one(doc)
    return {"status": "success", "message": "Vehicle registered successfully"}

# ---------------- Service: Update Vehicle ----------------
async def update_vehicle_service(update: VehicleUpdate):
    if update.Status and update.Status not in VALID_STATUSES:
        raise HTTPException(status_code=400, detail=f"Invalid Status. Allowed: {VALID_STATUSES}")

    result = await db["vehicles"].find_one_and_update(
        {"Vehicle_ID": update.Vehicle_ID},
        {"$set": {**update.dict(exclude_unset=True), "updated_at": datetime.utcnow()}},
    )
    if not result:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    return {"status": "success", "message": "Vehicle status updated"}

# ---------------- Service: Delete Vehicle ----------------
async def delete_vehicle_service(req: VehicleDelete):
    vehicle = await db["vehicles"].find_one({
        "Vehicle_ID": req.Vehicle_ID, "Vehicle_Number": req.Vehicle_Number
    })
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    vehicle["Closed_Date"] = datetime.utcnow()
    await db["ClosedVehicles"].insert_one(vehicle)
    await db["vehicles"].delete_one({"_id": vehicle["_id"]})

    return {"message": f"Vehicle {req.Vehicle_Number} deleted successfully"}

# ---------------- Service: Search Vehicle ----------------
async def search_vehicle_service(Vehicle_ID: str = None, Vehicle_Number: str = None, Status: str = None):
    query = {}
    if Vehicle_ID: query["Vehicle_ID"] = Vehicle_ID
    if Vehicle_Number: query["Vehicle_Number"] = Vehicle_Number
    if Status: query["Status"] = Status

    if not query:
        raise HTTPException(status_code=400, detail="No search criteria provided")

    #vehicles = await db["vehicles"].find(query).to_list(100)
    vehicles = await db["vehicles"].find(query, {"_id": 0}).to_list(100)
    return {"Available_Vehicles": vehicles}

# ---------------- Service: Dispatch Vehicle ----------------
async def dispatch_vehicle_service():
    dispatch = await db["Dispatches"].find_one({"Status": "In-Progress"})
    if not dispatch:
        return {"message": "No need to dispatch vehicle"}

    driver = await db["drivers"].find_one({"status": "active"})
    if not driver:
        return {"message": "Load is available for Dispatch but no driver available"}

    vehicle = await db["vehicles"].find_one({"Status": "Available"})
    if not vehicle:
        return {"message": "Load is available for Dispatch but no vehicle available"}

    await db["drivers"].update_one({"driver_id": driver["driver_id"]}, {"$set": {"status": "Assigned"}})
    await db["vehicles"].update_one({"Vehicle_ID": vehicle["Vehicle_ID"]}, {"$set": {"Status": "In-Transit"}})
    await db["Dispatches"].update_one(
        {"_id": dispatch["_id"]},
        {"$set": {
            "Status": "In-Transit",
            "Driver_Assigned": driver["driver_id"],
            "Vehicle_Assigned": vehicle["Vehicle_ID"]
        }}
    )

    return {"message": f"Vehicle {vehicle['Vehicle_ID']} and Driver {driver['name']} assigned successfully"}
