import json
from app.core.payloads.factory import TelemetryFactory
from datetime import datetime, timezone

class TelemetryFSM:
    def __init__(self):
        self.state = "RECEIVED"


    def logs(self, event, reason, payload_raw):
        device_id = None
        try:
            if payload_raw:
                data = json.loads(payload_raw)
                device_id = data.get("device_id")
        except Exception:
            pass

        print({
            "event": event,
            "reason": reason,
            "device_id": device_id,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })


    def process(self, payload_raw):
        self.state = "RECEIVED"

        data = self.parse(payload_raw)
        if not data:
            self.state = "REJECTED"
            self.logs("REJECTED", "PARSE_FAILED", payload_raw)
            return None

        obj = TelemetryFactory.create(
            data.get("sensor_type"),
            data.get("device_id"),
            data.get("value")
        )

        print("FSM result:", obj)

        if not obj:
            self.state = "REJECTED"
            self.logs("REJECTED", "FACTORY_FAILED", payload_raw)
            return None

        if not obj.validate():
            self.state = "REJECTED"
            self.logs("REJECTED", "VALIDATION_FAILED", payload_raw)
            return None

        self.state = "ACCEPTED"
        self.logs("ACCEPTED", "SUCCESS", payload_raw)
        return obj

    def parse(self, payload_raw):
        try:
            if not isinstance(payload_raw, str):
                self.logs("REJECTED", "INVALID_PAYLOAD_TYPE", payload_raw)
                return None
            data = json.loads(payload_raw)
            if not isinstance(data, dict):
                self.logs("REJECTED", "INVALID_PAYLOAD_STRUCTURE", payload_raw)
                return None

            self.state = "PARSED"
            return data

        except json.JSONDecodeError:
            self.logs("REJECTED", "INVALID_JSON_FORMAT", payload_raw)
            return None
