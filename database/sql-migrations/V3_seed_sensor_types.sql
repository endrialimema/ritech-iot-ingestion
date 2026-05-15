-- V3_seed_sensor_types.sql

-- Ensure sensor_name is unique so ON CONFLICT works and duplicates are impossible
ALTER TABLE iot.sensor_types
    ADD CONSTRAINT unique_sensor_name UNIQUE (sensor_name);

-- Seed the three supported sensor types
INSERT INTO iot.sensor_types (sensor_name, unit_of_measurement) VALUES
    ('temperature', 'C'),
    ('humidity',    '%'),
    ('pressure',    'hPa')
ON CONFLICT (sensor_name) DO NOTHING;
