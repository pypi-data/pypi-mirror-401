"""Tests for smart title generation in notification poller."""

import re
import pytest


def _generate_smart_title(handler_data: dict, original_title: str) -> str:
    """Generate a smart title from API response data.

    Copy of the method for isolated testing.
    """
    keyword = handler_data.get("keyword", "")
    schedule = handler_data.get("schedule")

    # Build schedule suffix if present
    schedule_suffix = f" ({schedule})" if schedule else ""

    # Weather: Use location + country from API response
    if keyword == "weather" and handler_data.get("weather"):
        weather = handler_data["weather"]
        location = weather.get("location", "")
        country = weather.get("country", "")
        if location:
            if country:
                return f"{location}, {country}{schedule_suffix}"
            return f"{location}{schedule_suffix}"

    # Stock: Use ticker from API response
    if keyword == "stock" and handler_data.get("stock"):
        stock = handler_data["stock"]
        ticker = stock.get("ticker", "")
        if ticker:
            return f"{ticker}{schedule_suffix}"

    # News: Use query or category
    if keyword == "news" and handler_data.get("news"):
        news = handler_data["news"]
        if news.get("query"):
            return f"{news['query'].title()} Headlines{schedule_suffix}"
        if news.get("category"):
            return f"{news['category'].title()} Headlines{schedule_suffix}"
        return f"Headlines{schedule_suffix}"

    # Help: Use topic or "Command Reference"
    if keyword == "help":
        handler_args = handler_data.get("handler_args", {})
        topic = handler_args.get("topic", "")
        if topic:
            return f"@eis Help: {topic.title()}"
        return "@eis Command Reference"

    # Fallback: Clean up original title
    clean = re.sub(r'^(@e(is)?\s*)?!?\w+\s*', '', original_title).strip()
    # Remove pipe and everything after (target project syntax)
    clean = re.sub(r'\s*\|.*$', '', clean).strip()
    if clean:
        return f"{clean}{schedule_suffix}"

    # Last resort: keyword-based default
    return f"{keyword.title() if keyword else 'Smart'} {'Update' if schedule else 'Info'}"


class TestGenerateSmartTitle:
    """Tests for _generate_smart_title method."""

    def test_weather_with_location_and_country(self):
        """Weather task: Tokyo, JP"""
        handler_data = {
            "keyword": "weather",
            "weather": {"location": "Tokyo", "country": "JP"},
        }
        result = _generate_smart_title(handler_data, "!w tokyo | correspondent")
        assert result == "Tokyo, JP"

    def test_weather_with_schedule(self):
        """Weather task with schedule: Tokyo, JP (hourly)"""
        handler_data = {
            "keyword": "weather",
            "weather": {"location": "Tokyo", "country": "JP"},
            "schedule": "hourly",
        }
        result = _generate_smart_title(handler_data, "!w tokyo / hourly")
        assert result == "Tokyo, JP (hourly)"

    def test_weather_location_only(self):
        """Weather task without country code."""
        handler_data = {
            "keyword": "weather",
            "weather": {"location": "San Francisco", "country": ""},
        }
        result = _generate_smart_title(handler_data, "!w sf")
        assert result == "San Francisco"

    def test_stock_ticker(self):
        """Stock task: AAPL"""
        handler_data = {
            "keyword": "stock",
            "stock": {"ticker": "AAPL", "price": 150.0},
        }
        result = _generate_smart_title(handler_data, "!s aapl")
        assert result == "AAPL"

    def test_stock_with_schedule(self):
        """Stock task with schedule: AAPL (daily)"""
        handler_data = {
            "keyword": "stock",
            "stock": {"ticker": "AAPL", "price": 150.0},
            "schedule": "daily",
        }
        result = _generate_smart_title(handler_data, "!s aapl / daily")
        assert result == "AAPL (daily)"

    def test_news_with_query(self):
        """News task with search query."""
        handler_data = {
            "keyword": "news",
            "news": {"query": "technology", "articles": []},
        }
        result = _generate_smart_title(handler_data, "!n technology")
        assert result == "Technology Headlines"

    def test_news_with_category(self):
        """News task with category."""
        handler_data = {
            "keyword": "news",
            "news": {"category": "sports", "articles": []},
        }
        result = _generate_smart_title(handler_data, "!n cat:sports")
        assert result == "Sports Headlines"

    def test_news_default(self):
        """News task with no query or category."""
        handler_data = {
            "keyword": "news",
            "news": {"articles": []},
        }
        result = _generate_smart_title(handler_data, "!n")
        assert result == "Headlines"

    def test_fallback_clean_title(self):
        """Fallback to cleaned original title."""
        handler_data = {
            "keyword": "unknown",
        }
        result = _generate_smart_title(handler_data, "!unknown some query")
        assert result == "some query"

    def test_fallback_removes_pipe_syntax(self):
        """Fallback removes target project syntax."""
        handler_data = {
            "keyword": "unknown",
        }
        result = _generate_smart_title(handler_data, "!unknown query | inbox")
        assert result == "query"

    def test_last_resort_default(self):
        """Last resort default title."""
        handler_data = {
            "keyword": "weather",
            "weather": {},  # No location
        }
        result = _generate_smart_title(handler_data, "")
        assert result == "Weather Info"

    def test_last_resort_with_schedule(self):
        """Last resort default title with schedule."""
        handler_data = {
            "keyword": "weather",
            "weather": {},  # No location
            "schedule": "daily",
        }
        result = _generate_smart_title(handler_data, "")
        assert result == "Weather Update"

    def test_help_overview(self):
        """Help command without topic."""
        handler_data = {
            "keyword": "help",
            "handler_args": {},
        }
        result = _generate_smart_title(handler_data, "!help")
        assert result == "@eis Command Reference"

    def test_help_with_topic(self):
        """Help command with specific topic."""
        handler_data = {
            "keyword": "help",
            "handler_args": {"topic": "weather"},
        }
        result = _generate_smart_title(handler_data, "!help weather")
        assert result == "@eis Help: Weather"
