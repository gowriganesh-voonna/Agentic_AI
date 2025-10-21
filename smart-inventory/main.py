# main.py - Smart Inventory Backend API
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.db.mongodb import connect_to_mongo, close_mongo_connection
from app.endpoints import hub_endpoints, inventory_endpoint, driver_endpoint, vehicle_endpoint, vehicle_inventory_endpoints

app = FastAPI(
    title="Smart Inventory & Dispatch Management API",
    description="Backend API for Smart Inventory and Dispatch Management System",
    version="1.0.0"
)

# Add CORS middleware for API access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(hub_endpoints.router, prefix="/api/hub_mangement", tags=["Hub Management"])
app.include_router(inventory_endpoint.router, prefix="/api/inventory_mangement", tags=["Inventory Management"])
app.include_router(driver_endpoint.router, prefix="/api/driver_mangement", tags=["Driver Management"])
app.include_router(vehicle_endpoint.router, prefix="/api/vehicle_mangement", tags=["Vehicle Management"])
app.include_router(vehicle_inventory_endpoints.router, prefix="/api/vehicle_inventory", tags=["Vehicle Inventory & Dispatch"])

@app.on_event("startup")
async def startup():
    try:
        await connect_to_mongo()
        print("✅ Database connected successfully")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")

@app.on_event("shutdown")
async def shutdown():
    try:
        await close_mongo_connection()
        print("✅ Database connection closed")
    except Exception as e:
        print(f"❌ Error closing database connection: {e}")

@app.get("/")
async def root():
    return {
        "message": "Smart Inventory & Dispatch Management API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/api")
async def api_root():
    return {"message": "Smart Inventory API running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)