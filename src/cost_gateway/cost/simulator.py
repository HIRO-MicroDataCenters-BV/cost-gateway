import math

from cost_gateway.cost.source import CostSource
from cost_gateway.util.clock import Clock


class CostSimulatorConfig:
    min_cost: float
    max_cost: float
    peak_time: int
    period: int

    def __init__(
        self,
        min_cost: float,
        max_cost: float,
        peak_time: int,
        period: int = 86400,
    ):
        self.min_cost = min_cost
        self.max_cost = max_cost
        self.peak_time = peak_time
        self.period = period


class CostSimulator(CostSource):
    config: CostSimulatorConfig
    clock: Clock
    costs: dict[str, CostSimulatorConfig]

    def __init__(self, clock: Clock):
        self.clock = clock
        self.costs = {}

    def add_cost(
        self,
        name: str,
        min_cost: float,
        max_cost: float,
        peak_time: int,
        period: int = 86400,
    ) -> None:
        self.costs[name] = CostSimulatorConfig(
            min_cost=min_cost,
            max_cost=max_cost,
            peak_time=peak_time,
            period=period,
        )

    async def get_cost(self, name: str) -> float:
        config = self.costs.get(name)
        if config is None:
            raise ValueError(f"Cost source '{name}' not configured")

        now_seconds = self.clock.now_seconds()
        time_diff = now_seconds - config.peak_time
        normalized_time = (time_diff % config.period) / config.period
        angle = normalized_time * 2 * math.pi - math.pi

        cos_value = math.cos(angle)
        cost = config.min_cost + (config.max_cost - config.min_cost) * (1 + cos_value) / 2

        return cost
