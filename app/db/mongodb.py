from motor.motor_asyncio import AsyncIOMotorClient
import os


_client = None

def get_client():
    global _client

    if _client is None:
        mongo_url = os.environ.get("MONGO_URL")
        if not mongo_url:
            raise RuntimeError("MONGO_URL environment variable is required but not set")
        _client = AsyncIOMotorClient(mongo_url)

    return _client



def get_db():
    client = get_client()
    return client["telemetry_db"]


db = get_db()
