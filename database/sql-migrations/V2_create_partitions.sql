-- V2_create_partitions.sql

-- 1. Create a default partition to catch anomalous timestamps safely
CREATE TABLE iot.telemetry_data_default
    PARTITION OF iot.telemetry_data DEFAULT;

-- 2. Monthly partitions for 2026
CREATE TABLE iot.telemetry_data_2026_04 PARTITION OF iot.telemetry_data
    FOR VALUES FROM ('2026-04-01 00:00:00') TO ('2026-05-01 00:00:00');

CREATE TABLE iot.telemetry_data_2026_05 PARTITION OF iot.telemetry_data
    FOR VALUES FROM ('2026-05-01 00:00:00') TO ('2026-06-01 00:00:00');

CREATE TABLE iot.telemetry_data_2026_06 PARTITION OF iot.telemetry_data
    FOR VALUES FROM ('2026-06-01 00:00:00') TO ('2026-07-01 00:00:00');

CREATE TABLE iot.telemetry_data_2026_07 PARTITION OF iot.telemetry_data
    FOR VALUES FROM ('2026-07-01 00:00:00') TO ('2026-08-01 00:00:00');

CREATE TABLE iot.telemetry_data_2026_08 PARTITION OF iot.telemetry_data
    FOR VALUES FROM ('2026-08-01 00:00:00') TO ('2026-09-01 00:00:00');

CREATE TABLE iot.telemetry_data_2026_09 PARTITION OF iot.telemetry_data
    FOR VALUES FROM ('2026-09-01 00:00:00') TO ('2026-10-01 00:00:00');

CREATE TABLE iot.telemetry_data_2026_10 PARTITION OF iot.telemetry_data
    FOR VALUES FROM ('2026-10-01 00:00:00') TO ('2026-11-01 00:00:00');

CREATE TABLE iot.telemetry_data_2026_11 PARTITION OF iot.telemetry_data
    FOR VALUES FROM ('2026-11-01 00:00:00') TO ('2026-12-01 00:00:00');

CREATE TABLE iot.telemetry_data_2026_12 PARTITION OF iot.telemetry_data
    FOR VALUES FROM ('2026-12-01 00:00:00') TO ('2027-01-01 00:00:00');

-- 3. Monthly partitions for 2027
CREATE TABLE iot.telemetry_data_2027_01 PARTITION OF iot.telemetry_data
    FOR VALUES FROM ('2027-01-01 00:00:00') TO ('2027-02-01 00:00:00');

CREATE TABLE iot.telemetry_data_2027_02 PARTITION OF iot.telemetry_data
    FOR VALUES FROM ('2027-02-01 00:00:00') TO ('2027-03-01 00:00:00');

CREATE TABLE iot.telemetry_data_2027_03 PARTITION OF iot.telemetry_data
    FOR VALUES FROM ('2027-03-01 00:00:00') TO ('2027-04-01 00:00:00');

CREATE TABLE iot.telemetry_data_2027_04 PARTITION OF iot.telemetry_data
    FOR VALUES FROM ('2027-04-01 00:00:00') TO ('2027-05-01 00:00:00');

CREATE TABLE iot.telemetry_data_2027_05 PARTITION OF iot.telemetry_data
    FOR VALUES FROM ('2027-05-01 00:00:00') TO ('2027-06-01 00:00:00');

CREATE TABLE iot.telemetry_data_2027_06 PARTITION OF iot.telemetry_data
    FOR VALUES FROM ('2027-06-01 00:00:00') TO ('2027-07-01 00:00:00');
