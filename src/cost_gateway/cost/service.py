from typing import Dict, List

import asyncio
from decimal import Decimal

from loguru import logger
from prometheus_client import Metric

from cost_gateway.cost.cost import Cost
from cost_gateway.cost.metrics import get_or_create_gauge
from cost_gateway.cost.source import CostSource
from cost_gateway.settings import CostSettings


class CostService:
    cost_source: CostSource
    settings: CostSettings
    custom_costs: Dict[str, Decimal]

    def __init__(self, cost_source: CostSource, settings: CostSettings):
        self.cost_source = cost_source
        self.settings = settings
        self.custom_costs = dict()

    async def list(self) -> List[Cost]:
        results = []
        for name, _ in self.settings.sources.items():
            try:
                gauge = get_or_create_gauge(name, f"Cost for {name}")
                custom_value = self.custom_costs.get(name)
                if custom_value is not None:
                    cost = Cost(name=name, description=gauge._documentation, value=custom_value, is_custom=True)
                    results.append(cost)
                else:
                    metrics = list(gauge.labels(source=name).collect())
                    if len(metrics) == 1:
                        metric: Metric = metrics[0]
                        if len(metric.samples) == 1:
                            sample = metric.samples[0]
                            cost = Cost(
                                name=name,
                                description=gauge._documentation,
                                value=Decimal(sample.value),
                                is_custom=False,
                            )
                            results.append(cost)
                        else:
                            logger.error(
                                f"Unexpected number of samples for metric {name}, {len(metric.samples)}, expected 1."
                            )
                    else:
                        logger.error(f"Unexpected number of metrics for gauge {name}, {len(metrics)}, expected 1.")

            except ValueError as e:
                logger.error(f"Value error: {e}")

        return results

    def set_custom_cost(self, name: str, value: Decimal) -> None:
        source = self.settings.sources.get(name)
        if source is None:
            raise Exception(f"source {name} not found")
        gauge = get_or_create_gauge(name, f"Cost for {name}")
        gauge.labels(source=name).set(float(value))
        self.custom_costs[name] = value

    async def remove_custom_cost(self, name: str) -> None:
        if name in self.custom_costs:
            del self.custom_costs[name]
            cost = await self.cost_source.get_cost(name)
            gauge = get_or_create_gauge(name, f"Cost for {name}")
            gauge.labels(source=name).set(cost)

    async def run_periodic_update(self, interval: int = 60) -> None:
        while True:
            await self.update_metrics()
            await asyncio.sleep(interval)

    async def update_metrics(self) -> None:
        if not self.settings.enabled:
            return

        for name, _ in self.settings.sources.items():
            try:
                if name not in self.custom_costs:
                    cost = await self.cost_source.get_cost(name)
                    gauge = get_or_create_gauge(name, f"Cost for {name}")
                    gauge.labels(source=name).set(cost)
            except ValueError as e:
                logger.error(f"Value error: {e}")
