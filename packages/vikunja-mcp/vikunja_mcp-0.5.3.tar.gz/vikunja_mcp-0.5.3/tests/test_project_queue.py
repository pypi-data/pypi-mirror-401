"""
Unit tests for project queue operations.

Tests the queue-based project creation flow where:
1. Bot queues project creation requests in PostgreSQL
2. User's browser fetches queue via /project-queue endpoint
3. Browser creates projects with user's Vikunja token
4. Browser marks queue entries as complete

Bead: solutions-eofy.1
"""

import json
import pytest
from datetime import datetime, timezone
from unittest.mock import Mock, patch, MagicMock
from starlette.requests import Request
from starlette.responses import JSONResponse


@pytest.fixture
def mock_vikunja_user_response():
    """Mock successful Vikunja /api/v1/user response."""
    return {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com"
    }


@pytest.fixture
def mock_queue_rows_batch():
    """Mock database rows for batch mode (projects JSONB)."""
    return [
        (
            1,  # id
            "vikunja:testuser",  # user_id
            "testuser",  # username
            "bot_testuser",  # bot_username
            None,  # title (null in batch mode)
            None,  # description
            None,  # hex_color
            None,  # parent_project_id
            [  # projects (JSONB - already parsed by psycopg)
                {"title": "Project 1", "description": "Desc 1", "hex_color": "#ff0000"},
                {"title": "Project 2", "description": "Desc 2", "parent_project_id": 123}
            ],
            datetime(2026, 1, 5, 17, 0, 0, tzinfo=timezone.utc)  # created_at
        )
    ]


@pytest.fixture
def mock_queue_rows_single():
    """Mock database rows for single mode (individual fields)."""
    return [
        (
            2,  # id
            "vikunja:testuser",  # user_id
            "testuser",  # username
            "bot_testuser",  # bot_username
            "Single Project",  # title
            "Single description",  # description
            "#00ff00",  # hex_color
            456,  # parent_project_id
            None,  # projects (null in single mode)
            datetime(2026, 1, 5, 17, 5, 0, tzinfo=timezone.utc)  # created_at
        )
    ]


@pytest.mark.asyncio
async def test_get_project_queue_batch_mode(mock_vikunja_user_response, mock_queue_rows_batch):
    """Test GET /project-queue returns batch mode entries correctly."""
    from vikunja_mcp.server import get_project_queue
    
    # Mock request with Bearer token
    mock_request = Mock(spec=Request)
    mock_request.headers = {"Authorization": "Bearer test_token_123"}
    
    # Mock Vikunja user verification
    with patch('httpx.get') as mock_httpx:
        mock_response = Mock()
        mock_response.json.return_value = mock_vikunja_user_response
        mock_response.raise_for_status = Mock()
        mock_httpx.return_value = mock_response
        
        # Mock database query
        with patch('vikunja_mcp.server.execute') as mock_execute:
            mock_execute.return_value = mock_queue_rows_batch
            
            # Call endpoint
            response = await get_project_queue(mock_request)
            
            # Verify response
            assert isinstance(response, JSONResponse)
            body = json.loads(response.body)
            
            assert len(body) == 1
            entry = body[0]
            assert entry["id"] == 1
            assert entry["username"] == "testuser"
            assert entry["bot_username"] == "bot_testuser"
            assert "projects" in entry
            assert len(entry["projects"]) == 2
            assert entry["projects"][0]["title"] == "Project 1"
            assert entry["projects"][1]["parent_project_id"] == 123
            
            # Verify database query
            mock_execute.assert_called_once()
            call_args = mock_execute.call_args
            assert "WHERE username = %s AND status = 'pending'" in call_args[0][0]
            assert call_args[0][1] == ("testuser",)


@pytest.mark.asyncio
async def test_get_project_queue_single_mode(mock_vikunja_user_response, mock_queue_rows_single):
    """Test GET /project-queue returns single mode entries correctly."""
    from vikunja_mcp.server import get_project_queue
    
    mock_request = Mock(spec=Request)
    mock_request.headers = {"Authorization": "Bearer test_token_123"}
    
    with patch('httpx.get') as mock_httpx:
        mock_response = Mock()
        mock_response.json.return_value = mock_vikunja_user_response
        mock_response.raise_for_status = Mock()
        mock_httpx.return_value = mock_response
        
        with patch('vikunja_mcp.server.execute') as mock_execute:
            mock_execute.return_value = mock_queue_rows_single
            
            response = await get_project_queue(mock_request)
            
            body = json.loads(response.body)
            assert len(body) == 1
            entry = body[0]
            assert entry["id"] == 2
            assert entry["title"] == "Single Project"
            assert entry["description"] == "Single description"
            assert entry["hex_color"] == "#00ff00"
            assert entry["parent_project_id"] == 456
            assert "projects" not in entry  # Single mode doesn't have projects array


@pytest.mark.asyncio
async def test_get_project_queue_missing_auth():
    """Test GET /project-queue returns 401 without Authorization header."""
    from vikunja_mcp.server import get_project_queue

    mock_request = Mock(spec=Request)
    mock_request.headers = {}

    response = await get_project_queue(mock_request)

    assert response.status_code == 401
    body = json.loads(response.body)
    assert "error" in body


@pytest.mark.asyncio
async def test_get_project_queue_invalid_token():
    """Test GET /project-queue returns 401 with invalid Vikunja token."""
    from vikunja_mcp.server import get_project_queue

    mock_request = Mock(spec=Request)
    mock_request.headers = {"Authorization": "Bearer invalid_token"}

    with patch('httpx.get') as mock_httpx:
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = Exception("401 Unauthorized")
        mock_httpx.return_value = mock_response

        response = await get_project_queue(mock_request)

        assert response.status_code == 500
        body = json.loads(response.body)
        assert "error" in body


@pytest.mark.asyncio
async def test_get_project_queue_empty_queue():
    """Test GET /project-queue returns empty array when no pending entries."""
    from vikunja_mcp.server import get_project_queue

    mock_request = Mock(spec=Request)
    mock_request.headers = {"Authorization": "Bearer test_token"}

    with patch('httpx.get') as mock_httpx:
        mock_response = Mock()
        mock_response.json.return_value = {"username": "testuser"}
        mock_response.raise_for_status = Mock()
        mock_httpx.return_value = mock_response

        with patch('vikunja_mcp.server.execute') as mock_execute:
            mock_execute.return_value = []  # Empty queue

            response = await get_project_queue(mock_request)

            body = json.loads(response.body)
            assert body == []


@pytest.mark.asyncio
async def test_mark_queue_complete_success(mock_vikunja_user_response):
    """Test POST /project-queue/{id}/complete marks entry as complete."""
    from vikunja_mcp.server import mark_queue_complete

    mock_request = Mock(spec=Request)
    mock_request.headers = {"Authorization": "Bearer test_token"}
    mock_request.path_params = {"queue_id": "123"}

    with patch('httpx.get') as mock_httpx:
        mock_response = Mock()
        mock_response.json.return_value = mock_vikunja_user_response
        mock_response.raise_for_status = Mock()
        mock_httpx.return_value = mock_response

        with patch('vikunja_mcp.server.execute') as mock_execute:
            mock_execute.return_value = []

            response = await mark_queue_complete(mock_request)

            assert response.status_code == 200
            body = json.loads(response.body)
            assert body["success"] is True

            # Verify UPDATE query
            mock_execute.assert_called_once()
            call_args = mock_execute.call_args
            assert "UPDATE project_creation_queue" in call_args[0][0]
            assert "SET status = 'complete'" in call_args[0][0]
            assert "WHERE id = %s AND username = %s" in call_args[0][0]
            assert call_args[0][1] == ("123", "testuser")


@pytest.mark.asyncio
async def test_mark_queue_complete_missing_auth():
    """Test POST /project-queue/{id}/complete returns 401 without auth."""
    from vikunja_mcp.server import mark_queue_complete

    mock_request = Mock(spec=Request)
    mock_request.headers = {}
    mock_request.path_params = {"queue_id": "123"}

    response = await mark_queue_complete(mock_request)

    assert response.status_code == 401
    body = json.loads(response.body)
    assert "error" in body


@pytest.mark.asyncio
async def test_get_project_queue_jsonb_already_parsed(mock_vikunja_user_response):
    """Test that JSONB projects column is not double-parsed."""
    from vikunja_mcp.server import get_project_queue

    mock_request = Mock(spec=Request)
    mock_request.headers = {"Authorization": "Bearer test_token"}

    # Simulate psycopg returning JSONB as already-parsed list
    mock_rows = [
        (
            1, "vikunja:user", "user", "bot", None, None, None, None,
            [{"title": "Test"}],  # Already a list, not a JSON string
            datetime.now(timezone.utc)
        )
    ]

    with patch('httpx.get') as mock_httpx:
        mock_response = Mock()
        mock_response.json.return_value = mock_vikunja_user_response
        mock_response.raise_for_status = Mock()
        mock_httpx.return_value = mock_response

        with patch('vikunja_mcp.server.execute') as mock_execute:
            mock_execute.return_value = mock_rows

            response = await get_project_queue(mock_request)

            body = json.loads(response.body)
            # Should not raise "JSON object must be str" error
            assert body[0]["projects"] == [{"title": "Test"}]


@pytest.mark.asyncio
async def test_get_project_queue_filters_by_username():
    """Test that queue only returns entries for authenticated user."""
    from vikunja_mcp.server import get_project_queue

    mock_request = Mock(spec=Request)
    mock_request.headers = {"Authorization": "Bearer test_token"}

    with patch('httpx.get') as mock_httpx:
        mock_response = Mock()
        mock_response.json.return_value = {"username": "alice"}
        mock_response.raise_for_status = Mock()
        mock_httpx.return_value = mock_response

        with patch('vikunja_mcp.server.execute') as mock_execute:
            mock_execute.return_value = []

            await get_project_queue(mock_request)

            # Verify query filters by username
            call_args = mock_execute.call_args
            assert call_args[0][1] == ("alice",)  # Username from token verification



@pytest.mark.asyncio
async def test_claim_project_queue_atomic(mock_vikunja_user_response, mock_queue_rows_batch):
    """Test POST /project-queue/claim atomically claims pending entries."""
    from vikunja_mcp.server import claim_project_queue
    
    mock_request = Mock(spec=Request)
    mock_request.headers = {"Authorization": "Bearer test_token"}
    
    with patch('httpx.get') as mock_httpx:
        mock_response = Mock()
        mock_response.json.return_value = mock_vikunja_user_response
        mock_response.raise_for_status = Mock()
        mock_httpx.return_value = mock_response
        
        with patch('vikunja_mcp.server.execute') as mock_execute:
            # Simulate UPDATE ... RETURNING
            mock_execute.return_value = mock_queue_rows_batch
            
            response = await claim_project_queue(mock_request)
            
            assert response.status_code == 200
            body = json.loads(response.body)
            assert len(body) == 1
            assert body[0]["id"] == 1
            
            # Verify UPDATE query with FOR UPDATE SKIP LOCKED
            call_args = mock_execute.call_args
            query = call_args[0][0]
            assert "UPDATE project_creation_queue" in query
            assert "SET status = 'processing'" in query
            assert "WHERE username = %s AND status = 'pending'" in query
            assert "FOR UPDATE SKIP LOCKED" in query
            assert "RETURNING" in query


@pytest.mark.asyncio
async def test_claim_project_queue_empty():
    """Test POST /project-queue/claim returns empty array when nothing to claim."""
    from vikunja_mcp.server import claim_project_queue
    
    mock_request = Mock(spec=Request)
    mock_request.headers = {"Authorization": "Bearer test_token"}
    
    with patch('httpx.get') as mock_httpx:
        mock_response = Mock()
        mock_response.json.return_value = {"username": "testuser"}
        mock_response.raise_for_status = Mock()
        mock_httpx.return_value = mock_response
        
        with patch('vikunja_mcp.server.execute') as mock_execute:
            mock_execute.return_value = []  # Nothing to claim
            
            response = await claim_project_queue(mock_request)
            
            body = json.loads(response.body)
            assert body == []


@pytest.mark.asyncio
async def test_claim_prevents_duplicates():
    """Test that claiming entries prevents duplicate processing on refresh."""
    from vikunja_mcp.server import claim_project_queue
    
    mock_request = Mock(spec=Request)
    mock_request.headers = {"Authorization": "Bearer test_token"}
    
    with patch('httpx.get') as mock_httpx:
        mock_response = Mock()
        mock_response.json.return_value = {"username": "testuser"}
        mock_response.raise_for_status = Mock()
        mock_httpx.return_value = mock_response
        
        with patch('vikunja_mcp.server.execute') as mock_execute:
            # First call: returns entries
            mock_execute.return_value = [(1, "vikunja:user", "user", "bot", "Test", "", "", 0, None, datetime.now(timezone.utc))]
            
            response1 = await claim_project_queue(mock_request)
            body1 = json.loads(response1.body)
            assert len(body1) == 1
            
            # Second call (refresh): returns empty (entries already claimed)
            mock_execute.return_value = []
            
            response2 = await claim_project_queue(mock_request)
            body2 = json.loads(response2.body)
            assert len(body2) == 0  # No duplicates\!
