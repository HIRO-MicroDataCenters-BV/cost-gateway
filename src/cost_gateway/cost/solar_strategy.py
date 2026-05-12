import math
import random

from cost_gateway.cost.cost_strategy import CostStrategy

# ============================================================
# SOLAR ENERGY PRICE STRATEGY
# ============================================================


class SolarEnergyCostStrategy(CostStrategy):
    """
    Simulates electricity market pricing in a solar-heavy grid.

    Characteristics:
    - expensive morning/evening
    - cheap or negative around noon
    - strong volatility
    - weather randomness
    """

    SECONDS_PER_DAY = 24 * 3600

    def compute_cost(
        self,
        min_cost: float,
        max_cost: float,
        now_seconds: int,
    ) -> float:

        day_time = now_seconds % self.SECONDS_PER_DAY
        hour = day_time / 3600

        # ----------------------------------------------------
        # Morning/evening demand peaks
        # ----------------------------------------------------

        morning_peak = math.exp(-((hour - 8) ** 2) / 6)
        evening_peak = math.exp(-((hour - 19) ** 2) / 5)

        # ----------------------------------------------------
        # Solar production dip at noon
        # ----------------------------------------------------

        solar_oversupply = math.exp(-((hour - 13) ** 2) / 8)

        # ----------------------------------------------------
        # Combine effects
        # ----------------------------------------------------

        normalized = 0.45 + 0.35 * morning_peak + 0.55 * evening_peak - 0.60 * solar_oversupply

        # ----------------------------------------------------
        # Weather/grid randomness
        # ----------------------------------------------------

        normalized += random.uniform(-0.12, 0.12)

        # ----------------------------------------------------
        # Rare extreme market spikes
        # ----------------------------------------------------

        if random.random() < 0.01:
            normalized += random.uniform(0.2, 0.5)

        # ----------------------------------------------------
        # Allow negative prices
        # ----------------------------------------------------

        raw_cost = min_cost + normalized * (max_cost - min_cost)

        return raw_cost
