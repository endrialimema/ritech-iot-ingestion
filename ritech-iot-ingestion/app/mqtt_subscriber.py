import asyncio
import aiomqtt
import os
from datetime import datetime, timezone
from app.db.mongodb import db
from app.core.fsm import TelemetryFSM

MQTT_BROKER = os.getenv("MQTT_BROKER", "mosquitto-broker")
MQTT_TOPIC = "telemetry/#"

async def listen():
    # Instantiate FSM ONCE outside the loop to prevent memory thrashing
    fsm = TelemetryFSM()
    
    while True:
        try:
            async with aiomqtt.Client(MQTT_BROKER) as client:
                await client.subscribe(MQTT_TOPIC)
                
                async for message in client.messages:
                    # Reset FSM state for each new message
                    fsm.state = "RECEIVED"
                    payload_raw = message.payload.decode()
                    
                    parsed_data = fsm.parse(payload_raw)
                    
                    if fsm.validate(parsed_data) and fsm.accept():
                        # Construct document strictly according to raw_payload_schema.json
                        document = {
                            "device_id": str(parsed_data["device_id"]),
                            "arrival_timestamp": datetime.now(timezone.utc),
                            "protocol": "MQTT",
                            "raw_payload": {
                                "value": float(parsed_data["value"])
                            },
                            "validation_status": "pending"
                        }
                        
                        await db.telemetry.insert_one(document)
                    else:
                        # Dead Letter Queue logic (log or route to DLQ collection)
                        pass
                        
        except aiomqtt.MqttError:
            await asyncio.sleep(2)

if __name__ == "__main__":
    asyncio.run(listen())
