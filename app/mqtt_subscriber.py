import asyncio
import aiomqtt
import os
import yappi
from datetime import datetime, timezone
from app.db.mongodb import db
from app.db.postgres import get_pool, close_pool
from app.core.fsm import TelemetryFSM

MQTT_BROKER = os.getenv("MQTT_BROKER", "mosquitto-broker")
MQTT_TOPIC = "telemetry/#"

async def load_sensor_type_ids(pg_pool) -> dict:
    rows = await pg_pool.fetch("SELECT sensor_type_id, sensor_name FROM iot.sensor_types")
    return {row["sensor_name"]: row["sensor_type_id"] for row in rows}

async def ensure_device(pg_pool, device_id: str, seen: set):
    if device_id not in seen:
        await pg_pool.execute(
            "INSERT INTO iot.devices (device_id, status) VALUES ($1, 'active')"
            " ON CONFLICT (device_id) DO NOTHING", device_id,)
        seen.add(device_id)

async def write_to_postgres(pg_pool, obj, sensor_type_ids: dict, seen_devices: set, ts: datetime):
    device_id = obj.get_device_id()
    sensor_type = obj.get_sensor_type()
    sensor_type_id = sensor_type_ids.get(sensor_type)

    if sensor_type_id is None:
        print(f"Unknown sensor type '{sensor_type}', skipping Postgres write")
        return

    await ensure_device(pg_pool, device_id, seen_devices)

    await pg_pool.execute(
        "INSERT INTO iot.telemetry_data (ts, device_id, sensor_type_id, reading_value)"
        " VALUES ($1, $2, $3, $4)",  ts.replace(tzinfo=None), device_id, sensor_type_id, float(obj.get_value()),)

async def listen():
    print("Subscriber started")
    fsm = TelemetryFSM()
    yappi.start()
    message_count = 0

    pg_pool = await get_pool()
    sensor_type_ids = await load_sensor_type_ids(pg_pool)
    seen_devices = set()

    print("Waiting for MQTT messages...")
    try:
        async with aiomqtt.Client(MQTT_BROKER) as client:
            print("Connecting to MQTT broker...")
            await client.subscribe(MQTT_TOPIC)
            print("Connected and subscribed")

            async for message in client.messages:
                message_count += 1
                payload_raw = message.payload.decode()

                print("Message received:", payload_raw)

                obj = fsm.process(payload_raw)
                if not obj:
                    continue

                ts = datetime.now(timezone.utc)

                document = {
                    "device_id": obj.get_device_id(),
                    "arrival_timestamp": ts,
                    "protocol": "MQTT",
                    "raw_payload": {
                        "value type": obj.get_sensor_type(),
                        "value": obj.get_value(),
                        "normalized": obj.normalize()
                    },
                    "validation_status": "accepted"
                }

                await db.telemetry.insert_one(document)

                try:
                    await write_to_postgres(pg_pool, obj, sensor_type_ids, seen_devices, ts)
                except Exception:
                    import traceback
                    print("Postgres write failed:")
                    traceback.print_exc()

                print("Message_Count: ", message_count)
                if message_count >= 500:
                    return

    except aiomqtt.MqttError:
        print("MQTT connection error")
        import traceback
        traceback.print_exc()

    except Exception:
        import traceback
        traceback.print_exc()

    finally:
        await close_pool()
        yappi.stop()
        stats = yappi.get_func_stats()
        stats.sort("tsub")
        print("\n===== CPU PROFILING RESULTS =====")
        stats.print_top(20)

if __name__ == "__main__":
    asyncio.run(listen())
