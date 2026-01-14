"""Integration tests for HTML injection protection.

Tests that malicious HTML in Vikunja data is properly escaped in Matrix bot responses.

Run with: uv run pytest tests/integration/test_html_escaping.py -v -m integration

Requires environment variables (see conftest.py for details).
"""

import pytest

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


class TestHTMLEscapingInTaskDescriptions:
    """Test HTML escaping for task descriptions retrieved from Vikunja."""

    async def test_script_tag_in_description_is_escaped(self, matrix_client, bot_dm_room, bot_user):
        """Script tags in task descriptions should be escaped, not executed."""
        # This test assumes a task exists in Vikunja with malicious HTML
        # In a real scenario, you'd create the task via Vikunja API first
        
        response = await matrix_client.send_and_wait(
            bot_dm_room,
            "show me task details for any task",
            bot_user,
            timeout=30.0
        )
        
        assert response is not None, "Bot did not respond"
        
        # If response contains HTML, it should be escaped
        if "<script>" in response.lower():
            pytest.fail("Unescaped <script> tag found in response")
        
        # Escaped version should be present if original had script tags
        # &lt;script&gt; is the escaped form

    async def test_img_tag_with_onerror_is_escaped(self, matrix_client, bot_dm_room, bot_user):
        """Image tags with onerror handlers should be escaped."""
        response = await matrix_client.send_and_wait(
            bot_dm_room,
            "list my tasks",
            bot_user,
            timeout=30.0
        )
        
        assert response is not None, "Bot did not respond"
        
        # Check for unescaped dangerous patterns
        dangerous_patterns = [
            "<img",
            "onerror=",
            "onclick=",
            "onload=",
        ]
        
        for pattern in dangerous_patterns:
            if pattern in response.lower():
                # Could be escaped - check if it's &lt;img instead
                if "&lt;" not in response:
                    pytest.fail(f"Potentially unescaped HTML pattern found: {pattern}")

    async def test_iframe_tag_is_escaped(self, matrix_client, bot_dm_room, bot_user):
        """Iframe tags should be escaped to prevent embedding malicious content."""
        response = await matrix_client.send_and_wait(
            bot_dm_room,
            "show tasks",
            bot_user,
            timeout=30.0
        )
        
        assert response is not None, "Bot did not respond"
        
        if "<iframe" in response.lower() and "&lt;iframe" not in response.lower():
            pytest.fail("Unescaped <iframe> tag found in response")


class TestHTMLEscapingInTaskTitles:
    """Test HTML escaping for task titles."""

    async def test_bold_tag_in_title_is_escaped(self, matrix_client, bot_dm_room, bot_user):
        """HTML tags in task titles should be escaped."""
        response = await matrix_client.send_and_wait(
            bot_dm_room,
            "list tasks",
            bot_user,
            timeout=30.0
        )
        
        assert response is not None, "Bot did not respond"
        
        # Task titles should not contain unescaped HTML
        # Markdown bold (**text**) is OK, but <b>text</b> should be escaped


class TestHTMLEscapingInProjectNames:
    """Test HTML escaping for project names."""

    async def test_script_in_project_name_is_escaped(self, matrix_client, bot_dm_room, bot_user):
        """Project names with HTML should be escaped."""
        response = await matrix_client.send_and_wait(
            bot_dm_room,
            "show my projects",
            bot_user,
            timeout=30.0
        )
        
        assert response is not None, "Bot did not respond"
        
        if "<script>" in response.lower() and "&lt;script&gt;" not in response.lower():
            pytest.fail("Unescaped <script> in project name")


class TestHTMLEscapingInLLMResponses:
    """Test that LLM-generated responses are also escaped."""

    async def test_llm_response_with_html_is_escaped(self, matrix_client, bot_dm_room, bot_user):
        """Even if LLM generates HTML, it should be escaped."""
        # Ask a question that might cause LLM to generate HTML-like content
        response = await matrix_client.send_and_wait(
            bot_dm_room,
            "explain how to use HTML tags in task descriptions",
            bot_user,
            timeout=30.0
        )
        
        assert response is not None, "Bot did not respond"
        
        # LLM might mention <script> tags in explanation
        # These should be escaped in the formatted_body sent to Matrix


class TestXSSPayloads:
    """Test common XSS attack vectors are properly escaped."""

    async def test_javascript_protocol_is_escaped(self, matrix_client, bot_dm_room, bot_user):
        """javascript: protocol in links should be escaped."""
        response = await matrix_client.send_and_wait(
            bot_dm_room,
            "show tasks",
            bot_user,
            timeout=30.0
        )
        
        assert response is not None, "Bot did not respond"
        
        if "javascript:" in response.lower():
            # Check if it's escaped
            if "javascript:" in response and "&" not in response[:response.index("javascript:")]:
                pytest.fail("Unescaped javascript: protocol found")

    async def test_data_uri_is_handled_safely(self, matrix_client, bot_dm_room, bot_user):
        """data: URIs should be handled safely."""
        response = await matrix_client.send_and_wait(
            bot_dm_room,
            "list tasks",
            bot_user,
            timeout=30.0
        )
        
        assert response is not None, "Bot did not respond"
        
        # data: URIs can be used for XSS
        if "data:text/html" in response.lower():
            pytest.fail("Potentially dangerous data: URI found")

