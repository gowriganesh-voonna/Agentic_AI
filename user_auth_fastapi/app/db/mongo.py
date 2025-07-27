from motor.motor_asyncio import AsyncIOMotorClient
 
MONGO_URI = "mongodb+srv://gowriganeshvoonna:3EhpwdUK0FnSh3YP@resume-data.wz0y1el.mongodb.net/"
 
# Create an asynchronous MongoDB client
client = AsyncIOMotorClient(MONGO_URI)
 
# Access the database and collection asynchronously
db = client["user_auth_db"]
user_collection = db["users"]