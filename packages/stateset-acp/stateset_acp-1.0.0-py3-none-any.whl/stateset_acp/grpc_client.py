"""
StateSet ACP Handler - gRPC Client
"""

import json
from typing import Optional, Any
from pathlib import Path

import grpc
from grpc import aio

from stateset_acp.types import (
    CheckoutSession,
    CheckoutSessionWithOrder,
    CreateCheckoutSessionRequest,
    UpdateCheckoutSessionRequest,
    CompleteCheckoutSessionRequest,
    DelegatePaymentRequest,
    DelegatePaymentResponse,
    RequestItem,
    Customer,
    FulfillmentState,
    PaymentRequest,
    LineItem,
    Money,
    Totals,
    Links,
    Message,
    Order,
    FulfillmentChoice,
    EstimatedDelivery,
    CheckoutSessionStatus,
    MessageType,
    OrderStatus,
)

# Import generated protobuf modules
try:
    from stateset_acp.proto import acp_handler_pb2
    from stateset_acp.proto import acp_handler_pb2_grpc
    PROTO_AVAILABLE = True
except ImportError:
    PROTO_AVAILABLE = False


class AcpGrpcError(Exception):
    """gRPC error from the ACP handler."""

    def __init__(
        self,
        message: str,
        code: grpc.StatusCode = grpc.StatusCode.UNKNOWN,
        details: Optional[str] = None,
    ):
        super().__init__(message)
        self.code = code
        self.details = details

    def __repr__(self) -> str:
        return f"AcpGrpcError(code={self.code.name}, message={str(self)!r})"


def _money_to_dict(money: Any) -> Optional[dict[str, Any]]:
    """Convert proto Money to dict."""
    if money is None or (money.amount == 0 and not money.currency):
        return None
    return {"amount": money.amount, "currency": money.currency}


def _proto_to_checkout_session(proto: Any) -> CheckoutSession:
    """Convert proto CheckoutSession to Pydantic model."""
    items = []
    for item in proto.items:
        items.append(LineItem(
            id=item.id,
            title=item.title,
            quantity=item.quantity,
            unit_price=Money(**_money_to_dict(item.unit_price)) if _money_to_dict(item.unit_price) else None,
            variant_id=item.variant_id or None,
            sku=item.sku or None,
            image_url=item.image_url or None,
        ))

    totals = None
    if proto.HasField("totals"):
        totals = Totals(
            subtotal=Money(**_money_to_dict(proto.totals.subtotal)) if _money_to_dict(proto.totals.subtotal) else None,
            tax=Money(**_money_to_dict(proto.totals.tax)) if _money_to_dict(proto.totals.tax) else None,
            shipping=Money(**_money_to_dict(proto.totals.shipping)) if _money_to_dict(proto.totals.shipping) else None,
            discount=Money(**_money_to_dict(proto.totals.discount)) if _money_to_dict(proto.totals.discount) else None,
            grand_total=Money(**_money_to_dict(proto.totals.grand_total)) if _money_to_dict(proto.totals.grand_total) else None,
        )

    fulfillment = None
    if proto.HasField("fulfillment"):
        options = []
        for opt in proto.fulfillment.options:
            est_delivery = None
            if opt.HasField("est_delivery"):
                est_delivery = EstimatedDelivery(
                    earliest=opt.est_delivery.earliest or None,
                    latest=opt.est_delivery.latest or None,
                )
            options.append(FulfillmentChoice(
                id=opt.id,
                label=opt.label,
                price=Money(**_money_to_dict(opt.price)) if _money_to_dict(opt.price) else None,
                est_delivery=est_delivery,
            ))
        fulfillment = FulfillmentState(
            selected_id=proto.fulfillment.selected_id or None,
            options=options if options else None,
        )

    customer = None
    if proto.HasField("customer"):
        from stateset_acp.types import Address
        billing = None
        shipping = None
        if proto.customer.HasField("billing_address"):
            addr = proto.customer.billing_address
            billing = Address(
                name=addr.name or None,
                line1=addr.line1 or None,
                line2=addr.line2 or None,
                city=addr.city or None,
                region=addr.region or None,
                postal_code=addr.postal_code or None,
                country=addr.country or None,
                phone=addr.phone or None,
                email=addr.email or None,
            )
        if proto.customer.HasField("shipping_address"):
            addr = proto.customer.shipping_address
            shipping = Address(
                name=addr.name or None,
                line1=addr.line1 or None,
                line2=addr.line2 or None,
                city=addr.city or None,
                region=addr.region or None,
                postal_code=addr.postal_code or None,
                country=addr.country or None,
                phone=addr.phone or None,
                email=addr.email or None,
            )
        customer = Customer(billing_address=billing, shipping_address=shipping)

    links = None
    if proto.HasField("links"):
        links = Links(
            terms=proto.links.terms or None,
            privacy=proto.links.privacy or None,
            order_permalink=proto.links.order_permalink or None,
        )

    messages = None
    if proto.messages:
        messages = [
            Message(
                type=MessageType(msg.type),
                code=msg.code or None,
                message=msg.message,
                param=msg.param or None,
            )
            for msg in proto.messages
        ]

    return CheckoutSession(
        id=proto.id,
        status=CheckoutSessionStatus(proto.status),
        items=items,
        totals=totals,
        fulfillment=fulfillment,
        customer=customer,
        links=links,
        messages=messages,
        created_at=proto.created_at or None,
        updated_at=proto.updated_at or None,
    )


class AcpGrpcClient:
    """
    gRPC client for the StateSet ACP Handler.

    Example:
        >>> client = AcpGrpcClient(
        ...     address="localhost:50051",
        ...     api_key="api_key_demo_123"
        ... )
        >>> await client.connect()
        >>> session = await client.create_checkout_session(
        ...     items=[{"id": "prod_123", "quantity": 1}]
        ... )
        >>> await client.close()
    """

    def __init__(
        self,
        address: str = "localhost:50051",
        api_key: Optional[str] = None,
        use_tls: bool = False,
    ):
        """
        Initialize the gRPC client.

        Args:
            address: gRPC server address (e.g., localhost:50051)
            api_key: API key for authentication
            use_tls: Whether to use TLS (secure channel)
        """
        if not PROTO_AVAILABLE:
            raise ImportError(
                "gRPC protobuf modules not found. Please generate them first:\n"
                "python -m grpc_tools.protoc -I./proto --python_out=./stateset_acp/proto "
                "--grpc_python_out=./stateset_acp/proto ./proto/acp_handler.proto"
            )

        self.address = address
        self.api_key = api_key
        self.use_tls = use_tls
        self._channel: Optional[aio.Channel] = None
        self._stub: Optional[acp_handler_pb2_grpc.AcpHandlerStub] = None

    async def connect(self) -> None:
        """Establish gRPC connection."""
        if self.use_tls:
            self._channel = aio.secure_channel(
                self.address,
                grpc.ssl_channel_credentials(),
            )
        else:
            self._channel = aio.insecure_channel(self.address)

        self._stub = acp_handler_pb2_grpc.AcpHandlerStub(self._channel)

    async def close(self) -> None:
        """Close gRPC connection."""
        if self._channel:
            await self._channel.close()
            self._channel = None
            self._stub = None

    async def __aenter__(self) -> "AcpGrpcClient":
        """Enter async context."""
        await self.connect()
        return self

    async def __aexit__(self, *args: Any) -> None:
        """Exit async context."""
        await self.close()

    def _get_metadata(self) -> list[tuple[str, str]]:
        """Get gRPC metadata with authentication."""
        metadata = []
        if self.api_key:
            metadata.append(("authorization", f"Bearer {self.api_key}"))
        return metadata

    def _ensure_connected(self) -> None:
        """Ensure client is connected."""
        if self._stub is None:
            raise AcpGrpcError(
                "Client not connected. Call connect() first.",
                grpc.StatusCode.UNAVAILABLE,
            )

    async def create_checkout_session(
        self,
        items: list[RequestItem] | list[dict[str, Any]],
        customer: Optional[Customer | dict[str, Any]] = None,
        fulfillment: Optional[FulfillmentState | dict[str, Any]] = None,
    ) -> CheckoutSession:
        """
        Create a new checkout session.

        Args:
            items: List of items to add to the session
            customer: Customer information
            fulfillment: Fulfillment/shipping options

        Returns:
            The created checkout session
        """
        self._ensure_connected()

        # Build request items
        proto_items = []
        for item in items:
            if isinstance(item, dict):
                proto_items.append(acp_handler_pb2.RequestItem(
                    id=item["id"],
                    quantity=item["quantity"],
                ))
            else:
                proto_items.append(acp_handler_pb2.RequestItem(
                    id=item.id,
                    quantity=item.quantity,
                ))

        request = acp_handler_pb2.CreateCheckoutSessionRequest(items=proto_items)

        # Add customer if provided
        if customer is not None:
            cust = Customer(**customer) if isinstance(customer, dict) else customer
            if cust.billing_address:
                request.customer.billing_address.CopyFrom(
                    self._address_to_proto(cust.billing_address)
                )
            if cust.shipping_address:
                request.customer.shipping_address.CopyFrom(
                    self._address_to_proto(cust.shipping_address)
                )

        try:
            response = await self._stub.CreateCheckoutSession(
                request,
                metadata=self._get_metadata(),
            )
            return _proto_to_checkout_session(response)
        except grpc.aio.AioRpcError as e:
            raise AcpGrpcError(str(e.details()), e.code(), e.details())

    def _address_to_proto(self, address: Any) -> Any:
        """Convert Address to proto."""
        return acp_handler_pb2.Address(
            name=address.name or "",
            line1=address.line1 or "",
            line2=address.line2 or "",
            city=address.city or "",
            region=address.region or "",
            postal_code=address.postal_code or "",
            country=address.country or "",
            phone=address.phone or "",
            email=address.email or "",
        )

    async def get_checkout_session(self, session_id: str) -> CheckoutSession:
        """
        Get an existing checkout session.

        Args:
            session_id: The session ID

        Returns:
            The checkout session
        """
        self._ensure_connected()

        request = acp_handler_pb2.GetCheckoutSessionRequest(session_id=session_id)

        try:
            response = await self._stub.GetCheckoutSession(
                request,
                metadata=self._get_metadata(),
            )
            return _proto_to_checkout_session(response)
        except grpc.aio.AioRpcError as e:
            raise AcpGrpcError(str(e.details()), e.code(), e.details())

    async def update_checkout_session(
        self,
        session_id: str,
        items: Optional[list[RequestItem] | list[dict[str, Any]]] = None,
        customer: Optional[Customer | dict[str, Any]] = None,
        fulfillment: Optional[FulfillmentState | dict[str, Any]] = None,
    ) -> CheckoutSession:
        """
        Update an existing checkout session.

        Args:
            session_id: The session ID
            items: Updated list of items
            customer: Updated customer information
            fulfillment: Updated fulfillment options

        Returns:
            The updated checkout session
        """
        self._ensure_connected()

        request = acp_handler_pb2.UpdateCheckoutSessionRequest(session_id=session_id)

        if items is not None:
            proto_items = []
            for item in items:
                if isinstance(item, dict):
                    proto_items.append(acp_handler_pb2.RequestItem(
                        id=item["id"],
                        quantity=item["quantity"],
                    ))
                else:
                    proto_items.append(acp_handler_pb2.RequestItem(
                        id=item.id,
                        quantity=item.quantity,
                    ))
            request.items.items.extend(proto_items)

        if customer is not None:
            cust = Customer(**customer) if isinstance(customer, dict) else customer
            if cust.billing_address:
                request.customer.billing_address.CopyFrom(
                    self._address_to_proto(cust.billing_address)
                )
            if cust.shipping_address:
                request.customer.shipping_address.CopyFrom(
                    self._address_to_proto(cust.shipping_address)
                )

        try:
            response = await self._stub.UpdateCheckoutSession(
                request,
                metadata=self._get_metadata(),
            )
            return _proto_to_checkout_session(response)
        except grpc.aio.AioRpcError as e:
            raise AcpGrpcError(str(e.details()), e.code(), e.details())

    async def complete_checkout_session(
        self,
        session_id: str,
        payment: PaymentRequest | dict[str, Any],
        customer: Optional[Customer | dict[str, Any]] = None,
        fulfillment: Optional[FulfillmentState | dict[str, Any]] = None,
    ) -> CheckoutSessionWithOrder:
        """
        Complete a checkout session with payment.

        Args:
            session_id: The session ID
            payment: Payment information
            customer: Customer information
            fulfillment: Fulfillment options

        Returns:
            The completed session with order
        """
        self._ensure_connected()

        pay = PaymentRequest(**payment) if isinstance(payment, dict) else payment

        request = acp_handler_pb2.CompleteCheckoutSessionRequest(
            session_id=session_id,
            payment=acp_handler_pb2.PaymentRequest(
                delegated_token=pay.delegated_token or "",
                method=pay.method or "",
            ),
        )

        if customer is not None:
            cust = Customer(**customer) if isinstance(customer, dict) else customer
            if cust.billing_address:
                request.customer.billing_address.CopyFrom(
                    self._address_to_proto(cust.billing_address)
                )
            if cust.shipping_address:
                request.customer.shipping_address.CopyFrom(
                    self._address_to_proto(cust.shipping_address)
                )

        try:
            response = await self._stub.CompleteCheckoutSession(
                request,
                metadata=self._get_metadata(),
            )

            session = _proto_to_checkout_session(response.session)
            order = Order(
                id=response.order.id,
                checkout_session_id=response.order.checkout_session_id,
                status=OrderStatus(response.order.status),
                permalink_url=response.order.permalink_url or None,
            )

            return CheckoutSessionWithOrder(session=session, order=order)
        except grpc.aio.AioRpcError as e:
            raise AcpGrpcError(str(e.details()), e.code(), e.details())

    async def cancel_checkout_session(self, session_id: str) -> CheckoutSession:
        """
        Cancel a checkout session.

        Args:
            session_id: The session ID

        Returns:
            The canceled checkout session
        """
        self._ensure_connected()

        request = acp_handler_pb2.CancelCheckoutSessionRequest(session_id=session_id)

        try:
            response = await self._stub.CancelCheckoutSession(
                request,
                metadata=self._get_metadata(),
            )
            return _proto_to_checkout_session(response)
        except grpc.aio.AioRpcError as e:
            raise AcpGrpcError(str(e.details()), e.code(), e.details())

    async def delegate_payment(
        self,
        request: DelegatePaymentRequest | dict[str, Any],
    ) -> DelegatePaymentResponse:
        """
        Delegate payment (PSP vault token).

        Args:
            request: Delegate payment request

        Returns:
            The delegate payment response with token ID
        """
        self._ensure_connected()

        req = DelegatePaymentRequest(**request) if isinstance(request, dict) else request

        proto_request = acp_handler_pb2.DelegatePaymentRequest(
            payment_method=acp_handler_pb2.PaymentMethod(
                type=req.payment_method.type,
                card_number_type=req.payment_method.card_number_type or "",
                number=req.payment_method.number or "",
                exp_month=req.payment_method.exp_month or "",
                exp_year=req.payment_method.exp_year or "",
                name=req.payment_method.name or "",
                cvc=req.payment_method.cvc or "",
                cryptogram=req.payment_method.cryptogram or "",
                eci_value=req.payment_method.eci_value or "",
                checks_performed=req.payment_method.checks_performed or [],
                iin=req.payment_method.iin or "",
                display_card_funding_type=req.payment_method.display_card_funding_type or "",
                display_wallet_type=req.payment_method.display_wallet_type or "",
                display_brand=req.payment_method.display_brand or "",
                display_last4=req.payment_method.display_last4 or "",
                metadata_json=json.dumps(req.payment_method.metadata) if req.payment_method.metadata else "",
            ),
            allowance=acp_handler_pb2.Allowance(
                reason=req.allowance.reason,
                max_amount=req.allowance.max_amount,
                currency=req.allowance.currency,
                checkout_session_id=req.allowance.checkout_session_id or "",
                merchant_id=req.allowance.merchant_id or "",
                expires_at=req.allowance.expires_at or "",
            ),
            metadata_json=json.dumps(req.metadata) if req.metadata else "",
        )

        if req.billing_address:
            proto_request.billing_address.CopyFrom(
                acp_handler_pb2.BillingAddress(
                    name=req.billing_address.name or "",
                    line_one=req.billing_address.line_one or "",
                    line_two=req.billing_address.line_two or "",
                    city=req.billing_address.city or "",
                    state=req.billing_address.state or "",
                    country=req.billing_address.country or "",
                    postal_code=req.billing_address.postal_code or "",
                )
            )

        if req.risk_signals:
            for signal in req.risk_signals:
                proto_request.risk_signals.append(
                    acp_handler_pb2.RiskSignal(
                        type=signal.type,
                        score=signal.score,
                        action=signal.action or "",
                    )
                )

        try:
            response = await self._stub.DelegatePayment(
                proto_request,
                metadata=self._get_metadata(),
            )

            return DelegatePaymentResponse(
                id=response.id,
                created=response.created,
                metadata=json.loads(response.metadata_json) if response.metadata_json else None,
            )
        except grpc.aio.AioRpcError as e:
            raise AcpGrpcError(str(e.details()), e.code(), e.details())
