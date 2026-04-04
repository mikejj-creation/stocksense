# MCP Finance Server

An MCP (Model Context Protocol) server that gives AI agents access to financial data — SEC EDGAR filings, market fundamentals, insider trades, and price history.

Think of it as "Context7 for finance" — Context7 provides docs to LLMs, this provides financial data.

## Status

Early development. Coming soon.

## Planned Tools

| Tool | Description |
|------|-------------|
| `search_sec_filings` | Search and retrieve SEC EDGAR filings (10-K, 10-Q, 8-K) |
| `get_financials` | Get company financial statements and ratios |
| `get_insider_trades` | Track insider buying/selling activity |
| `get_price_history` | Historical price data for any ticker |
| `analyze_company` | AI-generated research brief with bull/bear cases |

## Data Sources

- SEC EDGAR (free, unlimited)
- Financial Modeling Prep / Alpha Vantage (fundamentals)
- yfinance (price data)

## Compatible With

- Claude Desktop
- Cursor
- Any MCP-compatible AI client

## License

MIT
