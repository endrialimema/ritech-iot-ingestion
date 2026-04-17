CREATE SCHEMA IF NOT EXISTS iot;

-- 1. Facilities / Locations Table
CREATE TABLE iot.facilities (
    facility_id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    region VARCHAR(100)
);

-- 2. Devices Metadata Table
CREATE TABLE iot.devices (
    device_id VARCHAR(50) PRIMARY KEY,
    facility_id UUID REFERENCES iot.facilities(facility_id),
    firmware_version VARCHAR(50),
    status VARCHAR(20)
);

-- 3. Sensor Types Lookup Table
CREATE TABLE iot.sensor_types (
    sensor_type_id SERIAL PRIMARY KEY,
    sensor_name VARCHAR(50) NOT NULL,
    unit_of_measurement VARCHAR(20) NOT NULL
);

-- 4. Control Engineering Thresholds (For Alerting)
CREATE TABLE iot.alert_thresholds (
    threshold_id SERIAL PRIMARY KEY,
    device_id VARCHAR(50) REFERENCES iot.devices(device_id),
    sensor_type_id INT REFERENCES iot.sensor_types(sensor_type_id),
    min_critical FLOAT,
    max_critical FLOAT
);

-- 5. Master Time-Series Telemetry Table (Partitioned)
CREATE TABLE iot.telemetry_data (
    ts TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    device_id VARCHAR(50) REFERENCES iot.devices(device_id),
    sensor_type_id INT REFERENCES iot.sensor_types(sensor_type_id),
    reading_value FLOAT NOT NULL
) PARTITION BY RANGE (ts);