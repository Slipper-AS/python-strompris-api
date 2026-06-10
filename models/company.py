import re
from typing import List, Optional
from dataclasses import dataclass, field

from .product import Product


@dataclass
class Company:
    id: int
    name: str
    organizationNumber: int
    pricelistUrl: str
    products: List[Product] = field(default_factory=list)

    @property
    def pricelist_domain(self) -> Optional[str]:
        """Extract the root domain from pricelistUrl. Returns None if absent or no match."""
        if not self.pricelistUrl:
            return None
        match = re.match(r"^(https?:\/\/)?([a-z0-9]([a-z0-9-]*[a-z0-9])?\.)+[a-z]{2,}", self.pricelistUrl)
        return match.group(0) if match else None