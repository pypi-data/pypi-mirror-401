"""
StateSet ACP Handler - HTTP REST Client
"""

from typing import Optional, Any
import httpx

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
)


class AcpApiError(Exception):
    """API error from the ACP handler."""

    def __init__(
        self,
        message: str,
        error_type: str = "processing_error",
        code: str = "unknown",
        param: Optional[str] = None,
        status_code: int = 500,
    ):
        super().__init__(message)
        self.type = error_type
        self.code = code
        self.param = param
        self.status_code = status_code

    def __repr__(self) -> str:
        return f"AcpApiError(type={self.type!r}, code={self.code!r}, message={str(self)!r})"


class AcpHttpClient:
    """
    HTTP REST client for the StateSet ACP Handler.

    Example:
        >>> client = AcpHttpClient(
        ...     base_url="http://localhost:8080",
        ...     api_key="api_key_demo_123"
        ... )
        >>> session = await client.create_checkout_session(
        ...     items=[{"id": "prod_123", "quantity": 1}]
        ... )
    """

    def __init__(
        self,
        base_url: str = "http://localhost:8080",
        api_key: Optional[str] = None,
        timeout: float = 30.0,
    ):
        """
        Initialize the HTTP client.

        Args:
            base_url: Base URL of the ACP handler (e.g., http://localhost:8080)
            api_key: API key for authentication
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout
        self._client: Optional[httpx.AsyncClient] = None

    async def __aenter__(self) -> "AcpHttpClient":
        """Enter async context."""
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=self.timeout,
            headers=self._get_headers(),
        )
        return self

    async def __aexit__(self, *args: Any) -> None:
        """Exit async context."""
        if self._client:
            await self._client.aclose()
            self._client = None

    def _get_headers(self) -> dict[str, str]:
        """Get request headers."""
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client."""
        if self._client is None:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                timeout=self.timeout,
                headers=self._get_headers(),
            )
        return self._client

    async def _request(
        self,
        method: str,
        path: str,
        json: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """Make an HTTP request."""
        client = await self._get_client()
        response = await client.request(method, path, json=json)

        if response.status_code >= 400:
            try:
                error_data = response.json()
                raise AcpApiError(
                    message=error_data.get("message", "Unknown error"),
                    error_type=error_data.get("type", "processing_error"),
                    code=error_data.get("code", "unknown"),
                    param=error_data.get("param"),
                    status_code=response.status_code,
                )
            except ValueError:
                raise AcpApiError(
                    message=response.text or "Unknown error",
                    status_code=response.status_code,
                )

        return response.json() if response.text else {}

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
        request = CreateCheckoutSessionRequest(
            items=[RequestItem(**i) if isinstance(i, dict) else i for i in items],
            customer=Customer(**customer) if isinstance(customer, dict) else customer,
            fulfillment=FulfillmentState(**fulfillment) if isinstance(fulfillment, dict) else fulfillment,
        )
        data = await self._request("POST", "/checkout_sessions", json=request.model_dump(exclude_none=True))
        return CheckoutSession(**data)

    async def get_checkout_session(self, session_id: str) -> CheckoutSession:
        """
        Get an existing checkout session.

        Args:
            session_id: The session ID

        Returns:
            The checkout session
        """
        data = await self._request("GET", f"/checkout_sessions/{session_id}")
        return CheckoutSession(**data)

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
        request_data: dict[str, Any] = {}
        if items is not None:
            request_data["items"] = [
                (RequestItem(**i) if isinstance(i, dict) else i).model_dump()
                for i in items
            ]
        if customer is not None:
            cust = Customer(**customer) if isinstance(customer, dict) else customer
            request_data["customer"] = cust.model_dump(exclude_none=True)
        if fulfillment is not None:
            ful = FulfillmentState(**fulfillment) if isinstance(fulfillment, dict) else fulfillment
            request_data["fulfillment"] = ful.model_dump(exclude_none=True)

        data = await self._request("POST", f"/checkout_sessions/{session_id}", json=request_data)
        return CheckoutSession(**data)

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
            payment: Payment information (delegated token or method)
            customer: Customer information
            fulfillment: Fulfillment options

        Returns:
            The completed session with order
        """
        pay = PaymentRequest(**payment) if isinstance(payment, dict) else payment
        request_data: dict[str, Any] = {"payment": pay.model_dump(exclude_none=True)}

        if customer is not None:
            cust = Customer(**customer) if isinstance(customer, dict) else customer
            request_data["customer"] = cust.model_dump(exclude_none=True)
        if fulfillment is not None:
            ful = FulfillmentState(**fulfillment) if isinstance(fulfillment, dict) else fulfillment
            request_data["fulfillment"] = ful.model_dump(exclude_none=True)

        data = await self._request("POST", f"/checkout_sessions/{session_id}/complete", json=request_data)
        return CheckoutSessionWithOrder(**data)

    async def cancel_checkout_session(self, session_id: str) -> CheckoutSession:
        """
        Cancel a checkout session.

        Args:
            session_id: The session ID

        Returns:
            The canceled checkout session
        """
        data = await self._request("POST", f"/checkout_sessions/{session_id}/cancel")
        return CheckoutSession(**data)

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
        req = DelegatePaymentRequest(**request) if isinstance(request, dict) else request
        data = await self._request(
            "POST",
            "/agentic_commerce/delegate_payment",
            json=req.model_dump(exclude_none=True),
        )
        return DelegatePaymentResponse(**data)

    async def health_check(self) -> dict[str, str]:
        """
        Check the health of the service.

        Returns:
            Health status
        """
        return await self._request("GET", "/health")

    async def close(self) -> None:
        """Close the HTTP client."""
        if self._client:
            await self._client.aclose()
            self._client = None
