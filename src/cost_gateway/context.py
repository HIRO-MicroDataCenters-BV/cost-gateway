from typing import Any, List

import asyncio

from loguru import logger
from prometheus_async.aio.web import start_http_server

from cost_gateway.api.app import start_fastapi
from cost_gateway.cost.service import CostService
from cost_gateway.cost.simulator import CostSimulator
from cost_gateway.settings import Settings
from cost_gateway.util.clock import Clock


class Context:
    loop: asyncio.AbstractEventLoop
    terminated: asyncio.Event
    tasks: List[asyncio.Task[Any]]
    settings: Settings
    clock: Clock
    cost_service: CostService

    def __init__(
        self,
        clock: Clock,
        settings: Settings,
        loop: asyncio.AbstractEventLoop,
    ):
        self.settings = settings
        self.terminated = asyncio.Event()
        self.loop = loop
        self.tasks = []
        self.clock = clock
        simulator = CostSimulator(self.clock)
        for name, config in self.settings.cost.sources.items():
            simulator.add_cost(
                name=name,
                min_cost=config.min_cost,
                max_cost=config.max_cost,
                peak_time=config.peak_time,
                period=config.period,
            )
        self.cost_service = CostService(simulator, self.settings.cost)

    def start(self) -> None:
        if self.terminated.is_set():
            return
        self.terminated.clear()
        self.loop.run_until_complete(self.run_tasks())

    async def run_tasks(self) -> None:
        if self.settings.cost.enabled:
            task = self.loop.create_task(self.cost_service.run_periodic_update())
            self.tasks.append(task)
        self.tasks.append(self.loop.create_task(start_fastapi(self.settings.api.port, self.cost_service)))

        self.prometheus_server = await start_http_server(port=self.settings.prometheus.endpoint_port)

    def stop(self) -> None:
        self.terminated.set()
        for task in self.tasks:
            task.cancel()
        self.loop.run_until_complete(self.prometheus_server.close())

    def wait_for_termination(self) -> None:
        self.loop.run_until_complete(self.terminated.wait())
        logger.info("Application terminated.")

    def exit_gracefully(self, _1: Any, _2: Any) -> None:
        self.stop()
        self.wait_for_termination()
