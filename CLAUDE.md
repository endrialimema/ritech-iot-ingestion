# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Layout

The project root is the repo root (the nested structure was flattened). All commands run from the repo root.

```
ritech-iot-ingestion/
├── app/                   ← FastAPI app + MQTT subscriber
│   ├── api/               ← FastAPI routers
│   ├── core/
│   │   ├── cpp_normalizer/ ← pybind11 C++ extension (must be built separately)
│   │   ├── fsm.py
│   │   ├── middleware.py
│   │   ├── payloads/      ← sensor payload classes + registry
│   │   └── rate_limiter.py
│   ├── db/mongodb.py
│   ├── schemas/           ← Pydantic models
│   ├── services/
│   └── mqtt_subscriber.py
├── database/
│   ├── nosql-schemas/     ← MongoDB document schema reference
│   └── sql-migrations/    ← Postgres DDL (V1 schema + V2 partitions)
├── publisher/             ← standalone MQTT test publisher (own Dockerfile)
├── docs/                  ← ADRs and UML diagrams
├── docker_compose.yaml
└── Dockerfile
```

## Running the Stack

Requires a `.env` file with at minimum `MONGO_URL` and Postgres credentials (`POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`).

```bash
docker compose up --build
```

Services:
- `mosquitto-broker` — Eclipse Mosquitto MQTT broker (port 1883)
- `mongo-raw-ingestion` — MongoDB 6.0 for raw telemetry (port 27017)
- `postgres-analytics` — Postgres 15 with partitioned analytics schema (port 5432)
- `mqtt-subscriber` — Runs `app/mqtt_subscriber.py`; stops after 500 messages, then prints yappi CPU profile
- `publisher` — Sends 30 seconds of synthetic sensor data, then exits

## Running the FastAPI App Locally

The C++ normalizer must be built first (see below), then:

```bash
pip install -r requirements.txt
MONGO_URL=mongodb://localhost:27017 uvicorn app.main:app --reload
```

API base: `http://localhost:8000/api/v1`  
Health check: `GET /health`

## C++ Normalizer (pybind11)

The payload classes (`temperature.py`, `humidity.py`, `pressure.py`) call into a compiled C++ extension for normalization. It must be built before running anything locally:

```bash
cd app/core/cpp_normalizer
pip install pybind11
python setup.py build_ext --inplace
```

The extension is imported in `app/core/__init__.py`. Each payload class holds a **shared class-level `Normalizer` instance** (`_norm = cpp_normalizer.Normalizer()`), so normalization history is shared across all instances of the same payload type — not per-object.

## Architecture

Two ingestion paths:

**MQTT path (primary):** `publisher` → `mosquitto-broker` → `mqtt_subscriber.py` → MongoDB  
**HTTP path (secondary):** `POST /api/v1/telemetry/` → `telemetry_service.py` → MongoDB

### Processing Pipeline (`app/core/`)

- **`fsm.py` — `TelemetryFSM`**: States `RECEIVED → PARSED → ACCEPTED/REJECTED`. Calls `TelemetryFactory.create()` then `validate()`.
- **`payloads/factory.py` — `TelemetryFactory`**: Looks up payload class from `SensorRegistry` by `sensor_type` string.
- **`payloads/registry.py` — `SensorRegistry`**: Class-level dict of sensor type → payload class; populated at import time in `factory.py`.
- **`payloads/base.py` — `BaseTelemetryPayload`**: Abstract base; requires `validate()`. Provides `get_device_id()`, `get_value()`, `get_sensor_type()`.
- **Concrete payloads** (`temperature.py`, `humidity.py`, `pressure.py`): Each delegates normalization to the shared C++ `Normalizer` instance. `validate()` does a range check.

### Adding a New Sensor Type
1. Create `app/core/payloads/<type>.py` extending `BaseTelemetryPayload` — implement `validate()` and `normalize()`.
2. Register it in `app/core/payloads/factory.py` via `SensorRegistry.register("<type>", <Class>)`.

### HTTP Ingestion (`app/services/telemetry_service.py`)
Time-bucketing: readings are grouped into 60-second buckets per `device_id` using MongoDB `update_one` with `upsert=True`. Buckets cap at 5 readings; overflow shifts to the next minute bucket.

### Middleware
`app/core/middleware.py` wraps `TokenBucket` (from `rate_limiter.py`) as FastAPI middleware — 20 capacity, 5 tokens/sec refill.

### API Routes

| Method | Path | Description |
|---|---|---|
| `GET` | `/health` | Health check |
| `POST` | `/api/v1/telemetry/` | Ingest a telemetry reading (time-bucketed to MongoDB) |
| `POST` | `/api/v1/sensors/` | Create sensor metadata (stub — returns input, no persistence) |

### Postgres Analytics Schema (`database/sql-migrations/`)

`iot` schema with tables: `facilities`, `devices`, `sensor_types`, `alert_thresholds`, and `telemetry_data` (partitioned by `ts`). Partitions created in V2. **MongoDB is the active write path; Postgres is provisioned but not yet wired to the ingestion pipeline.**

## Environment Variables

| Variable | Used by | Notes |
|---|---|---|
| `MONGO_URL` | `app/db/mongodb.py` | Required; crashes on missing |
| `MQTT_BROKER` | `mqtt_subscriber.py`, `publisher.py` | Defaults to `mosquitto-broker` |
| `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB` | `docker_compose.yaml` | For Postgres container init |

## Key Design Decisions (see `docs/adr/`)

- **MQTT over REST** for IoT ingestion: lower overhead, pub/sub fan-out, fire-and-forget semantics.
- **MongoDB for raw payloads**, Postgres for analytics: MongoDB handles flexible/schemaless raw ingestion; Postgres (partitioned) handles structured analytics queries.
- **Monolith over microservices** at this stage: simpler deployment, lower operational overhead for current scale.
