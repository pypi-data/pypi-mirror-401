"""
Tests for API Clients (Weather, Stock, News).

Bead: solutions-hgwx.3
"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from contextlib import asynccontextmanager

from vikunja_mcp.api_clients import (
    WeatherClient,
    StockClient,
    NewsClient,
    APIResponse,
)


def create_mock_response(status: int, json_data: dict):
    """Create a properly mocked aiohttp response."""
    mock_resp = MagicMock()
    mock_resp.status = status
    mock_resp.json = AsyncMock(return_value=json_data)
    mock_resp.text = AsyncMock(return_value=str(json_data))
    return mock_resp


def create_mock_session(mock_resp):
    """Create a properly mocked aiohttp ClientSession."""
    @asynccontextmanager
    async def mock_get(*args, **kwargs):
        yield mock_resp

    mock_session = MagicMock()
    mock_session.get = mock_get
    return mock_session


class TestWeatherClient:
    """Tests for WeatherClient."""

    @pytest.fixture
    def client(self):
        return WeatherClient(api_key="test_key")

    @pytest.fixture
    def mock_weather_response(self):
        return {
            "name": "San Francisco",
            "sys": {"country": "US"},
            "main": {
                "temp": 65.0,
                "feels_like": 63.0,
                "humidity": 70,
            },
            "weather": [{"description": "partly cloudy", "icon": "02d"}],
            "wind": {"speed": 12.0},
        }

    async def test_get_weather_success(self, client, mock_weather_response):
        """Test successful weather API call."""
        mock_resp = create_mock_response(200, mock_weather_response)
        mock_session = create_mock_session(mock_resp)

        @asynccontextmanager
        async def mock_client_session(*args, **kwargs):
            yield mock_session

        with patch("vikunja_mcp.api_clients.aiohttp.ClientSession", mock_client_session):
            response = await client.get_weather("San Francisco")

        assert response.success is True
        assert response.data["location"] == "San Francisco"
        assert response.data["temp_f"] == 65
        assert "San Francisco" in response.formatted

    async def test_get_weather_no_api_key(self):
        """Test weather fails without API key."""
        client = WeatherClient(api_key=None)
        # Ensure env var is not set
        with patch.dict("os.environ", {}, clear=True):
            client.api_key = None
            response = await client.get_weather("San Francisco")

        assert response.success is False
        assert "not configured" in response.error

    async def test_get_weather_location_not_found(self, client):
        """Test weather with invalid location."""
        mock_resp = create_mock_response(404, {})
        mock_session = create_mock_session(mock_resp)

        @asynccontextmanager
        async def mock_client_session(*args, **kwargs):
            yield mock_session

        with patch("vikunja_mcp.api_clients.aiohttp.ClientSession", mock_client_session):
            response = await client.get_weather("InvalidCity12345")

        assert response.success is False
        assert "not found" in response.error.lower()

    async def test_weather_template_formatting(self, client, mock_weather_response):
        """Test weather template produces readable output."""
        mock_resp = create_mock_response(200, mock_weather_response)
        mock_session = create_mock_session(mock_resp)

        @asynccontextmanager
        async def mock_client_session(*args, **kwargs):
            yield mock_session

        with patch("vikunja_mcp.api_clients.aiohttp.ClientSession", mock_client_session):
            response = await client.get_weather("San Francisco")

        # Check formatted output has expected elements
        assert "⛅" in response.formatted  # partly cloudy icon
        assert "65°F" in response.formatted
        assert "Partly Cloudy" in response.formatted


class TestStockClient:
    """Tests for StockClient."""

    @pytest.fixture
    def client(self):
        return StockClient(api_key="test_key")

    @pytest.fixture
    def mock_stock_response(self):
        return {
            "Global Quote": {
                "01. symbol": "AAPL",
                "02. open": "180.50",
                "03. high": "182.00",
                "04. low": "179.00",
                "05. price": "181.25",
                "06. volume": "50000000",
                "08. previous close": "180.00",
                "09. change": "1.25",
                "10. change percent": "0.69%",
            }
        }

    async def test_get_quote_success(self, client, mock_stock_response):
        """Test successful stock quote."""
        mock_resp = create_mock_response(200, mock_stock_response)
        mock_session = create_mock_session(mock_resp)

        @asynccontextmanager
        async def mock_client_session(*args, **kwargs):
            yield mock_session

        with patch("vikunja_mcp.api_clients.aiohttp.ClientSession", mock_client_session):
            response = await client.get_quote("AAPL")

        assert response.success is True
        assert response.data["ticker"] == "AAPL"
        assert response.data["price"] == 181.25
        assert response.data["change"] == 1.25

    async def test_get_quote_no_api_key(self):
        """Test stock fails without API key."""
        client = StockClient(api_key=None)
        with patch.dict("os.environ", {}, clear=True):
            client.api_key = None
            response = await client.get_quote("AAPL")

        assert response.success is False
        assert "not configured" in response.error

    async def test_stock_rate_limit(self, client):
        """Test stock API rate limit handling."""
        mock_resp = create_mock_response(200, {"Note": "API call frequency exceeded"})
        mock_session = create_mock_session(mock_resp)

        @asynccontextmanager
        async def mock_client_session(*args, **kwargs):
            yield mock_session

        with patch("vikunja_mcp.api_clients.aiohttp.ClientSession", mock_client_session):
            response = await client.get_quote("AAPL")

        assert response.success is False
        assert "rate limit" in response.error.lower()

    async def test_stock_template_positive_change(self, client, mock_stock_response):
        """Test stock template shows positive change correctly."""
        mock_resp = create_mock_response(200, mock_stock_response)
        mock_session = create_mock_session(mock_resp)

        @asynccontextmanager
        async def mock_client_session(*args, **kwargs):
            yield mock_session

        with patch("vikunja_mcp.api_clients.aiohttp.ClientSession", mock_client_session):
            response = await client.get_quote("AAPL")

        assert "📈" in response.formatted  # Positive change icon
        assert "+1.25" in response.formatted
        assert "$181.25" in response.formatted


class TestNewsClient:
    """Tests for NewsClient."""

    @pytest.fixture
    def client(self):
        return NewsClient(api_key="test_key")

    @pytest.fixture
    def mock_news_response(self):
        return {
            "status": "ok",
            "totalResults": 100,
            "articles": [
                {
                    "title": "Tech stocks surge on AI optimism",
                    "description": "Major tech companies see gains...",
                    "source": {"name": "TechNews"},
                    "url": "https://example.com/article1",
                    "publishedAt": "2024-01-15T10:00:00Z",
                },
                {
                    "title": "New breakthrough in renewable energy",
                    "description": "Scientists announce...",
                    "source": {"name": "ScienceDaily"},
                    "url": "https://example.com/article2",
                    "publishedAt": "2024-01-15T09:00:00Z",
                },
            ],
        }

    async def test_get_headlines_success(self, client, mock_news_response):
        """Test successful news headlines fetch."""
        mock_resp = create_mock_response(200, mock_news_response)
        mock_session = create_mock_session(mock_resp)

        @asynccontextmanager
        async def mock_client_session(*args, **kwargs):
            yield mock_session

        with patch("vikunja_mcp.api_clients.aiohttp.ClientSession", mock_client_session):
            response = await client.get_headlines()

        assert response.success is True
        assert len(response.data["articles"]) == 2
        assert response.data["articles"][0]["title"] == "Tech stocks surge on AI optimism"

    async def test_get_headlines_with_query(self, client, mock_news_response):
        """Test headlines with search query."""
        mock_resp = create_mock_response(200, mock_news_response)
        mock_session = create_mock_session(mock_resp)

        @asynccontextmanager
        async def mock_client_session(*args, **kwargs):
            yield mock_session

        with patch("vikunja_mcp.api_clients.aiohttp.ClientSession", mock_client_session):
            response = await client.get_headlines(query="technology")

        assert response.success is True
        assert response.data["query"] == "technology"

    async def test_get_headlines_no_api_key(self):
        """Test news fails without API key."""
        client = NewsClient(api_key=None)
        with patch.dict("os.environ", {}, clear=True):
            client.api_key = None
            response = await client.get_headlines()

        assert response.success is False
        assert "not configured" in response.error

    async def test_news_template_formatting(self, client, mock_news_response):
        """Test news template produces readable output."""
        mock_resp = create_mock_response(200, mock_news_response)
        mock_session = create_mock_session(mock_resp)

        @asynccontextmanager
        async def mock_client_session(*args, **kwargs):
            yield mock_session

        with patch("vikunja_mcp.api_clients.aiohttp.ClientSession", mock_client_session):
            response = await client.get_headlines()

        assert "📰" in response.formatted
        assert "Tech stocks surge on AI optimism" in response.formatted
        assert "TechNews" in response.formatted


class TestCommandParserNews:
    """Tests for news command parsing."""

    def test_parse_news_command(self):
        """Test basic news command parsing."""
        from vikunja_mcp.command_parser import CommandParser

        parser = CommandParser()
        result = parser.parse("@eis !news")

        assert result.tier == "tier3"
        assert result.handler == "news_handler"

    def test_parse_news_with_query(self):
        """Test news command with search query."""
        from vikunja_mcp.command_parser import CommandParser

        parser = CommandParser()
        result = parser.parse("@eis !news technology")

        assert result.tier == "tier3"
        assert result.handler == "news_handler"
        assert result.args["query"] == "technology"

    def test_parse_news_with_category(self):
        """Test news command with category."""
        from vikunja_mcp.command_parser import CommandParser

        parser = CommandParser()
        result = parser.parse("@eis !n category:sports")

        assert result.tier == "tier3"
        assert result.handler == "news_handler"
        assert result.args["category"] == "sports"

    def test_parse_news_fuzzy(self):
        """Test fuzzy matching for news command."""
        from vikunja_mcp.command_parser import CommandParser

        parser = CommandParser()
        result = parser.parse("@eis !newz")  # Typo

        assert result.tier == "tier3"
        assert result.handler == "news_handler"
        assert result.confidence >= 0.7


class TestKeywordHandlersNews:
    """Tests for news handler integration."""

    async def test_news_handler_success(self):
        """Test news handler with mocked API."""
        from vikunja_mcp.keyword_handlers import KeywordHandlers

        # Pass a mock client to avoid VIKUNJA_BOT_TOKEN requirement
        mock_vikunja_client = MagicMock()
        handlers = KeywordHandlers(client=mock_vikunja_client)

        mock_response = APIResponse(
            success=True,
            data={"articles": [{"title": "Test Article"}]},
            formatted="📰 **Headlines**\n\n1. Test Article",
        )

        with patch("vikunja_mcp.keyword_handlers.get_news_client") as mock_client:
            mock_client.return_value.get_headlines = AsyncMock(return_value=mock_response)

            result = await handlers.news_handler({"query": "technology"})

        assert result.success is True
        assert "Headlines" in result.message

    async def test_news_handler_api_error(self):
        """Test news handler handles API errors."""
        from vikunja_mcp.keyword_handlers import KeywordHandlers

        # Pass a mock client to avoid VIKUNJA_BOT_TOKEN requirement
        mock_vikunja_client = MagicMock()
        handlers = KeywordHandlers(client=mock_vikunja_client)

        mock_response = APIResponse(
            success=False,
            error="API key invalid",
        )

        with patch("vikunja_mcp.keyword_handlers.get_news_client") as mock_client:
            mock_client.return_value.get_headlines = AsyncMock(return_value=mock_response)

            result = await handlers.news_handler({})

        assert result.success is False
        assert "error" in result.message.lower()
