"""
Mouser API Client Module

This module handles communication with the Mouser Electronics API.
Supports both Part Search API and Order/Cart API with separate authentication.
"""

import os
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv

# Load environment variables from multiple possible locations
_env_paths = [
    Path.cwd() / ".env",
    Path(__file__).parent.parent.parent.parent / ".env",
    Path.home() / ".env",
]

for env_path in _env_paths:
    if env_path.exists():
        load_dotenv(env_path)
        break


def get_client_config() -> dict[str, Any]:
    """
    Get the Mouser API client configuration from environment variables.

    Returns:
        A dictionary with configuration values including both API keys.
    """
    return {
        "part_api_key": os.getenv("MOUSER_PART_API_KEY", ""),
        "order_api_key": os.getenv("MOUSER_ORDER_API_KEY", ""),
        "api_base_url": os.getenv("MOUSER_API_BASE_URL", "https://api.mouser.com/api/v1"),
        "timeout": int(os.getenv("MOUSER_API_TIMEOUT", "30")),
        "debug": os.getenv("MOUSER_DEBUG", "false").lower() == "true",
    }


class APIClient:
    """
    HTTP client for Mouser Electronics API.

    Handles dual authentication with separate API keys for:
    - Part Search API (search endpoints)
    - Order/Cart/History API (order/cart/orderhistory endpoints)
    """

    def __init__(
        self,
        part_api_key: str,
        order_api_key: str,
        base_url: str,
        timeout: int,
        debug: bool = False,
    ) -> None:
        self.base_url = base_url
        self.timeout = timeout
        self.part_api_key = part_api_key
        self.order_api_key = order_api_key
        self.debug = debug

        self.session = requests.Session()
        self.session.headers["Content-Type"] = "application/json"

    def _set_api_key_header(self, endpoint: str) -> None:
        """Set the appropriate API key header based on the endpoint."""
        # Clear any existing API key headers
        self.session.headers.pop("SearchApi-Key", None)
        self.session.headers.pop("OrderApi-Key", None)

        # Set the correct key based on endpoint
        if "/search/" in endpoint:
            if self.part_api_key:
                self.session.headers["SearchApi-Key"] = self.part_api_key
        else:
            # Cart, Order, OrderHistory use order key
            if self.order_api_key:
                self.session.headers["OrderApi-Key"] = self.order_api_key

    def get(self, endpoint: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Make a GET request to the Mouser API."""
        self._set_api_key_header(endpoint)
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.session.get(url, params=params, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def post(self, endpoint: str, json: dict[str, Any] | None = None) -> dict[str, Any]:
        """Make a POST request to the Mouser API."""
        self._set_api_key_header(endpoint)
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.session.post(url, json=json, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def put(self, endpoint: str, json: dict[str, Any] | None = None) -> dict[str, Any]:
        """Make a PUT request to the Mouser API."""
        self._set_api_key_header(endpoint)
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.session.put(url, json=json, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def delete(self, endpoint: str) -> dict[str, Any]:
        """Make a DELETE request to the Mouser API."""
        self._set_api_key_header(endpoint)
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.session.delete(url, timeout=self.timeout)
        response.raise_for_status()
        return response.json()


# Singleton client instance
_client_instance: APIClient | None = None


def get_client() -> APIClient:
    """Get or create the singleton Mouser API client instance."""
    global _client_instance
    if _client_instance is None:
        config = get_client_config()
        _client_instance = APIClient(
            part_api_key=config["part_api_key"],
            order_api_key=config["order_api_key"],
            base_url=config["api_base_url"],
            timeout=config["timeout"],
            debug=config["debug"],
        )
    return _client_instance
