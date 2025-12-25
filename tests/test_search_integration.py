"""
Integration tests for Mouser Search API.

These tests make real API calls to the Mouser Electronics API.
Run with: pytest tests/test_search_integration.py -v -s
"""

import os
import pytest
from mouser_mcp.api.search import search_by_keyword


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_arduino_boards_integration():
    """
    Integration test: Search for Arduino boards using the real Mouser API.

    This test will make a real API call to Mouser's search endpoint.
    It requires valid API keys in the .env file.
    """
    # Check if API key is configured
    api_key = os.getenv("MOUSER_PART_API_KEY")
    if not api_key:
        pytest.skip("MOUSER_PART_API_KEY not configured in environment")

    # Search for Arduino boards
    keyword = "Arduino"
    records = 10  # Limit to 10 results for testing

    # Perform the search
    try:
        result = await search_by_keyword(keyword=keyword, records=records)

        # Verify the response structure
        assert result is not None, "Response should not be None"
        assert isinstance(result, dict), "Response should be a dictionary"

        # Check for errors in the response
        if "Errors" in result and result["Errors"]:
            errors = result["Errors"]
            pytest.fail(
                f"API returned errors: {errors}\n"
                f"This may indicate:\n"
                f"  1. Invalid API key (check PropertyName='API Key')\n"
                f"  2. API key is for wrong endpoint (Order vs Search API)\n"
                f"  3. API rate limits exceeded\n"
                f"  4. Network or service issues"
            )

        # Verify SearchResults exist
        assert "SearchResults" in result, "Response should contain 'SearchResults'"
        search_results = result["SearchResults"]
        assert search_results is not None, "SearchResults should not be None"

        # Verify we got parts back
        assert "Parts" in search_results, "SearchResults should contain 'Parts'"
        parts = search_results["Parts"]
        assert isinstance(parts, list), "Parts should be a list"
        assert len(parts) > 0, f"Should find at least one Arduino board, got {len(parts)}"

        # Verify the structure of the first part
        first_part = parts[0]
        assert "MouserPartNumber" in first_part, "Part should have MouserPartNumber"
        assert "Description" in first_part, "Part should have Description"
        assert "Manufacturer" in first_part, "Part should have Manufacturer"

        # Print some results for manual verification
        print(f"\n✓ Search successful! Found {len(parts)} Arduino-related parts")
        print(f"\nFirst result:")
        print(f"  Part Number: {first_part.get('MouserPartNumber', 'N/A')}")
        print(f"  Description: {first_part.get('Description', 'N/A')}")
        print(f"  Manufacturer: {first_part.get('Manufacturer', 'N/A')}")
        print(f"  Availability: {first_part.get('Availability', 'N/A')}")

        # Check that results are actually Arduino-related
        description = first_part.get("Description", "").lower()
        part_number = first_part.get("MouserPartNumber", "").lower()
        manufacturer = first_part.get("Manufacturer", "").lower()

        # At least one of these should contain "arduino" for our search
        has_arduino = any([
            "arduino" in description,
            "arduino" in part_number,
            "arduino" in manufacturer
        ])

        print(f"\n  Contains 'Arduino': {has_arduino}")

    except RuntimeError as e:
        pytest.fail(
            f"Search API call failed: {e}\n"
            f"This could indicate:\n"
            f"  1. Network connectivity issues\n"
            f"  2. Mouser API service down\n"
            f"  3. Invalid API endpoint URL\n"
            f"  4. Authentication failure"
        )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_specific_arduino_board():
    """
    Integration test: Search for a specific Arduino board by part number.
    """
    api_key = os.getenv("MOUSER_PART_API_KEY")
    if not api_key:
        pytest.skip("MOUSER_PART_API_KEY not configured in environment")

    # Search for Arduino Uno (a very common board)
    keyword = "Arduino Uno"
    records = 5

    result = await search_by_keyword(keyword=keyword, records=records)

    # Check for errors
    if "Errors" in result and result["Errors"]:
        pytest.fail(f"API returned errors: {result['Errors']}")

    # Verify we got results
    assert "SearchResults" in result
    assert result["SearchResults"] is not None
    parts = result["SearchResults"].get("Parts", [])
    assert len(parts) > 0, "Should find Arduino Uno boards"

    print(f"\n✓ Found {len(parts)} results for 'Arduino Uno'")
    for i, part in enumerate(parts[:3], 1):  # Show top 3
        print(f"\n{i}. {part.get('MouserPartNumber', 'N/A')}")
        print(f"   {part.get('Description', 'N/A')[:100]}...")
        print(f"   Price: {part.get('PriceBreaks', [{}])[0].get('Price', 'N/A') if part.get('PriceBreaks') else 'N/A'}")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_validation():
    """
    Test that validation errors are properly handled.
    """
    # Test empty keyword
    with pytest.raises(ValueError, match="Keyword cannot be empty"):
        await search_by_keyword(keyword="", records=10)

    # Test too many records
    with pytest.raises(ValueError, match="Maximum 50 records"):
        await search_by_keyword(keyword="Arduino", records=100)

    # Test zero records
    with pytest.raises(ValueError, match="Records must be at least 1"):
        await search_by_keyword(keyword="Arduino", records=0)

    print("\n✓ Validation tests passed")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_api_key_validation():
    """
    Test that provides helpful error messages for API key issues.
    """
    api_key = os.getenv("MOUSER_PART_API_KEY")

    if not api_key:
        print("\n⚠ MOUSER_PART_API_KEY is not set in environment")
        print("  To run integration tests:")
        print("  1. Get API keys from: https://www.mouser.com/api-hub/")
        print("  2. Set MOUSER_PART_API_KEY in .env file")
        print("  3. Ensure you have the SEARCH API key (not just Order API)")
        pytest.skip("API key not configured")

    print(f"\n✓ API key configured: {api_key[:8]}...{api_key[-4:]}")
    print(f"  Key length: {len(api_key)} characters")
    print(f"  Expected format: UUID (36 chars with dashes)")

    # Validate UUID format
    import re
    uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    is_valid_uuid = bool(re.match(uuid_pattern, api_key, re.IGNORECASE))

    if not is_valid_uuid:
        pytest.fail(
            f"API key does not match UUID format.\n"
            f"Expected: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx\n"
            f"Got: {api_key[:20]}..."
        )

    print(f"  Format validation: PASS")
