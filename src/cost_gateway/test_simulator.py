from cost_gateway.async_fixture import AsyncTestFixture
from cost_gateway.cost.simulator import CostSimulator
from cost_gateway.util.mock_clock import MockClock


class CostSimulatorTest(AsyncTestFixture):
    clock: MockClock
    simulator: CostSimulator

    def setUp(self) -> None:
        super().setUp()
        self.clock = MockClock()
        self.simulator = CostSimulator(self.clock)

    def tearDown(self) -> None:
        super().tearDown()

    def test_add_single_cost(self) -> None:
        self.simulator.add_cost("energy", min_cost=0.1, max_cost=0.5, peak_time=0)
        assert "energy" in self.simulator.costs

    async def test_simulate_cost_at_peak(self) -> None:
        self.simulator.add_cost("energy", min_cost=0.1, max_cost=0.5, peak_time=0, period=86400)
        self.clock.set_seconds(0)
        cost = await self.simulator.get_cost("energy")
        assert cost == 0.5

    async def test_simulate_cost_at_valley(self) -> None:
        self.simulator.add_cost("energy", min_cost=0.1, max_cost=0.5, peak_time=0, period=86400)
        self.clock.set_seconds(43200)
        cost = await self.simulator.get_cost("energy")
        assert cost == 0.1

    async def test_simulate_cost_in_round_trip(self) -> None:
        self.simulator.add_cost("energy", min_cost=0.1, max_cost=0.5, peak_time=0, period=86400)
        self.clock.set_seconds(21600)
        cost = await self.simulator.get_cost("energy")
        expected = 0.1 + (0.5 - 0.1) * (1 + 0) / 2
        assert abs(cost - expected) < 0.001

    async def test_simulate_cost_unknown_source_raises(self) -> None:
        self.simulator.add_cost("energy", min_cost=0.1, max_cost=0.5, peak_time=0)
        with self.assertRaises(ValueError):
            await self.simulator.get_cost("unknown")

    async def test_multiple_costs(self) -> None:
        self.simulator.add_cost("energy", min_cost=0.1, max_cost=0.5, peak_time=0, period=86400)
        self.simulator.add_cost("cloud", min_cost=100.0, max_cost=500.0, peak_time=43200, period=86400)

        self.clock.set_seconds(0)
        energy_cost = await self.simulator.get_cost("energy")
        cloud_cost = await self.simulator.get_cost("cloud")
        assert energy_cost == 0.5
        assert cloud_cost == 100.0

        self.clock.set_seconds(43200)
        energy_cost = await self.simulator.get_cost("energy")
        cloud_cost = await self.simulator.get_cost("cloud")
        assert energy_cost == 0.1
        assert cloud_cost == 500.0
