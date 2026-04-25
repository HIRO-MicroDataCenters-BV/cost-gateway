from cost_gateway.util.clock import Clock


class MockClock(Clock):
    millis: int

    def __init__(self):
        self.millis = 1000

    def set_seconds(self, seconds: int) -> None:
        self.millis = seconds * 1000

    def now_seconds(self) -> int:
        return int(self.millis / 1000)

    def now_millis(self) -> int:
        return self.millis
