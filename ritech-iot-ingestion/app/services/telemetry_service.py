from datetime import datetime, timedelta
from ..db.mongodb import db


BUCKET_SIZE_SECONDS = 60


def get_bucket_time(now: datetime):
    bucket_start = now.replace(second=0, microsecond=0)
    bucket_end = bucket_start + timedelta(seconds=BUCKET_SIZE_SECONDS)
    return bucket_start, bucket_end


async def create_telemetry(data):

    print("INSERT CALLED", data.dict())

    MAX_BUCKET_SIZE = 5

    now = datetime.utcnow()
    bucket_start, bucket_end = get_bucket_time(now)

    reading = {
        "ts": now,
        "value": data.value
    }

    query = {
        "device_id": data.device_id,
        "bucket_start": bucket_start
    }
    
    existing_bucket = await db.telemetry.find_one(query)

    if existing_bucket and len(existing_bucket.get("readings", [])) >= MAX_BUCKET_SIZE:
    # force new bucket by shifting time
      now = datetime.utcnow()
      bucket_start, bucket_end = get_bucket_time(now + timedelta(seconds=60))

    query = {
        "device_id": data.device_id,
        "bucket_start": bucket_start
    }

    update = {
        "$setOnInsert": {
            "device_id": data.device_id,
            "bucket_start": bucket_start,
            "bucket_end": bucket_end,
            #"readings": []
            },
        "$push": {
            "readings": reading
        }
    }

    result = await db.telemetry.update_one(
        query,
        update,
        upsert=True
    )

    print("BUCKET UPDATED")

    return {
        "status": "ok",
        "device_id": data.device_id
    }
