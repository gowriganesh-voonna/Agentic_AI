from datetime import datetime, timedelta
from app.db.mongo import db
from bson.objectid import ObjectId
 
session_collection = db["user_sessions"]
 
SESSION_DURATION_MINUTES = 60
 
async def store_token(email: str, token: str):
    # Remove existing session if any
    await session_collection.delete_many({"email": email})
 
    # Store new session
    await session_collection.insert_one({
        "email": email,
        "token": token,
        "created_at": datetime.utcnow(),
        "expires_at": datetime.utcnow() + timedelta(minutes=SESSION_DURATION_MINUTES)
    })
 
async def is_token_active(token: str) -> bool:
    session = await session_collection.find_one({"token": token})
    if not session:
        return False
    if datetime.utcnow() > session["expires_at"]:
        await session_collection.delete_one({"_id": session["_id"]})
        return False
    return True
 
async def remove_token(email: str):
    await session_collection.delete_many({"email": email})
 