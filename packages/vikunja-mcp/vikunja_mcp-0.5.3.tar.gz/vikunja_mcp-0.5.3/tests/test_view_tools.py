"""Unit tests for create_view, update_view, and delete_view tools.

Tests the MCP view management tools with mocked Vikunja API responses.

Covers:
- create_view_impl: Create views (list, kanban, gantt, table) with optional filters
- update_view_impl: Update view title and/or filter
- delete_view_impl: Delete a view
- _format_view: View formatting helper
"""

import pytest
from unittest.mock import patch, MagicMock

# Import at module level after conftest.py adds src to path
from vikunja_mcp.server import (
    _create_view_impl,
    _update_view_impl,
    _delete_view_impl,
    _format_view,
    TOOL_REGISTRY,
)


class TestCreateViewImpl:
    """Test create_view_impl function."""

    def test_create_basic_kanban_view(self):
        """Create a basic kanban view without filter."""
        with patch('vikunja_mcp.server._request') as mock_request:
            # Mock responses:
            # 1. GET existing views
            # 2. PUT create view
            # 3. GET buckets (to delete defaults)
            # 4-6. DELETE each default bucket (To-Do, Doing, Done)
            mock_request.side_effect = [
                [],  # GET existing views
                {    # PUT create view response
                    "id": 12345,
                    "title": "By Phase",
                    "project_id": 100,
                    "view_kind": "kanban",
                    "position": 100,
                },
                [    # GET buckets (default buckets)
                    {"id": 1, "title": "To-Do"},
                    {"id": 2, "title": "Doing"},
                    {"id": 3, "title": "Done"},
                ],
                {},  # DELETE bucket 1
                {},  # DELETE bucket 2
                {},  # DELETE bucket 3
            ]

            result = _create_view_impl(
                project_id=100,
                title="By Phase",
                view_kind="kanban"
            )

            assert result["id"] == 12345
            assert result["title"] == "By Phase"
            assert result["view_kind"] == "kanban"
            # 2 initial calls + 1 GET buckets + 3 DELETE buckets = 6
            assert mock_request.call_count == 6

    def test_create_view_with_filter(self):
        """Create a view with filter query."""
        with patch('vikunja_mcp.server._request') as mock_request:
            mock_request.side_effect = [
                [],  # GET existing views
                {    # PUT create view response
                    "id": 12346,
                    "title": "High Priority",
                    "project_id": 100,
                    "view_kind": "list",
                    "filter": {
                        "filter": "priority >= 3 && done = false"
                    }
                }
            ]

            result = _create_view_impl(
                project_id=100,
                title="High Priority",
                view_kind="list",
                filter_query="priority >= 3 && done = false"
            )

            assert result["id"] == 12346
            assert result["title"] == "High Priority"
            assert result["filter"] == "priority >= 3 && done = false"

            # Verify filter was passed in request
            put_call = mock_request.call_args_list[1]
            assert put_call[1]["json"]["filter"]["filter"] == "priority >= 3 && done = false"

    def test_create_view_position_after_existing(self):
        """New view should be positioned after existing views."""
        with patch('vikunja_mcp.server._request') as mock_request:
            mock_request.side_effect = [
                # GET existing views with various positions
                [
                    {"id": 1, "position": 100},
                    {"id": 2, "position": 200},
                    {"id": 3, "position": 50},
                ],
                {    # PUT create view response
                    "id": 12347,
                    "title": "New View",
                    "project_id": 100,
                    "view_kind": "table",
                    "position": 300,
                }
            ]

            result = _create_view_impl(
                project_id=100,
                title="New View",
                view_kind="table"
            )

            # Verify position is max + 100
            put_call = mock_request.call_args_list[1]
            assert put_call[1]["json"]["position"] == 300  # 200 + 100

    def test_create_view_all_kinds(self):
        """Test all view kinds: list, kanban, gantt, table."""
        view_kinds = ["list", "kanban", "gantt", "table"]

        for kind in view_kinds:
            with patch('vikunja_mcp.server._request') as mock_request:
                if kind == "kanban":
                    # Kanban views also get/delete default buckets
                    mock_request.side_effect = [
                        [],
                        {"id": 1, "title": f"Test {kind}", "project_id": 100, "view_kind": kind},
                        [],  # GET buckets (empty)
                    ]
                else:
                    mock_request.side_effect = [
                        [],
                        {"id": 1, "title": f"Test {kind}", "project_id": 100, "view_kind": kind}
                    ]

                result = _create_view_impl(
                    project_id=100,
                    title=f"Test {kind}",
                    view_kind=kind
                )

                assert result["view_kind"] == kind

    def test_create_kanban_sets_bucket_configuration_mode(self):
        """Kanban views should set bucket_configuration_mode to 'manual'.

        Without this, Vikunja defaults to 'none' which groups by labels,
        causing each task to appear as its own column instead of in buckets.
        """
        with patch('vikunja_mcp.server._request') as mock_request:
            mock_request.side_effect = [
                [],  # GET existing views
                {    # PUT create view response
                    "id": 12348,
                    "title": "Kanban View",
                    "project_id": 100,
                    "view_kind": "kanban",
                    "bucket_configuration_mode": "manual",
                },
                [],  # GET buckets (empty for this test)
            ]

            result = _create_view_impl(
                project_id=100,
                title="Kanban View",
                view_kind="kanban"
            )

            # Verify bucket_configuration_mode was passed in request
            put_call = mock_request.call_args_list[1]
            assert put_call[1]["json"]["bucket_configuration_mode"] == "manual"

    def test_create_kanban_with_delete_default_buckets_false(self):
        """When delete_default_buckets=False, keep default To-Do/Doing/Done buckets."""
        with patch('vikunja_mcp.server._request') as mock_request:
            mock_request.side_effect = [
                [],  # GET existing views
                {    # PUT create view response
                    "id": 12349,
                    "title": "Kanban Keep Defaults",
                    "project_id": 100,
                    "view_kind": "kanban",
                },
            ]

            result = _create_view_impl(
                project_id=100,
                title="Kanban Keep Defaults",
                view_kind="kanban",
                delete_default_buckets=False
            )

            assert result["id"] == 12349
            # Only 2 calls - no bucket deletion
            assert mock_request.call_count == 2

    def test_create_non_kanban_no_bucket_configuration_mode(self):
        """Non-kanban views should NOT set bucket_configuration_mode."""
        for kind in ["list", "gantt", "table"]:
            with patch('vikunja_mcp.server._request') as mock_request:
                mock_request.side_effect = [
                    [],
                    {"id": 1, "title": f"Test {kind}", "project_id": 100, "view_kind": kind}
                ]

                _create_view_impl(
                    project_id=100,
                    title=f"Test {kind}",
                    view_kind=kind
                )

                # Verify bucket_configuration_mode was NOT passed
                put_call = mock_request.call_args_list[1]
                assert "bucket_configuration_mode" not in put_call[1]["json"]


class TestUpdateViewImpl:
    """Test update_view_impl function."""

    def test_update_view_title(self):
        """Update only the view title."""
        with patch('vikunja_mcp.server._request') as mock_request:
            mock_request.return_value = {
                "id": 12345,
                "title": "Updated Title",
                "project_id": 100,
                "view_kind": "kanban",
            }

            result = _update_view_impl(
                project_id=100,
                view_id=12345,
                title="Updated Title"
            )

            assert result["title"] == "Updated Title"

            # Verify only title was sent
            post_call = mock_request.call_args
            assert post_call[1]["json"]["title"] == "Updated Title"
            assert "filter" not in post_call[1]["json"]

    def test_update_view_filter(self):
        """Update only the view filter."""
        with patch('vikunja_mcp.server._request') as mock_request:
            mock_request.return_value = {
                "id": 12345,
                "title": "Original Title",
                "project_id": 100,
                "view_kind": "list",
                "filter": {"filter": "done = false"}
            }

            result = _update_view_impl(
                project_id=100,
                view_id=12345,
                filter_query="done = false"
            )

            # Verify filter was sent
            post_call = mock_request.call_args
            assert post_call[1]["json"]["filter"]["filter"] == "done = false"
            assert "title" not in post_call[1]["json"]

    def test_update_view_title_and_filter(self):
        """Update both title and filter."""
        with patch('vikunja_mcp.server._request') as mock_request:
            mock_request.return_value = {
                "id": 12345,
                "title": "New Title",
                "project_id": 100,
                "view_kind": "kanban",
                "filter": {"filter": "priority >= 4"}
            }

            result = _update_view_impl(
                project_id=100,
                view_id=12345,
                title="New Title",
                filter_query="priority >= 4"
            )

            post_call = mock_request.call_args
            assert post_call[1]["json"]["title"] == "New Title"
            assert post_call[1]["json"]["filter"]["filter"] == "priority >= 4"


class TestDeleteViewImpl:
    """Test delete_view_impl function."""

    def test_delete_view_success(self):
        """Successfully delete a view."""
        with patch('vikunja_mcp.server._request') as mock_request:
            mock_request.return_value = {}  # Vikunja returns empty on delete

            result = _delete_view_impl(project_id=100, view_id=12345)

            assert result["success"] is True
            assert "12345" in result["message"]

            # Verify DELETE request
            mock_request.assert_called_once()
            call_args = mock_request.call_args
            assert call_args[0][0] == "DELETE"
            assert "/views/12345" in call_args[0][1]


class TestFormatView:
    """Test _format_view helper function."""

    def test_format_basic_view(self):
        """Format a basic view without filter."""
        view = {
            "id": 123,
            "title": "My View",
            "project_id": 100,
            "view_kind": "kanban",
            "position": 200,
        }

        result = _format_view(view)

        assert result["id"] == 123
        assert result["title"] == "My View"
        assert result["project_id"] == 100
        assert result["view_kind"] == "kanban"
        assert "filter" not in result

    def test_format_view_with_filter(self):
        """Format a view with filter query."""
        view = {
            "id": 124,
            "title": "Filtered View",
            "project_id": 100,
            "view_kind": "list",
            "filter": {
                "filter": "done = false && priority >= 3",
                "sort_by": None,
            }
        }

        result = _format_view(view)

        assert result["id"] == 124
        assert result["filter"] == "done = false && priority >= 3"

    def test_format_view_with_empty_filter(self):
        """Format a view with empty filter object."""
        view = {
            "id": 125,
            "title": "No Filter",
            "project_id": 100,
            "view_kind": "table",
            "filter": {}
        }

        result = _format_view(view)

        # Empty filter should not add filter key
        assert "filter" not in result or result.get("filter") == ""

    def test_format_view_with_string_filter(self):
        """Format a view with filter as string (new Vikunja API format).

        After Vikunja API change, filter field is returned as a string directly
        instead of an object with 'filter' key. This test ensures backward
        compatibility with the new format (fixes solutions-33jn7).
        """
        view = {
            "id": 126,
            "title": "String Filter View",
            "project_id": 100,
            "view_kind": "list",
            "filter": "priority >= 4 && done = false"
        }

        result = _format_view(view)

        assert result["id"] == 126
        assert result["filter"] == "priority >= 4 && done = false"

    def test_format_view_with_empty_string_filter(self):
        """Format a view with empty string filter."""
        view = {
            "id": 127,
            "title": "Empty String Filter",
            "project_id": 100,
            "view_kind": "gantt",
            "filter": ""
        }

        result = _format_view(view)

        # Empty string filter should not add filter key
        assert "filter" not in result

    def test_format_view_with_none_filter(self):
        """Format a view with None/null filter."""
        view = {
            "id": 128,
            "title": "None Filter",
            "project_id": 100,
            "view_kind": "table",
            "filter": None
        }

        result = _format_view(view)

        # None filter should not add filter key
        assert "filter" not in result

    def test_format_view_no_filter_key(self):
        """Format a view without filter key at all."""
        view = {
            "id": 129,
            "title": "No Filter Key",
            "project_id": 100,
            "view_kind": "kanban",
        }

        result = _format_view(view)

        # Missing filter key should not add filter to result
        assert "filter" not in result

    def test_format_view_string_vs_object_filter_equivalence(self):
        """String filter and object filter with same content should produce same result."""
        string_filter_view = {
            "id": 130,
            "title": "Test",
            "project_id": 100,
            "view_kind": "list",
            "filter": "labels in 7350"
        }
        object_filter_view = {
            "id": 130,
            "title": "Test",
            "project_id": 100,
            "view_kind": "list",
            "filter": {"filter": "labels in 7350"}
        }

        string_result = _format_view(string_filter_view)
        object_result = _format_view(object_filter_view)

        assert string_result["filter"] == object_result["filter"]
        assert string_result["filter"] == "labels in 7350"


class TestViewToolRegistry:
    """Test that view tools are properly registered."""

    def test_create_view_in_registry(self):
        """create_view tool should be in TOOL_REGISTRY."""
        assert "create_view" in TOOL_REGISTRY
        tool = TOOL_REGISTRY["create_view"]

        assert "description" in tool
        assert "input_schema" in tool
        assert "impl" in tool

        # Check required parameters
        schema = tool["input_schema"]
        assert "project_id" in schema["properties"]
        assert "title" in schema["properties"]
        assert "view_kind" in schema["properties"]
        assert schema["required"] == ["project_id", "title", "view_kind"]

    def test_update_view_in_registry(self):
        """update_view tool should be in TOOL_REGISTRY."""
        assert "update_view" in TOOL_REGISTRY
        tool = TOOL_REGISTRY["update_view"]

        schema = tool["input_schema"]
        assert "project_id" in schema["properties"]
        assert "view_id" in schema["properties"]
        assert "title" in schema["properties"]
        assert "filter_query" in schema["properties"]
        assert schema["required"] == ["project_id", "view_id"]

    def test_delete_view_in_registry(self):
        """delete_view tool should be in TOOL_REGISTRY."""
        assert "delete_view" in TOOL_REGISTRY
        tool = TOOL_REGISTRY["delete_view"]

        schema = tool["input_schema"]
        assert "project_id" in schema["properties"]
        assert "view_id" in schema["properties"]
        assert schema["required"] == ["project_id", "view_id"]
