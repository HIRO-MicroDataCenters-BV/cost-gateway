from cost_gateway.async_fixture import AsyncTestFixture
from cost_gateway.pydantic_yaml import from_yaml
from cost_gateway.settings import Settings


class CostSettingsTest(AsyncTestFixture):
    def test_load_settings_with_cost(self) -> None:
        settings = from_yaml("etc/config.yaml", Settings)
        assert settings.cost.enabled is True  # type: ignore[attr-defined]
        assert "energy" in settings.cost.sources  # type: ignore[attr-defined]
        assert "cloud" in settings.cost.sources  # type: ignore[attr-defined]
        assert settings.cost.sources["energy"].min_cost == 0.1  # type: ignore[attr-defined]
        assert settings.cost.sources["energy"].max_cost == 0.5  # type: ignore[attr-defined]
        assert settings.cost.sources["energy"].peak_time == 43200  # type: ignore[attr-defined]
        assert settings.cost.sources["cloud"].min_cost == 100.0  # type: ignore[attr-defined]
        assert settings.cost.sources["cloud"].max_cost == 500.0  # type: ignore[attr-defined]
        assert settings.cost.sources["cloud"].peak_time == 21600  # type: ignore[attr-defined]
