import asyncio
import re
import logging
from aiomqtt import Client
from core.fsm import TelemetryFSM
from db.mongodb import db

print("SUBSCRIBER STARTED")

TOPIC_REGEX = r"^telemetry\/[a-zA-Z0-9_-]+\/[a-zA-Z0-9_-]+\/[a-zA-Z0-9_-]+$"
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mqtt")

BROKER = "mosquitto-broker"  # can be changed later
PORT = 1883
FLUSH_INTERVAL = 5
BATCH_SIZE = 10

queue = asyncio.Queue()
dlq = asyncio.Queue()

async def mqtt_worker():

    print("MQTT WORKER STARTED")

    while True:
        try:
            async with Client(BROKER, PORT) as client:
                logger.info("MQTT CONNECTED")
                await client.subscribe("telemetry/+/+/+")
                logger.info("SUBSCRIBED")

                async for msg in client.messages:
                    topic = str(msg.topic)
                    
                    if not re.match(TOPIC_REGEX, topic):
                        logger.warning("Invalid topic: %s", topic)
                        continue

                    fsm = TelemetryFSM()

                    logger.info("Processing message from topic: %s", topic)
                    payload = fsm.parse(msg.payload.decode())
                    if payload is None:
                        logger.error("Invalid payload format")
                        await dlq.put(msg.payload.decode())
                        continue

                    topic_parts = topic.split("/")
                    if len(topic_parts) < 3:
                        logger.warning("Malformed topic: %s", topic)
                        continue
                    payload["device_id"] = topic_parts[2]
                    if not fsm.validate(payload):
                        logger.warning("Rejected: %s", payload)
                        await dlq.put(payload)
                        continue
                    if not fsm.accept():
                        logger.info("Not accepted: %s", payload)
                        await dlq.put(payload)
                        continue
                    data = {
                        "device_id": str(payload["device_id"]),
                        "value": float(payload["value"])
                    }
                    await queue.put(data)
                    logger.info("Queued: %s", data)
        except Exception as e:
            logger.error(f"MQTT DISCONNECTED → reconnecting in 3s: {e}")
            await asyncio.sleep(3)  # wait before retrying

async def db_writer():
    while True:
        await asyncio.sleep(FLUSH_INTERVAL)

        batch = []

        while not queue.empty() and len(batch) < BATCH_SIZE:
            batch.append(await queue.get())

        if not batch:
            continue

        try:
            result = await db.telemetry.insert_many(batch)
            logger.info(f"BATCH INSERTED: {len(batch)}")

        except Exception as e:
            logger.error("DB insert failed: %s", e)

async def dlq_worker():
    while True:
        item = await dlq.get()
        logger.error(f"DLQ STORE: {item}")
        
async def main():
    print("MQTT MAIN ENTERED")
    try:
        await asyncio.gather(
            mqtt_worker(),
            db_writer(),
            dlq_worker()
        )
    except Exception as e:
        logger.error(f"MQTT MAIN CRASHED: {e}")

if __name__ == "__main__":
    asyncio.run(main())