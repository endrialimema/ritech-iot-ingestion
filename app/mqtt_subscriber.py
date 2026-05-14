import asyncio
import aiomqtt
import os
import sys
import yappi
from datetime import datetime, timezone
from app.db.mongodb import db
from app.core.fsm import TelemetryFSM

MQTT_BROKER = os.getenv("MQTT_BROKER", "mosquitto-broker")
MQTT_TOPIC = "telemetry/#"

sys.path.append(os.path.abspath("cpp_normalizer"))  # Add C++ module path to sys.path

async def listen():
    # Instantiate FSM ONCE outside the loop to prevent memory thrashing

    print("Subscriber started")
    fsm = TelemetryFSM()
    yappi.start()
    start_time = datetime.now(timezone.utc)    
    message_count = 0
        
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

                document = {
                            "device_id": obj.get_device_id(),
                            "arrival_timestamp": datetime.now(timezone.utc),
                            "protocol": "MQTT",
                            "raw_payload": {
                            "value type": obj.get_sensor_type(),
                            "value": obj.get_value(),
                            "normalized": obj.normalize()
                            },
                            "validation_status": "accepted"
                            }

                
                await db.telemetry.insert_one(document)      

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
        yappi.stop()
        stats = yappi.get_func_stats()
        stats.sort("tsub")
        print("\n===== CPU PROFILING RESULTS =====")
        stats.print_top(20)
    
    

if __name__ == "__main__":
    asyncio.run(listen())
