import time

from cost_gateway.util.clock import Clock


class ClockImpl(Clock):
    def now_seconds(self) -> int:
        return int(time.time())

    def now_millis(self) -> int:
        return int(time.time() * 1000)
