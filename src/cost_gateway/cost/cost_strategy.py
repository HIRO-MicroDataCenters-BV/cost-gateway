import abc
import math


class CostStrategy(abc.ABC):
    @abc.abstractmethod
    def compute_cost(self, min_cost: float, max_cost: float, now_seconds: int) -> float:
        pass


class SinusoidalCostStrategy(CostStrategy):
    peak_time: int
    period: int

    def __init__(self, peak_time: int, period: int = 86400):
        self.peak_time = peak_time
        self.period = period

    def compute_cost(self, min_cost: float, max_cost: float, now_seconds: int) -> float:
        time_diff = now_seconds - self.peak_time
        normalized_time = (time_diff % self.period) / self.period
        angle = normalized_time * 2 * math.pi - math.pi
        cos_value = math.cos(angle)
        cost = min_cost + (max_cost - min_cost) * (1 + cos_value) / 2
        return cost


class ConstantCostStrategy(CostStrategy):
    value: float

    def __init__(self, value: float):
        self.value = value

    def compute_cost(self, min_cost: float, max_cost: float, now_seconds: int) -> float:
        return self.value


class LinearCostStrategy(CostStrategy):
    peak_time: int
    period: int

    def __init__(self, peak_time: int, period: int = 86400):
        self.peak_time = peak_time
        self.period = period

    def compute_cost(self, min_cost: float, max_cost: float, now_seconds: int) -> float:
        time_diff = now_seconds - self.peak_time
        normalized_time = (time_diff % self.period) / self.period
        if normalized_time <= 0.5:
            return min_cost + (max_cost - min_cost) * (normalized_time * 2)
        else:
            return max_cost - (max_cost - min_cost) * ((normalized_time - 0.5) * 2)
