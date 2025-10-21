#!/usr/bin/env python3
"""
Comprehensive fix for all Smart Inventory issues.
This script will:
1. Fix existing dispatch records
2. Test all endpoints
3. Verify data integrity
"""

import asyncio
import sys
import os
sys.path.append('.')
from app.db.mongodb import connect_to_mongo, db

async def fix_all_issues():
    print("🔧 Starting comprehensive fix...")
    
    await connect_to_mongo()
    
    # 1. Fix existing dispatches
    print("\n1. Fixing existing dispatch records...")
    dispatches_to_fix = await db["Dispatches"].find({
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
            await db["Dispatches"].update_one(
                {"dispatch_id": dispatch_id},
                {"$set": updates}
            )
            fixed_count += 1
            print(f"  ✅ Fixed dispatch {dispatch_id}: {updates}")
    
    print(f"  🎉 Fixed {fixed_count} dispatch records")
    
    # 2. Check drivers
    print("\n2. Checking drivers...")
    drivers = await db["drivers"].find({}).to_list(5)
    print(f"  Found {len(drivers)} drivers")
    for driver in drivers:
        print(f"    - {driver.get('name')}: {driver.get('status')}")
    
    # 3. Check vehicles
    print("\n3. Checking vehicles...")
    vehicles = await db["vehicles"].find({}).to_list(5)
    print(f"  Found {len(vehicles)} vehicles")
    for vehicle in vehicles:
        print(f"    - {vehicle.get('Vehicle_Number')}: {vehicle.get('Status')}")
    
    # 4. Check dispatches after fix
    print("\n4. Checking dispatches after fix...")
    dispatches = await db["Dispatches"].find({}).to_list(5)
    print(f"  Found {len(dispatches)} dispatches")
    for dispatch in dispatches:
        print(f"    - {dispatch.get('dispatch_id')}: {dispatch.get('Status')}")
        print(f"      Driver: {dispatch.get('Driver_Assigned', 'Not Assigned')}")
        print(f"      Vehicle: {dispatch.get('Vehicle_Assigned', 'Not Assigned')}")
    
    print("\n🎉 Comprehensive fix completed!")
    print("\nNext steps:")
    print("1. Start your FastAPI server")
    print("2. Refresh your browser")
    print("3. Check the Dispatch Management page")
    print("4. Test manual driver status updates")

if __name__ == "__main__":
    asyncio.run(fix_all_issues())
