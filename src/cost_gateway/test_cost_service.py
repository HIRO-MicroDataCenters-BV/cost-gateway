from unittest.mock import AsyncMock, MagicMock

from cost_gateway.async_fixture import AsyncTestFixture
from cost_gateway.cost.service import CostService
from cost_gateway.cost.simulator import CostSimulator
from cost_gateway.settings import CostSettings, CostSimulatorConfig


class CostServiceTest(AsyncTestFixture):
    mock_source: MagicMock
    settings: CostSettings
    service: CostService

    def setUp(self) -> None:
        super().setUp()
        self.mock_source = MagicMock(spec=CostSimulator)
        self.settings = CostSettings(
            enabled=True,
            sources={"energy": CostSimulatorConfig(min_cost=0.1, max_cost=0.5, peak_time=0, period=86400)},
        )
        self.service = CostService(self.mock_source, self.settings)

    def tearDown(self) -> None:
        super().tearDown()

    async def test_update_metrics_enabled(self) -> None:
        self.mock_source.get_cost = AsyncMock(return_value=0.3)
        await self.service.update_metrics()
        self.mock_source.get_cost.assert_called_once_with("energy")

    async def test_update_metrics_disabled(self) -> None:
        self.settings.enabled = False
        await self.service.update_metrics()
        assert not self.mock_source.get_cost.called

    async def test_update_metrics_multiple_sources(self) -> None:
        self.settings.sources["cloud"] = CostSimulatorConfig(
            min_cost=100.0, max_cost=500.0, peak_time=43200, period=86400
        )
        self.mock_source.get_cost = AsyncMock(return_value=200.0)
        await self.service.update_metrics()
        assert self.mock_source.get_cost.call_count == 2
