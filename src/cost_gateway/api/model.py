from decimal import Decimal

from pydantic import BaseModel

from cost_gateway.cost.cost import Cost


class CostModel(BaseModel):
    name: str
    description: str
    value: Decimal
    is_custom: bool

    @staticmethod
    def from_object(cost: Cost) -> "CostModel":
        return CostModel(name=cost.name, description=cost.description, value=cost.value, is_custom=cost.is_custom)
