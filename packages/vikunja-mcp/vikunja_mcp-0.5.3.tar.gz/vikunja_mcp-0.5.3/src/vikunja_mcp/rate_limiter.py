"""
Rate Limiter for External API Calls.

Enforces daily call limits to prevent runaway costs.

Usage:
    limiter = RateLimiter(daily_limit=500)

    if limiter.can_call("weather"):
        limiter.record_call("weather")
        # make API call
    else:
        # refuse, return error

Bead: solutions-hgwx.4
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class DailyCounter:
    """Tracks API calls for a single day."""
    date: str  # YYYY-MM-DD
    calls: int = 0


@dataclass
class RateLimiter:
    """Rate limiter with daily call limits.

    Thread-safe for single-process use (asyncio).
    Resets at midnight UTC.
    """

    daily_limit: int = 500  # 50% of OpenWeatherMap's 1000/day free tier

    # Per-API counters
    _counters: dict[str, DailyCounter] = field(default_factory=dict)

    def _today(self) -> str:
        """Get today's date string."""
        return datetime.now(timezone.utc).strftime("%Y-%m-%d")

    def _get_counter(self, api_name: str) -> DailyCounter:
        """Get or create counter for an API."""
        today = self._today()

        if api_name not in self._counters:
            self._counters[api_name] = DailyCounter(date=today)

        counter = self._counters[api_name]

        # Reset if new day
        if counter.date != today:
            logger.info(f"Rate limiter reset for {api_name}: new day")
            counter.date = today
            counter.calls = 0

        return counter

    def can_call(self, api_name: str) -> bool:
        """Check if an API call is allowed.

        Args:
            api_name: API identifier (e.g., "weather", "stock", "news")

        Returns:
            True if call is allowed, False if limit reached
        """
        counter = self._get_counter(api_name)
        return counter.calls < self.daily_limit

    def record_call(self, api_name: str) -> bool:
        """Record an API call.

        Args:
            api_name: API identifier

        Returns:
            True if recorded, False if limit already reached
        """
        counter = self._get_counter(api_name)

        if counter.calls >= self.daily_limit:
            logger.warning(f"Rate limit reached for {api_name}: {counter.calls}/{self.daily_limit}")
            return False

        counter.calls += 1

        # Log warnings at thresholds
        pct = (counter.calls / self.daily_limit) * 100
        if counter.calls == self.daily_limit:
            logger.error(f"RATE LIMIT REACHED for {api_name}: {counter.calls}/{self.daily_limit}")
            print(f"[RATE LIMIT] ⛔ {api_name} limit reached: {counter.calls}/{self.daily_limit}", flush=True)
        elif pct >= 80 and (counter.calls - 1) / self.daily_limit * 100 < 80:
            logger.warning(f"Rate limit warning for {api_name}: {counter.calls}/{self.daily_limit} (80%)")
            print(f"[RATE LIMIT] ⚠️ {api_name} at 80%: {counter.calls}/{self.daily_limit}", flush=True)
        elif pct >= 50 and (counter.calls - 1) / self.daily_limit * 100 < 50:
            logger.info(f"Rate limit notice for {api_name}: {counter.calls}/{self.daily_limit} (50%)")
            print(f"[RATE LIMIT] 📊 {api_name} at 50%: {counter.calls}/{self.daily_limit}", flush=True)

        return True

    def get_remaining(self, api_name: str) -> int:
        """Get remaining calls for an API today.

        Args:
            api_name: API identifier

        Returns:
            Number of remaining calls
        """
        counter = self._get_counter(api_name)
        return max(0, self.daily_limit - counter.calls)

    def get_usage(self, api_name: str) -> tuple[int, int]:
        """Get usage stats for an API.

        Args:
            api_name: API identifier

        Returns:
            Tuple of (calls_used, daily_limit)
        """
        counter = self._get_counter(api_name)
        return (counter.calls, self.daily_limit)

    def get_all_usage(self) -> dict[str, tuple[int, int]]:
        """Get usage stats for all APIs.

        Returns:
            Dict of api_name -> (calls_used, daily_limit)
        """
        today = self._today()
        return {
            name: (c.calls if c.date == today else 0, self.daily_limit)
            for name, c in self._counters.items()
        }


# Singleton instance
_limiter: Optional[RateLimiter] = None


def get_rate_limiter() -> RateLimiter:
    """Get rate limiter singleton."""
    global _limiter
    if _limiter is None:
        _limiter = RateLimiter(daily_limit=500)  # 50% safety margin
    return _limiter
