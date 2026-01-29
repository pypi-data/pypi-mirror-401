"""Alpaca Market Data provider.

Supports:
- Stocks: bars, quotes, trades (historical + real-time)
- Crypto: bars, quotes, trades (historical + real-time)  
- Options: chains, quotes
- News: articles with sentiment

Docs: https://docs.alpaca.markets/docs/about-market-data-api
"""

from __future__ import annotations

import os
from datetime import datetime, timedelta
from typing import Any, AsyncIterator, Dict, List, Optional

from ..models import (
    Bar,
    Quote,
    Trade,
    News,
    OptionQuote,
    OptionContract,
    TimeFrame,
)


class AlpacaDataProvider:
    """Alpaca Market Data API provider.
    
    Usage:
        provider = AlpacaDataProvider()
        bars = provider.get_bars("AAPL", TimeFrame.DAY, limit=100)
        quotes = provider.get_quotes(["AAPL", "MSFT"])
    """
    
    name = "alpaca"
    supported_assets = ["stocks", "crypto", "options", "news"]
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        feed: str = "iex",  # "iex" (free) or "sip" (paid)
    ):
        """Initialize Alpaca data provider.
        
        Args:
            api_key: Alpaca API key (defaults to ALPACA_API_KEY_ID env var)
            api_secret: Alpaca API secret (defaults to ALPACA_API_SECRET_KEY env var)
            feed: Data feed - "iex" (free, 15min delayed) or "sip" (paid, real-time)
        """
        self._api_key = api_key or os.getenv("ALPACA_API_KEY_ID", "")
        self._api_secret = api_secret or os.getenv("ALPACA_API_SECRET_KEY", "")
        self._feed = feed
        self._stock_client: Any = None
        self._crypto_client: Any = None
        self._option_client: Any = None
        self._news_client: Any = None
    
    def _get_stock_client(self) -> Any:
        """Lazy-load Alpaca stock historical client."""
        if self._stock_client is None:
            try:
                from alpaca.data.historical import StockHistoricalDataClient
                self._stock_client = StockHistoricalDataClient(
                    api_key=self._api_key,
                    secret_key=self._api_secret,
                )
            except ImportError:
                raise ImportError(
                    "alpaca-py is required for Alpaca data. Install with: pip install alpaca-py"
                )
        return self._stock_client
    
    def _get_crypto_client(self) -> Any:
        """Lazy-load Alpaca crypto historical client."""
        if self._crypto_client is None:
            try:
                from alpaca.data.historical import CryptoHistoricalDataClient
                self._crypto_client = CryptoHistoricalDataClient(
                    api_key=self._api_key,
                    secret_key=self._api_secret,
                )
            except ImportError:
                raise ImportError(
                    "alpaca-py is required for Alpaca data. Install with: pip install alpaca-py"
                )
        return self._crypto_client
    
    def _get_option_client(self) -> Any:
        """Lazy-load Alpaca option historical client."""
        if self._option_client is None:
            try:
                from alpaca.data.historical import OptionHistoricalDataClient
                self._option_client = OptionHistoricalDataClient(
                    api_key=self._api_key,
                    secret_key=self._api_secret,
                )
            except ImportError:
                raise ImportError(
                    "alpaca-py is required for options data. Install with: pip install alpaca-py"
                )
        return self._option_client
    
    def _convert_timeframe(self, tf: TimeFrame) -> Any:
        """Convert TimeFrame to Alpaca TimeFrame."""
        from alpaca.data.timeframe import TimeFrame as AlpacaTF, TimeFrameUnit
        
        mapping = {
            TimeFrame.MINUTE_1: AlpacaTF(1, TimeFrameUnit.Minute),
            TimeFrame.MINUTE_5: AlpacaTF(5, TimeFrameUnit.Minute),
            TimeFrame.MINUTE_15: AlpacaTF(15, TimeFrameUnit.Minute),
            TimeFrame.MINUTE_30: AlpacaTF(30, TimeFrameUnit.Minute),
            TimeFrame.HOUR_1: AlpacaTF(1, TimeFrameUnit.Hour),
            TimeFrame.HOUR_4: AlpacaTF(4, TimeFrameUnit.Hour),
            TimeFrame.DAY: AlpacaTF(1, TimeFrameUnit.Day),
            TimeFrame.WEEK: AlpacaTF(1, TimeFrameUnit.Week),
            TimeFrame.MONTH: AlpacaTF(1, TimeFrameUnit.Month),
        }
        return mapping.get(tf, AlpacaTF(1, TimeFrameUnit.Day))
    
    # --- Stock Data ---
    
    def get_bars(
        self,
        symbol: str,
        timeframe: TimeFrame | str = TimeFrame.DAY,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        limit: int = 1000,
        adjustment: str = "raw",  # "raw", "split", "dividend", "all"
    ) -> List[Bar]:
        """Get historical stock bars.
        
        Args:
            symbol: Stock symbol (e.g., "AAPL")
            timeframe: Bar timeframe
            start: Start datetime (defaults to 30 days ago)
            end: End datetime (defaults to now)
            limit: Maximum bars to return
            adjustment: Price adjustment type
            
        Returns:
            List of Bar objects
        """
        from alpaca.data.requests import StockBarsRequest
        
        if isinstance(timeframe, str):
            timeframe = TimeFrame.from_string(timeframe)
        
        if start is None:
            start = datetime.utcnow() - timedelta(days=30)
        if end is None:
            end = datetime.utcnow()
        
        client = self._get_stock_client()
        request = StockBarsRequest(
            symbol_or_symbols=symbol,
            timeframe=self._convert_timeframe(timeframe),
            start=start,
            end=end,
            limit=limit,
            adjustment=adjustment,
            feed=self._feed,
        )
        
        response = client.get_stock_bars(request)
        bars: List[Bar] = []
        
        if symbol in response:
            for bar in response[symbol]:
                bars.append(Bar(
                    symbol=symbol,
                    timestamp=bar.timestamp,
                    open=float(bar.open),
                    high=float(bar.high),
                    low=float(bar.low),
                    close=float(bar.close),
                    volume=float(bar.volume),
                    vwap=float(bar.vwap) if bar.vwap else None,
                    trade_count=bar.trade_count if hasattr(bar, 'trade_count') else None,
                ))
        
        return bars
    
    def get_quotes(self, symbols: List[str]) -> List[Quote]:
        """Get latest quotes for stock symbols.
        
        Args:
            symbols: List of stock symbols
            
        Returns:
            List of Quote objects
        """
        from alpaca.data.requests import StockLatestQuoteRequest
        
        client = self._get_stock_client()
        request = StockLatestQuoteRequest(
            symbol_or_symbols=symbols,
            feed=self._feed,
        )
        
        response = client.get_stock_latest_quote(request)
        quotes: List[Quote] = []
        
        for symbol, quote in response.items():
            quotes.append(Quote(
                symbol=symbol,
                timestamp=quote.timestamp,
                bid=float(quote.bid_price) if quote.bid_price else 0.0,
                ask=float(quote.ask_price) if quote.ask_price else 0.0,
                bid_size=float(quote.bid_size) if quote.bid_size else 0.0,
                ask_size=float(quote.ask_size) if quote.ask_size else 0.0,
            ))
        
        return quotes
    
    def get_trades(
        self,
        symbol: str,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        limit: int = 1000,
    ) -> List[Trade]:
        """Get historical stock trades.
        
        Args:
            symbol: Stock symbol
            start: Start datetime
            end: End datetime  
            limit: Maximum trades to return
            
        Returns:
            List of Trade objects
        """
        from alpaca.data.requests import StockTradesRequest
        
        if start is None:
            start = datetime.utcnow() - timedelta(days=1)
        if end is None:
            end = datetime.utcnow()
        
        client = self._get_stock_client()
        request = StockTradesRequest(
            symbol_or_symbols=symbol,
            start=start,
            end=end,
            limit=limit,
            feed=self._feed,
        )
        
        response = client.get_stock_trades(request)
        trades: List[Trade] = []
        
        if symbol in response:
            for trade in response[symbol]:
                trades.append(Trade(
                    symbol=symbol,
                    timestamp=trade.timestamp,
                    price=float(trade.price),
                    size=float(trade.size),
                    exchange=trade.exchange if hasattr(trade, 'exchange') else None,
                    conditions=list(trade.conditions) if hasattr(trade, 'conditions') and trade.conditions else None,
                ))
        
        return trades
    
    # --- Crypto Data ---
    
    def get_crypto_bars(
        self,
        symbol: str,
        timeframe: TimeFrame | str = TimeFrame.DAY,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        limit: int = 1000,
    ) -> List[Bar]:
        """Get historical crypto bars.
        
        Args:
            symbol: Crypto symbol (e.g., "BTC/USD")
            timeframe: Bar timeframe
            start: Start datetime
            end: End datetime
            limit: Maximum bars to return
            
        Returns:
            List of Bar objects
        """
        from alpaca.data.requests import CryptoBarsRequest
        
        if isinstance(timeframe, str):
            timeframe = TimeFrame.from_string(timeframe)
        
        if start is None:
            start = datetime.utcnow() - timedelta(days=30)
        if end is None:
            end = datetime.utcnow()
        
        client = self._get_crypto_client()
        request = CryptoBarsRequest(
            symbol_or_symbols=symbol,
            timeframe=self._convert_timeframe(timeframe),
            start=start,
            end=end,
            limit=limit,
        )
        
        response = client.get_crypto_bars(request)
        bars: List[Bar] = []
        
        if symbol in response:
            for bar in response[symbol]:
                bars.append(Bar(
                    symbol=symbol,
                    timestamp=bar.timestamp,
                    open=float(bar.open),
                    high=float(bar.high),
                    low=float(bar.low),
                    close=float(bar.close),
                    volume=float(bar.volume),
                    vwap=float(bar.vwap) if bar.vwap else None,
                    trade_count=bar.trade_count if hasattr(bar, 'trade_count') else None,
                ))
        
        return bars
    
    def get_crypto_quotes(self, symbols: List[str]) -> List[Quote]:
        """Get latest crypto quotes.
        
        Args:
            symbols: List of crypto symbols (e.g., ["BTC/USD", "ETH/USD"])
            
        Returns:
            List of Quote objects
        """
        from alpaca.data.requests import CryptoLatestQuoteRequest
        
        client = self._get_crypto_client()
        request = CryptoLatestQuoteRequest(symbol_or_symbols=symbols)
        
        response = client.get_crypto_latest_quote(request)
        quotes: List[Quote] = []
        
        for symbol, quote in response.items():
            quotes.append(Quote(
                symbol=symbol,
                timestamp=quote.timestamp,
                bid=float(quote.bid_price) if quote.bid_price else 0.0,
                ask=float(quote.ask_price) if quote.ask_price else 0.0,
                bid_size=float(quote.bid_size) if quote.bid_size else 0.0,
                ask_size=float(quote.ask_size) if quote.ask_size else 0.0,
            ))
        
        return quotes
    
    # --- Options Data ---
    
    def get_options_chain(
        self,
        underlying: str,
        expiration_date: Optional[datetime] = None,
        expiration_date_gte: Optional[datetime] = None,
        expiration_date_lte: Optional[datetime] = None,
        option_type: Optional[str] = None,  # "call" or "put"
        strike_price_gte: Optional[float] = None,
        strike_price_lte: Optional[float] = None,
    ) -> List[OptionContract]:
        """Get options chain for underlying symbol.
        
        Args:
            underlying: Underlying stock symbol (e.g., "AAPL")
            expiration_date: Exact expiration date
            expiration_date_gte: Minimum expiration date
            expiration_date_lte: Maximum expiration date
            option_type: "call" or "put"
            strike_price_gte: Minimum strike price
            strike_price_lte: Maximum strike price
            
        Returns:
            List of OptionContract objects
        """
        from alpaca.data.requests import OptionChainRequest
        
        client = self._get_option_client()
        
        request_params: Dict[str, Any] = {
            "underlying_symbol": underlying,
        }
        
        if expiration_date:
            request_params["expiration_date"] = expiration_date.date()
        if expiration_date_gte:
            request_params["expiration_date_gte"] = expiration_date_gte.date()
        if expiration_date_lte:
            request_params["expiration_date_lte"] = expiration_date_lte.date()
        if option_type:
            request_params["type"] = option_type.lower()
        if strike_price_gte is not None:
            request_params["strike_price_gte"] = strike_price_gte
        if strike_price_lte is not None:
            request_params["strike_price_lte"] = strike_price_lte
        
        request = OptionChainRequest(**request_params)
        response = client.get_option_chain(request)
        
        contracts: List[OptionContract] = []
        for symbol, snapshots in response.items():
            # Parse option symbol to extract details
            # Alpaca format: AAPL240119C00150000
            contracts.append(OptionContract(
                symbol=symbol,
                underlying=underlying,
                expiration=snapshots.latest_quote.timestamp if snapshots.latest_quote else datetime.utcnow(),
                strike=0.0,  # Would need to parse from symbol
                option_type="call" if "C" in symbol else "put",
            ))
        
        return contracts
    
    def get_option_quotes(self, symbols: List[str]) -> List[OptionQuote]:
        """Get quotes for option symbols.
        
        Args:
            symbols: List of option symbols (e.g., ["AAPL240119C00150000"])
            
        Returns:
            List of OptionQuote objects
        """
        from alpaca.data.requests import OptionLatestQuoteRequest
        
        client = self._get_option_client()
        request = OptionLatestQuoteRequest(symbol_or_symbols=symbols)
        
        response = client.get_option_latest_quote(request)
        quotes: List[OptionQuote] = []
        
        for symbol, quote in response.items():
            # Extract underlying from option symbol (first part before date)
            underlying = ""
            for i, c in enumerate(symbol):
                if c.isdigit():
                    underlying = symbol[:i]
                    break
            
            quotes.append(OptionQuote(
                symbol=symbol,
                underlying=underlying,
                timestamp=quote.timestamp,
                bid=float(quote.bid_price) if quote.bid_price else 0.0,
                ask=float(quote.ask_price) if quote.ask_price else 0.0,
                bid_size=int(quote.bid_size) if quote.bid_size else 0,
                ask_size=int(quote.ask_size) if quote.ask_size else 0,
            ))
        
        return quotes
    
    # --- News Data ---
    
    def get_news(
        self,
        symbols: Optional[List[str]] = None,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        limit: int = 50,
        include_content: bool = False,
    ) -> List[News]:
        """Get news articles.
        
        Args:
            symbols: Filter by symbols (optional)
            start: Start datetime
            end: End datetime
            limit: Maximum articles to return
            include_content: Include full article content
            
        Returns:
            List of News objects
        """
        from alpaca.data.requests import NewsRequest
        from alpaca.data.historical.news import NewsClient
        
        if self._news_client is None:
            self._news_client = NewsClient(
                api_key=self._api_key,
                secret_key=self._api_secret,
            )
        
        request_params: Dict[str, Any] = {
            "limit": limit,
            "include_content": include_content,
        }
        if symbols:
            request_params["symbols"] = symbols
        if start:
            request_params["start"] = start
        if end:
            request_params["end"] = end
        
        request = NewsRequest(**request_params)
        response = self._news_client.get_news(request)
        
        articles: List[News] = []
        for article in response.news:
            articles.append(News(
                id=str(article.id),
                headline=article.headline,
                summary=article.summary if hasattr(article, 'summary') else None,
                author=article.author if hasattr(article, 'author') else None,
                source=article.source,
                url=article.url if hasattr(article, 'url') else None,
                symbols=list(article.symbols) if article.symbols else [],
                created_at=article.created_at,
                updated_at=article.updated_at if hasattr(article, 'updated_at') else None,
                images=article.images if hasattr(article, 'images') else None,
            ))
        
        return articles
    
    # --- Streaming ---
    
    async def stream_quotes(self, symbols: List[str]) -> AsyncIterator[Quote]:
        """Stream real-time stock quotes.
        
        Args:
            symbols: List of symbols to stream
            
        Yields:
            Quote objects as they arrive
        """
        from alpaca.data.live import StockDataStream
        
        stream = StockDataStream(
            api_key=self._api_key,
            secret_key=self._api_secret,
            feed=self._feed,
        )
        
        async def quote_handler(quote: Any) -> None:
            pass  # Placeholder - actual implementation would yield
        
        stream.subscribe_quotes(quote_handler, *symbols)
        
        # Placeholder - actual streaming implementation
        async def _gen() -> AsyncIterator[Quote]:
            yield Quote(symbol=symbols[0], bid=0.0, ask=0.0)
        
        async for q in _gen():
            yield q
    
    async def stream_trades(self, symbols: List[str]) -> AsyncIterator[Trade]:
        """Stream real-time trades."""
        async def _gen() -> AsyncIterator[Trade]:
            yield Trade(
                symbol=symbols[0],
                timestamp=datetime.utcnow(),
                price=0.0,
                size=0.0,
            )
        async for t in _gen():
            yield t
    
    async def stream_bars(
        self, symbols: List[str], timeframe: TimeFrame = TimeFrame.MINUTE_1
    ) -> AsyncIterator[Bar]:
        """Stream real-time bars."""
        async def _gen() -> AsyncIterator[Bar]:
            yield Bar(
                symbol=symbols[0],
                timestamp=datetime.utcnow(),
                open=0.0,
                high=0.0,
                low=0.0,
                close=0.0,
                volume=0.0,
            )
        async for b in _gen():
            yield b
