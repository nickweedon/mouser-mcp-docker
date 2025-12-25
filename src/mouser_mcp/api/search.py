"""Mouser Search API - Find electronic components."""

from typing import Any

from ..client import get_client


async def search_by_keyword(
    keyword: str,
    records: int = 50,
    start_record: int = 0,
) -> dict[str, Any]:
    """
    Search for parts using keyword search.

    Search across part numbers, manufacturers, and descriptions to find
    electronic components. Returns up to 50 results per request with pricing,
    availability, datasheets, and specifications.

    Args:
        keyword: Search term (part number, manufacturer, description, etc.)
        records: Number of records to return (max 50, default 50)
        start_record: Starting record number for pagination (default 0)

    Returns:
        Search results with parts, pricing, and availability information

    Raises:
        ValueError: If keyword is empty or records > 50
        RuntimeError: If API request fails
    """
    if not keyword.strip():
        raise ValueError("Keyword cannot be empty")
    if records > 50:
        raise ValueError("Maximum 50 records per request (API limit)")
    if records < 1:
        raise ValueError("Records must be at least 1")

    client = get_client()
    payload = {
        "SearchByKeywordRequest": {
            "keyword": keyword,
            "records": records,
            "startingRecord": start_record,
        }
    }

    try:
        response = client.post("search/keyword", json=payload)
        return response
    except Exception as e:
        raise RuntimeError(f"Failed to search by keyword: {e}") from e


async def search_by_part_number(
    part_number: str,
) -> dict[str, Any]:
    """
    Search for a specific part by exact part number.

    Performs an exact match search for a Mouser or manufacturer part number.
    Returns detailed part information including pricing tiers, availability,
    datasheets, and specifications.

    Args:
        part_number: Exact Mouser or manufacturer part number

    Returns:
        Search results with part details if found

    Raises:
        ValueError: If part_number is empty
        RuntimeError: If API request fails
    """
    if not part_number.strip():
        raise ValueError("Part number cannot be empty")

    client = get_client()
    payload = {
        "SearchByPartRequest": {
            "mouserPartNumber": part_number,
        }
    }

    try:
        response = client.post("search/partnumber", json=payload)
        return response
    except Exception as e:
        raise RuntimeError(f"Failed to search by part number: {e}") from e
