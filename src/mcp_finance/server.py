"""MCP Finance Server — entry point."""

from mcp.server.fastmcp import FastMCP

from mcp_finance.tools.insider_trades import get_insider_trades as _get_insider_trades
from mcp_finance.tools.price_history import get_price_history, get_quote
from mcp_finance.tools.sec_filings import get_filing as _get_filing
from mcp_finance.tools.sec_filings import search_filings as _search_filings

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


@mcp.tool()
def search_filings(ticker: str, form_type: str = "10-K", limit: int = 10) -> dict:
    """Search SEC EDGAR filings for a company.

    Args:
        ticker: Stock ticker symbol (e.g. AAPL, MSFT, GOOGL)
        form_type: SEC form type — 10-K (annual), 10-Q (quarterly), 8-K (current events)
        limit: Maximum number of filings to return (default 10)
    """
    return _search_filings(ticker, form_type, limit)


@mcp.tool()
def get_filing(ticker: str, accession_number: str) -> dict:
    """Get the full text of a specific SEC filing.

    Args:
        ticker: Stock ticker symbol (e.g. AAPL, MSFT, GOOGL)
        accession_number: SEC accession number from search_filings results (e.g. 0000320193-24-000123)
    """
    return _get_filing(ticker, accession_number)


@mcp.tool()
def insider_trades(ticker: str, limit: int = 20) -> dict:
    """Get recent insider trades (buys and sells) for a company from SEC Form 4 filings.

    Args:
        ticker: Stock ticker symbol (e.g. AAPL, MSFT, GOOGL)
        limit: Maximum number of Form 4 filings to parse (default 20)
    """
    return _get_insider_trades(ticker, limit)


def main():
    """Run the MCP server on stdio transport."""
    mcp.run()


if __name__ == "__main__":
    main()
