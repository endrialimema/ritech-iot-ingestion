-- V2_create_partitions.sql

-- 1. Create a default partition to catch anomalous timestamps safely
CREATE TABLE iot.telemetry_data_default 
    PARTITION OF iot.telemetry_data DEFAULT;

-- 2. Create monthly partitions for the immediate operational window
CREATE TABLE iot.telemetry_data_2026_04 PARTITION OF iot.telemetry_data
    FOR VALUES FROM ('2026-04-01 00:00:00') TO ('2026-05-01 00:00:00');

CREATE TABLE iot.telemetry_data_2026_05 PARTITION OF iot.telemetry_data
    FOR VALUES FROM ('2026-05-01 00:00:00') TO ('2026-06-01 00:00:00');

CREATE TABLE iot.telemetry_data_2026_06 PARTITION OF iot.telemetry_data
    FOR VALUES FROM ('2026-06-01 00:00:00') TO ('2026-07-01 00:00:00');