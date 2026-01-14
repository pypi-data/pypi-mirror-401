"""Tests for task creation guardrails (date validation, HTML handling)."""

import pytest
from datetime import datetime, timezone, timedelta
from unittest.mock import patch


class TestDateValidation:
    """Tests for _validate_and_fix_date() guardrail."""

    def test_jan_date_in_december_autocorrects(self):
        """Jan/Feb dates created in Nov/Dec should auto-correct to next year."""
        from vikunja_mcp.server import _validate_and_fix_date

        # Mock "now" to be Dec 30, 2025
        with patch('vikunja_mcp.server.datetime') as mock_dt:
            mock_dt.now.return_value = datetime(2025, 12, 30, tzinfo=timezone.utc)
            mock_dt.fromisoformat = datetime.fromisoformat
            mock_dt.strptime = datetime.strptime

            result, warning = _validate_and_fix_date("2025-01-06", "due_date")

            assert result == "2026-01-06"
            assert "Auto-corrected" in warning
            assert "2026-01-06" in warning

    def test_feb_date_in_december_autocorrects(self):
        """February dates should also auto-correct."""
        from vikunja_mcp.server import _validate_and_fix_date

        with patch('vikunja_mcp.server.datetime') as mock_dt:
            mock_dt.now.return_value = datetime(2025, 12, 30, tzinfo=timezone.utc)
            mock_dt.fromisoformat = datetime.fromisoformat
            mock_dt.strptime = datetime.strptime

            result, warning = _validate_and_fix_date("2025-02-28", "due_date")

            assert result == "2026-02-28"
            assert "Auto-corrected" in warning

    def test_datetime_with_time_autocorrects(self):
        """Full datetime strings should also auto-correct."""
        from vikunja_mcp.server import _validate_and_fix_date

        with patch('vikunja_mcp.server.datetime') as mock_dt:
            mock_dt.now.return_value = datetime(2025, 12, 30, tzinfo=timezone.utc)
            mock_dt.fromisoformat = datetime.fromisoformat
            mock_dt.strptime = datetime.strptime

            result, warning = _validate_and_fix_date("2025-01-06T10:00:00Z", "due_date")

            assert result == "2026-01-06T10:00:00Z"
            assert "Auto-corrected" in warning

    def test_far_past_date_warns_only(self):
        """Dates far in past should warn but not change."""
        from vikunja_mcp.server import _validate_and_fix_date

        with patch('vikunja_mcp.server.datetime') as mock_dt:
            mock_dt.now.return_value = datetime(2025, 12, 30, tzinfo=timezone.utc)
            mock_dt.fromisoformat = datetime.fromisoformat
            mock_dt.strptime = datetime.strptime

            result, warning = _validate_and_fix_date("2024-06-15", "due_date")

            assert result == "2024-06-15"  # Unchanged
            assert "days in the past" in warning

    def test_future_date_passes_through(self):
        """Future dates should pass through unchanged."""
        from vikunja_mcp.server import _validate_and_fix_date

        with patch('vikunja_mcp.server.datetime') as mock_dt:
            mock_dt.now.return_value = datetime(2025, 12, 30, tzinfo=timezone.utc)
            mock_dt.fromisoformat = datetime.fromisoformat
            mock_dt.strptime = datetime.strptime

            result, warning = _validate_and_fix_date("2026-03-15", "due_date")

            assert result == "2026-03-15"
            assert warning is None

    def test_empty_date_passes_through(self):
        """Empty string should pass through."""
        from vikunja_mcp.server import _validate_and_fix_date

        result, warning = _validate_and_fix_date("", "due_date")

        assert result == ""
        assert warning is None


class TestHtmlDetection:
    """Tests for _is_html() detection."""

    def test_detects_p_tag(self):
        from vikunja_mcp.server import _is_html
        assert _is_html("<p>Hello</p>") is True

    def test_detects_div_tag(self):
        from vikunja_mcp.server import _is_html
        assert _is_html("<div>Content</div>") is True

    def test_detects_ul_tag(self):
        from vikunja_mcp.server import _is_html
        assert _is_html("<ul><li>Item</li></ul>") is True

    def test_detects_with_whitespace(self):
        from vikunja_mcp.server import _is_html
        assert _is_html("  <p>Indented</p>") is True

    def test_rejects_markdown(self):
        from vikunja_mcp.server import _is_html
        assert _is_html("**Bold** text") is False

    def test_rejects_plain_text(self):
        from vikunja_mcp.server import _is_html
        assert _is_html("Plain text") is False

    def test_rejects_empty(self):
        from vikunja_mcp.server import _is_html
        assert _is_html("") is False


class TestMdToHtml:
    """Tests for md_to_html() with HTML passthrough."""

    def test_html_passes_through_unchanged(self):
        from vikunja_mcp.server import md_to_html

        html_input = "<p><strong>Issue:</strong> Test</p>"
        result = md_to_html(html_input)

        assert result == html_input

    def test_markdown_converts_to_html(self):
        from vikunja_mcp.server import md_to_html

        md_input = "**Bold** and *italic*"
        result = md_to_html(md_input)

        assert "<strong>Bold</strong>" in result
        assert "<em>italic</em>" in result

    def test_empty_passes_through(self):
        from vikunja_mcp.server import md_to_html

        assert md_to_html("") == ""
        assert md_to_html(None) is None


class TestTimezoneConversion:
    """Tests for _convert_local_to_utc() timezone handling."""

    def test_utc_datetime_passes_through(self):
        """Datetimes with Z suffix should pass through unchanged."""
        from vikunja_mcp.server import _convert_local_to_utc

        result = _convert_local_to_utc("2025-01-06T18:00:00Z")
        assert result == "2025-01-06T18:00:00Z"

    def test_date_only_passes_through(self):
        """Date-only strings should pass through unchanged."""
        from vikunja_mcp.server import _convert_local_to_utc

        result = _convert_local_to_utc("2025-01-06")
        assert result == "2025-01-06"

    def test_empty_passes_through(self):
        """Empty string should pass through."""
        from vikunja_mcp.server import _convert_local_to_utc

        assert _convert_local_to_utc("") == ""

    def test_naive_datetime_converts_with_timezone_config(self):
        """Naive datetime should convert from local timezone to UTC."""
        from vikunja_mcp.server import _convert_local_to_utc

        with patch('vikunja_mcp.server._get_instance_timezone') as mock_tz:
            mock_tz.return_value = "America/Los_Angeles"

            # 6pm Pacific = 2am UTC next day (during PST, UTC-8)
            result = _convert_local_to_utc("2025-01-06T18:00:00")

            # Should add 8 hours for PST
            assert result == "2025-01-07T02:00:00Z"

    def test_naive_datetime_no_timezone_adds_z(self):
        """Naive datetime with no timezone config should add Z suffix."""
        from vikunja_mcp.server import _convert_local_to_utc

        with patch('vikunja_mcp.server._get_instance_timezone') as mock_tz:
            mock_tz.return_value = None

            result = _convert_local_to_utc("2025-01-06T18:00:00")

            assert result == "2025-01-06T18:00:00Z"

    def test_offset_datetime_passes_through(self):
        """Datetime with offset should pass through unchanged."""
        from vikunja_mcp.server import _convert_local_to_utc

        result = _convert_local_to_utc("2025-01-06T18:00:00-08:00")
        assert result == "2025-01-06T18:00:00-08:00"
