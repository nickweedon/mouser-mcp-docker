# Mouser Electronics MCP Server

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server for the Mouser Electronics API. Search for electronic components, manage shopping carts, and track orders directly through Claude or other MCP clients.

## Features

- **Part Search**: Find components by keyword or exact part number
- **Component Details**: Access specifications, pricing, availability, and datasheets
- **Cart Management**: Add items to cart and update quantities
- **Order Tracking**: View order details and history
- **Pricing Information**: Get quantity-based pricing with up to 4 price breaks
- **Real-time Availability**: Check stock levels and lead times

## Quick Start

### Prerequisites

- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) package manager (recommended)
- Mouser Electronics API keys (free at [mouser.com/api-hub](https://www.mouser.com/api-hub/))

### Installation

1. Clone this repository:

```bash
git clone <this-repo> mouser-mcp
cd mouser-mcp
```

2. Install dependencies:

```bash
uv sync
```

3. Create your environment file:

```bash
cp .env.example .env
# Edit .env with your Mouser API keys
```

You'll need **two separate API keys** from Mouser:
- **Part Search API Key**: For searching components
- **Order/Cart API Key**: For cart and order operations

Get both keys at: https://www.mouser.com/api-hub/

4. Run the server:

```bash
uv run mouser-mcp
```

## Project Structure

```
mouser-mcp/
├── src/mouser_mcp/
│   ├── __init__.py          # Package initialization
│   ├── server.py            # Main MCP server entry point
│   ├── client.py            # Mouser API client
│   ├── types.py             # TypedDict definitions
│   ├── api/                 # API modules
│   │   ├── search.py        # Search operations
│   │   ├── cart.py          # Cart management
│   │   ├── order.py         # Order operations
│   │   └── order_history.py # Order history
│   └── utils/               # Utility modules
├── tests/                   # Test suite
├── .env.example             # Environment template
└── README.md               # This file
```

## Available Tools

| Tool | Description |
|------|-------------|
| `search_by_keyword` | Search parts by keyword (e.g., "resistor 10k", "STM32F4") |
| `search_by_part_number` | Search by exact part number (e.g., "595-TPS54360DDAR") |
| `get_cart` | Retrieve cart contents by cart key |
| `add_to_cart` | Add item to shopping cart |
| `update_cart_item` | Update item quantity in cart |
| `get_order_options` | Get shipping/payment options for a cart |
| `get_order` | Retrieve order details by order number |
| `list_order_history` | View past orders (default: last 30 days) |
| `health_check` | Check server status and API configuration |

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MOUSER_PART_API_KEY` | API key for part search | (required) |
| `MOUSER_ORDER_API_KEY` | API key for cart/orders | (required) |
| `MOUSER_API_BASE_URL` | Base URL for Mouser API | `https://api.mouser.com/api/v1` |
| `MOUSER_API_TIMEOUT` | Request timeout in seconds | `30` |
| `MOUSER_DEBUG` | Enable debug logging | `false` |

## Claude Desktop Integration

Add to your Claude Desktop configuration (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "mouser": {
      "command": "uv",
      "args": ["--directory", "/path/to/mouser-mcp", "run", "mouser-mcp"]
    }
  }
}
```

Or with Docker:

```json
{
  "mcpServers": {
    "mouser": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "--env-file",
        "/path/to/mouser-mcp/.env",
        "mouser-mcp:latest"
      ]
    }
  }
}
```

## Development

### Running Tests

```bash
uv run pytest -v
```

### Linting

```bash
uv run ruff check src/ tests/
uv run ruff format src/ tests/
```

### Building

```bash
uv build
```

## Docker Deployment

### Build and run with Docker Compose:

```bash
docker compose up --build
```

### For development with VS Code Dev Containers:

1. Open the project in VS Code
2. Install the "Dev Containers" extension
3. Click "Reopen in Container" when prompted

## API Rate Limits

Mouser API has the following limits:
- **50 results** maximum per search request
- **30 requests per minute**
- **1000 requests per day**

The server will raise errors if you exceed these limits.

## Example Usage

Once integrated with Claude Desktop, you can ask:

- "Search for STM32F407 microcontrollers on Mouser"
- "Find 10k ohm resistors with 1% tolerance"
- "What's the price and availability for part number 595-TPS54360DDAR?"
- "Show me my recent Mouser orders"

## License

MIT License - See LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## Resources

- [Mouser API Hub](https://www.mouser.com/api-hub/)
- [Mouser API Documentation](https://api.mouser.com/api/docs/ui/index)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
