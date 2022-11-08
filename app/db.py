import motor.motor_asyncio
from motor.motor_asyncio import AsyncIOMotorDatabase

from app import config

DB_URL = config.db_url
DB_NAME = config.db_name

client = motor.motor_asyncio.AsyncIOMotorClient(DB_URL)

db: AsyncIOMotorDatabase = client[DB_NAME]

