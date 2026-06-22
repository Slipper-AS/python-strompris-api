from decimal import Decimal
from typing import List, Optional, ClassVar
from dataclasses import dataclass, field

from .association import Association
from .sales_network import SalesNetwork
from datetime import datetime

@dataclass
class Product:
    # Norwegian VAT (mva) is 25 %; multiply by this rate to get the ex-VAT amount.
    NON_MVA_RATE: ClassVar[Decimal] = Decimal("0.80")

    id: int
    productId: int
    name: str
    agreementTime: int
    agreementTimeUnit: str
    billingFrequency: int
    billingFrequencyUnit: str
    addonPriceMinimumFixedFor: int
    addonPriceMinimumFixedForUnit: str
    productType: str
    paymentType: str
    monthlyFee: float
    addonPrice: float
    elCertificatePrice: float
    maxKwhPerYear: float
    feeMandatoryType: str
    feePostalLetter: float
    feePostalLetterApplied: bool
    otherConditions: str
    orderUrl: str
    applicableToCustomerType: str
    standardAlert: Optional[str]
    cabinProduct: bool
    priceChangedAt: str
    purchaseAddonPrice: float
    expiredAt: Optional[str]
    createdAt: str
    updatedAt: str
    deletedAt: Optional[str]
    endDate: datetime
    vatExemption: bool
    linkedProduct: int
    canBeCombinedWithPlus: bool
    salesNetworks: List[SalesNetwork] = field(default_factory=list)
    associations: List[Association] = field(default_factory=list)

    @property
    def is_binding(self) -> bool:
        """Return True if the product has a positive agreement time (binding contract)."""
        if not self.agreementTime:
            return False
        return self.agreementTime > 0

    @property
    def is_tempting_offer(self) -> bool:
        """
        Return True if this product should be classified as a TEMPTING offer.

        A product is TEMPTING when:
        - addonPrice is negative, OR
        - addonPrice is 0 and monthlyFee is also 0 or negative.
        """
        return self.addonPrice < 0 or (self.addonPrice == 0 and self.monthlyFee <= 0)

    @property
    def max_consumption(self) -> Optional[float]:
        """Return None when there is no consumption cap (maxKwhPerYear == 0)."""
        return None if self.maxKwhPerYear == 0 else self.maxKwhPerYear

    @property
    def tempting_max_length(self) -> int:
        """Fixed-for length that applies only to TEMPTING offers; 0 otherwise."""
        return self.addonPriceMinimumFixedFor if self.is_tempting_offer else 0

    @property
    def fixed_fee_ex_vat(self) -> Decimal:
        """Monthly fixed fee excluding VAT."""
        return Decimal(self.monthlyFee) * self.NON_MVA_RATE

    @property
    def price_per_kwh_ex_vat(self) -> Decimal:
        """Add-on price per kWh excluding VAT."""
        return Decimal(self.addonPrice) * self.NON_MVA_RATE

    @property
    def postal_fee_ex_vat(self) -> Decimal:
        """Postal letter fee excluding VAT."""
        return Decimal(self.feePostalLetter) * self.NON_MVA_RATE
