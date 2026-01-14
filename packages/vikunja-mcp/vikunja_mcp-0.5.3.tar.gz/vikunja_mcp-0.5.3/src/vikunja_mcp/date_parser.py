"""
Natural language date parsing for ^ commands.

Parses common date expressions like "tomorrow", "friday", "next week".
Bead: solutions-dod7
"""

from datetime import datetime, date, timedelta
from typing import Optional
import re


def parse_natural_date(text: str) -> Optional[date]:
    """Parse natural language date expression.

    Supports:
    - Relative: today, tomorrow, yesterday
    - Weekdays: monday, tuesday, wed, thu, etc.
    - Relative weeks: next week, next monday
    - ISO format: 2024-01-15
    - US format: 1/15, 01/15/2024

    Args:
        text: Natural language date string

    Returns:
        date object or None if unparseable
    """
    text = text.lower().strip()
    today = date.today()

    # Relative dates
    if text in ("today", "now"):
        return today

    if text in ("tomorrow", "tom", "tmrw"):
        return today + timedelta(days=1)

    if text == "yesterday":
        return today - timedelta(days=1)

    # Day of week (find next occurrence)
    weekdays = {
        "monday": 0, "mon": 0,
        "tuesday": 1, "tue": 1, "tues": 1,
        "wednesday": 2, "wed": 2,
        "thursday": 3, "thu": 3, "thur": 3, "thurs": 3,
        "friday": 4, "fri": 4,
        "saturday": 5, "sat": 5,
        "sunday": 6, "sun": 6,
    }

    # Check for "next <weekday>"
    next_match = re.match(r"next\s+(\w+)", text)
    if next_match:
        day_name = next_match.group(1)
        if day_name in weekdays:
            target = weekdays[day_name]
            days_ahead = target - today.weekday()
            if days_ahead <= 0:  # Target day already happened this week
                days_ahead += 7
            days_ahead += 7  # "next" means next week
            return today + timedelta(days=days_ahead)
        if day_name == "week":
            # "next week" = next Monday
            days_ahead = 7 - today.weekday()  # Days until next Monday
            if days_ahead == 7:
                days_ahead = 7  # If today is Monday, next week's Monday
            return today + timedelta(days=days_ahead)

    # Plain weekday (find next occurrence)
    if text in weekdays:
        target = weekdays[text]
        days_ahead = target - today.weekday()
        if days_ahead <= 0:  # Target day already happened this week
            days_ahead += 7
        return today + timedelta(days=days_ahead)

    # ISO format: 2024-01-15
    iso_match = re.match(r"(\d{4})-(\d{1,2})-(\d{1,2})", text)
    if iso_match:
        try:
            return date(
                int(iso_match.group(1)),
                int(iso_match.group(2)),
                int(iso_match.group(3))
            )
        except ValueError:
            pass

    # US format: 1/15 or 01/15/2024
    us_match = re.match(r"(\d{1,2})/(\d{1,2})(?:/(\d{2,4}))?", text)
    if us_match:
        try:
            month = int(us_match.group(1))
            day = int(us_match.group(2))
            year_str = us_match.group(3)
            if year_str:
                year = int(year_str)
                if year < 100:
                    year += 2000
            else:
                year = today.year
                # If date is in the past, assume next year
                test_date = date(year, month, day)
                if test_date < today:
                    year += 1
            return date(year, month, day)
        except ValueError:
            pass

    # Relative days: "in 3 days", "3 days", "+3"
    rel_match = re.match(r"(?:in\s+)?(\d+)\s*(?:days?)?|^\+(\d+)$", text)
    if rel_match:
        days = int(rel_match.group(1) or rel_match.group(2))
        return today + timedelta(days=days)

    return None
