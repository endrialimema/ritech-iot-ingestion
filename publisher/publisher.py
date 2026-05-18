import time
import json
import random
import paho.mqtt.client as mqtt
import os

MQTT_BROKER = os.getenv("MQTT_BROKER", "mosquitto-broker")

client = mqtt.Client()
client.connect(MQTT_BROKER, 1883)
client.loop_start()


sensor_types = ["temperature", "humidity", "pressure"]

device_ids = []
for i in range(10000):
    a = "device_" + str(i)
    device_ids.append(a)

start_time = time.time()
i = 0
while time.time() - start_time < 30:
    sensor = random.choice(sensor_types)

    if sensor == "temperature":
        value = random.randint(-20, 50)
    elif sensor == "humidity":
        value = random.randint(0, 100)
    else:
        value = random.randint(300, 1100)


    msg = {
        "sensor_type": sensor,
        "device_id": random.choice(device_ids),
        "value": value
    }

    payload = json.dumps(msg)

    client.publish(f"telemetry/{msg['device_id']}", payload)

    print(f"[{i}]sent:", payload)
    i += 1

    time.sleep(0.1)

    