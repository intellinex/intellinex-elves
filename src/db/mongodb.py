from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from src.core.config import settings

class Database:
    client: AsyncIOMotorClient = None
    db:AsyncIOMotorDatabase = None

db_instance = Database()

async def connect_to_mongo():
    db_instance.client = AsyncIOMotorClient(settings.MONGODB_URL)
    db_instance.db = db_instance.client[settings.MONGODB_DATABASE]
    print("PRINT: ✅ Connected to MongoDB")

async def close_mongo_connection():
    db_instance.client.close()
    print("PRINT: ❌ Disconnected from MongoDB")

async def get_async_db ():
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.MONGODB_DATABASE]
    try:
        yield db
    finally:
        client.close()