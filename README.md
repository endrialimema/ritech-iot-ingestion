# RITECH IoT Ingestion System

A **Docker-native IoT telemetry ingestion pipeline** that processes real-time sensor data using MQTT, validates and normalizes it through a hybrid **Python + C++ (pybind11)** architecture, and stores it in a database layer for analytics.

---

## System Overview

This project simulates a scalable IoT ingestion backend with the following pipeline:



The system is fully containerized using Docker Compose and designed for high-throughput message ingestion and processing.

---

## Architecture

### Core Components

- **MQTT Broker (Mosquitto)**
  - Handles real-time message transport
- **Publisher Service**
  - Simulates IoT devices sending telemetry data
- **Subscriber Service**
  - Consumes MQTT messages asynchronously using `aiomqtt`
- **FSM (Finite State Machine) Layer**
  - Parses and validates incoming telemetry payloads
- **C++ Normalizer (pybind11)**
  - High-performance normalization of sensor values
  - Handles temperature, humidity, and pressure normalization
- **Database Layer**
  - MongoDB: raw telemetry ingestion
  - PostgreSQL: structured analytics storage

---

## Technologies Used

- Python 3.11
- C++17
- pybind11
- Docker & Docker Compose
- MQTT (Eclipse Mosquitto)
- MongoDB
- PostgreSQL
- asyncio / aiomqtt
- FSM-based payload processing

---

## Project Structure
``` text
ritech-iot-ingestion/
│
├── app/
│    ├── mqtt_subscriber.py
│    ├── main.py
│    │
│    ├── core/
│    │    ├── fsm.py
│    │    ├── middleware.py
│    │    ├── rate_limiter.py
│    │    ├── payloads/
│    │         ├── base.py
│    │         ├── temperature.py
│    │         ├── humidity.py
│    │         ├── pressure.py
│    │          └── factory.py
│    │
│    └── cpp_normalizer/
│            ├── bindings.cpp
│            ├── setup.py
│            ├── normalizer.cpp
│  
├── publisher/
│      ├── publisher.py
│      ├── Dockerfile
│      ├── requirements.txt
│
├── database/
│   ├── sql-migrations 
│   │        ├─ V1_initial_shcema.sql
│   │        └─ V2_create_partitions.sql
│   └── nosql-schemas/      
│        └── raw_payload_schema.json    
│
│
├── docker-compose.yaml
├── Dockerfile
├── requirements.txt

```
---

## Key Features

### Real-Time Streaming
- MQTT-based asynchronous ingestion pipeline
- High-frequency message handling

### FSM-Based Processing
- Structured validation of telemetry payloads
- Extensible factory pattern for sensor types

### C++ Performance Optimization
- Critical normalization logic moved from Python → C++
- pybind11 bindings for seamless integration
- Reduces Python GIL bottlenecks under load

### Fully Docker-Native
- All services containerized
- Reproducible builds using Docker Compose
- Isolated environments for each service

---

## Performance Testing

The system was stress-tested under simulated high-load conditions:

- 50+ messages per batch test
- Continuous MQTT streaming
- CPU profiling via `yappi`
- MongoDB ingestion validation

### Observations:
- Python FSM handles orchestration
- C++ layer handles compute-heavy normalization
- Reduced Python CPU overhead in normalization stage

---

## Running the System

### 1. Build and start all services

```bash
docker compose up --build
```

This command:

- Builds the Python services
- Compiles the C++ normalization module inside Docker
- Starts:
  - MQTT Broker (Mosquitto)
  - MQTT Publisher
  - MQTT Subscriber
  - MongoDB
  - PostgreSQL
- Creates the internal Docker network automatically

---

### 2. Verify Running Containers

```bash
docker ps
```

Expected services:

| Service | Purpose |
|---|---|
| `ritech_mosquitto` | MQTT message broker |
| `telemetry-subscriber` | Async telemetry ingestion worker |
| `publisher` | IoT telemetry simulator |
| `ritech_mongo` | Raw telemetry storage |
| `ritech_postgres` | Analytical relational database |

---

### 3️. Monitor Subscriber Logs

```bash
docker logs -f telemetry-subscriber
```

Example output:

```text
Subscriber started
Connecting to MQTT broker...
Connected and subscribed
Message received: {...}
C++ normalize called
```

This confirms:
- MQTT communication is working
- FSM processing is active
- C++ normalization layer is executing correctly

---

### 4️. Verify MongoDB Inserts

```bash
docker exec -it ritech_mongo mongosh
```

Inside Mongo shell:

```javascript
use telemetry
db.telemetry.find().pretty()
```

This verifies successful telemetry ingestion.

---

### 5️. Run Stress Tests

The publisher service can simulate high-throughput telemetry loads.

Stress testing validates:

- MQTT ingestion throughput
- Async subscriber performance
- FSM validation stability
- C++ normalization execution
- MongoDB insertion reliability

CPU profiling is performed using:

```python
yappi
```

---

### 6️. Stop the System

```bash
docker compose down
```

To also remove volumes:

```bash
docker compose down -v
```

---

## Docker-Native Execution

The system is designed to run entirely inside Docker containers.

### Key Characteristics

✔ Isolated service environments  
✔ Reproducible builds  
✔ Internal Docker networking  
✔ Containerized MQTT communication  
✔ Automatic dependency management  
✔ Platform-independent deployment  

The C++ normalization layer is compiled during the Docker build process using:

- `g++`
- `pybind11`
- Python 3.11 build environment

This ensures the runtime environment remains consistent across machines.


