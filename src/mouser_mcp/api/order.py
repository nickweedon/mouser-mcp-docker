"""Mouser Order API - Submit and manage orders."""

from typing import Any

from ..client import get_client


async def get_order_options(cart_key: str) -> dict[str, Any]:
    """
    Get available order options for a cart.

    Retrieves billing/shipping addresses, payment methods, shipping options,
    and other order configuration details for the specified cart.

    Args:
        cart_key: Cart key to get order options for

    Returns:
        Available addresses, payment methods, shipping options, and currency

    Raises:
        ValueError: If cart_key is empty
        RuntimeError: If API request fails
    """
    if not cart_key.strip():
        raise ValueError("Cart key cannot be empty")

    client = get_client()
    payload = {"CartKey": cart_key}

    try:
        response = client.post("order/options/query", json=payload)
        return response
    except Exception as e:
        raise RuntimeError(f"Failed to get order options: {e}") from e


async def get_order(order_number: str) -> dict[str, Any]:
    """
    Get order details by order number.

    Retrieves complete order information including status, items, totals,
    shipping details, and tracking information.

    Args:
        order_number: Mouser order number or web order number

    Returns:
        Order details including status, items, addresses, and total

    Raises:
        ValueError: If order_number is empty
        RuntimeError: If API request fails or order not found
    """
    if not order_number.strip():
        raise ValueError("Order number cannot be empty")

    client = get_client()
    payload = {"OrderNumber": order_number}

    try:
        response = client.post("order/get", json=payload)
        return response
    except Exception as e:
        raise RuntimeError(f"Failed to get order: {e}") from e
