from motor.motor_asyncio import AsyncIOMotorClient
import os
import time

def get_db():
    mongo_url = os.getenv(
        "MONGO_URL",
        "mongodb://mongo-raw-ingestion:27017/admin"
    )

    for _ in range(10):
        try:
            print("MONGO URL:", mongo_url)

            client = AsyncIOMotorClient(
                mongo_url,
                serverSelectionTimeoutMS=2000
            )

            client.server_info()  # force connection check

            print("Mongo connected")
            return client["telemetry_db"]

        except Exception as e:
            print("Mongo not ready, retrying...", e)
            time.sleep(2)

    raise Exception("Failed to connect to MongoDB after 10 retries")

db = get_db()
