from app.db.mongodb import db
from app.db.postgres import get_pool


async def get_stats() -> dict:
    total = await db.telemetry.count_documents({})

    pipeline = [{"$group": {"_id": "$raw_payload.value type", "count": {"$sum": 1}}}]
    by_type_raw = await db.telemetry.aggregate(pipeline).to_list(None)
    by_type = {row["_id"]: row["count"] for row in by_type_raw if row["_id"]}

    device_count = len(await db.telemetry.distinct("device_id"))

    pg_total = 0
    try:
        pool = await get_pool()
        pg_total = await pool.fetchval("SELECT COUNT(*) FROM iot.telemetry_data") or 0
    except Exception:
        pass

    return {
        "total_messages": total,
        "device_count": device_count,
        "by_sensor_type": by_type,
        "postgres_total": int(pg_total),
    }


async def get_recent(limit: int = 20) -> list:
    cursor = db.telemetry.find(
        {},
        {"_id": 0, "device_id": 1, "arrival_timestamp": 1, "raw_payload": 1},
    ).sort("arrival_timestamp", -1).limit(limit)

    docs = await cursor.to_list(None)
    return [
        {
            "device_id": d["device_id"],
            "sensor_type": d.get("raw_payload", {}).get("value type"),
            "value": d.get("raw_payload", {}).get("value"),
            "normalized": round(d.get("raw_payload", {}).get("normalized", 0), 4),
            "timestamp": d["arrival_timestamp"].isoformat(),
        }
        for d in docs
    ]
