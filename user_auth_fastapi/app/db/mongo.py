from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import MONGO_URI
 
# Create an asynchronous MongoDB client
client = AsyncIOMotorClient(MONGO_URI)
 
# Access the database and collection asynchronously
db = client["user_auth_db"]
user_collection = db["users"]