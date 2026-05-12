from typing import Any

from enum import Enum

from pydantic import BaseModel, field_validator
from pydantic_settings import BaseSettings


class PrometheusSettings(BaseSettings):
    endpoint_port: int = 8080


class StrategyType(str, Enum):
    sinusoidal = "sinusoidal"
    constant = "constant"
    linear = "linear"


class CostSourceConfig(BaseModel):
    strategy: StrategyType = StrategyType.sinusoidal
    min_cost: float = 0.0
    max_cost: float = 1.0
    value: float | None = None
    peak_time: int = 0
    period: int = 86400

    @field_validator("min_cost", "max_cost")
    @classmethod
    def validate_min_max(cls, v: float, info: Any) -> float:
        return v

    @field_validator("period")
    @classmethod
    def validate_period(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("period must be positive")
        if v > 86400 * 365:
            raise ValueError("period must be at most 1 year")
        return v


class CostSettings(BaseSettings):
    enabled: bool = False
    sources: dict[str, CostSourceConfig] = {}


class ApiSettings(BaseSettings):
    port: int = 8000


class Settings(BaseSettings):
    prometheus: PrometheusSettings
    api: ApiSettings
    cost: CostSettings = CostSettings()

    model_config = {"extra": "allow"}
