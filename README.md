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
| `search_filings` | Search SEC EDGAR filings (10-K, 10-Q, 8-K) |
| `get_filing` | Get full text of a specific SEC filing |
| `insider_trades` | Get recent insider buys/sells from Form 4 filings |
| `financials` | Get income statement, balance sheet, cash flow, and key ratios |
| `analyze_company` | Comprehensive research brief aggregating all data sources |

### Example queries

- "What's AAPL's price history for the last month?"
- "Get me a quote for MSFT"
- "Show me TSLA's weekly prices over the past year"
- "Show me Apple's recent 10-K filings"
- "What insider trades happened at Tesla recently?"
- "Show me Apple's financial statements"
- "Give me a research brief on Tesla"

## Data Sources

- **yfinance** — price data, quotes, financial statements, analyst consensus
- **SEC EDGAR** — free, unlimited filings and insider trades (no API key needed)

## Development

```bash
# Run tests
pytest

# Run linter
ruff check src/ tests/
```

## License

MIT
