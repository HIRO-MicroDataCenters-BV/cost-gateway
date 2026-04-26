from pydantic import BaseModel
from pydantic_settings import BaseSettings


class PrometheusSettings(BaseSettings):
    endpoint_port: int = 8080


class CostSimulatorConfig(BaseModel):
    min_cost: float
    max_cost: float
    peak_time: int
    period: int = 86400


class CostSettings(BaseSettings):
    enabled: bool = False
    sources: dict[str, CostSimulatorConfig] = {}


class Settings(BaseSettings):
    prometheus: PrometheusSettings
    cost: CostSettings = CostSettings()
