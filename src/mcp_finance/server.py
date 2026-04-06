"""MCP Finance Server — entry point."""

from mcp.server.fastmcp import FastMCP

from mcp_finance.tools.price_history import get_price_history, get_quote

mcp = FastMCP("mcp-finance")


@mcp.tool()
def price_history(ticker: str, period: str = "1mo", interval: str = "1d") -> dict:
    """Get historical price data for a stock ticker.

    Args:
        ticker: Stock ticker symbol (e.g. AAPL, MSFT, GOOGL)
        period: Time period — 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, max
        interval: Data interval — 1m, 5m, 15m, 1h, 1d, 1wk, 1mo
    """
    return get_price_history(ticker, period, interval)


@mcp.tool()
def quote(ticker: str) -> dict:
    """Get current price quote and key stats for a stock ticker.

    Args:
        ticker: Stock ticker symbol (e.g. AAPL, MSFT, GOOGL)
    """
    return get_quote(ticker)


def main():
    """Run the MCP server on stdio transport."""
    mcp.run()


if __name__ == "__main__":
    main()
