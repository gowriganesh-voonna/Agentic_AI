# app/services/vehicle_inventory_service.py

from app.utiles.logger import get_logger
from fastapi import HTTPException
from datetime import datetime
from typing import Dict, Any
from app.db.mongodb import db
from app.utiles.custom_helpers import _now_utc, _gen_transaction_id   


# Collection names (centralized for consistency)
COL_DISPATCHES = "Dispatches"
COL_INV_BATCHES = "InventoryBatches"
COL_STOCK_TX = "StockTransactions"
COL_VEHICLES = "vehicles"
COL_DRIVERS = "drivers"

# Configure logger
logger = get_logger(__name__)

async def mark_dispatch_received_service(dispatch_id: str) -> Dict[str, Any]:
    """
    Marks a dispatch as received at the destination hub:
    - Updates stock in the destination hub.
    - Records stock IN transaction.
    - Resets driver and vehicle availability.
    - Updates dispatch record as Completed.
    """

    logger.info(f"Processing received dispatch: {dispatch_id}")

    # 1. Fetch dispatch
    dispatch = await db[COL_DISPATCHES].find_one({"dispatch_id": dispatch_id})
    if not dispatch:
        logger.error(f"Dispatch {dispatch_id} not found")
        raise HTTPException(status_code=404, detail="Dispatch not found")

    if dispatch["Status"] != "In-Transit":
        logger.warning(f"Dispatch {dispatch_id} is not in transit. Current status: {dispatch['Status']}")
        raise HTTPException(status_code=400, detail="Dispatch is not in-transit")

    now = _now_utc()
    product_id = dispatch["Product_ID"]
    to_hub = dispatch["To_Hub_ID"]

    logger.info(f"Updating inventory at destination hub {to_hub} for product {product_id}")

    # 2. Update inventory at destination hub
    for batch in dispatch["Batch_Consumption"]:
        qty = batch["Qty"]
        unit_cost = batch["Unit_Cost"]
        batch_no = batch["Batch_No"]

        logger.debug(f"Processing batch {batch_no}: Qty={qty}, Unit_Cost={unit_cost}")

        # Insert stock transaction (IN)
        txn = {
            "transaction_id": _gen_transaction_id(),
            "type": "IN",
            "Product_ID": product_id,
            "Hub_ID": to_hub,
            "Batch_No": batch_no,  # keep same batch number
            "Quantity": qty,
            "Unit_Price": unit_cost,
            "Total_Value": float(unit_cost * qty),
            "reference": dispatch_id,
            "timestamp": now,
            "remarks": f"Received from {dispatch['From_Hub_ID']}"
        }
        await db[COL_STOCK_TX].insert_one(txn)
        logger.debug(f"Stock transaction inserted for batch {batch_no}")

        # Upsert into inventory batches at destination hub
        await db[COL_INV_BATCHES].update_one(
            {"Product_ID": product_id, "Hub_ID": to_hub, "Batch_No": batch_no},
            {"$inc": {"Quantity": qty}, "$set": {"status": "active", "last_updated": now}},
            upsert=True
        )
        logger.debug(f"Batch {batch_no} updated in InventoryBatches for hub {to_hub}")

    # 3. Reset driver & vehicle
    await db[COL_DRIVERS].update_one(
        {"driver_id": dispatch["Driver_Assigned"]},
        {"$set": {"status": "active"}}
    )
    logger.info(f"Driver {dispatch['Driver_Assigned']} reset to active")

    await db[COL_VEHICLES].update_one(
        {"Vehicle_ID": dispatch["Vehicle_Assigned"]},
        {"$set": {"Status": "Available"}}
    )
    logger.info(f"Vehicle {dispatch['Vehicle_Assigned']} reset to Available")

    # 4. Update dispatch record
    await db[COL_DISPATCHES].update_one(
        {"dispatch_id": dispatch_id},
        {"$set": {"Status": "Completed", "Arrival_Time": now}}
    )
    logger.info(f"Dispatch {dispatch_id} marked as Completed at {to_hub}")

    return {
        "message": f"Dispatch {dispatch_id} received at {to_hub} and inventory updated",
        "dispatch_id": dispatch_id,
        "status": "Completed",
        "hub": to_hub,
        "arrival_time": now
    }


async def get_dispatch_status_service(dispatch_id: str) -> Dict[str, Any]:
    """
    Returns a user-friendly status for a dispatch with availability details for
    driver and vehicle so the UI can render precise messages before assignment.
    """
    # Fetch dispatch
    dispatch = await db[COL_DISPATCHES].find_one({"dispatch_id": dispatch_id})
    if not dispatch:
        raise HTTPException(status_code=404, detail="Dispatch not found")

    # Current assignment info
    driver_assigned = dispatch.get("Driver_Assigned")
    vehicle_assigned = dispatch.get("Vehicle_Assigned")

    # Availability (is there at least one available?)
    driver_available_doc = await db[COL_DRIVERS].find_one({"status": "active"})
    vehicle_available_doc = await db[COL_VEHICLES].find_one({"Status": "Available"})
    driver_available = driver_available_doc is not None
    vehicle_available = vehicle_available_doc is not None

    # Build user-facing messages
    messages = []
    status_label = dispatch.get("Status", "In-Progress")

    if status_label == "In-Progress":
        # Nothing assigned yet or partial assignment
        if not driver_assigned or driver_assigned == "In-Progress":
            if driver_available:
                messages.append("Driver available and will be assigned shortly")
            else:
                messages.append("Driver not available, will be assigned shortly")
        else:
            messages.append(f"Driver assigned: {driver_assigned}")

        if not vehicle_assigned or vehicle_assigned == "In-Progress":
            if vehicle_available:
                messages.append("Vehicle available and will be assigned shortly")
            else:
                messages.append("Vehicle not available, will be assigned shortly")
        else:
            messages.append(f"Vehicle assigned: {vehicle_assigned}")

        if (
            (driver_assigned and driver_assigned != "In-Progress") and
            (vehicle_assigned and vehicle_assigned != "In-Progress")
        ):
            computed_status = "In-Transit"
        elif (
            (driver_assigned and driver_assigned != "In-Progress") or
            (vehicle_assigned and vehicle_assigned != "In-Progress")
        ):
            computed_status = "Partially Assigned"
        else:
            computed_status = "Pending Assignment"

    elif status_label == "In-Transit":
        computed_status = "In-Transit"
        messages.append("Dispatch is in transit")
        if driver_assigned and driver_assigned != "In-Progress":
            messages.append(f"Driver: {driver_assigned}")
        if vehicle_assigned and vehicle_assigned != "In-Progress":
            messages.append(f"Vehicle: {vehicle_assigned}")

    elif status_label == "Completed":
        computed_status = "Completed"
        messages.append("Dispatch completed")
    else:
        computed_status = status_label
        messages.append(f"Status: {status_label}")

    return {
        "dispatch_id": dispatch_id,
        "status": computed_status,
        "driver_available": driver_available,
        "vehicle_available": vehicle_available,
        "driver_assigned": None if driver_assigned in (None, "In-Progress") else driver_assigned,
        "vehicle_assigned": None if vehicle_assigned in (None, "In-Progress") else vehicle_assigned,
        "messages": messages,
    }


async def list_dispatches_service(skip: int = 0, limit: int = 50) -> Dict[str, Any]:
    """
    List all dispatches with their current status and assignment details.
    """
    logger.info(f"Listing dispatches: skip={skip}, limit={limit}")
    
    # Get dispatches sorted by timestamp (newest first)
    cursor = db[COL_DISPATCHES].find({}).sort("Timestamp", -1).skip(skip).limit(limit)
    dispatches = []
    
    async for dispatch in cursor:
        # Get driver and vehicle names if assigned
        driver_name = "Not Assigned"
        vehicle_name = "Not Assigned"
        
        if dispatch.get("Driver_Assigned") and dispatch["Driver_Assigned"] != "In-Progress":
            driver_doc = await db[COL_DRIVERS].find_one({"driver_id": dispatch["Driver_Assigned"]})
            if driver_doc:
                driver_name = driver_doc.get("name", dispatch["Driver_Assigned"])
        
        if dispatch.get("Vehicle_Assigned") and dispatch["Vehicle_Assigned"] != "In-Progress":
            vehicle_doc = await db[COL_VEHICLES].find_one({"Vehicle_ID": dispatch["Vehicle_Assigned"]})
            if vehicle_doc:
                vehicle_name = vehicle_doc.get("Vehicle_Number", dispatch["Vehicle_Assigned"])
        
        # Format dispatch for UI
        dispatch_info = {
            "dispatch_id": dispatch["dispatch_id"],
            "product_id": dispatch["Product_ID"],
            "from_hub": dispatch["From_Hub_ID"],
            "to_hub": dispatch["To_Hub_ID"],
            "quantity": dispatch["Quantity"],
            "status": dispatch["Status"],
            "driver_assigned": driver_name,
            "vehicle_assigned": vehicle_name,
            "timestamp": dispatch["Timestamp"]
        }
        dispatches.append(dispatch_info)
    
    logger.info(f"Found {len(dispatches)} dispatches")
    return {"dispatches": dispatches}


async def auto_assign_driver_vehicle_service(dispatch_id: str) -> Dict[str, Any]:
    """
    Automatically assign available driver and vehicle to a dispatch.
    This should be called after dispatch creation to assign resources.
    """
    logger.info(f"Auto-assigning driver and vehicle for dispatch: {dispatch_id}")
    
    # Find the dispatch
    dispatch = await db[COL_DISPATCHES].find_one({"dispatch_id": dispatch_id})
    if not dispatch:
        raise HTTPException(status_code=404, detail="Dispatch not found")
    
    if dispatch["Status"] != "In-Progress":
        logger.warning(f"Dispatch {dispatch_id} is not in progress, current status: {dispatch['Status']}")
        return {"message": f"Dispatch is not in progress, current status: {dispatch['Status']}"}
    
    # Find available driver
    driver = await db[COL_DRIVERS].find_one({"status": "active"})
    if not driver:
        logger.warning(f"No available driver for dispatch {dispatch_id}")
        return {"message": "No driver available, will be assigned when available"}
    
    # Find available vehicle
    vehicle = await db[COL_VEHICLES].find_one({"Status": "Available"})
    if not vehicle:
        logger.warning(f"No available vehicle for dispatch {dispatch_id}")
        return {"message": "No vehicle available, will be assigned when available"}
    
    # Assign driver and vehicle
    await db[COL_DRIVERS].update_one(
        {"driver_id": driver["driver_id"]}, 
        {"$set": {"status": "Assigned"}}
    )
    await db[COL_VEHICLES].update_one(
        {"Vehicle_ID": vehicle["Vehicle_ID"]}, 
        {"$set": {"Status": "In-Transit"}}
    )
    await db[COL_DISPATCHES].update_one(
        {"dispatch_id": dispatch_id},
        {"$set": {
            "Status": "In-Transit",
            "Driver_Assigned": driver["driver_id"],
            "Vehicle_Assigned": vehicle["Vehicle_ID"]
        }}
    )
    
    logger.info(f"Auto-assigned: Driver={driver['name']}, Vehicle={vehicle['Vehicle_Number']}")
    return {
        "message": f"Driver {driver['name']} and Vehicle {vehicle['Vehicle_Number']} assigned successfully",
        "driver_assigned": driver["name"],
        "vehicle_assigned": vehicle["Vehicle_Number"]
    }

async def fix_existing_dispatches_service() -> Dict[str, Any]:
    """
    Fix existing dispatch records that have "In-Progress" values.
    This is a one-time fix for existing data.
    """
    logger.info("Fixing existing dispatch records...")
    
    # Get all dispatches with "In-Progress" values
    dispatches_to_fix = await db[COL_DISPATCHES].find({
        "$or": [
            {"Driver_Assigned": "In-Progress"},
            {"Vehicle_Assigned": "In-Progress"}
        ]
    }).to_list(None)
    
    fixed_count = 0
    
    for dispatch in dispatches_to_fix:
        dispatch_id = dispatch["dispatch_id"]
        updates = {}
        
        # Fix "In-Progress" values to None
        if dispatch.get("Driver_Assigned") == "In-Progress":
            updates["Driver_Assigned"] = None
            
        if dispatch.get("Vehicle_Assigned") == "In-Progress":
            updates["Vehicle_Assigned"] = None
        
        # Update status based on actual assignments
        if dispatch.get("Status") == "In-Progress":
            driver_assigned = dispatch.get("Driver_Assigned")
            vehicle_assigned = dispatch.get("Vehicle_Assigned")
            
            if (driver_assigned and driver_assigned != "In-Progress" and 
                vehicle_assigned and vehicle_assigned != "In-Progress"):
                updates["Status"] = "In-Transit"
            else:
                updates["Status"] = "Pending Assignment"
        
        # Apply updates
        if updates:
            await db[COL_DISPATCHES].update_one(
                {"dispatch_id": dispatch_id},
                {"$set": updates}
            )
            fixed_count += 1
            logger.info(f"Fixed dispatch {dispatch_id}: {updates}")
    
    logger.info(f"Fixed {fixed_count} dispatch records")
    return {
        "message": f"Fixed {fixed_count} dispatch records",
        "fixed_count": fixed_count
    }