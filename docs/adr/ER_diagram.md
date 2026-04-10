---
config:
  layout: dagre
  look: neo
---
erDiagram
	direction TB
	sensor_types {
		serial sensor_type_id PK ""  
		string sensor_name  ""  
		string unit_of_measurement  ""  
	}

	alert_thresholds {
		int threshold_id PK ""  
		string device_id FK ""
        int sensor_type_id FK
        float min_critical
        float max_critical  
	}

	devices {
		string device_id PK ""  
		uuid facility_id FK ""  
		string firmware_version  ""  
		string status  ""  
	}

	telemetry_data {
		timestamp ts  ""  
		string device_id FK ""  
		int sensor_type_id FK ""  
		float reading_value  ""  
	}

	facilities {
		uuid facility_id PK ""  
		string name  ""  
		string region  ""  
	}

	facilities||--|{devices:"  "
	devices||--|{telemetry_data:"  "
	devices||--|{alert_thresholds:"  "
	telemetry_data}|--||sensor_types:"  "
