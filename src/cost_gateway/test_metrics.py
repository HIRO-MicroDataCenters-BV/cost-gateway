from cost_gateway.async_fixture import AsyncTestFixture
from cost_gateway.cost.metrics import get_or_create_gauge


class CostMetricsTest(AsyncTestFixture):
    def setUp(self) -> None:
        super().setUp()

    def tearDown(self) -> None:
        super().tearDown()

    def test_register_metric_creates_new(self) -> None:
        gauge = get_or_create_gauge("energy", "Energy cost")
        assert gauge is not None

    def test_register_metric_returns_cached(self) -> None:
        gauge1 = get_or_create_gauge("energy", "Energy cost")
        gauge2 = get_or_create_gauge("energy", "Energy cost different")
        assert gauge1 is gauge2
