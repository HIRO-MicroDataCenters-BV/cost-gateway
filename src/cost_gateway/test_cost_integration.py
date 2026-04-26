from cost_gateway.async_fixture import AsyncTestFixture
from cost_gateway.context import Context
from cost_gateway.settings import (
    CostSettings,
    CostSimulatorConfig,
    PrometheusSettings,
    Settings,
)
from cost_gateway.util.mock_clock import MockClock


class CostIntegrationTest(AsyncTestFixture):
    clock: MockClock
    settings: Settings
    context: Context

    def setUp(self) -> None:
        super().setUp()
        self.clock = MockClock()
        self.settings = self.make_settings()
        self.context = Context(
            self.clock,
            self.settings,
            self.loop,
        )

    def tearDown(self) -> None:
        super().tearDown()

    def make_settings(self) -> Settings:
        settings = Settings(
            prometheus=PrometheusSettings(endpoint_port=8080),
            cost=CostSettings(
                enabled=True,
                sources={
                    "energy": CostSimulatorConfig(min_cost=0.1, max_cost=0.5, peak_time=0, period=86400),
                    "cloud": CostSimulatorConfig(min_cost=100.0, max_cost=500.0, peak_time=43200, period=86400),
                },
            ),
        )
        return settings

    def test_end_to_end_with_cost(self) -> None:
        self.context.start()
        self.context.stop()
