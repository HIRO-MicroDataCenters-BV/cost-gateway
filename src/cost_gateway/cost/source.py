from abc import ABC, abstractmethod


class CostSource(ABC):
    @abstractmethod
    async def get_cost(self, name: str) -> float:
        pass
