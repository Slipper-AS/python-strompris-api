from dataclasses import dataclass


@dataclass
class SalesNetwork:
    id: str
    type: str
    name: str
    kwPrice: float
    purchaseKwPrice: float