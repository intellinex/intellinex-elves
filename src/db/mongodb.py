from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from src.core.config import settings

class Database:
    client: AsyncIOMotorClient = None
    db:AsyncIOMotorDatabase = None

db_instance = Database()

async def connect_to_mongo():
    """Connect to MongoDB asynchronously."""
    db_instance.client = AsyncIOMotorClient(settings.MONGODB_URL)
    db_instance.db = db_instance.client[settings.MONGODB_DATABASE]


    print("✅ Connected to MongoDB")

async def close_mongo_connection():
    """Close MongoDB connection."""
    db_instance.client.close()
    print("❌ Disconnected from MongoDB")