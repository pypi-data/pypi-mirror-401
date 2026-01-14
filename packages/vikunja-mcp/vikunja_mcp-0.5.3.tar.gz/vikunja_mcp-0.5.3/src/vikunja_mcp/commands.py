"""
Matrix Bot Commands - Clean rewrite using PostgreSQL only.

This module contains the rewritten command handlers for the Matrix bot.
Each command is a standalone function that returns a response dict.

Key design decisions:
- Uses context.py for instance/project context management
- Uses vikunja_client.py for Vikunja API calls
- No MCP, no YAML, no server.py dependencies
- Simple, testable, focused

Bead: solutions-lt0f.5, solutions-lt0f.6, solutions-lt0f.7, solutions-lt0f.8
"""

import logging
from typing import Any, Optional
from datetime import date

from .context import (
    get_user_context,
    get_project_context,
    set_project_context,
    clear_project_context,
    switch_instance,
    UserContext,
)
from .vikunja_client import VikunjaClient, VikunjaAPIError, Task
from .token_broker import get_user_instances, get_user_active_instance, AuthRequired

logger = logging.getLogger(__name__)


def _format_context(ctx: UserContext) -> str:
    """Format user context for display."""
    parts = []
    if ctx.active_instance:
        parts.append(f"Instance: **{ctx.active_instance}**")
    else:
        parts.append("Instance: _(default)_")

    if ctx.project:
        parts.append(f"Project: **{ctx.project.project_name or ctx.project.project_id}**")
    else:
        parts.append("Project: All")

    return " | ".join(parts)


def _format_tasks(tasks: list[Task], title: str) -> str:
    """Format task list for display."""
    if not tasks:
        return f"**{title}**\n\n✨ No tasks found."

    lines = [f"**{title}** ({len(tasks)} task{'s' if len(tasks) != 1 else ''})", ""]

    for task in tasks[:20]:  # Limit to 20 tasks
        priority_marker = "🔥 " if task.priority >= 4 else "⚡ " if task.priority >= 3 else ""
        due_str = ""
        if task.due_date:
            due_str = f" (due {task.due_date.strftime('%m/%d')})"
        lines.append(f"- {priority_marker}{task.title}{due_str}")

    if len(tasks) > 20:
        lines.append(f"\n_...and {len(tasks) - 20} more_")

    return "\n".join(lines)


# =============================================================================
# !switch - Switch active Vikunja instance
# =============================================================================


def handle_switch(args: str, user_id: str) -> dict[str, Any]:
    """Handle !switch command - switch active Vikunja instance.

    Usage:
        !switch - Show current instance and available options
        !switch personal - Switch to 'personal' instance
        !switch clear - Clear instance preference (use default)

    When switching instances, project context is automatically restored
    for the new instance (if previously set).
    """
    args = args.strip().lower()
    instances = get_user_instances(user_id)

    # No args - show current instance and available options
    if not args:
        current = get_user_active_instance(user_id)

        if not instances:
            return {
                "success": True,
                "response": "No Vikunja instances connected.\n\nUse `!vik <token>` to connect.",
                "tool": "switch",
                "needs_llm": False,
                "eco_mode": True,
            }

        lines = ["**Instance Management**", ""]

        if current:
            lines.append(f"Active instance: **{current}**")
            ctx = get_user_context(user_id)
            if ctx.project:
                lines.append(f"Active project: **{ctx.project.project_name}**")
        else:
            lines.append("Active instance: _(default)_")

        lines.append("")
        lines.append("**Your instances:**")
        for name in instances:
            marker = " *(active)*" if name == current else ""
            lines.append(f"- `{name}`{marker}")

        lines.append("")
        lines.append("Switch: `!switch <name>`")

        return {
            "success": True,
            "response": "\n".join(lines),
            "tool": "switch",
            "needs_llm": False,
            "eco_mode": True,
        }

    # Clear command - not really needed with per-instance context, but keep for compat
    if args == "clear":
        return {
            "success": True,
            "response": "ℹ️ Use `!switch <instance>` to switch between instances.",
            "tool": "switch",
            "needs_llm": False,
            "eco_mode": True,
        }

    # Switch to specified instance
    if args not in instances:
        instance_list = ", ".join(f"`{i}`" for i in instances)
        return {
            "success": False,
            "response": f"❌ Instance '{args}' not found.\n\nAvailable: {instance_list}",
            "tool": None,
            "needs_llm": False,
        }

    # Switch instance (this also restores project context)
    ctx = switch_instance(user_id, args)

    lines = [f"✅ Switched to **{args}**"]
    if ctx.project:
        lines.append(f"Project context restored: **{ctx.project.project_name}**")
    lines.append("")
    lines.append(_format_context(ctx))

    return {
        "success": True,
        "response": "\n".join(lines),
        "tool": "switch",
        "needs_llm": False,
        "eco_mode": True,
    }


# =============================================================================
# !project - Set or show active project context
# =============================================================================


def handle_project(args: str, user_id: str) -> dict[str, Any]:
    """Handle !project command - set or show active project context.

    Usage:
        !project - Show current project
        !project Kitchen - Set active project to Kitchen (fuzzy match)
        !project clear - Clear active project (query all projects)

    Project context is per-instance: switching instances restores that
    instance's project context.
    """
    args = args.strip()
    ctx = get_user_context(user_id)

    if not ctx.active_instance:
        return {
            "success": False,
            "response": "❌ No Vikunja instance connected.\n\nUse `!vik <token>` to connect.",
            "tool": None,
            "needs_llm": False,
        }

    # No args - show current project
    if not args:
        if ctx.project:
            return {
                "success": True,
                "response": (
                    f"**Active project:** {ctx.project.project_name}\n\n"
                    f"{_format_context(ctx)}\n\n"
                    "Use `!project clear` to query all projects."
                ),
                "tool": "project",
                "needs_llm": False,
                "eco_mode": True,
            }
        else:
            return {
                "success": True,
                "response": (
                    "No active project set. Commands query all projects.\n\n"
                    f"{_format_context(ctx)}\n\n"
                    "Use `!project <name>` to focus on a specific project."
                ),
                "tool": "project",
                "needs_llm": False,
                "eco_mode": True,
            }

    # Clear command
    if args.lower() == "clear":
        clear_project_context(user_id, ctx.active_instance)
        ctx = get_user_context(user_id)  # Refresh
        return {
            "success": True,
            "response": f"✅ Project context cleared.\n\n{_format_context(ctx)}",
            "tool": "project",
            "needs_llm": False,
            "eco_mode": True,
        }

    # Fuzzy match project name
    try:
        client = VikunjaClient(user_id, ctx.active_instance)
        project = client.find_project_by_name(args)

        if not project:
            # Get list of projects for suggestions
            projects = client.get_projects()
            if not projects:
                return {
                    "success": False,
                    "response": "No projects found. Create a project in Vikunja first.",
                    "tool": None,
                    "needs_llm": False,
                }

            project_list = "\n".join(f"- {p.title}" for p in projects[:10])
            return {
                "success": False,
                "response": f"No project found matching '{args}'.\n\n**Available:**\n{project_list}",
                "tool": None,
                "needs_llm": False,
            }

        # Set the project context
        set_project_context(user_id, ctx.active_instance, project.id, project.title)
        ctx = get_user_context(user_id)  # Refresh

        return {
            "success": True,
            "response": f"✅ Active project: **{project.title}**\n\n{_format_context(ctx)}",
            "tool": "project",
            "needs_llm": False,
            "eco_mode": True,
        }

    except AuthRequired as e:
        return {
            "success": False,
            "response": f"❌ {e}",
            "tool": None,
            "needs_llm": False,
        }
    except VikunjaAPIError as e:
        logger.exception("Error in !project")
        return {
            "success": False,
            "response": f"❌ API error: {e}",
            "tool": None,
            "needs_llm": False,
        }
    except Exception as e:
        logger.exception("Error in !project")
        return {
            "success": False,
            "response": f"❌ Error: {e}",
            "tool": None,
            "needs_llm": False,
        }


# =============================================================================
# !now - Tasks due today
# =============================================================================


def handle_now(user_id: str) -> dict[str, Any]:
    """Handle !now command - show tasks due today.

    Uses the user's active instance and project context.
    """
    ctx = get_user_context(user_id)

    if not ctx.active_instance:
        return {
            "success": False,
            "response": "❌ No Vikunja instance connected.\n\nUse `!vik <token>` to connect.",
            "tool": None,
            "needs_llm": False,
        }

    try:
        client = VikunjaClient(user_id, ctx.active_instance)
        project_id = ctx.project.project_id if ctx.project else None
        tasks = client.get_tasks_due_today(project_id=project_id)

        title = "Due Today"
        if ctx.project:
            title = f"Due Today ({ctx.project.project_name})"

        response = _format_tasks(tasks, title)
        response += f"\n\n_{_format_context(ctx)}_"

        return {
            "success": True,
            "response": response,
            "tool": "now",
            "needs_llm": False,
            "eco_mode": True,
        }

    except AuthRequired as e:
        return {
            "success": False,
            "response": f"❌ {e}",
            "tool": None,
            "needs_llm": False,
        }
    except VikunjaAPIError as e:
        logger.exception("Error in !now")
        return {
            "success": False,
            "response": f"❌ API error: {e}",
            "tool": None,
            "needs_llm": False,
        }
    except Exception as e:
        logger.exception("Error in !now")
        return {
            "success": False,
            "response": f"❌ Error: {e}",
            "tool": None,
            "needs_llm": False,
        }


# =============================================================================
# !week - Tasks due this week
# =============================================================================


def handle_week(user_id: str) -> dict[str, Any]:
    """Handle !week command - show tasks due this week.

    Uses the user's active instance and project context.
    """
    ctx = get_user_context(user_id)

    if not ctx.active_instance:
        return {
            "success": False,
            "response": "❌ No Vikunja instance connected.\n\nUse `!vik <token>` to connect.",
            "tool": None,
            "needs_llm": False,
        }

    try:
        client = VikunjaClient(user_id, ctx.active_instance)
        project_id = ctx.project.project_id if ctx.project else None
        tasks = client.get_tasks_due_this_week(project_id=project_id)

        title = "Due This Week"
        if ctx.project:
            title = f"Due This Week ({ctx.project.project_name})"

        response = _format_tasks(tasks, title)
        response += f"\n\n_{_format_context(ctx)}_"

        return {
            "success": True,
            "response": response,
            "tool": "week",
            "needs_llm": False,
            "eco_mode": True,
        }

    except AuthRequired as e:
        return {
            "success": False,
            "response": f"❌ {e}",
            "tool": None,
            "needs_llm": False,
        }
    except VikunjaAPIError as e:
        logger.exception("Error in !week")
        return {
            "success": False,
            "response": f"❌ API error: {e}",
            "tool": None,
            "needs_llm": False,
        }
    except Exception as e:
        logger.exception("Error in !week")
        return {
            "success": False,
            "response": f"❌ Error: {e}",
            "tool": None,
            "needs_llm": False,
        }


# =============================================================================
# !clear - Clear project context
# =============================================================================


def handle_clear(user_id: str) -> dict[str, Any]:
    """Handle !clear command - clear project context for current instance.

    Clears the project binding so filter commands like !now and !week
    will show tasks from ALL projects.
    """
    ctx = get_user_context(user_id)

    if not ctx.active_instance:
        return {
            "success": True,
            "response": "ℹ️ No Vikunja instance connected.\n\nUse `!vik <token>` to connect.",
            "tool": "clear",
            "needs_llm": False,
            "eco_mode": True,
        }

    # Check if there was a project set
    had_project = ctx.project is not None

    if had_project:
        clear_project_context(user_id, ctx.active_instance)
        ctx = get_user_context(user_id)  # Refresh
        return {
            "success": True,
            "response": f"✅ Project context cleared.\n\nFilter commands will now show tasks from **all projects**.\n\n{_format_context(ctx)}",
            "tool": "clear",
            "needs_llm": False,
            "eco_mode": True,
        }
    else:
        return {
            "success": True,
            "response": f"ℹ️ No project was set.\n\nYou can set a project with `!project <name>`.\n\n{_format_context(ctx)}",
            "tool": "clear",
            "needs_llm": False,
            "eco_mode": True,
        }


# =============================================================================
# !p - List projects or tasks in a project
# =============================================================================


def handle_p(args: str, user_id: str) -> dict[str, Any]:
    """Handle !p command - list projects or tasks in a project.

    Usage:
        !p - List all projects
        !p inbox - List tasks in project matching "inbox" (fuzzy)
        !p kit - Fuzzy matches "Kitchen"
    """
    args = args.strip()
    ctx = get_user_context(user_id)

    if not ctx.active_instance:
        return {
            "success": False,
            "response": "❌ No Vikunja instance connected.\n\nUse `!vik <token>` to connect.",
            "tool": None,
            "needs_llm": False,
        }

    try:
        client = VikunjaClient(user_id, ctx.active_instance)

        # No args - list all projects
        if not args:
            projects = client.get_projects()
            if not projects:
                return {
                    "success": True,
                    "response": "No projects found.",
                    "tool": "p",
                    "needs_llm": False,
                    "eco_mode": True,
                }

            lines = [f"**Projects** ({len(projects)})"]
            for p in projects[:25]:
                lines.append(f"- {p.title} `#{p.id}`")
            if len(projects) > 25:
                lines.append(f"_...and {len(projects) - 25} more_")

            return {
                "success": True,
                "response": "\n".join(lines),
                "tool": "p",
                "needs_llm": False,
                "eco_mode": True,
            }

        # With args - fuzzy match project and list its tasks
        project = client.find_project_by_name(args)
        if not project:
            projects = client.get_projects()
            project_list = ", ".join(p.title for p in projects[:10])
            return {
                "success": False,
                "response": f"No project matching '{args}'.\n\nAvailable: {project_list}",
                "tool": None,
                "needs_llm": False,
            }

        # Get tasks in this project
        tasks = client.get_tasks(project_id=project.id, filter_by="done = false")

        if not tasks:
            return {
                "success": True,
                "response": f"**{project.title}** - No open tasks",
                "tool": "p",
                "needs_llm": False,
                "eco_mode": True,
            }

        response = _format_tasks(tasks, project.title)
        last_task_id = tasks[0].id if len(tasks) == 1 else None

        return {
            "success": True,
            "response": response,
            "tool": "p",
            "needs_llm": False,
            "eco_mode": True,
            "last_task_id": last_task_id,
        }

    except AuthRequired as e:
        return {
            "success": False,
            "response": f"❌ {e}",
            "tool": None,
            "needs_llm": False,
        }
    except VikunjaAPIError as e:
        logger.exception("Error in !p")
        return {
            "success": False,
            "response": f"❌ API error: {e}",
            "tool": None,
            "needs_llm": False,
        }
    except Exception as e:
        logger.exception("Error in !p")
        return {
            "success": False,
            "response": f"❌ Error: {e}",
            "tool": None,
            "needs_llm": False,
        }


# =============================================================================
# !t - Search/list tasks
# =============================================================================


def handle_t(args: str, user_id: str) -> dict[str, Any]:
    """Handle !t command - search or list tasks.

    Usage:
        !t - List all open tasks (in current project context if set)
        !t dentist - Search tasks matching "dentist"
        !t /done - Include completed tasks
    """
    args = args.strip()
    ctx = get_user_context(user_id)

    if not ctx.active_instance:
        return {
            "success": False,
            "response": "❌ No Vikunja instance connected.\n\nUse `!vik <token>` to connect.",
            "tool": None,
            "needs_llm": False,
        }

    try:
        client = VikunjaClient(user_id, ctx.active_instance)
        project_id = ctx.project.project_id if ctx.project else None

        # Check for flags
        include_done = "/done" in args
        args = args.replace("/done", "").strip()

        # Search or list tasks
        if args:
            tasks = client.search_tasks(args, project_id=project_id, include_done=include_done)
            title = f"Tasks matching '{args}'"
        else:
            filter_by = None if include_done else "done = false"
            tasks = client.get_tasks(project_id=project_id, filter_by=filter_by)
            title = "Open Tasks"

        if ctx.project:
            title = f"{title} ({ctx.project.project_name})"

        if not tasks:
            return {
                "success": True,
                "response": f"**{title}**\n\n✨ No tasks found.",
                "tool": "t",
                "needs_llm": False,
                "eco_mode": True,
            }

        response = _format_tasks(tasks, title)
        response += f"\n\n_{_format_context(ctx)}_"

        # Set last_task_id if only one result
        last_task_id = tasks[0].id if len(tasks) == 1 else None

        return {
            "success": True,
            "response": response,
            "tool": "t",
            "needs_llm": False,
            "eco_mode": True,
            "last_task_id": last_task_id,
        }

    except AuthRequired as e:
        return {
            "success": False,
            "response": f"❌ {e}",
            "tool": None,
            "needs_llm": False,
        }
    except VikunjaAPIError as e:
        logger.exception("Error in !t")
        return {
            "success": False,
            "response": f"❌ API error: {e}",
            "tool": None,
            "needs_llm": False,
        }
    except Exception as e:
        logger.exception("Error in !t")
        return {
            "success": False,
            "response": f"❌ Error: {e}",
            "tool": None,
            "needs_llm": False,
        }
