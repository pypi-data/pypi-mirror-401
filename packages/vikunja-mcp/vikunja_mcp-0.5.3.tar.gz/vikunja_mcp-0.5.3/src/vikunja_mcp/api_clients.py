"""
External API Clients for @eis Smart Tasks.

Weather: OpenWeatherMap API
Stock: Alpha Vantage API (or free yfinance)
News: NewsAPI

Each client handles:
- API calls with proper error handling
- Response parsing to normalized dict format
- Template formatting (free tier)

Bead: solutions-hgwx.3
"""

import logging
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

import aiohttp

from .rate_limiter import get_rate_limiter

logger = logging.getLogger(__name__)


@dataclass
class APIResponse:
    """Normalized response from external API."""

    success: bool
    data: Optional[dict] = None
    formatted: str = ""  # Free tier template-formatted output
    error: Optional[str] = None


class WeatherClient:
    """OpenWeatherMap API client.

    Usage:
        client = WeatherClient()
        response = await client.get_weather("San Francisco")

        if response.success:
            print(response.formatted)  # Free tier: template output
            print(response.data)       # Raw data for LLM formatting
    """

    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    def __init__(self, api_key: Optional[str] = None):
        """Initialize weather client.

        Args:
            api_key: OpenWeatherMap API key (falls back to OPENWEATHERMAP_API_KEY env var)
        """
        self.api_key = api_key or os.environ.get("OPENWEATHERMAP_API_KEY")

    async def get_weather(self, location: str) -> APIResponse:
        """Get current weather for a location.

        Args:
            location: City name (e.g., "San Francisco" or "London,UK")

        Returns:
            APIResponse with weather data
        """
        if not self.api_key:
            return APIResponse(
                success=False,
                error="Weather API not configured. Set OPENWEATHERMAP_API_KEY environment variable."
            )

        # Check rate limit before making call
        limiter = get_rate_limiter()
        if not limiter.can_call("weather"):
            used, limit = limiter.get_usage("weather")
            return APIResponse(
                success=False,
                error=f"Daily API limit reached ({used}/{limit} calls). Try again tomorrow."
            )

        params = {
            "q": location,
            "appid": self.api_key,
            "units": "imperial",  # Fahrenheit
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.BASE_URL, params=params, timeout=10) as resp:
                    if resp.status == 404:
                        return APIResponse(
                            success=False,
                            error=f"Location not found: {location}"
                        )
                    if resp.status != 200:
                        text = await resp.text()
                        logger.error(f"Weather API error {resp.status}: {text}")
                        return APIResponse(
                            success=False,
                            error=f"Weather API error: {resp.status}"
                        )

                    data = await resp.json()

                    # Record successful API call
                    limiter.record_call("weather")

        except aiohttp.ClientError as e:
            logger.error(f"Weather API request failed: {e}")
            return APIResponse(success=False, error=f"Network error: {e}")
        except Exception as e:
            logger.exception(f"Weather API unexpected error: {e}")
            return APIResponse(success=False, error=str(e))

        # Parse response
        # OpenWeatherMap returns timezone as offset in seconds from UTC
        tz_offset_seconds = data.get("timezone", 0)
        tz_offset_hours = tz_offset_seconds // 3600
        tz_offset_minutes = abs(tz_offset_seconds % 3600) // 60

        # Format timezone string (e.g., "+1:00", "-5:00", "+5:30")
        if tz_offset_hours >= 0:
            tz_str = f"UTC+{tz_offset_hours}"
        else:
            tz_str = f"UTC{tz_offset_hours}"
        if tz_offset_minutes:
            tz_str += f":{tz_offset_minutes:02d}"

        weather = {
            "location": data.get("name", location),
            "country": data.get("sys", {}).get("country", ""),
            "temp_f": round(data.get("main", {}).get("temp", 0)),
            "temp_c": round((data.get("main", {}).get("temp", 32) - 32) * 5 / 9),
            "feels_like_f": round(data.get("main", {}).get("feels_like", 0)),
            "humidity": data.get("main", {}).get("humidity", 0),
            "description": data.get("weather", [{}])[0].get("description", "Unknown"),
            "icon": data.get("weather", [{}])[0].get("icon", ""),
            "wind_mph": round(data.get("wind", {}).get("speed", 0)),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "tz_offset": tz_offset_seconds,  # Offset in seconds for local time calc
            "tz_label": tz_str,  # Human-readable timezone label
        }

        # Template formatting (free tier)
        formatted = self._format_template(weather)

        return APIResponse(success=True, data=weather, formatted=formatted)

    def _format_template(self, weather: dict) -> str:
        """Format weather data as template (free tier).

        Args:
            weather: Parsed weather dict

        Returns:
            Formatted string
        """
        icon_map = {
            "01d": "☀️", "01n": "🌙",
            "02d": "⛅", "02n": "☁️",
            "03d": "☁️", "03n": "☁️",
            "04d": "☁️", "04n": "☁️",
            "09d": "🌧️", "09n": "🌧️",
            "10d": "🌦️", "10n": "🌧️",
            "11d": "⛈️", "11n": "⛈️",
            "13d": "❄️", "13n": "❄️",
            "50d": "🌫️", "50n": "🌫️",
        }
        icon = icon_map.get(weather.get("icon", ""), "🌡️")

        country = f", {weather['country']}" if weather.get("country") else ""

        # Format timestamp for display in location's local time
        from datetime import datetime, timedelta
        try:
            ts = datetime.fromisoformat(weather.get("timestamp", "").replace("Z", "+00:00"))
            # Convert UTC to location's local time
            tz_offset = weather.get("tz_offset", 0)
            local_ts = ts + timedelta(seconds=tz_offset)
            time_str = local_ts.strftime("%I:%M %p").lstrip("0")
            # Add timezone label
            tz_label = weather.get("tz_label", "UTC")
            time_str = f"{time_str} {tz_label}"
        except (ValueError, AttributeError):
            time_str = "just now"

        return (
            f"{icon} **{weather['location']}{country}**\n\n"
            f"**{weather['temp_f']}°F** ({weather['temp_c']}°C) - {weather['description'].title()}\n"
            f"Feels like: {weather['feels_like_f']}°F | Humidity: {weather['humidity']}% | Wind: {weather['wind_mph']} mph\n\n"
            f"*Updated: {time_str}*"
        )


class StockClient:
    """Stock quote API client using Alpha Vantage.

    Usage:
        client = StockClient()
        response = await client.get_quote("AAPL")

        if response.success:
            print(response.formatted)  # Free tier output
    """

    BASE_URL = "https://www.alphavantage.co/query"

    def __init__(self, api_key: Optional[str] = None):
        """Initialize stock client.

        Args:
            api_key: Alpha Vantage API key (falls back to ALPHAVANTAGE_API_KEY env var)
        """
        self.api_key = api_key or os.environ.get("ALPHAVANTAGE_API_KEY")

    async def get_quote(self, ticker: str) -> APIResponse:
        """Get current stock quote.

        Args:
            ticker: Stock ticker symbol (e.g., "AAPL", "MSFT")

        Returns:
            APIResponse with stock data
        """
        if not self.api_key:
            return APIResponse(
                success=False,
                error="Stock API not configured. Set ALPHAVANTAGE_API_KEY environment variable."
            )

        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": ticker.upper(),
            "apikey": self.api_key,
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.BASE_URL, params=params, timeout=10) as resp:
                    if resp.status != 200:
                        text = await resp.text()
                        logger.error(f"Stock API error {resp.status}: {text}")
                        return APIResponse(
                            success=False,
                            error=f"Stock API error: {resp.status}"
                        )

                    data = await resp.json()

        except aiohttp.ClientError as e:
            logger.error(f"Stock API request failed: {e}")
            return APIResponse(success=False, error=f"Network error: {e}")
        except Exception as e:
            logger.exception(f"Stock API unexpected error: {e}")
            return APIResponse(success=False, error=str(e))

        # Check for API errors
        if "Error Message" in data:
            return APIResponse(success=False, error=data["Error Message"])

        if "Note" in data:
            # Rate limit hit
            return APIResponse(success=False, error="API rate limit reached. Try again later.")

        quote_data = data.get("Global Quote", {})
        if not quote_data:
            return APIResponse(success=False, error=f"No data found for ticker: {ticker}")

        # Parse response
        price = float(quote_data.get("05. price", 0))
        change = float(quote_data.get("09. change", 0))
        change_pct = quote_data.get("10. change percent", "0%").rstrip("%")

        stock = {
            "ticker": quote_data.get("01. symbol", ticker.upper()),
            "price": price,
            "change": change,
            "change_percent": float(change_pct) if change_pct else 0,
            "open": float(quote_data.get("02. open", 0)),
            "high": float(quote_data.get("03. high", 0)),
            "low": float(quote_data.get("04. low", 0)),
            "volume": int(quote_data.get("06. volume", 0)),
            "previous_close": float(quote_data.get("08. previous close", 0)),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        formatted = self._format_template(stock)
        return APIResponse(success=True, data=stock, formatted=formatted)

    def _format_template(self, stock: dict) -> str:
        """Format stock data as template (free tier).

        Args:
            stock: Parsed stock dict

        Returns:
            Formatted string
        """
        change = stock["change"]
        change_pct = stock["change_percent"]

        if change > 0:
            icon = "📈"
            sign = "+"
        elif change < 0:
            icon = "📉"
            sign = ""
        else:
            icon = "➖"
            sign = ""

        return (
            f"{icon} **{stock['ticker']}** ${stock['price']:.2f}\n\n"
            f"**{sign}{change:.2f}** ({sign}{change_pct:.2f}%)\n"
            f"Open: ${stock['open']:.2f} | High: ${stock['high']:.2f} | Low: ${stock['low']:.2f}\n"
            f"Volume: {stock['volume']:,}"
        )


class NewsClient:
    """NewsAPI client.

    Usage:
        client = NewsClient()
        response = await client.get_headlines(query="technology")

        if response.success:
            print(response.formatted)
    """

    BASE_URL = "https://newsapi.org/v2/top-headlines"

    def __init__(self, api_key: Optional[str] = None):
        """Initialize news client.

        Args:
            api_key: NewsAPI key (falls back to NEWSAPI_KEY env var)
        """
        self.api_key = api_key or os.environ.get("NEWSAPI_KEY")

    async def get_headlines(
        self,
        query: Optional[str] = None,
        category: Optional[str] = None,
        country: str = "us",
        limit: int = 5,
    ) -> APIResponse:
        """Get top headlines.

        Args:
            query: Search keywords (optional)
            category: News category (business, entertainment, general, health, science, sports, technology)
            country: Country code (default "us")
            limit: Max number of articles (default 5)

        Returns:
            APIResponse with news data
        """
        if not self.api_key:
            return APIResponse(
                success=False,
                error="News API not configured. Set NEWSAPI_KEY environment variable."
            )

        params = {
            "apiKey": self.api_key,
            "country": country,
            "pageSize": min(limit, 10),  # Cap at 10
        }

        if query:
            params["q"] = query
        if category:
            params["category"] = category

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.BASE_URL, params=params, timeout=10) as resp:
                    if resp.status == 401:
                        return APIResponse(success=False, error="Invalid News API key")
                    if resp.status == 429:
                        return APIResponse(success=False, error="News API rate limit reached")
                    if resp.status != 200:
                        text = await resp.text()
                        logger.error(f"News API error {resp.status}: {text}")
                        return APIResponse(
                            success=False,
                            error=f"News API error: {resp.status}"
                        )

                    data = await resp.json()

        except aiohttp.ClientError as e:
            logger.error(f"News API request failed: {e}")
            return APIResponse(success=False, error=f"Network error: {e}")
        except Exception as e:
            logger.exception(f"News API unexpected error: {e}")
            return APIResponse(success=False, error=str(e))

        if data.get("status") != "ok":
            return APIResponse(success=False, error=data.get("message", "Unknown error"))

        articles = data.get("articles", [])
        if not articles:
            return APIResponse(success=False, error="No articles found")

        # Parse articles
        news = {
            "query": query,
            "category": category,
            "country": country,
            "total_results": data.get("totalResults", 0),
            "articles": [
                {
                    "title": a.get("title", ""),
                    "description": a.get("description", ""),
                    "source": a.get("source", {}).get("name", "Unknown"),
                    "url": a.get("url", ""),
                    "published_at": a.get("publishedAt", ""),
                }
                for a in articles[:limit]
            ],
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        formatted = self._format_template(news)
        return APIResponse(success=True, data=news, formatted=formatted)

    def _format_template(self, news: dict) -> str:
        """Format news data as template (free tier).

        Args:
            news: Parsed news dict

        Returns:
            Formatted string
        """
        lines = ["📰 **Headlines**\n"]

        if news.get("query"):
            lines[0] = f"📰 **Headlines: {news['query']}**\n"
        elif news.get("category"):
            lines[0] = f"📰 **{news['category'].title()} Headlines**\n"

        for i, article in enumerate(news["articles"], 1):
            title = article["title"]
            source = article["source"]
            url = article["url"]

            # Truncate title if too long
            if len(title) > 80:
                title = title[:77] + "..."

            lines.append(f"{i}. [{title}]({url})")
            lines.append(f"   *{source}*\n")

        return "\n".join(lines)


# Singleton instances
_weather_client: Optional[WeatherClient] = None
_stock_client: Optional[StockClient] = None
_news_client: Optional[NewsClient] = None


def get_weather_client() -> WeatherClient:
    """Get weather client singleton."""
    global _weather_client
    if _weather_client is None:
        _weather_client = WeatherClient()
    return _weather_client


def get_stock_client() -> StockClient:
    """Get stock client singleton."""
    global _stock_client
    if _stock_client is None:
        _stock_client = StockClient()
    return _stock_client


def get_news_client() -> NewsClient:
    """Get news client singleton."""
    global _news_client
    if _news_client is None:
        _news_client = NewsClient()
    return _news_client


class RSSClient:
    """RSS/Atom feed client using feedparser.

    No API key needed - works with any public RSS/Atom feed.

    Usage:
        client = RSSClient()
        response = await client.get_feed("https://blog.example.com/feed.xml")

        if response.success:
            print(response.formatted)  # Template output
            print(response.data)       # Raw data
    """

    def __init__(self):
        """Initialize RSS client."""
        pass  # No rate limiting needed for RSS (no paid API)

    async def get_feed(
        self,
        url: str,
        limit: int = 5,
    ) -> APIResponse:
        """Fetch and parse RSS/Atom feed.

        Args:
            url: Feed URL
            limit: Max entries to return (default 5)

        Returns:
            APIResponse with feed data
        """
        import feedparser

        try:
            # feedparser handles both sync fetching and parsing
            # Run in executor to avoid blocking
            import asyncio
            loop = asyncio.get_event_loop()
            feed = await loop.run_in_executor(None, feedparser.parse, url)
        except Exception as e:
            logger.exception(f"RSS fetch error: {e}")
            return APIResponse(success=False, error=str(e))

        # Check for feed errors
        if feed.bozo and not feed.entries:
            error_msg = str(feed.bozo_exception) if feed.bozo_exception else "Invalid feed"
            return APIResponse(success=False, error=f"Feed error: {error_msg}")

        if not feed.entries:
            return APIResponse(success=False, error="No entries found in feed")

        # Parse feed metadata
        feed_title = feed.feed.get("title", "RSS Feed")
        feed_link = feed.feed.get("link", url)

        # Parse entries
        entries = []
        for entry in feed.entries[:limit]:
            # Get published date
            published = ""
            if hasattr(entry, "published_parsed") and entry.published_parsed:
                try:
                    from time import mktime
                    dt = datetime.fromtimestamp(mktime(entry.published_parsed), tz=timezone.utc)
                    published = dt.strftime("%Y-%m-%d %H:%M")
                except Exception:
                    published = entry.get("published", "")
            elif hasattr(entry, "updated_parsed") and entry.updated_parsed:
                try:
                    from time import mktime
                    dt = datetime.fromtimestamp(mktime(entry.updated_parsed), tz=timezone.utc)
                    published = dt.strftime("%Y-%m-%d %H:%M")
                except Exception:
                    published = entry.get("updated", "")

            entries.append({
                "title": entry.get("title", "Untitled"),
                "link": entry.get("link", ""),
                "published": published,
                "summary": entry.get("summary", "")[:200] if entry.get("summary") else "",
            })

        data = {
            "feed_title": feed_title,
            "feed_link": feed_link,
            "feed_url": url,
            "entry_count": len(feed.entries),
            "entries": entries,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        formatted = self._format_template(data)
        return APIResponse(success=True, data=data, formatted=formatted)

    def _format_template(self, data: dict) -> str:
        """Format RSS data as template.

        Args:
            data: Parsed feed dict

        Returns:
            Formatted string
        """
        lines = [f"📡 **{data['feed_title']}**\n"]

        for i, entry in enumerate(data["entries"], 1):
            title = entry["title"]
            link = entry["link"]
            published = entry["published"]

            # Truncate title if too long
            if len(title) > 80:
                title = title[:77] + "..."

            if link:
                lines.append(f"{i}. [{title}]({link})")
            else:
                lines.append(f"{i}. {title}")

            if published:
                lines.append(f"   *{published}*\n")
            else:
                lines.append("")

        lines.append(f"\n[View feed]({data['feed_link']})")
        return "\n".join(lines)


_rss_client: Optional[RSSClient] = None


def get_rss_client() -> RSSClient:
    """Get RSS client singleton."""
    global _rss_client
    if _rss_client is None:
        _rss_client = RSSClient()
    return _rss_client
