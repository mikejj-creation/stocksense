"""yfinance wrapper for market data fetching."""

import yfinance as yf

from mcp_finance.data.cache import price_cache, quote_cache


def fetch_price_history(
    ticker: str,
    period: str = "1mo",
    interval: str = "1d",
) -> list[dict]:
    """Fetch historical price data for a ticker.

    Returns list of dicts with keys: date, open, high, low, close, volume.
    """
    cache_key = f"price:{ticker}:{period}:{interval}"
    cached = price_cache.get(cache_key)
    if cached is not None:
        return cached

    try:
        df = yf.download(
            ticker,
            period=period,
            interval=interval,
            auto_adjust=False,
            progress=False,
        )
    except Exception as e:
        raise RuntimeError(f"Failed to fetch price data for {ticker}: {e}") from e

    if df.empty:
        raise ValueError(f"No price data returned for ticker '{ticker}'")

    # yf.download returns MultiIndex columns when single ticker; flatten
    if hasattr(df.columns, "droplevel") and df.columns.nlevels > 1:
        df.columns = df.columns.droplevel(1)

    records: list[dict] = []
    for idx, row in df.iterrows():
        records.append(
            {
                "date": idx.strftime("%Y-%m-%d") if interval in ("1d", "1wk", "1mo") else idx.isoformat(),
                "open": round(float(row["Open"]), 2),
                "high": round(float(row["High"]), 2),
                "low": round(float(row["Low"]), 2),
                "close": round(float(row["Close"]), 2),
                "volume": int(row["Volume"]),
            }
        )

    price_cache.set(cache_key, records)
    return records


def fetch_quote(ticker: str) -> dict:
    """Fetch current quote snapshot for a ticker."""
    cache_key = f"quote:{ticker}"
    cached = quote_cache.get(cache_key)
    if cached is not None:
        return cached

    try:
        info = yf.Ticker(ticker).info
    except Exception as e:
        raise RuntimeError(f"Failed to fetch quote for {ticker}: {e}") from e

    if not info or info.get("regularMarketPrice") is None:
        raise ValueError(f"No quote data available for ticker '{ticker}'")

    quote = {
        "ticker": ticker.upper(),
        "price": info.get("regularMarketPrice"),
        "previous_close": info.get("previousClose"),
        "open": info.get("regularMarketOpen"),
        "day_high": info.get("dayHigh"),
        "day_low": info.get("dayLow"),
        "volume": info.get("volume"),
        "market_cap": info.get("marketCap"),
        "pe_ratio": info.get("trailingPE"),
        "fifty_two_week_high": info.get("fiftyTwoWeekHigh"),
        "fifty_two_week_low": info.get("fiftyTwoWeekLow"),
        "name": info.get("shortName"),
    }

    quote_cache.set(cache_key, quote)
    return quote
