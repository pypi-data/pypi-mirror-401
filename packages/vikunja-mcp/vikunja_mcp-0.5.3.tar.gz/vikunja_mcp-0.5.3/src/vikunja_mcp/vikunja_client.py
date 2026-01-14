"""
Vikunja API Client - Direct HTTP client for Vikunja REST API.

This module provides a clean HTTP client for Vikunja API calls without MCP.
It uses the token broker for secure token retrieval and handles all API
communication directly.

Key design decisions:
- No MCP dependency - direct HTTP calls
- Token broker integration for secure token retrieval
- Instance URL from PostgreSQL (supports multi-instance)
- Clean error handling with typed exceptions

Bead: solutions-lt0f.3
"""

import logging
from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional

from rapidfuzz import fuzz, process
import httpx

from .token_broker import (
    get_user_token,
    get_user_instance_url,
    get_user_active_instance,
    AuthRequired,
)

logger = logging.getLogger(__name__)

# Default timeout for API calls
DEFAULT_TIMEOUT = 30.0


class VikunjaAPIError(Exception):
    """Raised when Vikunja API returns an error."""
    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.status_code = status_code


@dataclass
class Task:
    """A Vikunja task."""
    id: int
    title: str
    done: bool
    due_date: Optional[datetime] = None
    project_id: Optional[int] = None
    priority: int = 0
    description: Optional[str] = None


@dataclass
class Project:
    """A Vikunja project."""
    id: int
    title: str
    description: Optional[str] = None
    parent_project_id: Optional[int] = None


class VikunjaClient:
    """HTTP client for Vikunja REST API.

    Usage:
        client = VikunjaClient(user_id="@user:matrix.example.com")
        tasks = client.get_tasks_due_today()
        projects = client.get_projects()
    """

    def __init__(
        self,
        user_id: str,
        instance: Optional[str] = None,
        timeout: float = DEFAULT_TIMEOUT
    ):
        """Initialize Vikunja client.

        Args:
            user_id: Matrix or Slack user ID
            instance: Vikunja instance name (default: user's active instance)
            timeout: HTTP timeout in seconds
        """
        self.user_id = user_id
        self.instance = instance or get_user_active_instance(user_id) or "default"
        self.timeout = timeout
        self._token: Optional[str] = None
        self._base_url: Optional[str] = None

    def _get_token(self) -> str:
        """Get Vikunja API token for the user's instance."""
        if self._token is None:
            self._token = get_user_token(
                self.user_id,
                purpose="vikunja_api_call",
                instance=self.instance,
                caller="VikunjaClient._get_token"
            )
            if not self._token:
                raise AuthRequired(
                    f"No token found for instance '{self.instance}'. "
                    "Please connect with !vik <url> <token> <name>"
                )
        return self._token

    def _get_base_url(self) -> str:
        """Get Vikunja base URL for the user's instance."""
        if self._base_url is None:
            self._base_url = get_user_instance_url(self.user_id, self.instance)
            if not self._base_url:
                raise AuthRequired(
                    f"No URL found for instance '{self.instance}'. "
                    "Please reconnect with !vik <url> <token> <name>"
                )
        return self._base_url

    def _request(
        self,
        method: str,
        path: str,
        params: Optional[dict] = None,
        json: Optional[dict] = None
    ) -> dict | list:
        """Make authenticated request to Vikunja API.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            path: API path (e.g., "/api/v1/tasks/all")
            params: Query parameters
            json: JSON body

        Returns:
            Parsed JSON response

        Raises:
            AuthRequired: If token is missing or expired
            VikunjaAPIError: If API returns an error
        """
        url = f"{self._get_base_url()}{path}"
        headers = {"Authorization": f"Bearer {self._get_token()}"}

        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.request(
                    method=method,
                    url=url,
                    headers=headers,
                    params=params,
                    json=json
                )

            if response.status_code == 401:
                raise AuthRequired(
                    "Token expired or invalid. Please reconnect with !vik"
                )

            if response.status_code >= 400:
                error_msg = response.text[:200] if response.text else "Unknown error"
                raise VikunjaAPIError(
                    f"API error {response.status_code}: {error_msg}",
                    status_code=response.status_code
                )

            return response.json()

        except httpx.TimeoutException:
            raise VikunjaAPIError("Request timed out", status_code=None)
        except httpx.RequestError as e:
            raise VikunjaAPIError(f"Request failed: {e}", status_code=None)

    def get_tasks(
        self,
        project_id: Optional[int] = None,
        filter_by: Optional[str] = None
    ) -> list[Task]:
        """Get tasks, optionally filtered by project and/or filter.

        Args:
            project_id: Filter by project ID (optional)
            filter_by: Vikunja filter query string (optional)

        Returns:
            List of Task objects
        """
        params = {}
        if filter_by:
            params["filter"] = filter_by

        if project_id:
            # Use project-specific endpoint
            path = f"/api/v1/projects/{project_id}/tasks"
        else:
            # Use global tasks endpoint
            path = "/api/v1/tasks/all"

        response = self._request("GET", path, params=params)

        tasks = []
        for item in response:
            due_date = None
            if item.get("due_date") and item["due_date"] != "0001-01-01T00:00:00Z":
                try:
                    due_date = datetime.fromisoformat(
                        item["due_date"].replace("Z", "+00:00")
                    )
                except ValueError:
                    pass

            tasks.append(Task(
                id=item["id"],
                title=item["title"],
                done=item.get("done", False),
                due_date=due_date,
                project_id=item.get("project_id"),
                priority=item.get("priority", 0),
                description=item.get("description")
            ))

        return tasks

    def get_tasks_due_today(self, project_id: Optional[int] = None) -> list[Task]:
        """Get tasks due today.

        Args:
            project_id: Filter by project ID (optional)

        Returns:
            List of Task objects due today
        """
        today = date.today().isoformat()
        filter_query = f'due_date = "{today}" && done = false'
        return self.get_tasks(project_id=project_id, filter_by=filter_query)

    def get_tasks_due_this_week(self, project_id: Optional[int] = None) -> list[Task]:
        """Get tasks due this week (next 7 days).

        Args:
            project_id: Filter by project ID (optional)

        Returns:
            List of Task objects due this week
        """
        today = date.today().isoformat()
        filter_query = f'due_date >= "{today}" && due_date <= now+7d && done = false'
        return self.get_tasks(project_id=project_id, filter_by=filter_query)

    def get_projects(self) -> list[Project]:
        """Get all projects accessible to the user.

        Returns:
            List of Project objects
        """
        response = self._request("GET", "/api/v1/projects")

        projects = []
        for item in response:
            projects.append(Project(
                id=item["id"],
                title=item["title"],
                description=item.get("description"),
                parent_project_id=item.get("parent_project_id")
            ))

        return projects

    def find_project_by_name(self, name: str, threshold: int = 60) -> Optional[Project]:
        """Find a project by name using fuzzy matching.

        Args:
            name: Project name to search for
            threshold: Minimum confidence score (0-100, default 60)

        Returns:
            Best matching Project above threshold, or None if not found
        """
        projects = self.get_projects()
        if not projects:
            return None

        # Build title -> project mapping
        project_map = {p.title: p for p in projects}

        # Fuzzy match
        matches = process.extract(
            name,
            project_map.keys(),
            scorer=fuzz.WRatio,
            limit=1
        )

        if not matches or matches[0][1] < threshold:
            return None

        best_title = matches[0][0]
        return project_map[best_title]

    def search_tasks(
        self,
        query: str,
        project_id: Optional[int] = None,
        include_done: bool = False,
        threshold: int = 50
    ) -> list[Task]:
        """Search tasks by title using fuzzy matching.

        Args:
            query: Search string to match against task titles
            project_id: Limit search to specific project (optional)
            include_done: Include completed tasks (default: False)
            threshold: Minimum confidence score (0-100, default 50)

        Returns:
            List of matching Task objects, sorted by relevance score
        """
        # Get all tasks (with project filter if specified)
        filter_by = None if include_done else "done = false"
        tasks = self.get_tasks(project_id=project_id, filter_by=filter_by)

        if not query or not tasks:
            return tasks

        # Fuzzy match - get all results above threshold
        matches = process.extract(
            query,
            [t.title for t in tasks],  # Match against titles only
            scorer=fuzz.WRatio,
            limit=len(tasks)  # Get all matches
        )

        # Filter by threshold and return tasks in score order
        result = []
        seen_ids = set()
        for title, score, idx in matches:
            if score >= threshold:
                task = tasks[idx]
                if task.id not in seen_ids:
                    result.append(task)
                    seen_ids.add(task.id)

        return result

    def get_task(self, task_id: int) -> Optional[Task]:
        """Get a single task by ID.

        Args:
            task_id: Task ID

        Returns:
            Task object, or None if not found
        """
        try:
            item = self._request("GET", f"/api/v1/tasks/{task_id}")
            due_date = None
            if item.get("due_date") and item["due_date"] != "0001-01-01T00:00:00Z":
                try:
                    due_date = datetime.fromisoformat(
                        item["due_date"].replace("Z", "+00:00")
                    )
                except ValueError:
                    pass

            return Task(
                id=item["id"],
                title=item["title"],
                done=item.get("done", False),
                due_date=due_date,
                project_id=item.get("project_id"),
                priority=item.get("priority", 0),
                description=item.get("description")
            )
        except VikunjaAPIError as e:
            if e.status_code == 404:
                return None
            raise

    def delete_task(self, task_id: int) -> bool:
        """Delete a task by ID.

        Args:
            task_id: Task ID

        Returns:
            True if deleted successfully
        """
        self._request("DELETE", f"/api/v1/tasks/{task_id}")
        return True

    def complete_task(self, task_id: int) -> Task:
        """Mark a task as complete.

        Args:
            task_id: Task ID

        Returns:
            Updated Task object
        """
        return self.update_task(task_id, done=True)

    def update_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        due_date: Optional[str] = None,
        priority: Optional[int] = None,
        done: Optional[bool] = None
    ) -> Task:
        """Update a task.

        Args:
            task_id: Task ID
            title: New title (optional)
            description: New description (optional)
            due_date: New due date ISO format (optional)
            priority: New priority 0-5 (optional)
            done: Mark done/undone (optional)

        Returns:
            Updated Task object
        """
        # Get current task first (Vikunja requires full object)
        current = self._request("GET", f"/api/v1/tasks/{task_id}")

        if title is not None:
            current["title"] = title
        if description is not None:
            current["description"] = description
        if due_date is not None:
            current["due_date"] = due_date
        if priority is not None:
            current["priority"] = priority
        if done is not None:
            current["done"] = done

        item = self._request("POST", f"/api/v1/tasks/{task_id}", json=current)

        due_dt = None
        if item.get("due_date") and item["due_date"] != "0001-01-01T00:00:00Z":
            try:
                due_dt = datetime.fromisoformat(
                    item["due_date"].replace("Z", "+00:00")
                )
            except ValueError:
                pass

        return Task(
            id=item["id"],
            title=item["title"],
            done=item.get("done", False),
            due_date=due_dt,
            project_id=item.get("project_id"),
            priority=item.get("priority", 0),
            description=item.get("description")
        )

    def move_task(self, task_id: int, project_id: int) -> Task:
        """Move a task to a different project.

        Args:
            task_id: Task ID
            project_id: Target project ID

        Returns:
            Updated Task object
        """
        current = self._request("GET", f"/api/v1/tasks/{task_id}")
        current["project_id"] = project_id
        item = self._request("POST", f"/api/v1/tasks/{task_id}", json=current)

        due_dt = None
        if item.get("due_date") and item["due_date"] != "0001-01-01T00:00:00Z":
            try:
                due_dt = datetime.fromisoformat(
                    item["due_date"].replace("Z", "+00:00")
                )
            except ValueError:
                pass

        return Task(
            id=item["id"],
            title=item["title"],
            done=item.get("done", False),
            due_date=due_dt,
            project_id=item.get("project_id"),
            priority=item.get("priority", 0),
            description=item.get("description")
        )

    def add_comment(self, task_id: int, comment: str) -> dict:
        """Add a comment to a task.

        Args:
            task_id: Task ID
            comment: Comment text

        Returns:
            Created comment object from API
        """
        return self._request(
            "PUT",
            f"/api/v1/tasks/{task_id}/comments",
            json={"comment": comment}
        )


class BotVikunjaClient:
    """Vikunja client using bot JWT authentication (for @eis operations).

    Unlike VikunjaClient which uses per-user tokens from the token broker,
    this client uses bot credentials to get JWT tokens.

    NOTE: API tokens are broken in Vikunja (GitHub issue #105), so we use JWT tokens.
    Bot logs in with username/password to get JWT tokens instead of API tokens.

    Usage:
        # With user_id (recommended - uses personal bot)
        client = BotVikunjaClient(user_id="vikunja:alice")
        client.add_comment(task_id, "✅ Done!")

        # Legacy: with explicit token (deprecated)
        client = BotVikunjaClient(token="tk_xxx")
    """

    def __init__(self, token: str = None, user_id: str = None, timeout: float = DEFAULT_TIMEOUT):
        """Initialize bot client.

        Args:
            token: DEPRECATED - Bot API token (for backward compatibility only)
            user_id: Owner's user_id for this personal bot (uses JWT auth)
            timeout: HTTP timeout in seconds
        """
        import os
        import logging
        self.timeout = timeout
        self.user_id = user_id
        self._token = None  # Will be set by _get_token()
        self._base_url = os.environ.get("VIKUNJA_URL", "https://vikunja.factumerit.app").strip()

        # Bot credentials for JWT auth (if using user_id)
        self._bot_username = None
        self._bot_password = None

        logger = logging.getLogger(__name__)

        # Legacy token support (deprecated)
        if token:
            logger.warning("[BotVikunjaClient] Using explicit token is deprecated (API tokens are broken)")
            self._token = token.strip()
        elif not user_id:
            # Fallback to env var (deprecated)
            env_token = os.environ.get("VIKUNJA_BOT_TOKEN")
            if env_token:
                logger.warning("[BotVikunjaClient] Using VIKUNJA_BOT_TOKEN is deprecated (API tokens are broken)")
                self._token = env_token.strip()
            else:
                raise ValueError(
                    "BotVikunjaClient requires either:\n"
                    "  - user_id parameter (recommended, uses JWT auth)\n"
                    "  - token parameter (deprecated, API tokens are broken)\n"
                    "  - VIKUNJA_BOT_TOKEN env var (deprecated, API tokens are broken)"
                )

        # If user_id provided, load bot credentials for JWT auth
        if user_id:
            from .bot_provisioning import get_user_bot_credentials
            credentials = get_user_bot_credentials(user_id)
            if not credentials:
                raise ValueError(f"No bot credentials found for user {user_id}")
            self._bot_username, self._bot_password = credentials
            logger.info(f"[BotVikunjaClient] Initialized for bot {self._bot_username} (JWT auth)")

    def _get_token(self) -> str:
        """Get JWT token for bot authentication (with caching)."""
        # If using legacy token, return it
        if self._token and not self._bot_username:
            return self._token

        # Use JWT manager for bot authentication
        if self._bot_username and self._bot_password:
            from .bot_jwt_manager import get_bot_jwt
            return get_bot_jwt(
                bot_username=self._bot_username,
                bot_password=self._bot_password,
                vikunja_url=self._base_url
            )

        raise ValueError("No authentication method available")

    def _request(
        self,
        method: str,
        path: str,
        params: Optional[dict] = None,
        json: Optional[dict] = None
    ) -> dict | list:
        """Make authenticated request to Vikunja API."""
        url = f"{self._base_url}{path}"

        try:
            token = self._get_token()
            headers = {"Authorization": f"Bearer {token}"}

            with httpx.Client(timeout=self.timeout) as client:
                response = client.request(
                    method=method,
                    url=url,
                    headers=headers,
                    params=params,
                    json=json
                )
                response.raise_for_status()
                if response.status_code == 204:
                    return {}
                return response.json()
        except httpx.HTTPStatusError as e:
            # If 401, try refreshing JWT token
            if e.response.status_code == 401 and self._bot_username:
                import logging
                logger = logging.getLogger(__name__)
                logger.info(f"[BotVikunjaClient] 401 error, refreshing JWT token for {self._bot_username}")

                from .bot_jwt_manager import get_bot_jwt
                token = get_bot_jwt(
                    bot_username=self._bot_username,
                    bot_password=self._bot_password,
                    vikunja_url=self._base_url,
                    force_refresh=True
                )
                headers = {"Authorization": f"Bearer {token}"}

                # Retry request with new token
                with httpx.Client(timeout=self.timeout) as client:
                    response = client.request(
                        method=method,
                        url=url,
                        headers=headers,
                        params=params,
                        json=json
                    )
                    response.raise_for_status()
                    if response.status_code == 204:
                        return {}
                    return response.json()

            raise VikunjaAPIError(
                f"API error: {e.response.status_code} - {e.response.text}",
                status_code=e.response.status_code
            )
        except httpx.RequestError as e:
            raise VikunjaAPIError(f"Request failed: {e}")

    def get_task(self, task_id: int) -> dict:
        """Get a task by ID."""
        return self._request("GET", f"/api/v1/tasks/{task_id}")

    def update_task(self, task_id: int, **updates) -> dict:
        """Update a task.

        Args:
            task_id: Task ID
            **updates: Fields to update (title, description, due_date, priority, done)

        Returns:
            Updated task object
        """
        current = self._request("GET", f"/api/v1/tasks/{task_id}")
        for key, value in updates.items():
            if value is not None:
                current[key] = value
        return self._request("POST", f"/api/v1/tasks/{task_id}", json=current)

    def add_comment(self, task_id: int, comment: str) -> dict:
        """Add a comment to a task."""
        return self._request(
            "PUT",
            f"/api/v1/tasks/{task_id}/comments",
            json={"comment": comment}
        )

    def get_comments(self, task_id: int) -> list[dict]:
        """Get all comments for a task.

        Args:
            task_id: Task ID

        Returns:
            List of comment objects, sorted by creation date (oldest first)
        """
        comments = self._request("GET", f"/api/v1/tasks/{task_id}/comments")
        if not comments:
            return []
        # Sort by created date (oldest first for conversation order)
        return sorted(comments, key=lambda c: c.get("created", ""))

    def delete_task(self, task_id: int) -> dict:
        """Delete a task.

        Args:
            task_id: Task ID to delete

        Returns:
            Empty dict on success
        """
        return self._request("DELETE", f"/api/v1/tasks/{task_id}")

    def list_tasks(self, project_id: int) -> list[dict]:
        """List all tasks in a project.

        Args:
            project_id: Project ID

        Returns:
            List of task objects
        """
        return self._request("GET", f"/api/v1/projects/{project_id}/tasks")

    # =========================================================================
    # Attachments API
    # =========================================================================

    def add_attachment(self, task_id: int, filename: str, content: bytes, content_type: str = "text/plain") -> dict:
        """Add an attachment to a task.

        Args:
            task_id: Task ID
            filename: Name for the attachment file
            content: File content as bytes
            content_type: MIME type (default: text/plain)

        Returns:
            Attachment object from API
        """
        files = {"files": (filename, content, content_type)}
        response = httpx.put(
            f"{self.instance_url}/api/v1/tasks/{task_id}/attachments",
            headers={"Authorization": f"Bearer {self.token}"},
            files=files,
            timeout=DEFAULT_TIMEOUT,
        )
        if response.status_code >= 400:
            raise VikunjaAPIError(f"API error: {response.status_code} - {response.text}", response.status_code)
        return response.json()

    def get_attachments(self, task_id: int) -> list[dict]:
        """Get all attachments for a task.

        Args:
            task_id: Task ID

        Returns:
            List of attachment objects
        """
        task = self._request("GET", f"/api/v1/tasks/{task_id}")
        return task.get("attachments") or []

    def get_attachment_content(self, task_id: int, attachment_id: int) -> bytes:
        """Download attachment content.

        Args:
            task_id: Task ID
            attachment_id: Attachment ID

        Returns:
            File content as bytes
        """
        response = httpx.get(
            f"{self.instance_url}/api/v1/tasks/{task_id}/attachments/{attachment_id}",
            headers={"Authorization": f"Bearer {self.token}"},
            timeout=DEFAULT_TIMEOUT,
        )
        if response.status_code >= 400:
            raise VikunjaAPIError(f"API error: {response.status_code} - {response.text}", response.status_code)
        return response.content

    def delete_attachment(self, task_id: int, attachment_id: int) -> dict:
        """Delete an attachment.

        Args:
            task_id: Task ID
            attachment_id: Attachment ID

        Returns:
            Empty dict on success
        """
        return self._request("DELETE", f"/api/v1/tasks/{task_id}/attachments/{attachment_id}")

    # =========================================================================
    # Notifications API (for @eis polling)
    # =========================================================================

    def get_notifications(self, page: int = 1, per_page: int = 50) -> list[dict]:
        """Get notifications for the bot user.

        When users mention @eis in a task or comment, Vikunja creates a
        notification. This allows us to poll for @eis mentions without
        processing every task/comment (much more efficient than webhooks).

        Args:
            page: Page number (1-indexed)
            per_page: Items per page (max 50)

        Returns:
            List of notification objects from Vikunja API
        """
        return self._request(
            "GET",
            "/api/v1/notifications",
            params={"page": page, "per_page": per_page}
        )

    def mark_notification_read(self, notification_id: int) -> dict:
        """Mark a notification as read.

        Args:
            notification_id: Notification ID to mark as read

        Returns:
            Updated notification object
        """
        return self._request(
            "POST",
            f"/api/v1/notifications/{notification_id}/read"
        )

    def mark_all_notifications_read(self) -> dict:
        """Mark all notifications as read.

        Returns:
            Empty dict on success
        """
        return self._request("POST", "/api/v1/notifications/read")

    def get_projects(self) -> list[dict]:
        """Get all projects accessible to the bot user.

        Returns:
            List of project dicts
        """
        return self._request("GET", "/api/v1/projects")

    def create_task(self, project_id: int, title: str, description: str = "") -> dict:
        """Create a new task in a project.

        Args:
            project_id: Project ID to create task in
            title: Task title
            description: Task description (optional)

        Returns:
            Created task object
        """
        return self._request(
            "PUT",
            f"/api/v1/projects/{project_id}/tasks",
            json={"title": title, "description": description}
        )

    def get_labels(self) -> list[dict]:
        """Get all labels available to this user."""
        return self._request("GET", "/api/v1/labels")

    def get_or_create_label(self, title: str, hex_color: str = "") -> dict:
        """Get label by title, or create if not exists.

        Args:
            title: Label title (e.g., "⏳", "🤖", "💬", "❌")
            hex_color: Optional hex color (e.g., "ff0000")

        Returns:
            Label object with id, title, hex_color
        """
        labels = self.get_labels()
        for label in labels:
            if label.get("title") == title:
                return label

        # Create new label
        payload = {"title": title}
        if hex_color:
            payload["hex_color"] = hex_color
        return self._request("PUT", "/api/v1/labels", json=payload)

    def add_label_to_task(self, task_id: int, label_id: int) -> dict:
        """Add a label to a task.

        Args:
            task_id: Task ID
            label_id: Label ID to add

        Returns:
            Updated label-task relation
        """
        return self._request(
            "PUT",
            f"/api/v1/tasks/{task_id}/labels",
            json={"label_id": label_id}
        )

    def remove_label_from_task(self, task_id: int, label_id: int) -> dict:
        """Remove a label from a task.

        Args:
            task_id: Task ID
            label_id: Label ID to remove

        Returns:
            Empty dict on success
        """
        return self._request(
            "DELETE",
            f"/api/v1/tasks/{task_id}/labels/{label_id}"
        )

    def get_task_labels(self, task_id: int) -> list[dict]:
        """Get all labels on a task.

        Args:
            task_id: Task ID

        Returns:
            List of label objects
        """
        task = self.get_task(task_id)
        return task.get("labels", []) or []

    def get_project(self, project_id: int) -> dict:
        """Get a project by ID.

        Args:
            project_id: Project ID

        Returns:
            Project object
        """
        return self._request("GET", f"/api/v1/projects/{project_id}")

    def get_bot_user(self) -> dict:
        """Get the Vikunja user info for the bot (auto-discover).

        Returns:
            User object with id, username, email, etc.
        """
        return self._request("GET", "/api/v1/user")

    def get_bot_user_id(self) -> int:
        """Get the Vikunja user ID for the bot.

        Returns:
            User ID (integer)
        """
        if not hasattr(self, '_bot_user_id'):
            user = self.get_bot_user()
            self._bot_user_id = user["id"]
        return self._bot_user_id

    def share_project_with_user(self, project_id: int, user_id: int, right: int = 1) -> dict:
        """Share a project with a user.

        Args:
            project_id: Project to share
            user_id: Vikunja user ID to add
            right: Permission level (0=read, 1=read/write, 2=admin)

        Returns:
            API response
        """
        return self._request(
            "PUT",
            f"/api/v1/projects/{project_id}/users",
            json={"user_id": user_id, "right": right}
        )

    def add_bot_to_project(self, project_id: int, right: int = 1) -> dict:
        """Add the bot (@eis) to a project.

        Convenience method that auto-discovers bot user ID.

        Args:
            project_id: Project to add bot to
            right: Permission level (0=read, 1=read/write, 2=admin)

        Returns:
            API response
        """
        bot_id = self.get_bot_user_id()
        return self.share_project_with_user(project_id, bot_id, right)

    # -------------------------------------------------------------------------
    # Link Shares (anonymous access for people without Vikunja accounts)
    # Bead: solutions-ekim
    # -------------------------------------------------------------------------

    def get_link_shares(self, project_id: int) -> list[dict]:
        """Get all link shares for a project.

        Args:
            project_id: Project ID

        Returns:
            List of link share objects with hash, right, sharing_type, etc.
        """
        result = self._request("GET", f"/api/v1/projects/{project_id}/shares")
        return result if isinstance(result, list) else []

    def create_link_share(
        self,
        project_id: int,
        right: int = 0,
        password: str = "",
        sharing_type: int = 0,
    ) -> dict:
        """Create a new link share for a project.

        Args:
            project_id: Project ID to share
            right: Permission level (0=read, 1=read/write, 2=admin)
            password: Optional password protection
            sharing_type: 0=without password, 1=with password

        Returns:
            Link share object with 'hash' field for building URLs
        """
        data = {"right": right}
        if password:
            data["password"] = password
            data["sharing_type"] = 1
        else:
            data["sharing_type"] = sharing_type

        return self._request("PUT", f"/api/v1/projects/{project_id}/shares", json=data)

    def delete_link_share(self, project_id: int, share_id: int) -> dict:
        """Delete a link share.

        Args:
            project_id: Project ID
            share_id: Share ID to delete

        Returns:
            API response
        """
        return self._request("DELETE", f"/api/v1/projects/{project_id}/shares/{share_id}")

    def get_project_views(self, project_id: int) -> list[dict]:
        """Get all views for a project.

        Args:
            project_id: Project ID

        Returns:
            List of view objects with id, title, view_kind, etc.
        """
        result = self._request("GET", f"/api/v1/projects/{project_id}/views")
        return result if isinstance(result, list) else []

    def get_project_tasks(self, project_id: int) -> list[dict]:
        """Get all tasks in a project.

        Args:
            project_id: Project ID

        Returns:
            List of task objects
        """
        # Get project with tasks
        return self._request("GET", f"/api/v1/projects/{project_id}/tasks")
