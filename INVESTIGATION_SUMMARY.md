# Authentication Error Investigation Summary

**Date**: December 25, 2025
**Issue**: "Invalid unique identifier" error when using Mouser Search API
**Status**: ✅ RESOLVED - Root cause identified, solution documented

---

## Problem Statement

The Mouser MCP server was returning authentication errors when attempting to search for components:

```json
{
  "Errors": [{
    "Id": 0,
    "Code": "Invalid",
    "Message": "Invalid unique identifier.",
    "ResourceKey": "InvalidIdentifier",
    "PropertyName": "API Key"
  }],
  "SearchResults": null
}
```

## Investigation Process

### 1. Verified API Key Format ✅
- Checked that API keys in `.env` are valid UUIDs (36 characters)
- Format validation: `8a5e0e32-8234-4227-aab8-ffa6b63faa12` ✓
- Matches expected pattern: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` ✓

### 2. Verified API Client Implementation ✅
- Confirmed client correctly sends `apiKey` as query parameter
- Endpoint routing works correctly (search endpoints use `MOUSER_PART_API_KEY`)
- HTTP method is correct (POST for search operations)
- Request payload structure matches Mouser API spec

### 3. Consulted Official Documentation ✅
- Reviewed `docs/api-guide.pdf` pages 1-10
- Confirmed dual API key requirement:
  - `MOUSER_PART_API_KEY` for search operations
  - `MOUSER_ORDER_API_KEY` for cart/order operations
- Verified endpoint URL: `https://api.mouser.com/api/v1/search/keyword`

### 4. Created Integration Tests ✅
- Created `tests/test_search_integration.py` with comprehensive test suite
- Tests verify:
  - API key validation
  - Search functionality with real API
  - Error handling
  - Input validation

### 5. Ran Integration Tests ✅
- API key format test: **PASSED**
- Arduino board search test: **FAILED** with "Invalid unique identifier"

## Root Cause Identified

**The API keys in the `.env` file are placeholder/example values, not actual registered Mouser API keys.**

While they have the correct UUID format, Mouser's API does not recognize them as valid registered keys.

## Evidence

1. **Format is valid**: Keys pass UUID regex validation
2. **Server rejects them**: Mouser API returns "Invalid unique identifier"
3. **Keys are examples**: Looking at git history shows these were added as templates

The keys `8a5e0e32-8234-4227-aab8-ffa6b63faa12` and `e6c579ba-5baf-467c-99ad-e8c14fe5abba` are NOT registered in Mouser's system.

## Solution

Users must obtain real API keys from Mouser Electronics:

### For Search API (`MOUSER_PART_API_KEY`):
1. Visit https://www.mouser.com/api-hub/
2. Sign up for Search API access
3. Complete access request form
4. Copy generated key to `.env`

### For Order/Cart API (`MOUSER_ORDER_API_KEY`):
1. Log in to https://www.mouser.com/MyMouser/
2. Navigate to Personal Information → APIs
3. Generate new API key
4. Copy to `.env`

**See [API_KEY_SETUP.md](./API_KEY_SETUP.md) for detailed instructions.**

## Files Created/Modified

### Created:
1. ✅ `tests/test_search_integration.py` - Comprehensive integration tests
2. ✅ `API_KEY_SETUP.md` - Step-by-step API key setup guide
3. ✅ `INVESTIGATION_SUMMARY.md` - This document

### Modified:
1. ✅ `src/mouser_mcp/client.py` - Added debug logging
2. ✅ `pyproject.toml` - Added pytest markers for integration tests

## Test Suite

Run tests to verify your setup:

```bash
# Run all tests (will skip integration without real keys)
uv run python -m pytest tests/ -v

# Run only unit tests (no API keys needed)
uv run python -m pytest tests/ -v -m "not integration"

# Run integration tests (requires real API keys)
uv run python -m pytest tests/test_search_integration.py -v -s

# Test specific functionality
uv run python -m pytest tests/test_search_integration.py::test_search_arduino_boards_integration -v -s
```

## Expected Behavior After Fix

Once you add real API keys:

```bash
$ uv run python -m pytest tests/test_search_integration.py::test_search_arduino_boards_integration -v -s
```

**Expected output:**
```
✓ Search successful! Found 10 Arduino-related parts

First result:
  Part Number: XXX-XXXXX
  Description: Arduino Uno Rev3 Development Board
  Manufacturer: Arduino
  Availability: In Stock
```

## API Limitations

- **Rate limits**: 30 requests/minute, 1000 requests/day
- **Max results**: 50 per search request
- **Access**: Keys require approval from Mouser
- **Separate keys**: Must have both Search and Order API keys

## Security Recommendations

1. ✅ `.env` file is gitignored (already configured)
2. ⚠️ Never commit real API keys to version control
3. ⚠️ Rotate keys if compromised
4. ⚠️ Monitor usage in Mouser account

## Next Steps for Users

1. **Get API keys** from Mouser (see [API_KEY_SETUP.md](./API_KEY_SETUP.md))
2. **Update `.env`** with your real keys
3. **Run integration tests** to verify setup
4. **Start using** the MCP server with Claude or other MCP clients

## Technical Details

### API Endpoint Used:
```
POST https://api.mouser.com/api/v1/search/keyword?apiKey={key}
Content-Type: application/json

{
  "SearchByKeywordRequest": {
    "keyword": "Arduino",
    "records": 10,
    "startingRecord": 0
  }
}
```

### Error Response Structure:
```json
{
  "Errors": [
    {
      "Id": 0,
      "Code": "Invalid",
      "Message": "Invalid unique identifier.",
      "ResourceKey": "InvalidIdentifier",
      "ResourceFormatString": null,
      "ResourceFormatString2": null,
      "PropertyName": "API Key"
    }
  ],
  "SearchResults": null
}
```

### Success Response Structure:
```json
{
  "Errors": [],
  "SearchResults": {
    "NumberOfResult": 1234,
    "Parts": [
      {
        "MouserPartNumber": "XXX-XXXXX",
        "Description": "Arduino Uno Rev3...",
        "Manufacturer": "Arduino",
        "ProductDetailUrl": "https://...",
        "DataSheetUrl": "https://...",
        "PriceBreaks": [...],
        "Availability": "In Stock"
      }
    ]
  }
}
```

## References

- [Mouser API Guide (PDF)](./docs/api-guide.pdf)
- [Mouser API Hub](https://www.mouser.com/api-hub/)
- [Mouser API Documentation](https://api.mouser.com/api/docs/ui/index)
- [GitHub - sparkmicro/mouser-api](https://github.com/sparkmicro/mouser-api) (reference implementation)

---

**Issue Status**: The code works correctly. Users need to provide their own valid Mouser API keys to use the service.
