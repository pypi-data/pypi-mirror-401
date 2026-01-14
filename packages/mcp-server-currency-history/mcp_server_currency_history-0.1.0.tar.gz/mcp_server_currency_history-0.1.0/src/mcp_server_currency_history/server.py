from fastmcp import FastMCP
import httpx
from datetime import datetime

# Create the MCP server instance
mcp = FastMCP("CurrencyHistory")

# API Configuration
# Using Frankfurter API (Free, open source, no API key required)
BASE_URL = "https://api.frankfurter.app/"

@mcp.tool()
async def get_historical_rate(date: str, base: str = "USD", symbols: str = "CNY,EUR,JPY,GBP") -> str:
    """
    Get historical exchange rates for a specific date.
    
    Args:
        date: The date in YYYY-MM-DD format (e.g., '2023-01-01').
        base: Base currency code (default: USD).
        symbols: Comma-separated list of target currencies (default: 'CNY,EUR,JPY,GBP').
    """
    # Simple date format validation
    try:
        datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        return "Error: Invalid date format. Please use YYYY-MM-DD."

    url = f"{BASE_URL}{date}"
    params = {"from": base.upper(), "to": symbols.upper()}
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params)
            if response.status_code == 404:
                return f"Error: Exchange rate data not found for {date} (could be a weekend or date is too old)."
            if response.status_code != 200:
                return f"Error: API request failed with status code {response.status_code}."

            data = response.json()
            rates = data.get("rates", {})
            return f"Date: {data.get('date')}\nBase: 1 {base.upper()}\nRates: {rates}"
        except Exception as e:
            return f"Error connecting to API: {str(e)}"

@mcp.tool()
async def convert_historical_amount(amount: float, from_curr: str, to_curr: str, date: str) -> str:
    """
    Convert an amount between currencies using historical rates.
    
    Args:
        amount: The amount to convert.
        from_curr: The source currency code.
        to_curr: The target currency code.
        date: Historical date (YYYY-MM-DD).
    """
    # Simple date format validation
    try:
        datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        return "Error: Invalid date format. Please use YYYY-MM-DD."

    url = f"{BASE_URL}{date}"
    params = {"from": from_curr.upper(), "to": to_curr.upper(), "amount": amount}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params)
            if response.status_code != 200:
                return "Error: Unable to fetch exchange rates. Check the date or currency codes."
            
            data = response.json()
            # The API returns rates relative to base, forcing 'to' in params might result in direct conversion if API supports it
            # Frankfurter API with 'amount' and 'from'/'to' params usually handles conversion.
            # Let's check response structure for conversion.
            # Frankfurter response for ?amount=10&from=USD&to=EUR usually looks like: {"amount": 10, "base": "USD", "date": "...", "rates": {"EUR": 9.something}}
            
            rate_value = data.get("rates", {}).get(to_curr.upper())
            if rate_value is None:
                 return f"Error: Could not find rate for {to_curr.upper()}."

            return f"On {date}:\n{amount} {from_curr.upper()} = {rate_value} {to_curr.upper()}"
        except Exception as e:
            return f"Error connecting to API: {str(e)}"

def main():
    mcp.run()

if __name__ == "__main__":
    main()
