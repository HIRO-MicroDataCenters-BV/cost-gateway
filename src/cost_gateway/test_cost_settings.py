from cost_gateway.async_fixture import AsyncTestFixture
from cost_gateway.pydantic_yaml import from_yaml
from cost_gateway.settings import CostSourceConfig, Settings, StrategyType


class CostSettingsTest(AsyncTestFixture):
    def test_load_settings_with_cost(self) -> None:
        settings = from_yaml("etc/config.yaml", Settings)
        self.assertTrue(settings.cost.enabled)  # type: ignore[attr-defined]
        self.assertIn("energy", settings.cost.sources)  # type: ignore[attr-defined]
        self.assertIn("cloud", settings.cost.sources)  # type: ignore[attr-defined]
        self.assertEqual(settings.cost.sources["energy"].min_cost, 0.1)  # type: ignore[attr-defined]
        self.assertEqual(settings.cost.sources["energy"].max_cost, 0.5)  # type: ignore[attr-defined]
        self.assertEqual(settings.cost.sources["energy"].peak_time, 43200)  # type: ignore[attr-defined]
        self.assertEqual(settings.cost.sources["cloud"].min_cost, 100.0)  # type: ignore[attr-defined]
        self.assertEqual(settings.cost.sources["cloud"].max_cost, 500.0)  # type: ignore[attr-defined]
        self.assertEqual(settings.cost.sources["cloud"].peak_time, 21600)  # type: ignore[attr-defined]

    def test_cost_source_config_defaults(self) -> None:
        config = CostSourceConfig()
        self.assertEqual(config.strategy, StrategyType.sinusoidal)
        self.assertEqual(config.min_cost, 0.0)
        self.assertEqual(config.max_cost, 1.0)
        self.assertEqual(config.peak_time, 0)
        self.assertEqual(config.period, 86400)
        self.assertIsNone(config.value)
        self.assertIsNone(config.seed)

    def test_cost_source_config_with_values(self) -> None:
        config = CostSourceConfig(
            strategy=StrategyType.constant,
            min_cost=0.1,
            max_cost=0.5,
            value=0.75,
            peak_time=43200,
            period=3600,
        )

        self.assertEqual(config.strategy, StrategyType.constant)
        self.assertEqual(config.min_cost, 0.1)
        self.assertEqual(config.max_cost, 0.5)
        self.assertEqual(config.value, 0.75)
        self.assertEqual(config.peak_time, 43200)
        self.assertEqual(config.period, 3600)
