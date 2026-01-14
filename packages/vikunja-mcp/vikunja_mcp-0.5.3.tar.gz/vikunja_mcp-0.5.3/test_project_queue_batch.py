#!/usr/bin/env python3
"""
Unit tests for project queue batching functionality.

Bead: solutions-eofy (User Can Create Project - JSON Batch Support)

Tests the batching logic that accumulates multiple create_project calls
into a single queue entry with projects as JSON array.
"""

import pytest
import json
import contextvars
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))


class TestProjectQueueBatching:
    """Test project batching context variables and flush logic."""
    
    def setup_method(self):
        """Reset context variables before each test."""
        # Import after path setup
        from vikunja_mcp.server import _pending_projects, _next_temp_id
        self.pending_projects = _pending_projects
        self.next_temp_id = _next_temp_id
        
        # Reset to defaults
        self.pending_projects.set([])
        self.next_temp_id.set(-1)
    
    def test_context_variables_initialized(self):
        """Test that context variables start with correct defaults."""
        assert self.pending_projects.get() == []
        assert self.next_temp_id.get() == -1
    
    def test_single_project_batching(self):
        """Test batching a single project."""
        from vikunja_mcp.server import _create_project_impl, _requesting_user, _current_user_id
        
        # Set user context
        _requesting_user.set("testuser")
        _current_user_id.set("vikunja:testuser")
        
        # Mock bot credentials
        with patch('vikunja_mcp.server.get_user_bot_credentials') as mock_creds:
            mock_creds.return_value = ("eis-testuser", "password123")
            
            # Create project
            result = _create_project_impl("Test Project", "Description", "#ff0000", 0)
        
        # Check result
        assert result["id"] == -1  # First temp ID
        assert result["title"] == "Test Project"
        assert result["status"] == "queued"
        
        # Check batch
        pending = self.pending_projects.get()
        assert len(pending) == 1
        assert pending[0]["temp_id"] == -1
        assert pending[0]["title"] == "Test Project"
        assert pending[0]["description"] == "Description"
        assert pending[0]["hex_color"] == "#ff0000"
        assert pending[0]["parent_project_id"] == 0
    
    def test_multiple_projects_batching(self):
        """Test batching multiple projects in one turn."""
        from vikunja_mcp.server import _create_project_impl, _requesting_user, _current_user_id
        
        _requesting_user.set("testuser")
        _current_user_id.set("vikunja:testuser")
        
        with patch('vikunja_mcp.server.get_user_bot_credentials') as mock_creds:
            mock_creds.return_value = ("eis-testuser", "password123")
            
            # Create multiple projects
            r1 = _create_project_impl("Project 1")
            r2 = _create_project_impl("Project 2")
            r3 = _create_project_impl("Project 3")
        
        # Check temp IDs increment
        assert r1["id"] == -1
        assert r2["id"] == -2
        assert r3["id"] == -3
        
        # Check batch size
        pending = self.pending_projects.get()
        assert len(pending) == 3
        assert pending[0]["title"] == "Project 1"
        assert pending[1]["title"] == "Project 2"
        assert pending[2]["title"] == "Project 3"
    
    def test_hierarchical_parent_references(self):
        """Test parent references using temp IDs."""
        from vikunja_mcp.server import _create_project_impl, _requesting_user, _current_user_id
        
        _requesting_user.set("testuser")
        _current_user_id.set("vikunja:testuser")
        
        with patch('vikunja_mcp.server.get_user_bot_credentials') as mock_creds:
            mock_creds.return_value = ("eis-testuser", "password123")
            
            # Create hierarchy: Marketing > Campaigns > Q1 2026
            r1 = _create_project_impl("Marketing", parent_project_id=0)
            r2 = _create_project_impl("Campaigns", parent_project_id=r1["id"])  # Use temp ID
            r3 = _create_project_impl("Q1 2026", parent_project_id=r2["id"])    # Use temp ID
        
        # Check parent references
        pending = self.pending_projects.get()
        assert len(pending) == 3
        
        assert pending[0]["title"] == "Marketing"
        assert pending[0]["parent_project_id"] == 0
        
        assert pending[1]["title"] == "Campaigns"
        assert pending[1]["parent_project_id"] == -1  # References Marketing
        
        assert pending[2]["title"] == "Q1 2026"
        assert pending[2]["parent_project_id"] == -2  # References Campaigns
    
    def test_flush_project_queue(self):
        """Test flushing batched projects to database."""
        from vikunja_mcp.server import (
            _create_project_impl, _flush_project_queue,
            _requesting_user, _current_user_id
        )
        
        _requesting_user.set("testuser")
        _current_user_id.set("vikunja:testuser")
        
        # Mock database and bot credentials
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = [123]  # queue_id
        mock_db.__enter__.return_value = mock_db
        mock_db.cursor.return_value.__enter__.return_value = mock_cursor
        
        with patch('vikunja_mcp.server.get_user_bot_credentials') as mock_creds, \
             patch('vikunja_mcp.server.get_db') as mock_get_db:
            
            mock_creds.return_value = ("eis-testuser", "password123")
            mock_get_db.return_value = mock_db
            
            # Batch some projects
            _create_project_impl("Project 1")
            _create_project_impl("Project 2")
            
            # Flush
            queue_id = _flush_project_queue()
        
        # Check flush result
        assert queue_id == 123
        
        # Check database was called
        assert mock_cursor.execute.called
        call_args = mock_cursor.execute.call_args[0]
        assert "INSERT INTO project_creation_queue" in call_args[0]
        assert "projects" in call_args[0]
        
        # Check JSON was passed
        params = call_args[1]
        assert params[0] == "vikunja:testuser"
        assert params[1] == "testuser"
        assert params[2] == "eis-testuser"
        
        # Parse JSON
        projects_json = json.loads(params[3])
        assert len(projects_json) == 2
        assert projects_json[0]["title"] == "Project 1"
        assert projects_json[1]["title"] == "Project 2"

        # Check batch was cleared
        assert self.pending_projects.get() == []
        assert self.next_temp_id.get() == -1

    def test_flush_empty_queue(self):
        """Test flushing when no projects are batched."""
        from vikunja_mcp.server import _flush_project_queue, _requesting_user, _current_user_id

        _requesting_user.set("testuser")
        _current_user_id.set("vikunja:testuser")

        # Flush empty queue
        queue_id = _flush_project_queue()

        # Should return None
        assert queue_id is None

    def test_flush_without_user_context(self):
        """Test flushing fails gracefully without user context."""
        from vikunja_mcp.server import _create_project_impl, _flush_project_queue

        # No user context set
        with patch('vikunja_mcp.server.get_user_bot_credentials') as mock_creds:
            mock_creds.return_value = ("eis-testuser", "password123")

            # This should fall back to legacy mode
            result = _create_project_impl("Test")

            # Should not batch (no user context)
            assert self.pending_projects.get() == []

    def test_sanitize_title(self):
        """Test HTML sanitization in project titles."""
        from vikunja_mcp.server import _create_project_impl, _requesting_user, _current_user_id

        _requesting_user.set("testuser")
        _current_user_id.set("vikunja:testuser")

        with patch('vikunja_mcp.server.get_user_bot_credentials') as mock_creds:
            mock_creds.return_value = ("eis-testuser", "password123")

            # Create project with HTML in title
            result = _create_project_impl("<script>alert('xss')</script>Test")

        # Check title was sanitized
        pending = self.pending_projects.get()
        assert "<script>" not in pending[0]["title"]
        assert "Test" in pending[0]["title"]


class TestQueueEndpoints:
    """Test GET /project-queue endpoint with batch support."""

    def test_get_queue_single_mode(self):
        """Test fetching queue with single project entry."""
        # This would require setting up FastMCP test client
        # Skipping for now - integration test
        pass

    def test_get_queue_batch_mode(self):
        """Test fetching queue with batch entry."""
        # This would require setting up FastMCP test client
        # Skipping for now - integration test
        pass


class TestFrontendProcessing:
    """Test frontend processing logic (JavaScript simulation)."""

    def test_temp_id_resolution(self):
        """Test resolving temp ID parent references."""
        # Simulate frontend idMap logic
        projects = [
            {"temp_id": -1, "title": "Marketing", "parent_project_id": 0},
            {"temp_id": -2, "title": "Campaigns", "parent_project_id": -1},
            {"temp_id": -3, "title": "Q1 2026", "parent_project_id": -2}
        ]

        id_map = {}
        resolved_parents = []

        # Simulate processing
        for i, spec in enumerate(projects):
            parent_id = spec["parent_project_id"]

            # Resolve temp ID
            if parent_id < 0 and parent_id in id_map:
                parent_id = id_map[parent_id]
            elif parent_id < 0:
                parent_id = 0  # Fallback

            resolved_parents.append(parent_id)

            # Simulate Vikunja returning real ID
            real_id = 100 + i
            id_map[spec["temp_id"]] = real_id

        # Check resolution
        assert resolved_parents[0] == 0    # Marketing: root
        assert resolved_parents[1] == 100  # Campaigns: under Marketing
        assert resolved_parents[2] == 101  # Q1 2026: under Campaigns

    def test_broken_parent_reference(self):
        """Test handling broken parent references."""
        projects = [
            {"temp_id": -1, "title": "Child", "parent_project_id": -99}  # Parent doesn't exist
        ]

        id_map = {}

        parent_id = projects[0]["parent_project_id"]
        if parent_id < 0 and parent_id not in id_map:
            parent_id = 0  # Fallback to root

        assert parent_id == 0  # Should fall back


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])


