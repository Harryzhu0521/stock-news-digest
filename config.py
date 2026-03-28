import os

# --- RSS Feeds ---
RSS_FEEDS = [
    # Yahoo Finance
    {"name": "Yahoo Finance - Top Stories", "url": "https://finance.yahoo.com/news/rssindex"},
    {"name": "Yahoo Finance - Stock Market", "url": "https://finance.yahoo.com/rss/topstories"},

    # Bloomberg (via Google News RSS workaround)
    {"name": "Bloomberg via Google News", "url": "https://news.google.com/rss/search?q=site:bloomberg.com+stocks+OR+options+OR+tech&hl=en-US&gl=US&ceid=US:en"},

    # Reuters
    {"name": "Reuters - Markets", "url": "https://news.google.com/rss/search?q=site:reuters.com+stock+market+OR+options+OR+tech&hl=en-US&gl=US&ceid=US:en"},

    # NYT Business
    {"name": "NYT - Business", "url": "https://rss.nytimes.com/services/xml/rss/nyt/Business.xml"},

    # CNBC
    {"name": "CNBC - Finance", "url": "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10000664"},
    {"name": "CNBC - Technology", "url": "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=19854910"},

    # TechCrunch
    {"name": "TechCrunch", "url": "https://techcrunch.com/feed/"},

    # MarketWatch
    {"name": "MarketWatch - Top Stories", "url": "https://feeds.marketwatch.com/marketwatch/topstories/"},
    {"name": "MarketWatch - Market Pulse", "url": "https://feeds.marketwatch.com/marketwatch/marketpulse/"},
]

# --- Filter keywords (at least one must appear in title/summary) ---
KEYWORDS = [
    # Stocks & Markets
    "stock", "stocks", "equity", "equities", "S&P", "Nasdaq", "Dow",
    "bull", "bear", "rally", "sell-off", "selloff", "earnings",
    "IPO", "market", "trading", "investor",
    # Options
    "option", "options", "call", "put", "strike", "expiry",
    "volatility", "VIX", "derivative", "hedge",
    # Tech
    "tech", "technology", "AI", "artificial intelligence",
    "semiconductor", "chip", "NVIDIA", "Apple", "Google", "Microsoft",
    "Amazon", "Meta", "Tesla", "AMD", "TSMC", "Broadcom",
    "software", "cloud", "SaaS",
    # Macro relevant to quant
    "Fed", "interest rate", "inflation", "GDP", "CPI",
    "Treasury", "yield", "bond",
]

# --- Gemini ---
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL = "gemini-2.0-flash"  # free tier model

# --- Email ---
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = os.environ.get("EMAIL_SENDER", "")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD", "")  # Gmail App Password
EMAIL_RECIPIENT = os.environ.get("EMAIL_RECIPIENT", "")  # can be same as sender

# --- Digest settings ---
MAX_ARTICLES = 30  # max articles per digest
SUMMARY_LANGUAGE = "zh"  # "zh" for Chinese, "en" for English
