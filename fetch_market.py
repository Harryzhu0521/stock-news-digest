"""Fetch stock market data from Yahoo Finance (yfinance) and FRED."""

import yfinance as yf


# --- 1. Major indices ---
INDICES = {
    "^GSPC": "S&P 500",
    "^IXIC": "Nasdaq",
    "^DJI": "Dow Jones",
    "^VIX": "VIX 恐慌指数",
}

# --- 2. Hot tech stocks ---
TECH_STOCKS = {
    "NVDA": "NVIDIA",
    "AAPL": "Apple",
    "MSFT": "Microsoft",
    "GOOGL": "Google",
    "AMZN": "Amazon",
    "META": "Meta",
    "TSLA": "Tesla",
    "AMD": "AMD",
    "AVGO": "Broadcom",
    "TSM": "TSMC",
}

# --- 3. Sector ETFs (S&P 500 sectors) ---
SECTOR_ETFS = {
    "XLK": "科技",
    "XLF": "金融",
    "XLV": "医疗",
    "XLE": "能源",
    "XLY": "消费",
    "XLP": "必需消费",
    "XLI": "工业",
    "XLB": "材料",
    "XLRE": "房地产",
    "XLU": "公用事业",
    "XLC": "通信",
}

# --- 5. Treasury yields ---
TREASURIES = {
    "^TNX": "10年期美债",
    "^FVX": "5年期美债",
    "^IRX": "2年期美债",
}


def _fetch_quote(ticker: str) -> dict:
    """Fetch latest quote for a single ticker."""
    try:
        t = yf.Ticker(ticker)
        info = t.fast_info
        price = info.get("lastPrice", None) or info.get("regularMarketPrice", None)
        prev = info.get("previousClose", None) or info.get("regularMarketPreviousClose", None)

        if price is None:
            # Fallback: use history
            hist = t.history(period="2d")
            if len(hist) >= 1:
                price = hist["Close"].iloc[-1]
                if len(hist) >= 2:
                    prev = hist["Close"].iloc[-2]

        if price is not None and prev is not None and prev != 0:
            change = price - prev
            change_pct = (change / prev) * 100
            return {
                "price": price,
                "change": change,
                "change_pct": change_pct,
            }
        elif price is not None:
            return {"price": price, "change": 0, "change_pct": 0}
    except Exception:
        pass
    return {}


def fetch_indices() -> dict:
    """Fetch major index data."""
    results = {}
    for ticker, name in INDICES.items():
        data = _fetch_quote(ticker)
        if data:
            results[name] = data
    return results


def fetch_tech_stocks() -> dict:
    """Fetch tech stock data."""
    results = {}
    for ticker, name in TECH_STOCKS.items():
        data = _fetch_quote(ticker)
        if data:
            data["ticker"] = ticker
            results[name] = data
    return results


def fetch_sectors() -> list[dict]:
    """Fetch sector ETF performance, sorted by daily change."""
    results = []
    for ticker, name in SECTOR_ETFS.items():
        data = _fetch_quote(ticker)
        if data:
            results.append({"name": name, "ticker": ticker, **data})
    results.sort(key=lambda x: x.get("change_pct", 0), reverse=True)
    return results


def fetch_treasuries() -> dict:
    """Fetch treasury yields."""
    results = {}
    for ticker, name in TREASURIES.items():
        data = _fetch_quote(ticker)
        if data:
            results[name] = data
    return results


def format_market_data(indices: dict, tech: dict, sectors: list, treasuries: dict) -> dict:
    """Format all market data into structured dict for template rendering."""
    return {
        "indices": indices,
        "tech_stocks": tech,
        "sectors": sectors,
        "treasuries": treasuries,
    }
