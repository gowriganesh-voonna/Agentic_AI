from fastapi import FastAPI
from app.services.user_routes import router
from app.db.mongo import blacklist_collection
 
app = FastAPI()

@app.on_event("startup")
async def create_indexes():
    await blacklist_collection.create_index("created_at",expireAfterSeconds=3600)
 
app.include_router(router, prefix="/api/v1", tags=["User Auth"])
 