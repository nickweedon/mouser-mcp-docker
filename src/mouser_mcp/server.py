"""
Mouser Electronics MCP Server

This is the main entry point for the Mouser MCP server. It registers all tools,
resources, and prompts for interacting with the Mouser Electronics API.

Features:
- Search for electronic components by keyword or part number
- Manage shopping carts and add items
- Retrieve order information and history
- Access pricing, availability, and datasheets
"""

import logging
import time
from collections.abc import Callable
from functools import wraps
from typing import Any

from fastmcp import FastMCP

from .api import cart, order, order_history, search
from .client import get_client_config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Initialize the MCP server
mcp = FastMCP(
    name="Mouser Electronics MCP Server",
    instructions="""
    This server provides access to the Mouser Electronics API for electronic component
    search, shopping cart management, and order processing.

    Available capabilities:
    - Search for electronic components by keyword or part number
    - Retrieve component specifications, pricing, and availability
    - View datasheets and product details
    - Manage shopping carts and add items
    - Retrieve order information and options
    - View order history

    Rate limits: 50 results per search, 30 calls/minute, 1000 calls/day
    """,
)


def timing_middleware(func: Callable) -> Callable:
    """Middleware to log execution time for tools."""

    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.time()
        try:
            result = await func(*args, **kwargs)
            elapsed = time.time() - start_time
            logger.info(f"{func.__name__} completed in {elapsed:.3f}s")
            return result
        except Exception as e:
            elapsed = time.time() - start_time
            logger.error(f"{func.__name__} failed after {elapsed:.3f}s: {e}")
            raise

    return wrapper


# =============================================================================
# TOOLS
# =============================================================================
# Register your MCP tools here. Tools are functions that can be called by
# MCP clients to perform actions.


@mcp.tool()
async def health_check() -> dict[str, Any]:
    """
    Check the health status of the Mouser MCP server.

    Returns:
        A dictionary with the server status and API configuration info.
    """
    config = get_client_config()
    return {
        "status": "healthy",
        "server": "Mouser Electronics MCP Server",
        "version": "0.1.0",
        "part_api_configured": bool(config.get("part_api_key")),
        "order_api_configured": bool(config.get("order_api_key")),
        "base_url": config.get("api_base_url"),
    }


# Register Search API tools
mcp.tool()(search.search_by_keyword)
mcp.tool()(search.search_by_part_number)

# Register Cart API tools
mcp.tool()(cart.get_cart)
mcp.tool()(cart.add_to_cart)
mcp.tool()(cart.update_cart_item)

# Register Order API tools
mcp.tool()(order.get_order_options)
mcp.tool()(order.get_order)

# Register Order History API tools
mcp.tool()(order_history.list_order_history)


# =============================================================================
# RESOURCES
# =============================================================================
# Register your MCP resources here. Resources provide read-only access to
# data that clients can retrieve.


@mcp.resource("mouser://status")
async def get_server_status() -> str:
    """Get the Mouser MCP server status and configuration."""
    config = get_client_config()

    # Check if API keys are configured (don't expose actual keys)
    part_key_configured = bool(config.get("part_api_key"))
    order_key_configured = bool(config.get("order_api_key"))

    return f"""
Mouser MCP Server Status:
- Base URL: {config["api_base_url"]}
- Part Search API Key: {"✓ Configured" if part_key_configured else "✗ Not configured"}
- Order API Key: {"✓ Configured" if order_key_configured else "✗ Not configured"}
- Timeout: {config["timeout"]}s
- Debug Mode: {config["debug"]}
    """


# =============================================================================
# PROMPTS
# =============================================================================
# Register your MCP prompts here. Prompts are templates that help guide
# how clients interact with your server.


@mcp.prompt()
def component_search_workflow() -> str:
    """Guide for searching and purchasing electronic components."""
    return """
    To search for and purchase electronic components from Mouser:

    1. Search for components:
       - Use search_by_keyword for general searches (e.g., "resistor 10k", "STM32F4")
       - Use search_by_part_number for exact part lookups (e.g., "595-TPS54360DDAR")

    2. Review results:
       - Check MouserPartNumber, ManufacturerPartNumber, and Description
       - Review Availability and LeadTime
       - Check PriceBreaks for quantity pricing
       - Access DataSheetUrl for specifications
       - Verify ROHSStatus and LifecycleStatus

    3. Add to cart (optional):
       - Use add_to_cart with your cart key, part number, and quantity
       - Use update_cart_item to modify quantities
       - Use get_cart to review cart contents

    4. Order management:
       - Use get_order_options to see shipping/payment options
       - Use get_order to track order status
       - Use list_order_history to view past orders

    Note: You'll need valid Mouser API keys configured in your environment.
    """


# =============================================================================
# MAIN
# =============================================================================


def main() -> None:
    """Run the Mouser MCP server."""
    logger.info("Starting Mouser Electronics MCP Server...")
    mcp.run()


if __name__ == "__main__":
    main()
