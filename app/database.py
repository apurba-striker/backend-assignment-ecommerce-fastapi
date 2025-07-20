from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Database:
    client: AsyncIOMotorClient = None
    
db = Database()

async def get_database():
    return db.client[os.getenv("DB_NAME")]

async def connect_to_mongo():
    db.client = AsyncIOMotorClient(os.getenv("MONGODB_URL"))
    
async def close_mongo_connection():
    if db.client:
        db.client.close() 