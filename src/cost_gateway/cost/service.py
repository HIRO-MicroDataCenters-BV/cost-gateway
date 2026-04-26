import asyncio

from cost_gateway.cost.metrics import get_or_create_gauge
from cost_gateway.cost.source import CostSource
from cost_gateway.settings import CostSettings


class CostService:
    cost_source: CostSource
    settings: CostSettings

    def __init__(self, cost_source: CostSource, settings: CostSettings):
        self.cost_source = cost_source
        self.settings = settings

    async def update_metrics(self) -> None:
        if not self.settings.enabled:
            return

        for name, config in self.settings.sources.items():
            try:
                cost = await self.cost_source.get_cost(name)
                gauge = get_or_create_gauge(name, f"Cost for {name}")
                gauge.labels(source=name).set(cost)
            except ValueError:
                pass

    async def run_periodic_update(self, interval: int = 60) -> None:
        while True:
            await self.update_metrics()
            await asyncio.sleep(interval)
