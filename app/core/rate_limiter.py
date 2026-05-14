import time
import threading


class TokenBucket:
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_rate  # tokens per second
        self.last_update = time.time()
        self.lock = threading.Lock()

    def _refill(self):
        now = time.time()
        elapsed = now - self.last_update
        self.last_update = now

        added_tokens = elapsed * self.refill_rate
        self.tokens = min(self.capacity, self.tokens + added_tokens)

    def allow_request(self) -> bool:
        with self.lock:
            self._refill()

            if self.tokens >= 1:
                self.tokens -= 1
                return True

            return False