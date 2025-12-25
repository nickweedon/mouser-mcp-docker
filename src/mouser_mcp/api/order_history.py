"""Mouser Order History API - View past orders."""

from typing import Any

from ..client import get_client


async def list_order_history(
    days: int = 30,
) -> dict[str, Any]:
    """
    List order history for the past N days.

    Retrieves a summary of past orders including order numbers, dates,
    statuses, and totals. Useful for tracking order history and status.

    Args:
        days: Number of days to look back (default 30, must be positive)

    Returns:
        List of past orders with summary information

    Raises:
        ValueError: If days is not positive
        RuntimeError: If API request fails
    """
    if days < 1:
        raise ValueError("Days must be at least 1")

    client = get_client()
    payload = {"Days": days}

    try:
        response = client.post("orderhistory/query", json=payload)
        return response
    except Exception as e:
        raise RuntimeError(f"Failed to get order history: {e}") from e
