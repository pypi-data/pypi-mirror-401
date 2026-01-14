# MCP Server Currency History

A Model Context Protocol (MCP) server that provides historical currency exchange rates and currency conversion.
Powered by the [Frankfurter API](https://api.frankfurter.app/), which is free and open-source.

## Features

- **Get Historical Rates**: Fetch exchange rates for a specific date (e.g., "2023-01-01").
- **Convert Currency**: Convert amounts between currencies using historical rates.

## Installation & Usage (with uv)

You can run this MCP server directly using `uv` without manually installing it everywhere:

```bash
# Run directly
uvx mcp-server-currency-history
```

Or install it as a tool:

```bash
uv tool install mcp-server-currency-history
```

## Manual Installation

```bash
pip install mcp-server-currency-history
```

## Running the Server

```bash
# If installed via pip
mcp-server-currency-history

# Or connect via an MCP client inspector
npx @modelcontextprotocol/inspector uvx mcp-server-currency-history
```

## Tools

1. `get_historical_rate`
   - `date`: YYYY-MM-DD
   - `base`: Base currency (default USD)
   - `symbols`: Target currencies (default CNY, EUR, JPY, GBP)

2. `convert_historical_amount`
   - `amount`: Amount to convert
   - `from_curr`: Source currency
   - `to_curr`: Target currency
   - `date`: YYYY-MM-DD
