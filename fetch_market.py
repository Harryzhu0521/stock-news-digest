"""Fetch stock market data from Yahoo Finance (yfinance) and FRED."""

import requests
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


# --- Options / Volatility ---
OPTIONS_TICKERS = {
    "^VIX": "VIX",
    "^VIX3M": "VIX3M (3个月)",
}

# IV tracking for major stocks
IV_STOCKS = ["NVDA", "TSLA", "AAPL", "MSFT", "AMZN", "META", "SPY", "QQQ"]


def _fetch_put_call_ratio() -> dict:
    """Fetch CBOE Total Put/Call Ratio."""
    try:
        # Use FRED for equity put/call (not available), fallback to yfinance for proxy
        # We'll compute from SPY options chain as a proxy
        spy = yf.Ticker("SPY")
        exp = spy.options[0]  # nearest expiry
        calls = spy.option_chain(exp).calls
        puts = spy.option_chain(exp).puts
        call_vol = calls["volume"].sum()
        put_vol = puts["volume"].sum()
        if call_vol > 0:
            ratio = put_vol / call_vol
            return {
                "ratio": round(ratio, 3),
                "put_vol": int(put_vol),
                "call_vol": int(call_vol),
                "expiry": exp,
            }
    except Exception:
        pass
    return {}


def _fetch_iv(ticker: str) -> float | None:
    """Fetch approximate implied volatility for a stock from nearest-expiry ATM options."""
    try:
        t = yf.Ticker(ticker)
        price = t.fast_info.get("lastPrice", None)
        if not price:
            return None
        exp = t.options[0]
        chain = t.option_chain(exp)
        calls = chain.calls
        # Find ATM call (closest strike to current price)
        calls = calls[calls["impliedVolatility"] > 0].copy()
        if calls.empty:
            return None
        calls["strike_diff"] = (calls["strike"] - price).abs()
        atm = calls.loc[calls["strike_diff"].idxmin()]
        return round(atm["impliedVolatility"] * 100, 1)
    except Exception:
        return None


def fetch_options_data() -> dict:
    """Fetch options market data: VIX term structure, P/C ratio, IVs."""
    result = {}

    # VIX term structure
    vix_data = {}
    for ticker, name in OPTIONS_TICKERS.items():
        data = _fetch_quote(ticker)
        if data:
            vix_data[name] = data
    result["vix"] = vix_data

    # VIX contango/backwardation
    if "VIX" in vix_data and "VIX3M (3个月)" in vix_data:
        vix_val = vix_data["VIX"]["price"]
        vix3m_val = vix_data["VIX3M (3个月)"]["price"]
        if vix3m_val > 0:
            ratio = vix_val / vix3m_val
            result["vix_term"] = {
                "ratio": round(ratio, 3),
                "status": "Backwardation (近期恐慌)" if ratio > 1 else "Contango (正常)",
            }

    # Put/Call ratio
    pc = _fetch_put_call_ratio()
    if pc:
        result["put_call"] = pc

    # Implied volatility for major stocks
    ivs = {}
    for ticker in IV_STOCKS:
        iv = _fetch_iv(ticker)
        if iv is not None:
            ivs[ticker] = iv
    result["ivs"] = ivs

    return result


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


def format_market_data(indices: dict, tech: dict, sectors: list, treasuries: dict, options: dict) -> dict:
    """Format all market data into structured dict for template rendering."""
    return {
        "indices": indices,
        "tech_stocks": tech,
        "sectors": sectors,
        "treasuries": treasuries,
        "options": options,
    }
