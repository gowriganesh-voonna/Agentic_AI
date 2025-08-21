# mongodb.py
 
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
from app.core.config import MONGO_URI, MONGO_DB
from app.utiles.logger import get_logger
 
logger = get_logger(__name__)
 
# Global client and db instances
# client: Optional[AsyncIOMotorClient] = None
# db = None
client = AsyncIOMotorClient(MONGO_URI)
db = client[MONGO_DB]
 
async def connect_to_mongo():
    """Connect to MongoDB when app starts."""
    global client, db
    
 
    # Ensure indexes are created
    await ensure_indexes()
 
    logger.info("✅ MongoDB connection established")
 
 
async def close_mongo_connection():
    """Close MongoDB connection when app shuts down."""
    global client
    if client:
        client.close()
        logger.warning("⚠️ MongoDB connection closed")
 
 
async def ensure_indexes():
    """Create necessary indexes for collections."""
    # Unique indexes for Hubs
    await db["Hubs"].create_index("hub_id", unique=True)
    await db["Hubs"].create_index("hub_name", unique=True)
 
    # Non-unique index for hub_manager (helps queries)
    await db["Hubs"].create_index("hub_manager")
 
    # Unique index for ClosedHubs hub_id
    await db["ClosedHubs"].create_index("hub_id", unique=True)

    await db["InventoryProducts"].create_index("Product_ID", unique=True)
    await db["InventoryProducts"].create_index([("Product_Name", 1), ("Hub_ID", 1)])
    await db["InventoryBatches"].create_index([("Product_ID", 1), ("Hub_ID", 1), ("Expiry_Date", 1)])
    await db["InventoryBatches"].create_index([("Product_ID", 1), ("Hub_ID", 1), ("Batch_No", 1)], unique=True)
    await db["StockTransactions"].create_index([("Product_ID", 1), ("Hub_ID", 1), ("timestamp", -1)])
    await db["Dispatches"].create_index([("Status", 1), ("Timestamp", -1)])
    
    logger.info("✅ Indexes ensured for Hubs and ClosedHubs collections")
 