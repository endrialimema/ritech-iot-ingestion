from motor.motor_asyncio import AsyncIOMotorClient
import os
import time

def get_db():
    # Fails safely if the environment variable is missing
    mongo_url = os.environ["MONGO_URL"]

    for _ in range(10):
        try:
            client = AsyncIOMotorClient(
                mongo_url,
                serverSelectionTimeoutMS=2000
            )
            client.server_info()
            return client["telemetry_db"]
        except Exception as e:
            time.sleep(2)

    raise Exception("Failed to connect to MongoDB after 10 retries")

db = get_db()
