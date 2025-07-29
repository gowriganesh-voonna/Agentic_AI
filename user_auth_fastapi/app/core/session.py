from datetime import datetime, timedelta
from app.db.mongo import session_collection, blacklist_collection
from fastapi import HTTPException
from app.utiles.logger import get_logger  # Ensure you have a logger utility
 
logger = get_logger(__name__)
 
# Define session expiry duration (in minutes)
SESSION_EXPIRY_MINUTES = 60
 
# ----------------------------
# Store a new session
# ----------------------------
async def store_session(email: str, username: str, token: str):
    # Remove any old sessions beyond expiry duration
    await session_collection.delete_many({
        "email": email,
        "created_at": {
            "$lt": datetime.utcnow() - timedelta(minutes=SESSION_EXPIRY_MINUTES)
        }
    })
    # Check if an active session already exists
    existing = await session_collection.find_one({"email": email})
    if existing:
        logger.warning(f"Attempted login while active session exists for {email}")
        raise HTTPException(status_code=410, detail="Active session exists. Please logout or wait till it expires.")
    
    session_doc = {
        "email": email,
        "username": username,
        "token": token,
        "created_at": datetime.utcnow(),
        "status": "active"
    }
    await session_collection.insert_one(session_doc)
    logger.info(f"Session created for user {username} with email {email}")
 
# ----------------------------
# Remove session on logout
# ----------------------------
async def remove_session(token: str):
    session = await session_collection.find_one({"token": token})
    if not session:
        logger.warning(f"Logout attempt with invalid or already removed token")
        return "No active session"
 
    # Check if token has expired
    is_expired = datetime.utcnow() > session["created_at"] + timedelta(minutes=SESSION_EXPIRY_MINUTES)
 
    # Remove session and blacklist the token
    await session_collection.delete_one({"token": token})
    await blacklist_collection.insert_one({
        "token": token,
        "created_at": datetime.utcnow()
    })
 
    if is_expired:
        logger.info(f"Expired token removed and blacklisted: {token}")
        return "Session expired"
    else:
        logger.info(f"User {session['username']} logged out successfully")
        return "Logout successful"
 
# ----------------------------
# Validate session before protected endpoints (e.g., update, change password)
# ----------------------------
async def validate_session(token: str):
    # Check if token is blacklisted
    if await blacklist_collection.find_one({"token": token}):
        logger.warning(f"Blacklisted token used: {token}")
        raise HTTPException(status_code=403, detail="Token blacklisted. Please login again.")
 
    # Find active session
    session = await session_collection.find_one({"token": token})
    if not session:
        logger.warning(f"Access attempt without active session for token: {token}")
        raise HTTPException(status_code=404, detail="No active session. Please login.")
 
    # Check if session expired
    if datetime.utcnow() > session["created_at"] + timedelta(minutes=SESSION_EXPIRY_MINUTES):
        await session_collection.update_one(
            {"token": token},
            {"$set": {"status": "expired"}}
        )
        logger.info(f"Session expired for user {session['username']}")
        raise HTTPException(status_code=401, detail="Session expired. Please login again.")
 
