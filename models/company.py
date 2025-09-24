from typing import List
from dataclasses import dataclass, field

from .product import Product


@dataclass
class Company:
    id: int
    name: str
    organizationNumber: int
    pricelistUrl: str
    products: List[Product] = field(default_factory=list)