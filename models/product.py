from typing import List, Optional
from dataclasses import dataclass, field

from .association import Association
from .sales_network import SalesNetwork


@dataclass
class Product:
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
    vatExemption: bool
    salesNetworks: List[SalesNetwork] = field(default_factory=list)
    associations: List[Association] = field(default_factory=list)