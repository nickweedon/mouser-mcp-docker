"""Mouser Cart API - Manage shopping cart operations."""

from typing import Any

from ..client import get_client


async def get_cart(cart_key: str) -> dict[str, Any]:
    """
    Retrieve shopping cart contents by cart key.

    Gets the current state of a shopping cart including all items,
    quantities, pricing, and totals.

    Args:
        cart_key: Unique cart identifier (UUID format)

    Returns:
        Cart details with items, pricing, and subtotal

    Raises:
        ValueError: If cart_key is empty
        RuntimeError: If API request fails or cart not found
    """
    if not cart_key.strip():
        raise ValueError("Cart key cannot be empty")

    client = get_client()

    try:
        # Per Mouser API docs: GET /api/v{version}/cart with cartKey as query param
        response = client.get("cart", params={"cartKey": cart_key})
        return response
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve cart: {e}") from e


async def add_to_cart(
    cart_key: str,
    mouser_part_number: str,
    quantity: int,
    customer_part_number: str = "",
) -> dict[str, Any]:
    """
    Add an item to an existing shopping cart.

    Adds a single part to the cart with the specified quantity. If the part
    already exists in the cart, the quantity will be updated.

    Args:
        cart_key: Unique cart identifier (UUID format)
        mouser_part_number: Mouser part number to add
        quantity: Quantity to add (must be positive integer)
        customer_part_number: Optional customer reference number

    Returns:
        Updated cart details

    Raises:
        ValueError: If cart_key or part_number is empty, or quantity invalid
        RuntimeError: If API request fails
    """
    if not cart_key.strip():
        raise ValueError("Cart key cannot be empty")
    if not mouser_part_number.strip():
        raise ValueError("Mouser part number cannot be empty")
    if quantity < 1:
        raise ValueError("Quantity must be at least 1")

    client = get_client()
    payload = {
        "CartKey": cart_key,
        "CartItems": [
            {
                "MouserPartNumber": mouser_part_number,
                "Quantity": quantity,
                "CustomerPartNumber": customer_part_number,
            }
        ],
    }

    try:
        # Per Mouser API docs: POST /api/v{version}/cart/items/insert
        response = client.post("cart/items/insert", json=payload)
        return response
    except Exception as e:
        raise RuntimeError(f"Failed to add item to cart: {e}") from e


async def update_cart_item(
    cart_key: str,
    mouser_part_number: str,
    quantity: int,
) -> dict[str, Any]:
    """
    Update the quantity of an item in the cart.

    Changes the quantity of an existing cart item. To remove an item,
    set quantity to 0.

    Args:
        cart_key: Unique cart identifier
        mouser_part_number: Mouser part number to update
        quantity: New quantity (0 to remove item)

    Returns:
        Updated cart details

    Raises:
        ValueError: If cart_key or part_number is empty, or quantity negative
        RuntimeError: If API request fails
    """
    if not cart_key.strip():
        raise ValueError("Cart key cannot be empty")
    if not mouser_part_number.strip():
        raise ValueError("Mouser part number cannot be empty")
    if quantity < 0:
        raise ValueError("Quantity cannot be negative")

    client = get_client()
    payload = {
        "CartKey": cart_key,
        "CartItems": [
            {
                "MouserPartNumber": mouser_part_number,
                "Quantity": quantity,
            }
        ],
    }

    try:
        # Per Mouser API docs: POST /api/v{version}/cart/items/update
        response = client.post("cart/items/update", json=payload)
        return response
    except Exception as e:
        raise RuntimeError(f"Failed to update cart item: {e}") from e
