# main.py (project root)
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.db.mongodb import connect_to_mongo, close_mongo_connection
from app.endpoints import hub_endpoints,inventory_endpoint,driver_endpoint ,vehicle_endpoint, vehicle_inventory_endpoints
 
app = FastAPI(title="Smart Inventory - Hub Management")
 

app.include_router(hub_endpoints.router, prefix="/api/hub_mangement", tags=["Hub"])
app.include_router(inventory_endpoint.router, prefix="/api/inventory_mangement")
app.include_router(driver_endpoint.router, prefix="/api/driver_mangement")
app.include_router(vehicle_endpoint.router, prefix="/api/vehicle_mangement")
app.include_router(vehicle_inventory_endpoints.router, prefix="/api/vehicle_inventory")

# Mount static files for CSS and JS
app.mount("/static", StaticFiles(directory="."), name="static")

# Serve CSS and JS files directly
@app.get("/styles.css")
async def get_css():
    return FileResponse("styles.css", media_type="text/css")

@app.get("/script.js")
async def get_js():
    return FileResponse("script.js", media_type="application/javascript")

@app.on_event("startup")
async def startup():
    await connect_to_mongo()


 
@app.on_event("shutdown")
async def shutdown():
    await close_mongo_connection()
 
@app.get("/")
async def root():
    return FileResponse("index.html")

@app.get("/api")
async def api_root():
    return {"message": "Smart Inventory API running"}

@app.get("/api_test.html")
async def get_api_test():
    return FileResponse("api_test.html", media_type="text/html")

@app.get("/test_connection.html")
async def get_test_connection():
    return FileResponse("test_connection.html", media_type="text/html")