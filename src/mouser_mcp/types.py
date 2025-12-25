"""
Mouser API Type Definitions

TypedDict classes for structured data from the Mouser Electronics API.
These types provide type hints and documentation for API responses.
"""

from typing import TypedDict

# =============================================================================
# Search API Types
# =============================================================================


class PriceBreak(TypedDict, total=False):
    """Price break information for a part."""

    Quantity: int
    Price: str
    Currency: str


class PartData(TypedDict, total=False):
    """Electronic component part data from Mouser search."""

    MouserPartNumber: str
    ManufacturerPartNumber: str
    Manufacturer: str
    Description: str
    DataSheetUrl: str
    ImagePath: str
    ProductDetailUrl: str
    Category: str
    LifecycleStatus: str
    ROHSStatus: str
    Availability: str
    Min: int  # Minimum order quantity
    Mult: int  # Order multiple
    LeadTime: str
    PriceBreaks: list[PriceBreak]


class SearchResults(TypedDict, total=False):
    """Search results container."""

    NumberOfResult: int
    Parts: list[PartData]


class SearchResponse(TypedDict, total=False):
    """Response from search API."""

    SearchResults: SearchResults
    Errors: list[dict]


# =============================================================================
# Cart API Types
# =============================================================================


class CartItem(TypedDict, total=False):
    """Item in a shopping cart."""

    MouserPartNumber: str
    Quantity: int
    CustomerPartNumber: str


class CartPricing(TypedDict, total=False):
    """Cart pricing information."""

    Subtotal: str
    Tax: str
    Total: str
    Currency: str


class Cart(TypedDict, total=False):
    """Shopping cart data."""

    CartKey: str
    CartItems: list[CartItem]
    Pricing: CartPricing


# =============================================================================
# Order API Types
# =============================================================================


class Address(TypedDict, total=False):
    """Shipping or billing address."""

    AddressLine1: str
    AddressLine2: str
    City: str
    StateOrProvince: str
    PostalCode: str
    Country: str


class ShippingMethod(TypedDict, total=False):
    """Available shipping method."""

    MethodId: str
    MethodName: str
    Cost: str
    Currency: str


class PaymentMethod(TypedDict, total=False):
    """Available payment method."""

    MethodId: str
    MethodName: str


class OrderOptions(TypedDict, total=False):
    """Available order options."""

    BillingAddresses: list[Address]
    ShippingAddresses: list[Address]
    ShippingMethods: list[ShippingMethod]
    PaymentMethods: list[PaymentMethod]
    CurrencyCode: str


class Order(TypedDict, total=False):
    """Order information."""

    OrderNumber: str
    WebOrderNumber: str
    Status: str
    OrderTotal: str
    Currency: str
    OrderDate: str
    Items: list[CartItem]
    ShippingAddress: Address
    BillingAddress: Address


# =============================================================================
# Order History API Types
# =============================================================================


class OrderHistoryItem(TypedDict, total=False):
    """Summary of a past order."""

    OrderNumber: str
    WebOrderNumber: str
    OrderDate: str
    Status: str
    OrderTotal: str
    Currency: str


class OrderHistory(TypedDict, total=False):
    """Order history response."""

    Orders: list[OrderHistoryItem]


# =============================================================================
# Common Types
# =============================================================================


class ErrorDetail(TypedDict):
    """API error detail."""

    Code: str
    Message: str
    ResourceKey: str


class ErrorResponse(TypedDict):
    """Standard error response."""

    Errors: list[ErrorDetail]
