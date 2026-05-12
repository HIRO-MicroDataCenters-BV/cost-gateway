import math
import random

from cost_gateway.cost.cost_strategy import CostStrategy

# ============================================================
# CLOUD COST STRATEGY
# ============================================================


class CloudCostStrategy(CostStrategy):
    """
    Simulates relatively stable cloud costs with:
    - daily usage cycles
    - weekday/weekend behavior
    - mild randomness
    - occasional traffic spikes
    """

    SECONDS_PER_DAY = 24 * 3600
    SECONDS_PER_WEEK = 7 * SECONDS_PER_DAY

    def compute_cost(
        self,
        min_cost: float,
        max_cost: float,
        now_seconds: int,
    ) -> float:

        day_time = now_seconds % self.SECONDS_PER_DAY
        week_time = now_seconds % self.SECONDS_PER_WEEK

        hour = day_time / 3600
        weekday = int(week_time / self.SECONDS_PER_DAY)

        # ----------------------------------------------------
        # Daily activity curve
        #
        # Low at night
        # High during business hours
        # ----------------------------------------------------

        daily_wave = (math.sin((hour - 6) / 24 * 2 * math.pi) + 1) / 2

        # ----------------------------------------------------
        # Weekend reduction
        # ----------------------------------------------------

        is_weekend = weekday in (5, 6)
        weekend_factor = 0.75 if is_weekend else 1.0

        # ----------------------------------------------------
        # Base normalized load
        # ----------------------------------------------------

        normalized = 0.25 + 0.55 * daily_wave
        normalized *= weekend_factor

        # ----------------------------------------------------
        # Small random fluctuations
        # ----------------------------------------------------

        normalized += random.uniform(-0.03, 0.03)

        # ----------------------------------------------------
        # Rare traffic spikes
        # ----------------------------------------------------

        if random.random() < 0.002:
            normalized += random.uniform(0.1, 0.25)

        normalized = max(0.0, min(1.0, normalized))

        return min_cost + normalized * (max_cost - min_cost)
