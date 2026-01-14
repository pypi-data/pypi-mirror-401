"""
User Context Management - Instance and project context for Matrix bot commands.

This module provides context management for the Matrix bot rewrite (solutions-lt0f):
- Active instance: Which Vikunja instance the user is working with
- Project context: Which project to filter tasks by (per-instance)

Key design decisions:
- PostgreSQL is source of truth (no YAML, no MCP state)
- Instance context is per-user (stored in user_preferences.active_instance)
- Project context is per-instance (stored in user_project_context table)
- Switching instances restores that instance's project context

Bead: solutions-lt0f.2
"""

import logging
from dataclasses import dataclass
from typing import Optional

from .token_broker import get_db, get_user_active_instance, set_user_active_instance

logger = logging.getLogger(__name__)


@dataclass
class ProjectContext:
    """Project context for a specific Vikunja instance."""
    project_id: int
    project_name: Optional[str] = None


@dataclass
class UserContext:
    """Complete user context for bot commands."""
    user_id: str
    active_instance: Optional[str] = None
    project: Optional[ProjectContext] = None
    last_task_id: Optional[int] = None


# In-memory cache for last_task_id (doesn't need persistence)
_last_task_cache: dict[str, int] = {}


def get_project_context(user_id: str, instance_name: str) -> Optional[ProjectContext]:
    """Get project context for a specific instance.

    Args:
        user_id: Matrix or Slack user ID
        instance_name: Vikunja instance name

    Returns:
        ProjectContext if set, None otherwise
    """
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT project_id, project_name
                    FROM user_project_context
                    WHERE user_id = %s AND instance_name = %s
                    """,
                    (user_id, instance_name)
                )
                row = cur.fetchone()
                if row:
                    return ProjectContext(project_id=row[0], project_name=row[1])
                return None
    except Exception as e:
        logger.error(f"Error getting project context for {user_id}/{instance_name}: {e}")
        return None


def set_project_context(
    user_id: str,
    instance_name: str,
    project_id: int,
    project_name: Optional[str] = None
) -> None:
    """Set project context for a specific instance.

    Args:
        user_id: Matrix or Slack user ID
        instance_name: Vikunja instance name
        project_id: Vikunja project ID
        project_name: Project name for display (optional)
    """
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO user_project_context (user_id, instance_name, project_id, project_name)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (user_id, instance_name) DO UPDATE
                    SET project_id = %s, project_name = %s, set_at = NOW()
                    """,
                    (user_id, instance_name, project_id, project_name, project_id, project_name)
                )
                conn.commit()
                logger.info(f"Set project context: {user_id}/{instance_name} -> {project_id} ({project_name})")
    except Exception as e:
        logger.error(f"Error setting project context for {user_id}/{instance_name}: {e}")
        raise


def clear_project_context(user_id: str, instance_name: str) -> None:
    """Clear project context for a specific instance.

    Args:
        user_id: Matrix or Slack user ID
        instance_name: Vikunja instance name
    """
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    DELETE FROM user_project_context
                    WHERE user_id = %s AND instance_name = %s
                    """,
                    (user_id, instance_name)
                )
                conn.commit()
                logger.info(f"Cleared project context for {user_id}/{instance_name}")
    except Exception as e:
        logger.error(f"Error clearing project context for {user_id}/{instance_name}: {e}")
        raise


def get_last_task_id(user_id: str) -> Optional[int]:
    """Get the last task ID for a user (for ^ commands)."""
    return _last_task_cache.get(user_id)


def set_last_task_id(user_id: str, task_id: Optional[int]) -> None:
    """Set the last task ID for a user (for ^ commands)."""
    if task_id is not None:
        _last_task_cache[user_id] = task_id
    elif user_id in _last_task_cache:
        del _last_task_cache[user_id]


def get_user_context(user_id: str) -> UserContext:
    """Get complete user context (instance + project + last task).

    This is the main entry point for bot commands. Returns the user's
    active instance and the project context for that instance.

    Args:
        user_id: Matrix or Slack user ID

    Returns:
        UserContext with active instance, project, and last_task_id (if set)
    """
    active_instance = get_user_active_instance(user_id)

    project = None
    if active_instance:
        project = get_project_context(user_id, active_instance)

    return UserContext(
        user_id=user_id,
        active_instance=active_instance,
        project=project,
        last_task_id=get_last_task_id(user_id)
    )


def switch_instance(user_id: str, instance_name: str) -> UserContext:
    """Switch user's active instance and restore project context.

    When switching instances:
    1. Set the new active instance
    2. Load project context for that instance (if any)

    Args:
        user_id: Matrix or Slack user ID
        instance_name: Instance name to switch to

    Returns:
        Updated UserContext with new instance and its project context
    """
    # Set the new active instance
    set_user_active_instance(user_id, instance_name)

    # Load project context for the new instance
    project = get_project_context(user_id, instance_name)

    return UserContext(
        user_id=user_id,
        active_instance=instance_name,
        project=project
    )
