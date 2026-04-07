# Milestones

---

## Milestone 1: Working MCP Server with Price History Tool

**Status: COMPLETE**

Delivered a functional MCP server that can be `pip install`-ed, connected to Claude Desktop, and queried for real price data — proving the end-to-end MCP plumbing works.

### Action Items

- [x] `src/mcp_finance/data/cache.py` — In-memory TTL cache with expiry timestamps
- [x] `src/mcp_finance/data/market.py` — yfinance wrapper with caching (`fetch_price_history`, `fetch_quote`)
- [x] `src/mcp_finance/tools/price_history.py` — Tool functions (`get_price_history`, `get_quote`)
- [x] `src/mcp_finance/server.py` — FastMCP server with stdio transport, registers price tools
- [x] `src/mcp_finance/__main__.py` — Module runner (`python -m mcp_finance`)
- [x] `tests/test_cache.py` — 6 unit tests for TTL cache
- [x] `tests/test_price_history.py` — 6 integration tests for price data + tool output format
- [x] `pyproject.toml` — Add `[project.scripts]` entry point
- [x] `README.md` — Installation, Claude Desktop config, usage docs

### Key Decisions

- **FastMCP** over low-level Server API — cleaner, decorator-based
- **Stdio transport** — standard for Claude Desktop / CLI
- **List of dicts** (not DataFrame) as internal format — easy JSON serialization
- **In-memory cache** (not file-based) — server is stateless, restarts are cheap

---

## Milestone 2: SEC EDGAR Filings & Insider Trades

**Status: COMPLETE**

Add two new tools backed by SEC EDGAR (free, unlimited API). These are the core differentiators — no API key needed, rich structured data. Reuse battle-tested patterns from `ai-investment-research-engine`.

### Context

SEC EDGAR provides:
- **Company filings** (10-K, 10-Q, 8-K) via `data.sec.gov/submissions/CIK{cik}.json`
- **Insider trades** (Form 4) via the same submissions endpoint + XML parsing
- Rate limit: 10 req/sec, requires descriptive User-Agent header
- CIK mapping from `sec.gov/files/company_tickers.json`

### Action Items

#### Data Layer

- [x] `src/mcp_finance/data/edgar.py` — SEC EDGAR client
  - [x] `_build_cik_map()` — Fetch and cache ticker→CIK mapping from `company_tickers.json`
  - [x] `_edgar_get(url)` — Shared request helper with User-Agent header, rate limiting (0.12s delay), 30s timeout, gzip decompression
  - [x] `fetch_filings(ticker, form_type, limit)` — Query submissions JSON, return filing metadata (date, accession, form type, items, primary doc)
  - [x] `fetch_filing_document(ticker, accession_number)` — Download and return primary filing document content
  - [x] `fetch_insider_trades(ticker, limit)` — Filter Form 4/4A filings, parse XML for transactions (insider name, title, relationship, buy/sell, shares, price, value)
  - [x] Integrate with TTL cache (filings: 30 min, CIK map: 24 hr)

#### Tools

- [x] `src/mcp_finance/tools/sec_filings.py` — MCP tool definitions
  - [x] `search_filings(ticker, form_type="10-K", limit=10)` — Search SEC filings, return metadata list
  - [x] `get_filing(ticker, accession_number)` — Fetch full filing document text (truncated for LLM context)
- [x] `src/mcp_finance/tools/insider_trades.py` — MCP tool definitions
  - [x] `get_insider_trades(ticker, limit=20)` — Return recent insider transactions with structured data

#### Server Registration

- [x] `src/mcp_finance/server.py` — Register new tools (`search_filings`, `get_filing`, `insider_trades`)

#### Tests

- [x] `tests/test_edgar.py` — Unit/integration tests (10 tests)
  - [x] Test CIK mapping lookup (AAPL → valid CIK)
  - [x] Test `fetch_filings` returns valid metadata for known ticker
  - [x] Test `fetch_insider_trades` returns structured transaction data
  - [x] Test invalid ticker handling
- [x] `tests/test_sec_filings.py` — Tool output format tests (3 tests)
- [x] `tests/test_insider_trades.py` — Tool output format tests (2 tests)

#### Docs

- [x] `README.md` — Add new tools to Available Tools table and example queries

### Key Decisions

- **No API key required** — SEC EDGAR is free and unlimited
- **User-Agent header** — Required by EDGAR policy; use project name + contact
- **Rate limiting at data layer** — 0.12s delay between requests (10 req/sec limit)
- **CIK map cached for 24 hours** — Changes infrequently, expensive to fetch
- **Filing text truncated** — Full 10-K can be 100k+ tokens; truncate to first N chars with a note
- **XML parsing with stdlib `xml.etree`** — No lxml dependency needed for Form 4 parsing
- **Accession number as filing ID** — Unique, stable, used in URLs

### EDGAR API Reference

| Endpoint | Purpose |
|----------|---------|
| `sec.gov/files/company_tickers.json` | Ticker → CIK mapping |
| `data.sec.gov/submissions/CIK{cik}.json` | Filing metadata (recent 100) |
| `sec.gov/Archives/edgar/data/{cik}/{accession}/{doc}` | Filing document |

### Verification

1. `pytest` — All new + existing tests pass
2. In Claude Desktop: "Show me Apple's recent 10-K filings"
3. In Claude Desktop: "What insider trades happened at Tesla recently?"
4. Existing price tools still work (no regressions)
