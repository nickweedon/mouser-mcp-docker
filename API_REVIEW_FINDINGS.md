# Mouser MCP Server - API Review Findings

**Date**: 2025-12-25
**Source**: Official Mouser API Guide PDF (`api-guide.pdf`)

## Critical Issues Fixed

### 1. ✅ **FIXED: API Key Authentication Method**
- **Issue**: API key was sent as HTTP headers (`SearchApi-Key`, `OrderApi-Key`)
- **Correct**: API key must be sent as query parameter `?apiKey={key}`
- **Location**: `src/mouser_mcp/client.py`
- **Impact**: ALL API calls were failing with 404 errors
- **Reference**: PDF pages 4-6 (query parameters section)

### 2. ✅ **FIXED: Cart API Endpoint Paths**
- **Issue**: Incorrect endpoint paths using path parameters
  - Was: `cart/{cart_key}`, `cart/{cart_key}/insert`, `cart/{cart_key}/update`
  - Should be: `cart`, `cart/items/insert`, `cart/items/update`
- **Location**: `src/mouser_mcp/api/cart.py`
- **Impact**: Cart operations would fail
- **Reference**: PDF pages 20-26 (Cart API endpoints)

**Specific fixes:**
- `get_cart()`: Changed from `GET cart/{cart_key}` to `GET cart?cartKey={cart_key}`
- `add_to_cart()`: Changed from `POST cart/{cart_key}/insert` to `POST cart/items/insert`
- `update_cart_item()`: Changed from `POST cart/{cart_key}/update` to `POST cart/items/update`

### 3. ✅ **FIXED: Order Retrieval Method**
- **Issue**: Used POST request with JSON body
- **Correct**: Should use GET with order number in path
  - Was: `POST order/get` with `{"OrderNumber": "..."}`
  - Should be: `GET order/{orderNumber}`
- **Location**: `src/mouser_mcp/api/order.py`
- **Impact**: Order retrieval would fail
- **Reference**: PDF page 37 (endpoint 5)

## Missing API Endpoints

Based on the PDF documentation, the following endpoints are **NOT** implemented but are available in the Mouser API:

### Cart API (Missing 5 of 8 endpoints)
1. ❌ **POST `/api/v1/cart`** - Update entire cart
   - Replaces all cart items; deletes items not in request
   - At least one part number required
   - Reference: PDF page 20, endpoint 2

2. ❌ **POST `/api/v1/cart/item/remove`** - Remove single cart item
   - Removes one cart item by Mouser part number
   - Reference: PDF page 20, endpoint 5

3. ❌ **POST `/api/v1/cart/insert/schedule`** - Add scheduled deliveries
   - Adds scheduled release dates for cart items
   - Must follow scheduling restrictions
   - Reference: PDF pages 20-23, endpoint 6

4. ❌ **POST `/api/v1/cart/update/schedule`** - Update scheduled deliveries
   - Updates or adds new scheduled deliveries
   - Reference: PDF pages 23-25, endpoint 7

5. ❌ **POST `/api/v1/cart/deleteall/schedule`** - Remove all schedules
   - Removes all scheduled deliveries for a cart
   - Reference: PDF page 26, endpoint 8

### Order API (Missing 3 of 5 endpoints)
1. ❌ **GET `/api/v1/order/currencies`** - Get available currencies
   - Returns currencies based on billing/shipping address
   - Optional shipping country code parameter
   - Reference: PDF page 31

2. ❌ **GET `/api/v1/order/countries`** - Get countries and states
   - Returns all countries with state/province codes
   - Can filter by country code
   - Reference: PDF page 31

3. ❌ **POST `/api/v1/order`** - Submit an order
   - Creates actual orders (not test orders!)
   - Requires cart, shipping method, payment, currency
   - Optional shipping address override
   - Reference: PDF pages 32-36

## API Documentation Key Findings

### Request Format (PDF pages 4-6)
- **Query Parameters**: Added to URL after `?` and `&`
  - Example: `?apiKey={key}&cartKey={cart_key}`
- **Path Parameters**: Embedded in URL path
  - Example: `/order/{orderNumber}` → `/order/12345`
- **Request Body**: JSON payload for POST requests
  - Must wrap properties in parent object (e.g., `SearchByKeywordRequest`)

### API Key Usage (PDF pages 1-2)
- **Two separate API keys required**:
  1. Part Search API Key - for search endpoints
  2. Order/Cart API Key - for cart, order, and history endpoints
- **Format**: UUID string
- **Location**: Query parameter `apiKey` (NOT header!)

### Error Handling (PDF pages 15-18)
- **Status Code 200**: Request errors (validation, business logic)
  - Check response body `Errors` array
  - Errors can be at root level or nested in sections
- **Status Code 500**: Server-side errors
- **Error Structure**:
  ```json
  {
    "Errors": [{
      "Code": "Required|Invalid|NotFound|...",
      "Message": "Human-readable description",
      "PropertyName": "FieldName"
    }]
  }
  ```

### Common Error Codes (PDF page 17)
- `Required` - Missing required field
- `Invalid` - Invalid value for field
- `NotFound` - Resource not found
- `MinLength` / `MaxLength` - String length validation
- `InvalidFormat` - Wrong format (e.g., postal code)
- `NotAvailable` - Value not available based on other values
- `NotAllowed` - Trying to submit order with errored cart items
- `EmptyCart` - At least one cart item required
- `NoValidItemsInCart` - All cart items in error state

### Rate Limits (PDF introduction)
- **50 results** maximum per search request
- **30 requests** per minute
- **1000 requests** per day

### Important Notes
1. **API Explorer is NOT a sandbox** - Orders created are real! (PDF page 2)
2. **Only HTTPS supported** - All requests must use secure connection (PDF page 2)
3. **Version 1.0 is current** - Use `1.0` for version parameter (PDF page 11)
4. **Only Mouser part numbers supported** - Cart API doesn't accept manufacturer part numbers (PDF page 19)
5. **Billing address cannot be modified via API** - Must use My Mouser account page (PDF page 19)

## Request Body Examples

### Search by Keyword (PDF page 49)
```json
{
  "SearchByKeywordRequest": {
    "keyword": "Arduino",
    "records": 50,
    "startingRecord": 0
  }
}
```

### Search by Part Number (PDF page 86)
```json
{
  "SearchByPartRequest": {
    "mouserPartNumber": "546-1590B"
  }
}
```

### Add to Cart (PDF page 26)
```json
{
  "CartKey": "00000000-0000-0000-0000-000000000000",
  "CartItems": [
    {
      "MouserPartNumber": "546-1590B",
      "Quantity": 1
    }
  ]
}
```

### Get Order Options (PDF page 28)
```json
{
  "OrderInitialize": {
    "CurrencyCode": "EUR",
    "CartKey": "00000000-0000-0000-0000-000000000000"
  }
}
```
*Note: Entire request body is optional*

## Recommendations

### High Priority (Required for Basic Functionality)
1. ✅ **COMPLETED**: Fix API key authentication (query parameter vs header)
2. ✅ **COMPLETED**: Fix cart endpoint paths
3. ✅ **COMPLETED**: Fix order retrieval to use GET
4. 🔴 **TODO**: Add comprehensive error response handling with proper error code mapping
5. 🔴 **TODO**: Add request/response validation based on PDF schemas

### Medium Priority (Enhanced Functionality)
1. 🔴 **TODO**: Implement missing Cart API endpoints (especially `item/remove`)
2. 🔴 **TODO**: Implement missing Order API endpoints (currencies, countries, submit order)
3. 🔴 **TODO**: Add rate limiting tracking/warnings
4. 🔴 **TODO**: Add request payload validation before sending to API

### Low Priority (Nice to Have)
1. 🔴 **TODO**: Add support for scheduled deliveries
2. 🔴 **TODO**: Add support for XML content type (in addition to JSON)
3. 🔴 **TODO**: Implement retry logic with exponential backoff
4. 🔴 **TODO**: Add comprehensive logging for debugging

## Testing Checklist

After implementing fixes, verify:
- [x] Search by keyword works
- [ ] Search by part number works
- [ ] Get cart returns correct data
- [ ] Add to cart succeeds
- [ ] Update cart item quantity works
- [ ] Get order options returns shipping/payment methods
- [ ] Get order by number returns order details
- [ ] Get order history returns past orders
- [ ] Error responses are properly parsed and returned
- [ ] API key is correctly included in all requests
- [ ] Rate limits are respected

## Version Compatibility

- **Current Implementation**: API v1.0
- **Base URL**: `https://api.mouser.com/api/v1`
- **Tested Against**: PDF guide dated 2020 (still current as of 2025)
- **Next Steps**: Monitor for API v2 announcements

---

**Summary**: The main issue was authentication method (headers vs query params). All Cart and Order endpoint paths have been corrected to match official API documentation. Several optional endpoints remain unimplemented but are not critical for basic functionality.
