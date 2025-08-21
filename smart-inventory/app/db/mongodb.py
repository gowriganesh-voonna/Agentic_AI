from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import (
    MONGO_URI,MONGO_DB
)

from typing import Optional
from app.utiles.logger import get_logger

logger = get_logger(__name__)

client: Optional[AsyncIOMotorClient] = None

db = None

async def connect_to_mongo():
    global client,db
    client = AsyncIOMotorClient(MONGO_URI)
    db= client[MONGO_DB]

    # ensures indexes (callers can await )
    await ensure_indexes()
    logger.info("MongoDB connection established")

async def close_mongo_connection():
    global client
    if client:
        client.close()
        logger.warning("MongoDB connection closed")

async def ensure_indexes():

    #create unquie indexes for hub_id and Hub_name and a non-unquie index for status
    await db["Hubs"].create_index("hub_id",unique = True)
    await db["Hubs"].create_index("hub_name", unique = True)

    #We cannot a partial unique index on hub_manger across active docs in all deployements,
    # but we create a compound index to help queries and enforce uniqueness at service-level.
    await db["Hubs"].create_index("hub_manger")
    await db["ClosedHubs"].create_index("hub_id",unique = True)
