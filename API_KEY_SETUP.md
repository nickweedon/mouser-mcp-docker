# Mouser API Key Setup Guide

## Issue Identified

The authentication error you're experiencing:
```
"Invalid unique identifier." for "PropertyName":"API Key"
```

This occurs because the API keys in your [.env](./.env) file are **placeholder/example keys**, not actual valid Mouser API keys.

## Root Cause

The keys currently in `.env` are:
- `MOUSER_PART_API_KEY=8a5e0e32-8234-4227-aab8-ffa6b63faa12`
- `MOUSER_ORDER_API_KEY=e6c579ba-5baf-467c-99ad-e8c14fe5abba`

While these have the correct UUID format, they are not registered with Mouser's API system.

## Solution: Obtain Real API Keys

### Step 1: Create a My Mouser Account

1. Go to [Mouser.com](https://www.mouser.com) and create an account if you don't have one
2. Navigate to your account settings

### Step 2: Generate API Keys

Mouser provides **TWO separate API keys** for different purposes:

#### A. Search API Key (`MOUSER_PART_API_KEY`)
- **Purpose**: For searching parts, getting product information, datasheets
- **Used by**: `search_by_keyword()`, `search_by_part_number()`
- **How to get it**:
  1. Go to [Mouser API Hub](https://www.mouser.com/api-hub/)
  2. Sign up for the **Search API**
  3. Fill out the access request form
  4. Copy the generated API key to `MOUSER_PART_API_KEY` in your `.env` file

#### B. Order/Cart API Key (`MOUSER_ORDER_API_KEY`)
- **Purpose**: For cart management, orders, and order history
- **Used by**: `get_cart()`, `add_to_cart()`, `get_order()`, etc.
- **How to get it**:
  1. Log in to your [My Mouser account](https://www.mouser.com/MyMouser/)
  2. Under "Personal Information", click on "APIs"
  3. Fill out the form to create a new API Key for Cart and Order APIs
  4. Copy the generated API key to `MOUSER_ORDER_API_KEY` in your `.env` file

### Step 3: Update Your .env File

Replace the placeholder keys in `.env` with your real API keys:

```bash
# Part Search API Key (from https://www.mouser.com/api-hub/)
MOUSER_PART_API_KEY=your-real-search-api-key-here

# Order/Cart API Key (from My Mouser account)
MOUSER_ORDER_API_KEY=your-real-order-api-key-here
```

**⚠️ IMPORTANT**: Keep these keys secret! Never commit them to version control.

### Step 4: Verify Your Setup

Run the integration test to verify your API keys work:

```bash
# Test API key format
uv run python -m pytest tests/test_search_integration.py::test_api_key_validation -v -s

# Test actual search functionality
uv run python -m pytest tests/test_search_integration.py::test_search_arduino_boards_integration -v -s

# Run all integration tests
uv run python -m pytest tests/test_search_integration.py -v -s
```

## API Key Limitations

According to Mouser's documentation:

- **Rate Limits**:
  - 30 requests per minute
  - 1,000 requests per day
  - Maximum 50 results per search request

- **Access**: API keys are tied to your Mouser account and may require approval

- **Separate Keys Required**: You must have both keys to use all features of this MCP server

## Troubleshooting

### Error: "Invalid unique identifier"
- **Cause**: API key is not valid or not registered with Mouser
- **Solution**: Follow the steps above to get real API keys

### Error: "Authorization has been denied"
- **Cause**: API key is incorrect or has extra spaces
- **Solution**: Double-check the key, ensure no leading/trailing spaces

### Error: Rate limit exceeded
- **Cause**: Too many requests in a short time
- **Solution**: Wait a minute and try again; implement rate limiting in your application

### SearchResults returns empty
- **Cause**: Search term doesn't match any products
- **Solution**: Try a different search term, check Mouser.com for available products

## Testing Without Real API Keys

If you don't have API keys yet, you can:

1. **Skip integration tests**:
   ```bash
   uv run python -m pytest tests/test_server.py -v
   ```

2. **Use mock tests** (if available):
   ```bash
   uv run python -m pytest tests/ -v -m "not integration"
   ```

## Security Best Practices

1. **Never commit API keys** to version control
2. **Use environment variables** or `.env` files (already gitignored)
3. **Rotate keys** if you suspect they've been compromised
4. **Monitor usage** in your Mouser account to detect unauthorized use

## Reference Links

- [Mouser API Hub](https://www.mouser.com/api-hub/)
- [Mouser API Documentation (PDF)](./docs/api-guide.pdf)
- [Mouser API Terms](https://www.mouser.com/apiterms/)
- [My Mouser Account API Settings](https://www.mouser.com/MyMouser/)

---

For more information about this MCP server, see [README.md](./README.md) or [CLAUDE.md](./CLAUDE.md).
