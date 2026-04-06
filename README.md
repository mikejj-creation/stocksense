# MCP Finance Server

An MCP (Model Context Protocol) server that gives AI agents access to financial data — SEC EDGAR filings, market fundamentals, insider trades, and price history.

## Installation

```bash
pip install -e .
```

For development:

```bash
pip install -e ".[dev]"
```

## Usage

### Run the server

```bash
# Either:
mcp-finance

# Or:
python -m mcp_finance
```

### Claude Desktop configuration

Add to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "finance": {
      "command": "mcp-finance"
    }
  }
}
```

### Available Tools

| Tool | Description |
|------|-------------|
| `price_history` | Get historical OHLCV price data for any ticker |
| `quote` | Get current price, market cap, P/E, 52-week range |

### Example queries

- "What's AAPL's price history for the last month?"
- "Get me a quote for MSFT"
- "Show me TSLA's weekly prices over the past year"

## Planned Tools

| Tool | Description |
|------|-------------|
| `search_sec_filings` | Search and retrieve SEC EDGAR filings (10-K, 10-Q, 8-K) |
| `get_financials` | Get company financial statements and ratios |
| `get_insider_trades` | Track insider buying/selling activity |
| `analyze_company` | AI-generated research brief with bull/bear cases |

## Data Sources

- **yfinance** — price data and quotes
- **SEC EDGAR** (coming soon) — free, unlimited filings
- **Financial Modeling Prep / Alpha Vantage** (coming soon) — fundamentals

## Development

```bash
# Run tests
pytest

# Run linter
ruff check src/ tests/
```

## License

MIT
