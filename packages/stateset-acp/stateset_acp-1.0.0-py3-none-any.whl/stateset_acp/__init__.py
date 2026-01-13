"""
StateSet ACP Handler - Python Client

Official Python bindings for the StateSet Agentic Commerce Protocol Handler.
Supports both HTTP REST and gRPC transports.

Example:
    >>> from stateset_acp import AcpHttpClient, AcpGrpcClient
    >>>
    >>> # HTTP Client
    >>> client = AcpHttpClient(
    ...     base_url="http://localhost:8080",
    ...     api_key="api_key_demo_123"
    ... )
    >>>
    >>> session = await client.create_checkout_session(
    ...     items=[{"id": "prod_123", "quantity": 1}]
    ... )
    >>>
    >>> # gRPC Client
    >>> grpc_client = AcpGrpcClient(
    ...     address="localhost:50051",
    ...     api_key="api_key_demo_123"
    ... )
    >>>
    >>> session = await grpc_client.create_checkout_session(
    ...     items=[{"id": "prod_123", "quantity": 1}]
    ... )
"""

from stateset_acp.http_client import AcpHttpClient, AcpApiError
from stateset_acp.grpc_client import AcpGrpcClient, AcpGrpcError
from stateset_acp.types import (
    CheckoutSessionStatus,
    MessageType,
    OrderStatus,
    Money,
    Totals,
    Address,
    Customer,
    EstimatedDelivery,
    FulfillmentChoice,
    FulfillmentState,
    LineItem,
    RequestItem,
    Links,
    Message,
    Order,
    CheckoutSession,
    CheckoutSessionWithOrder,
    CreateCheckoutSessionRequest,
    UpdateCheckoutSessionRequest,
    PaymentRequest,
    CompleteCheckoutSessionRequest,
    PaymentMethod,
    BillingAddress,
    Allowance,
    RiskSignal,
    DelegatePaymentRequest,
    DelegatePaymentResponse,
    AcpClientConfig,
)

__version__ = "1.0.0"
__all__ = [
    # Clients
    "AcpHttpClient",
    "AcpGrpcClient",
    # Errors
    "AcpApiError",
    "AcpGrpcError",
    # Enums
    "CheckoutSessionStatus",
    "MessageType",
    "OrderStatus",
    # Types
    "Money",
    "Totals",
    "Address",
    "Customer",
    "EstimatedDelivery",
    "FulfillmentChoice",
    "FulfillmentState",
    "LineItem",
    "RequestItem",
    "Links",
    "Message",
    "Order",
    "CheckoutSession",
    "CheckoutSessionWithOrder",
    "CreateCheckoutSessionRequest",
    "UpdateCheckoutSessionRequest",
    "PaymentRequest",
    "CompleteCheckoutSessionRequest",
    "PaymentMethod",
    "BillingAddress",
    "Allowance",
    "RiskSignal",
    "DelegatePaymentRequest",
    "DelegatePaymentResponse",
    "AcpClientConfig",
]
