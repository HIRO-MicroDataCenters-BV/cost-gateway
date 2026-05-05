from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Cost:
    name: str
    description: str
    value: Decimal
    is_custom: bool
