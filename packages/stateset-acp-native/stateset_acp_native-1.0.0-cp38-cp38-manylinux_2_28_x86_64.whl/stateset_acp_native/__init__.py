"""
StateSet ACP Native - Python bindings powered by PyO3/Rust

This module provides high-performance native bindings for the StateSet
Agentic Commerce Protocol Handler.

Example:
    >>> from stateset_acp_native import AcpClient, RequestItem, PaymentRequest
    >>>
    >>> client = AcpClient(api_key="your_api_key")
    >>>
    >>> # Create a checkout session
    >>> session = client.create_checkout_session([
    ...     RequestItem("prod_laptop_001", 1),
    ...     RequestItem("prod_mouse_002", 2),
    ... ])
    >>>
    >>> print(f"Session ID: {session.id}")
    >>> print(f"Grand Total: ${session.totals.grand_total.amount / 100:.2f}")
    >>>
    >>> # Complete checkout
    >>> result = client.complete_checkout_session(
    ...     session.id,
    ...     PaymentRequest(delegated_token="tok_xxx")
    ... )
    >>> print(f"Order ID: {result.order.id}")
"""

from .stateset_acp_native import (
    Money,
    Address,
    Customer,
    LineItem,
    Totals,
    CheckoutSession,
    Order,
    CheckoutSessionWithOrder,
    RequestItem,
    PaymentRequest,
    AcpClient,
    version,
)

__version__ = version()
__all__ = [
    "Money",
    "Address",
    "Customer",
    "LineItem",
    "Totals",
    "CheckoutSession",
    "Order",
    "CheckoutSessionWithOrder",
    "RequestItem",
    "PaymentRequest",
    "AcpClient",
    "version",
]
