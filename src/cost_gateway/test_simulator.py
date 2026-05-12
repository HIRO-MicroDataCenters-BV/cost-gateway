from cost_gateway.async_fixture import AsyncTestFixture
from cost_gateway.cost.simulator import CostSimulator
from cost_gateway.settings import CostSourceConfig, StrategyType
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
        config = CostSourceConfig(
            strategy=StrategyType.sinusoidal,
            min_cost=0.1,
            max_cost=0.5,
            peak_time=0,
            period=86400,
        )
        self.simulator.add_cost("energy", config=config)
        self.assertIn("energy", self.simulator.strategies)

    def test_simulate_cost_at_peak(self) -> None:
        config = CostSourceConfig(
            strategy=StrategyType.sinusoidal,
            min_cost=0.1,
            max_cost=0.5,
            peak_time=43200,
            period=86400,
        )
        self.simulator.add_cost("energy", config=config)
        self.clock.set_seconds(0)
        cost = self.simulator.get_cost("energy")
        self.assertEqual(cost, 0.5)

    def test_simulate_cost_at_valley(self) -> None:
        config = CostSourceConfig(
            strategy=StrategyType.sinusoidal,
            min_cost=0.1,
            max_cost=0.5,
            peak_time=43200,
            period=86400,
        )
        self.simulator.add_cost("energy", config=config)
        self.clock.set_seconds(43200)
        cost = self.simulator.get_cost("energy")
        self.assertEqual(cost, 0.1)

    def test_simulate_cost_in_round_trip(self) -> None:
        config = CostSourceConfig(
            strategy=StrategyType.sinusoidal,
            min_cost=0.1,
            max_cost=0.5,
            peak_time=21600,
            period=86400,
        )
        self.simulator.add_cost("energy", config=config)
        self.clock.set_seconds(0)
        cost = self.simulator.get_cost("energy")
        expected = 0.1 + (0.5 - 0.1) * (1 + 0) / 2
        self.assertAlmostEqual(cost, expected, places=3)

    def test_simulate_cost_unknown_source_raises(self) -> None:
        config = CostSourceConfig(
            strategy=StrategyType.sinusoidal,
            min_cost=0.1,
            max_cost=0.5,
            peak_time=0,
            period=86400,
        )
        self.simulator.add_cost("energy", config=config)
        with self.assertRaises(ValueError):
            self.simulator.get_cost("unknown")

    def test_multiple_costs(self) -> None:
        energy_config = CostSourceConfig(
            strategy=StrategyType.sinusoidal,
            min_cost=0.1,
            max_cost=0.5,
            peak_time=43200,
            period=86400,
        )
        cloud_config = CostSourceConfig(
            strategy=StrategyType.sinusoidal,
            min_cost=100.0,
            max_cost=500.0,
            peak_time=0,
            period=86400,
        )
        self.simulator.add_cost("energy", config=energy_config)
        self.simulator.add_cost("cloud", config=cloud_config)

        self.clock.set_seconds(0)
        energy_cost = self.simulator.get_cost("energy")
        cloud_cost = self.simulator.get_cost("cloud")
        self.assertEqual(energy_cost, 0.5)
        self.assertEqual(cloud_cost, 100.0)

        self.clock.set_seconds(43200)
        energy_cost = self.simulator.get_cost("energy")
        cloud_cost = self.simulator.get_cost("cloud")
        self.assertEqual(energy_cost, 0.1)
        self.assertEqual(cloud_cost, 500.0)

    def test_constant_strategy(self) -> None:
        config = CostSourceConfig(
            strategy=StrategyType.constant,
            min_cost=0.1,
            max_cost=0.5,
            value=0.75,
        )
        self.simulator.add_cost("energy", config=config)

        self.clock.set_seconds(0)
        self.assertAlmostEqual(self.simulator.get_cost("energy"), 0.75, places=3)
        self.clock.set_seconds(86400)
        self.assertAlmostEqual(self.simulator.get_cost("energy"), 0.75, places=3)

    def test_constant_strategy_defaults_to_min_cost(self) -> None:
        config = CostSourceConfig(
            strategy=StrategyType.constant,
            min_cost=0.42,
            max_cost=0.5,
        )
        self.simulator.add_cost("energy", config=config)
        self.clock.set_seconds(0)
        cost = self.simulator.get_cost("energy")
        self.assertAlmostEqual(cost, 0.42, places=3)

    def test_linear_strategy(self) -> None:
        config = CostSourceConfig(
            strategy=StrategyType.linear,
            min_cost=0.0,
            max_cost=1.0,
            peak_time=0,
            period=86400,
        )
        self.simulator.add_cost("energy", config=config)

        self.clock.set_seconds(0)
        self.assertAlmostEqual(self.simulator.get_cost("energy"), 0.0, places=3)
        self.clock.set_seconds(21600)
        self.assertAlmostEqual(self.simulator.get_cost("energy"), 0.5, places=3)
        self.clock.set_seconds(43200)
        self.assertAlmostEqual(self.simulator.get_cost("energy"), 1.0, places=3)
        self.clock.set_seconds(64800)
        self.assertAlmostEqual(self.simulator.get_cost("energy"), 0.5, places=3)
        self.clock.set_seconds(86400)
        self.assertAlmostEqual(self.simulator.get_cost("energy"), 0.0, places=3)
