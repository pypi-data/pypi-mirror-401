"""
Schedule Parser for @eis Smart Tasks.

Converts natural language schedule strings to cron expressions.

Examples:
    "every morning at 7am" → {"hour": 7, "minute": 0}
    "hourly" → {"minute": 0}  (every hour on the hour)
    "daily at 3pm" → {"hour": 15, "minute": 0}
    "every 30 minutes" → {"minute": "*/30"}

Bead: solutions-hgwx.4
"""

import re
from dataclasses import dataclass
from typing import Optional


@dataclass
class ScheduleConfig:
    """Parsed schedule configuration for APScheduler."""

    # Cron-style fields (None = any/*)
    minute: Optional[str] = None
    hour: Optional[str] = None
    day: Optional[str] = None
    day_of_week: Optional[str] = None

    # Interval-style (alternative to cron)
    interval_minutes: Optional[int] = None
    interval_hours: Optional[int] = None

    # Original string for display
    original: str = ""

    # Whether parsing succeeded
    valid: bool = True
    error: Optional[str] = None

    def to_apscheduler_trigger(self) -> tuple[str, dict]:
        """Convert to APScheduler trigger type and kwargs.

        Returns:
            Tuple of (trigger_type, kwargs)
            e.g., ("cron", {"hour": 7, "minute": 0})
            or ("interval", {"minutes": 30})
        """
        if self.interval_minutes:
            return ("interval", {"minutes": self.interval_minutes})
        if self.interval_hours:
            return ("interval", {"hours": self.interval_hours})

        # Build cron kwargs
        kwargs = {}
        if self.minute is not None:
            kwargs["minute"] = self.minute
        if self.hour is not None:
            kwargs["hour"] = self.hour
        if self.day is not None:
            kwargs["day"] = self.day
        if self.day_of_week is not None:
            kwargs["day_of_week"] = self.day_of_week

        return ("cron", kwargs)

    def get_next_run_description(self) -> Optional[str]:
        """Get a human-readable description of when the next run will be.

        Returns:
            Description like "in 30 minutes", "at 7:00 AM", or None if can't determine
        """
        from datetime import datetime, timedelta

        now = datetime.now()

        # For intervals, calculate next run
        if self.interval_minutes:
            next_run = now + timedelta(minutes=self.interval_minutes)
            if self.interval_minutes < 60:
                return f"in {self.interval_minutes} min"
            else:
                return next_run.strftime("%I:%M %p").lstrip("0")

        if self.interval_hours:
            next_run = now + timedelta(hours=self.interval_hours)
            if self.interval_hours == 1:
                return "in 1 hour"
            elif self.interval_hours < 24:
                return f"in {self.interval_hours} hours"
            else:
                return next_run.strftime("%I:%M %p").lstrip("0")

        # For cron-style, estimate next run
        if self.hour is not None:
            try:
                target_hour = int(self.hour)
                target_minute = int(self.minute or 0)

                # Today's target time
                target_today = now.replace(hour=target_hour, minute=target_minute, second=0, microsecond=0)

                if target_today > now:
                    # Later today
                    return target_today.strftime("%I:%M %p").lstrip("0")
                else:
                    # Tomorrow
                    target_tomorrow = target_today + timedelta(days=1)
                    return f"tomorrow {target_tomorrow.strftime('%I:%M %p').lstrip('0')}"
            except (ValueError, TypeError):
                pass

        return None


class ScheduleParser:
    """Parse natural language schedules.

    Usage:
        parser = ScheduleParser()
        config = parser.parse("every morning at 7am")

        if config.valid:
            trigger_type, kwargs = config.to_apscheduler_trigger()
            scheduler.add_job(func, trigger_type, **kwargs)
    """

    # Time patterns
    TIME_12H = re.compile(r'(\d{1,2}):?(\d{2})?\s*(am|pm)', re.IGNORECASE)
    TIME_24H = re.compile(r'(\d{1,2}):(\d{2})(?!\s*(am|pm))', re.IGNORECASE)

    # Interval patterns
    EVERY_N_MINUTES = re.compile(r'every\s+(\d+)\s+minutes?', re.IGNORECASE)
    EVERY_N_HOURS = re.compile(r'every\s+(\d+)\s+hours?', re.IGNORECASE)

    # Named times
    NAMED_TIMES = {
        "morning": (7, 0),
        "noon": (12, 0),
        "afternoon": (14, 0),
        "evening": (18, 0),
        "night": (21, 0),
        "midnight": (0, 0),
    }

    # Day patterns
    WEEKDAYS = {
        "monday": "mon", "mon": "mon",
        "tuesday": "tue", "tue": "tue",
        "wednesday": "wed", "wed": "wed",
        "thursday": "thu", "thu": "thu",
        "friday": "fri", "fri": "fri",
        "saturday": "sat", "sat": "sat",
        "sunday": "sun", "sun": "sun",
        "weekday": "mon-fri", "weekdays": "mon-fri",
        "weekend": "sat,sun", "weekends": "sat,sun",
    }

    def parse(self, schedule: str) -> ScheduleConfig:
        """Parse a schedule string.

        Args:
            schedule: Natural language schedule (e.g., "every morning at 7am")

        Returns:
            ScheduleConfig with parsed values
        """
        if not schedule:
            return ScheduleConfig(valid=False, error="Empty schedule", original="")

        schedule = schedule.strip().lower()
        config = ScheduleConfig(original=schedule)

        # Try interval patterns first
        interval_result = self._parse_interval(schedule)
        if interval_result:
            return interval_result

        # Try simple keywords
        if schedule == "hourly":
            config.minute = "0"
            return config

        if schedule == "daily":
            config.hour = "9"  # Default to 9am
            config.minute = "0"
            return config

        # Parse time component
        hour, minute = self._extract_time(schedule)
        if hour is not None:
            config.hour = str(hour)
            config.minute = str(minute or 0)

        # Parse day component
        day_of_week = self._extract_day_of_week(schedule)
        if day_of_week:
            config.day_of_week = day_of_week

        # If we found nothing, mark as invalid
        if config.hour is None and config.minute is None and config.day_of_week is None:
            config.valid = False
            config.error = f"Could not parse schedule: {schedule}"

        return config

    def _parse_interval(self, schedule: str) -> Optional[ScheduleConfig]:
        """Try to parse as interval schedule."""
        # Every N minutes
        match = self.EVERY_N_MINUTES.search(schedule)
        if match:
            minutes = int(match.group(1))
            if minutes < 1 or minutes > 1440:
                return ScheduleConfig(
                    valid=False,
                    error=f"Invalid interval: {minutes} minutes",
                    original=schedule
                )
            return ScheduleConfig(interval_minutes=minutes, original=schedule)

        # Every N hours
        match = self.EVERY_N_HOURS.search(schedule)
        if match:
            hours = int(match.group(1))
            if hours < 1 or hours > 24:
                return ScheduleConfig(
                    valid=False,
                    error=f"Invalid interval: {hours} hours",
                    original=schedule
                )
            return ScheduleConfig(interval_hours=hours, original=schedule)

        return None

    def _extract_time(self, schedule: str) -> tuple[Optional[int], Optional[int]]:
        """Extract time from schedule string.

        Returns:
            Tuple of (hour, minute) or (None, None)
        """
        # Try 12-hour format (e.g., "7am", "3:30pm")
        match = self.TIME_12H.search(schedule)
        if match:
            hour = int(match.group(1))
            minute = int(match.group(2)) if match.group(2) else 0
            am_pm = match.group(3).lower()

            if am_pm == "pm" and hour != 12:
                hour += 12
            elif am_pm == "am" and hour == 12:
                hour = 0

            return (hour, minute)

        # Try 24-hour format (e.g., "14:30")
        match = self.TIME_24H.search(schedule)
        if match:
            return (int(match.group(1)), int(match.group(2)))

        # Try named times (e.g., "morning", "evening")
        for name, (hour, minute) in self.NAMED_TIMES.items():
            if name in schedule:
                return (hour, minute)

        return (None, None)

    def _extract_day_of_week(self, schedule: str) -> Optional[str]:
        """Extract day of week from schedule string.

        Returns:
            APScheduler day_of_week string or None
        """
        for name, cron_day in self.WEEKDAYS.items():
            if name in schedule:
                return cron_day

        return None


# Singleton instance
_parser: Optional[ScheduleParser] = None


def get_schedule_parser() -> ScheduleParser:
    """Get schedule parser singleton."""
    global _parser
    if _parser is None:
        _parser = ScheduleParser()
    return _parser


def parse_schedule(schedule: str) -> ScheduleConfig:
    """Convenience function to parse a schedule.

    Args:
        schedule: Natural language schedule string

    Returns:
        ScheduleConfig with parsed values
    """
    return get_schedule_parser().parse(schedule)
