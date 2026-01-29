"""Unified Data Client with hybrid namespace design.

The DataClient provides:
1. Simple unified methods (client.data.bars, client.data.news, etc.)
2. Direct provider access for power users (client.data.alpaca, client.data.fred, etc.)

Usage:
    from cpz import CPZClient
    
    client = CPZClient()
    
    # Simple unified interface (smart routing)
    bars = client.data.bars("AAPL", timeframe="1D")
    quotes = client.data.quotes(["AAPL", "MSFT"])
    news = client.data.news("AAPL")
    economic = client.data.economic("GDP")
    filings = client.data.filings("AAPL", form="10-K")
    social = client.data.social("AAPL", source="reddit")
    
    # Direct provider access (power users)
    options = client.data.alpaca.get_options_chain("AAPL")
    series = client.data.fred.get_series("UNRATE")
    rsi = client.data.twelve.get_rsi("AAPL")
"""

from __future__ import annotations

import os
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Union

from .models import (
    Bar,
    Quote,
    Trade,
    News,
    OptionQuote,
    OptionContract,
    EconomicSeries,
    Filing,
    SocialPost,
    TimeFrame,
)


class _AlpacaNamespace:
    """Direct access to Alpaca Market Data API."""
    
    def __init__(self, parent: "DataClient"):
        self._parent = parent
        self._provider: Any = None
    
    def _get_provider(self) -> Any:
        if self._provider is None:
            from .providers.alpaca import AlpacaDataProvider
            self._provider = AlpacaDataProvider(
                api_key=self._parent._config.get("alpaca_api_key"),
                api_secret=self._parent._config.get("alpaca_api_secret"),
                feed=self._parent._config.get("alpaca_feed", "iex"),
            )
        return self._provider
    
    def get_bars(self, symbol: str, timeframe: TimeFrame | str = TimeFrame.DAY, **kwargs: Any) -> List[Bar]:
        """Get stock bars from Alpaca."""
        return self._get_provider().get_bars(symbol, timeframe, **kwargs)
    
    def get_quotes(self, symbols: List[str]) -> List[Quote]:
        """Get stock quotes from Alpaca."""
        return self._get_provider().get_quotes(symbols)
    
    def get_trades(self, symbol: str, **kwargs: Any) -> List[Trade]:
        """Get stock trades from Alpaca."""
        return self._get_provider().get_trades(symbol, **kwargs)
    
    def get_crypto_bars(self, symbol: str, timeframe: TimeFrame | str = TimeFrame.DAY, **kwargs: Any) -> List[Bar]:
        """Get crypto bars from Alpaca."""
        return self._get_provider().get_crypto_bars(symbol, timeframe, **kwargs)
    
    def get_crypto_quotes(self, symbols: List[str]) -> List[Quote]:
        """Get crypto quotes from Alpaca."""
        return self._get_provider().get_crypto_quotes(symbols)
    
    def get_options_chain(self, underlying: str, **kwargs: Any) -> List[OptionContract]:
        """Get options chain from Alpaca."""
        return self._get_provider().get_options_chain(underlying, **kwargs)
    
    def get_option_quotes(self, symbols: List[str]) -> List[OptionQuote]:
        """Get option quotes from Alpaca."""
        return self._get_provider().get_option_quotes(symbols)
    
    def get_news(self, symbols: Optional[List[str]] = None, **kwargs: Any) -> List[News]:
        """Get news from Alpaca."""
        return self._get_provider().get_news(symbols, **kwargs)


class _FREDNamespace:
    """Direct access to FRED economic data."""
    
    def __init__(self, parent: "DataClient"):
        self._parent = parent
        self._provider: Any = None
    
    def _get_provider(self) -> Any:
        if self._provider is None:
            from .providers.fred import FREDProvider
            self._provider = FREDProvider(
                api_key=self._parent._config.get("fred_api_key"),
            )
        return self._provider
    
    def get_series(self, series_id: str, **kwargs: Any) -> List[EconomicSeries]:
        """Get economic data series."""
        return self._get_provider().get_series(series_id, **kwargs)
    
    def search(self, query: str, **kwargs: Any) -> List[Dict[str, str]]:
        """Search for series."""
        return self._get_provider().search_series(query, **kwargs)
    
    def categories(self, category_id: int = 0) -> List[Dict[str, Any]]:
        """Get categories."""
        return self._get_provider().get_categories(category_id)


class _EDGARNamespace:
    """Direct access to SEC EDGAR filings."""
    
    def __init__(self, parent: "DataClient"):
        self._parent = parent
        self._provider: Any = None
    
    def _get_provider(self) -> Any:
        if self._provider is None:
            from .providers.edgar import EDGARProvider
            self._provider = EDGARProvider()
        return self._provider
    
    def get_filings(self, symbol: str, **kwargs: Any) -> List[Filing]:
        """Get SEC filings."""
        return self._get_provider().get_filings(symbol=symbol, **kwargs)
    
    def get_content(self, accession_number: str) -> str:
        """Get filing content."""
        return self._get_provider().get_filing_content(accession_number)
    
    def get_facts(self, symbol: str) -> Dict[str, Any]:
        """Get company XBRL facts."""
        return self._get_provider().get_company_facts(symbol)
    
    def get_concept(self, symbol: str, concept: str, taxonomy: str = "us-gaap") -> List[Dict[str, Any]]:
        """Get specific XBRL concept values."""
        return self._get_provider().get_company_concept(symbol, taxonomy, concept)
    
    def insider_transactions(self, symbol: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get insider transactions."""
        return self._get_provider().get_insider_transactions(symbol, limit)


class _TwelveNamespace:
    """Direct access to Twelve Data."""
    
    def __init__(self, parent: "DataClient"):
        self._parent = parent
        self._provider: Any = None
    
    def _get_provider(self) -> Any:
        if self._provider is None:
            from .providers.twelve import TwelveDataProvider
            self._provider = TwelveDataProvider(
                api_key=self._parent._config.get("twelve_api_key"),
            )
        return self._provider
    
    def get_bars(self, symbol: str, timeframe: TimeFrame | str = TimeFrame.DAY, **kwargs: Any) -> List[Bar]:
        """Get bars from Twelve Data."""
        return self._get_provider().get_bars(symbol, timeframe, **kwargs)
    
    def get_quote(self, symbol: str) -> Quote:
        """Get quote from Twelve Data."""
        return self._get_provider().get_quote(symbol)
    
    def get_forex(self, symbol: str) -> Dict[str, Any]:
        """Get forex quote."""
        return self._get_provider().get_forex_quote(symbol)
    
    def get_crypto(self, symbol: str) -> Dict[str, Any]:
        """Get crypto quote."""
        return self._get_provider().get_crypto_quote(symbol)
    
    # Technical Indicators
    def get_sma(self, symbol: str, period: int = 20, **kwargs: Any) -> List[Dict[str, Any]]:
        """Get Simple Moving Average."""
        return self._get_provider().get_sma(symbol, period=period, **kwargs)
    
    def get_ema(self, symbol: str, period: int = 20, **kwargs: Any) -> List[Dict[str, Any]]:
        """Get Exponential Moving Average."""
        return self._get_provider().get_ema(symbol, period=period, **kwargs)
    
    def get_rsi(self, symbol: str, period: int = 14, **kwargs: Any) -> List[Dict[str, Any]]:
        """Get RSI."""
        return self._get_provider().get_rsi(symbol, period=period, **kwargs)
    
    def get_macd(self, symbol: str, **kwargs: Any) -> List[Dict[str, Any]]:
        """Get MACD."""
        return self._get_provider().get_macd(symbol, **kwargs)
    
    def get_bbands(self, symbol: str, period: int = 20, **kwargs: Any) -> List[Dict[str, Any]]:
        """Get Bollinger Bands."""
        return self._get_provider().get_bbands(symbol, period=period, **kwargs)
    
    def indicator(self, name: str, symbol: str, **kwargs: Any) -> List[Dict[str, Any]]:
        """Get any technical indicator."""
        return self._get_provider().get_indicator(name, symbol, **kwargs)


class _SocialNamespace:
    """Direct access to social sentiment data."""
    
    def __init__(self, parent: "DataClient"):
        self._parent = parent
        self._reddit: Any = None
        self._stocktwits: Any = None
    
    def _get_reddit(self) -> Any:
        if self._reddit is None:
            from .providers.social import RedditProvider
            self._reddit = RedditProvider()
        return self._reddit
    
    def _get_stocktwits(self) -> Any:
        if self._stocktwits is None:
            from .providers.social import StocktwitsProvider
            self._stocktwits = StocktwitsProvider()
        return self._stocktwits
    
    def get_posts(
        self,
        symbols: Optional[List[str]] = None,
        source: str = "reddit",
        **kwargs: Any,
    ) -> List[SocialPost]:
        """Get social media posts."""
        if source.lower() == "stocktwits":
            return self._get_stocktwits().get_posts(symbols=symbols, **kwargs)
        return self._get_reddit().get_posts(symbols=symbols, **kwargs)
    
    def trending(self, source: str = "reddit", limit: int = 20) -> List[str]:
        """Get trending symbols."""
        if source.lower() == "stocktwits":
            return self._get_stocktwits().get_trending(limit=limit)
        return self._get_reddit().get_trending(limit=limit)
    
    def sentiment(self, symbol: str, source: str = "reddit") -> Dict[str, float]:
        """Get aggregated sentiment."""
        if source.lower() == "stocktwits":
            return self._get_stocktwits().get_sentiment(symbol)
        return self._get_reddit().get_sentiment(symbol)


class DataClient:
    """Unified data client with hybrid namespace design.
    
    Provides both simple unified methods and direct provider access.
    
    Simple Usage:
        client.data.bars("AAPL")           # Stock bars (routes to Alpaca)
        client.data.quotes(["AAPL"])       # Stock quotes
        client.data.news("AAPL")           # News articles
        client.data.economic("GDP")        # Economic data (routes to FRED)
        client.data.filings("AAPL")        # SEC filings (routes to EDGAR)
        client.data.social("AAPL")         # Social sentiment
    
    Power User Access:
        client.data.alpaca.get_options_chain("AAPL")
        client.data.fred.get_series("UNRATE")
        client.data.twelve.get_rsi("AAPL")
    """
    
    def __init__(
        self,
        alpaca_api_key: Optional[str] = None,
        alpaca_api_secret: Optional[str] = None,
        alpaca_feed: str = "iex",
        fred_api_key: Optional[str] = None,
        twelve_api_key: Optional[str] = None,
    ):
        """Initialize data client.
        
        Args:
            alpaca_api_key: Alpaca API key (or ALPACA_API_KEY_ID env var)
            alpaca_api_secret: Alpaca API secret (or ALPACA_API_SECRET_KEY env var)
            alpaca_feed: Alpaca data feed ("iex" or "sip")
            fred_api_key: FRED API key (or FRED_API_KEY env var)
            twelve_api_key: Twelve Data API key (or TWELVE_DATA_API_KEY env var)
        """
        self._config: Dict[str, Any] = {
            "alpaca_api_key": alpaca_api_key or os.getenv("ALPACA_API_KEY_ID"),
            "alpaca_api_secret": alpaca_api_secret or os.getenv("ALPACA_API_SECRET_KEY"),
            "alpaca_feed": alpaca_feed,
            "fred_api_key": fred_api_key or os.getenv("FRED_API_KEY"),
            "twelve_api_key": twelve_api_key or os.getenv("TWELVE_DATA_API_KEY"),
        }
        
        # Provider namespaces (lazy-loaded)
        self._alpaca: Optional[_AlpacaNamespace] = None
        self._fred: Optional[_FREDNamespace] = None
        self._edgar: Optional[_EDGARNamespace] = None
        self._twelve: Optional[_TwelveNamespace] = None
        self._social: Optional[_SocialNamespace] = None
    
    # --- Provider Namespaces (Power User Access) ---
    
    @property
    def alpaca(self) -> _AlpacaNamespace:
        """Direct access to Alpaca Market Data."""
        if self._alpaca is None:
            self._alpaca = _AlpacaNamespace(self)
        return self._alpaca
    
    @property
    def fred(self) -> _FREDNamespace:
        """Direct access to FRED economic data."""
        if self._fred is None:
            self._fred = _FREDNamespace(self)
        return self._fred
    
    @property
    def edgar(self) -> _EDGARNamespace:
        """Direct access to SEC EDGAR filings."""
        if self._edgar is None:
            self._edgar = _EDGARNamespace(self)
        return self._edgar
    
    @property
    def twelve(self) -> _TwelveNamespace:
        """Direct access to Twelve Data."""
        if self._twelve is None:
            self._twelve = _TwelveNamespace(self)
        return self._twelve
    
    @property
    def social(self) -> _SocialNamespace:
        """Direct access to social sentiment data."""
        if self._social is None:
            self._social = _SocialNamespace(self)
        return self._social
    
    # --- Unified Simple Interface ---
    
    def bars(
        self,
        symbol: str,
        timeframe: TimeFrame | str = TimeFrame.DAY,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        limit: int = 1000,
        provider: str = "auto",  # "auto", "alpaca", "twelve"
    ) -> List[Bar]:
        """Get historical price bars.
        
        Smart routing: Uses Alpaca for US stocks/crypto, Twelve for forex.
        
        Args:
            symbol: Symbol (e.g., "AAPL", "BTC/USD", "EUR/USD")
            timeframe: Bar timeframe (e.g., "1D", "1H", TimeFrame.DAY)
            start: Start datetime
            end: End datetime
            limit: Maximum bars to return
            provider: Force specific provider or "auto" for smart routing
            
        Returns:
            List of Bar objects
            
        Examples:
            >>> bars = client.data.bars("AAPL", timeframe="1D", limit=100)
            >>> crypto = client.data.bars("BTC/USD", timeframe="1H")
            >>> forex = client.data.bars("EUR/USD", provider="twelve")
        """
        if isinstance(timeframe, str):
            timeframe = TimeFrame.from_string(timeframe)
        
        # Smart routing
        if provider == "auto":
            if "/" in symbol and not any(c in symbol for c in ["BTC", "ETH", "SOL"]):
                # Likely forex pair
                provider = "twelve"
            else:
                provider = "alpaca"
        
        if provider == "twelve":
            return self.twelve.get_bars(symbol, timeframe, start=start, end=end, limit=limit)
        
        # Alpaca - detect crypto vs stock
        if "/" in symbol:
            return self.alpaca.get_crypto_bars(symbol, timeframe, start=start, end=end, limit=limit)
        return self.alpaca.get_bars(symbol, timeframe, start=start, end=end, limit=limit)
    
    def quotes(
        self,
        symbols: Union[str, List[str]],
        provider: str = "auto",
    ) -> List[Quote]:
        """Get latest quotes.
        
        Args:
            symbols: Symbol or list of symbols
            provider: Force specific provider or "auto"
            
        Returns:
            List of Quote objects
            
        Examples:
            >>> quotes = client.data.quotes(["AAPL", "MSFT", "GOOGL"])
            >>> quote = client.data.quotes("AAPL")[0]
        """
        if isinstance(symbols, str):
            symbols = [symbols]
        
        # Smart routing - check if any are crypto
        has_crypto = any("/" in s for s in symbols)
        
        if has_crypto:
            crypto_symbols = [s for s in symbols if "/" in s]
            stock_symbols = [s for s in symbols if "/" not in s]
            
            quotes: List[Quote] = []
            if crypto_symbols:
                quotes.extend(self.alpaca.get_crypto_quotes(crypto_symbols))
            if stock_symbols:
                quotes.extend(self.alpaca.get_quotes(stock_symbols))
            return quotes
        
        return self.alpaca.get_quotes(symbols)
    
    def trades(
        self,
        symbol: str,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        limit: int = 1000,
    ) -> List[Trade]:
        """Get historical trades.
        
        Args:
            symbol: Stock symbol
            start: Start datetime
            end: End datetime
            limit: Maximum trades
            
        Returns:
            List of Trade objects
        """
        return self.alpaca.get_trades(symbol, start=start, end=end, limit=limit)
    
    def news(
        self,
        symbols: Optional[Union[str, List[str]]] = None,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        limit: int = 50,
    ) -> List[News]:
        """Get news articles.
        
        Args:
            symbols: Filter by symbols (optional)
            start: Start datetime
            end: End datetime
            limit: Maximum articles
            
        Returns:
            List of News objects
            
        Examples:
            >>> news = client.data.news("AAPL", limit=10)
            >>> news = client.data.news(["AAPL", "TSLA"])
        """
        if isinstance(symbols, str):
            symbols = [symbols]
        return self.alpaca.get_news(symbols, start=start, end=end, limit=limit)
    
    def options(
        self,
        underlying: str,
        expiration: Optional[datetime] = None,
        option_type: Optional[str] = None,
        strike_min: Optional[float] = None,
        strike_max: Optional[float] = None,
    ) -> List[OptionContract]:
        """Get options chain.
        
        Args:
            underlying: Underlying stock symbol
            expiration: Expiration date filter
            option_type: "call" or "put"
            strike_min: Minimum strike price
            strike_max: Maximum strike price
            
        Returns:
            List of OptionContract objects
            
        Examples:
            >>> chain = client.data.options("AAPL")
            >>> calls = client.data.options("AAPL", option_type="call")
        """
        return self.alpaca.get_options_chain(
            underlying,
            expiration_date=expiration,
            option_type=option_type,
            strike_price_gte=strike_min,
            strike_price_lte=strike_max,
        )
    
    def economic(
        self,
        series_id: str,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        limit: int = 1000,
    ) -> List[EconomicSeries]:
        """Get economic data series from FRED.
        
        Args:
            series_id: FRED series ID (e.g., "GDP", "UNRATE", "CPIAUCSL")
            start: Start datetime
            end: End datetime
            limit: Maximum observations
            
        Returns:
            List of EconomicSeries observations
            
        Examples:
            >>> gdp = client.data.economic("GDP")
            >>> unemployment = client.data.economic("UNRATE", limit=12)
            >>> cpi = client.data.economic("CPIAUCSL", start=datetime(2020, 1, 1))
        """
        return self.fred.get_series(series_id, start=start, end=end, limit=limit)
    
    def filings(
        self,
        symbol: str,
        form: Optional[str] = None,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        limit: int = 100,
    ) -> List[Filing]:
        """Get SEC filings.
        
        Args:
            symbol: Stock symbol
            form: Form type (e.g., "10-K", "10-Q", "8-K")
            start: Start datetime
            end: End datetime
            limit: Maximum filings
            
        Returns:
            List of Filing objects
            
        Examples:
            >>> filings = client.data.filings("AAPL", form="10-K")
            >>> recent = client.data.filings("TSLA", limit=5)
        """
        return self.edgar.get_filings(
            symbol, form_type=form, start=start, end=end, limit=limit
        )
    
    def sentiment(
        self,
        symbol: str,
        source: str = "all",  # "all", "reddit", "stocktwits"
    ) -> Dict[str, Any]:
        """Get social sentiment for a symbol.
        
        Args:
            symbol: Stock symbol
            source: "reddit", "stocktwits", or "all"
            
        Returns:
            Aggregated sentiment data
            
        Examples:
            >>> sentiment = client.data.sentiment("AAPL")
            >>> reddit = client.data.sentiment("GME", source="reddit")
        """
        if source == "all":
            reddit = self.social.sentiment(symbol, source="reddit")
            stocktwits = self.social.sentiment(symbol, source="stocktwits")
            
            # Combine sentiments
            total_posts = reddit.get("post_count", 0) + stocktwits.get("post_count", 0)
            if total_posts == 0:
                return {
                    "score": 0.0,
                    "bullish_pct": 0.0,
                    "bearish_pct": 0.0,
                    "neutral_pct": 1.0,
                    "post_count": 0,
                    "sources": {"reddit": reddit, "stocktwits": stocktwits},
                }
            
            # Weighted average
            reddit_weight = reddit.get("post_count", 0) / total_posts
            stocktwits_weight = stocktwits.get("post_count", 0) / total_posts
            
            return {
                "score": reddit.get("score", 0) * reddit_weight + stocktwits.get("score", 0) * stocktwits_weight,
                "bullish_pct": reddit.get("bullish_pct", 0) * reddit_weight + stocktwits.get("bullish_pct", 0) * stocktwits_weight,
                "bearish_pct": reddit.get("bearish_pct", 0) * reddit_weight + stocktwits.get("bearish_pct", 0) * stocktwits_weight,
                "neutral_pct": reddit.get("neutral_pct", 0) * reddit_weight + stocktwits.get("neutral_pct", 0) * stocktwits_weight,
                "post_count": total_posts,
                "sources": {"reddit": reddit, "stocktwits": stocktwits},
            }
        
        return self.social.sentiment(symbol, source=source)
    
    def trending(self, source: str = "stocktwits", limit: int = 20) -> List[str]:
        """Get trending stock symbols.
        
        Args:
            source: "reddit" or "stocktwits"
            limit: Maximum symbols
            
        Returns:
            List of trending symbols
            
        Examples:
            >>> trending = client.data.trending()
            >>> reddit_trending = client.data.trending(source="reddit")
        """
        return self.social.trending(source=source, limit=limit)
    
    # --- Technical Indicators (convenience) ---
    
    def sma(
        self,
        symbol: str,
        period: int = 20,
        timeframe: TimeFrame | str = TimeFrame.DAY,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """Get Simple Moving Average.
        
        Args:
            symbol: Stock symbol
            period: SMA period
            timeframe: Bar timeframe
            limit: Number of data points
            
        Returns:
            List of SMA values with timestamps
        """
        return self.twelve.get_sma(symbol, period=period, timeframe=timeframe, limit=limit)
    
    def rsi(
        self,
        symbol: str,
        period: int = 14,
        timeframe: TimeFrame | str = TimeFrame.DAY,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """Get Relative Strength Index.
        
        Args:
            symbol: Stock symbol
            period: RSI period
            timeframe: Bar timeframe
            limit: Number of data points
            
        Returns:
            List of RSI values with timestamps
        """
        return self.twelve.get_rsi(symbol, period=period, timeframe=timeframe, limit=limit)
    
    def macd(
        self,
        symbol: str,
        timeframe: TimeFrame | str = TimeFrame.DAY,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """Get MACD.
        
        Args:
            symbol: Stock symbol
            timeframe: Bar timeframe
            limit: Number of data points
            
        Returns:
            List of MACD values with timestamps
        """
        return self.twelve.get_macd(symbol, timeframe=timeframe, limit=limit)
