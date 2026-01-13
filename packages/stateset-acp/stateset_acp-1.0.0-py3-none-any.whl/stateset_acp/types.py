"""
StateSet ACP Handler - Python Type Definitions
"""

from enum import IntEnum
from typing import Optional, Any
from pydantic import BaseModel, Field


class CheckoutSessionStatus(IntEnum):
    """Checkout session status enum."""
    UNSPECIFIED = 0
    NOT_READY_FOR_PAYMENT = 1
    READY_FOR_PAYMENT = 2
    COMPLETED = 3
    CANCELED = 4


class MessageType(IntEnum):
    """Message type enum."""
    UNSPECIFIED = 0
    INFO = 1
    WARNING = 2
    ERROR = 3


class OrderStatus(IntEnum):
    """Order status enum."""
    UNSPECIFIED = 0
    PLACED = 1
    FAILED = 2
    REFUNDED = 3


class Money(BaseModel):
    """Monetary amount."""
    amount: int
    currency: str


class Totals(BaseModel):
    """Checkout totals."""
    subtotal: Optional[Money] = None
    tax: Optional[Money] = None
    shipping: Optional[Money] = None
    discount: Optional[Money] = None
    grand_total: Optional[Money] = None


class Address(BaseModel):
    """Physical address."""
    name: Optional[str] = None
    line1: Optional[str] = None
    line2: Optional[str] = None
    city: Optional[str] = None
    region: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None


class Customer(BaseModel):
    """Customer information."""
    billing_address: Optional[Address] = None
    shipping_address: Optional[Address] = None


class EstimatedDelivery(BaseModel):
    """Estimated delivery window."""
    earliest: Optional[str] = None
    latest: Optional[str] = None


class FulfillmentChoice(BaseModel):
    """Fulfillment/shipping option."""
    id: str
    label: str
    price: Optional[Money] = None
    est_delivery: Optional[EstimatedDelivery] = None


class FulfillmentState(BaseModel):
    """Fulfillment state with selected option."""
    selected_id: Optional[str] = None
    options: Optional[list[FulfillmentChoice]] = None


class LineItem(BaseModel):
    """Line item in a checkout session."""
    id: str
    title: str
    quantity: int
    unit_price: Optional[Money] = None
    variant_id: Optional[str] = None
    sku: Optional[str] = None
    image_url: Optional[str] = None


class RequestItem(BaseModel):
    """Item request for creating/updating sessions."""
    id: str
    quantity: int


class Links(BaseModel):
    """Helpful links for the checkout."""
    terms: Optional[str] = None
    privacy: Optional[str] = None
    order_permalink: Optional[str] = None


class Message(BaseModel):
    """Status message."""
    type: MessageType = MessageType.INFO
    code: Optional[str] = None
    message: str
    param: Optional[str] = None


class Order(BaseModel):
    """Order created from checkout."""
    id: str
    checkout_session_id: str
    status: OrderStatus = OrderStatus.UNSPECIFIED
    permalink_url: Optional[str] = None


class CheckoutSession(BaseModel):
    """Checkout session."""
    id: str
    status: CheckoutSessionStatus = CheckoutSessionStatus.UNSPECIFIED
    items: list[LineItem] = Field(default_factory=list)
    totals: Optional[Totals] = None
    fulfillment: Optional[FulfillmentState] = None
    customer: Optional[Customer] = None
    links: Optional[Links] = None
    messages: Optional[list[Message]] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class CheckoutSessionWithOrder(BaseModel):
    """Checkout session with associated order."""
    session: CheckoutSession
    order: Order


class CreateCheckoutSessionRequest(BaseModel):
    """Request to create a checkout session."""
    items: list[RequestItem]
    customer: Optional[Customer] = None
    fulfillment: Optional[FulfillmentState] = None


class UpdateCheckoutSessionRequest(BaseModel):
    """Request to update a checkout session."""
    session_id: str
    items: Optional[list[RequestItem]] = None
    customer: Optional[Customer] = None
    fulfillment: Optional[FulfillmentState] = None


class PaymentRequest(BaseModel):
    """Payment information."""
    delegated_token: Optional[str] = None
    method: Optional[str] = None


class CompleteCheckoutSessionRequest(BaseModel):
    """Request to complete a checkout session."""
    session_id: str
    payment: PaymentRequest
    customer: Optional[Customer] = None
    fulfillment: Optional[FulfillmentState] = None


class PaymentMethod(BaseModel):
    """Payment method details for delegated payment."""
    type: str
    card_number_type: Optional[str] = None
    number: Optional[str] = None
    exp_month: Optional[str] = None
    exp_year: Optional[str] = None
    name: Optional[str] = None
    cvc: Optional[str] = None
    cryptogram: Optional[str] = None
    eci_value: Optional[str] = None
    checks_performed: Optional[list[str]] = None
    iin: Optional[str] = None
    display_card_funding_type: Optional[str] = None
    display_wallet_type: Optional[str] = None
    display_brand: Optional[str] = None
    display_last4: Optional[str] = None
    metadata: Optional[dict[str, Any]] = None


class BillingAddress(BaseModel):
    """Billing address for delegated payment."""
    name: Optional[str] = None
    line_one: Optional[str] = None
    line_two: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None


class Allowance(BaseModel):
    """Payment allowance."""
    reason: str
    max_amount: int
    currency: str
    checkout_session_id: Optional[str] = None
    merchant_id: Optional[str] = None
    expires_at: Optional[str] = None


class RiskSignal(BaseModel):
    """Risk signal for fraud detection."""
    type: str
    score: int
    action: Optional[str] = None


class DelegatePaymentRequest(BaseModel):
    """Request to delegate payment (PSP vault)."""
    payment_method: PaymentMethod
    allowance: Allowance
    billing_address: Optional[BillingAddress] = None
    risk_signals: Optional[list[RiskSignal]] = None
    metadata: Optional[dict[str, Any]] = None


class DelegatePaymentResponse(BaseModel):
    """Response from delegated payment."""
    id: str
    created: str
    metadata: Optional[dict[str, Any]] = None


class AcpClientConfig(BaseModel):
    """Client configuration."""
    base_url: str = "http://localhost:8080"
    grpc_address: str = "localhost:50051"
    api_key: Optional[str] = None
    timeout: float = 30.0
