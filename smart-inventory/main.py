# main.py (project root)
from fastapi import FastAPI
import uvicorn
from app.db.mongodb import connect_to_mongo, close_mongo_connection
from app.endpoints import hub_endpoints
 
app = FastAPI(title="Smart Inventory - Hub Management")
 

app.include_router(hub_endpoints.router, prefix="/api/hub_mangement", tags=["Hub"])

@app.on_event("startup")
async def startup():
    await connect_to_mongo()


 
@app.on_event("shutdown")
async def shutdown():
    await close_mongo_connection()
 
@app.get("/")
async def root():
    return {"message": "Smart Inventory API running"}