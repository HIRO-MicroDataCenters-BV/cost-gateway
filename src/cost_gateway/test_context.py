from cost_gateway.async_fixture import AsyncTestFixture
from cost_gateway.context import Context
from cost_gateway.settings import (
    ApiSettings,
    PrometheusSettings,
    Settings,
)
from cost_gateway.util.clock import Clock
from cost_gateway.util.mock_clock import MockClock


class ContextTest(AsyncTestFixture):
    clock: Clock
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

    def test_end_to_end_minimal(self) -> None:
        self.context.start()
        self.context.stop()

    def make_settings(self) -> Settings:
        settings = Settings(prometheus=PrometheusSettings(endpoint_port=8080), api=ApiSettings(port=8085))
        return settings
