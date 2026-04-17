from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb://endri_admin:secure_password_123@localhost:27017/?authSource=admin"

client = AsyncIOMotorClient(MONGO_URL)

db = client["telemetry_db"]