"""
Pytest Configuration and Fixtures

This module provides shared fixtures for all Mouser MCP tests.
"""

import pytest


@pytest.fixture
def sample_part() -> dict:
    """Provide a sample Mouser part for testing."""
    return {
        "MouserPartNumber": "595-TPS54360DDAR",
        "ManufacturerPartNumber": "TPS54360DDAR",
        "Manufacturer": "Texas Instruments",
        "Description": "Switching Voltage Regulators 3.5V-60V 3.5A Step Down Swift",
        "DataSheetUrl": "https://www.mouser.com/datasheet/2/405/tps54360-1767969.pdf",
        "ImagePath": "https://www.mouser.com/images/texasinstruments/lrg/tps54360dda.jpg",
        "Category": "Power Management ICs",
        "LifecycleStatus": "Active",
        "ROHSStatus": "RoHS Compliant",
        "Availability": "In Stock",
        "Min": 1,
        "Mult": 1,
        "LeadTime": "10 Weeks",
        "PriceBreaks": [
            {"Quantity": 1, "Price": "2.15", "Currency": "USD"},
            {"Quantity": 10, "Price": "1.93", "Currency": "USD"},
            {"Quantity": 100, "Price": "1.72", "Currency": "USD"},
        ],
    }


@pytest.fixture
def sample_search_result(sample_part) -> dict:
    """Provide a sample search result for testing."""
    return {
        "SearchResults": {
            "NumberOfResult": 1,
            "Parts": [sample_part],
        }
    }


@pytest.fixture
def sample_cart() -> dict:
    """Provide a sample cart for testing."""
    return {
        "CartKey": "test-cart-key-123",
        "CartItems": [
            {
                "MouserPartNumber": "595-TPS54360DDAR",
                "Quantity": 10,
                "CustomerPartNumber": "",
            }
        ],
        "Pricing": {
            "Subtotal": "19.30",
            "Tax": "0.00",
            "Total": "19.30",
            "Currency": "USD",
        },
    }


@pytest.fixture
def sample_order() -> dict:
    """Provide a sample order for testing."""
    return {
        "OrderNumber": "WEB12345678",
        "WebOrderNumber": "12345678",
        "Status": "Shipped",
        "OrderTotal": "19.30",
        "Currency": "USD",
        "OrderDate": "2024-01-15",
    }
