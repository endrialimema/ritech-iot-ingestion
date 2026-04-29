import json

class TelemetryFSM:
    def _init_(self):
        self.state = "RECEIVED"

    def parse(self, payload_raw):
        try:
            data = json.loads(payload_raw)
            self.state = "PARSED"
            return data
        except Exception:
            self.state = "REJECTED"
            return None

    def validate(self, data):
        if not data:
            self.state = "REJECTED"
            return False
        
        required_fields = ["device_id", "value"]
        for field in required_fields:
            if field not in data:
                self.state = "REJECTED"
                return False
        
        if not isinstance(data["device_id"], str):
            self.state = "REJECTED"
            return False

        if not isinstance(data["value"], (int, float)):
            self.state = "REJECTED"
            return False

        self.state = "VALIDATED"
        return True

    def accept(self):
        if self.state == "VALIDATED":
            self.state = "ACCEPTED"
            return True
        return False
