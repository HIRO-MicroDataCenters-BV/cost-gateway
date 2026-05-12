from cost_gateway.cost.cost_strategy import (
    ConstantCostStrategy,
    CostStrategy,
    LinearCostStrategy,
    RandomCostStrategy,
    SinusoidalCostStrategy,
)
from cost_gateway.cost.source import CostSource
from cost_gateway.settings import CostSourceConfig, StrategyType
from cost_gateway.util.clock import Clock


class CostSimulator(CostSource):
    clock: Clock
    strategies: dict[str, tuple[CostStrategy, CostSourceConfig]]

    def __init__(self, clock: Clock):
        self.clock = clock
        self.strategies = {}

    def add_cost(
        self,
        name: str,
        config: CostSourceConfig,
    ) -> None:
        strategy = self._create_strategy(config)
        self.strategies[name] = (strategy, config)

    def _create_strategy(self, config: CostSourceConfig) -> CostStrategy:
        match config.strategy:
            case StrategyType.sinusoidal:
                return SinusoidalCostStrategy(peak_time=config.peak_time, period=config.period)
            case StrategyType.constant:
                if config.value is None:
                    config.value = config.min_cost
                return ConstantCostStrategy(value=config.value)
            case StrategyType.linear:
                return LinearCostStrategy(peak_time=config.peak_time, period=config.period)
            case StrategyType.random:
                return RandomCostStrategy(seed=config.seed)

    def get_cost(self, name: str) -> float:
        entry = self.strategies.get(name)
        if entry is None:
            raise ValueError(f"Cost source '{name}' not configured")

        strategy, config = entry
        now_seconds = self.clock.now_seconds()
        return strategy.compute_cost(config.min_cost, config.max_cost, now_seconds)
