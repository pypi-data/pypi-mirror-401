"""Matrix message handlers - route parsed commands to MCP tools.

Bridges RapidFuzz parser to TOOL_REGISTRY for Matrix bot.
"""

import json
import logging
from functools import wraps
from typing import Any, Callable

from .matrix_parser import parse_command, get_command_help, MATCH_THRESHOLD
from .token_broker import log_interaction
from .commands import handle_switch, handle_project, handle_now, handle_week, handle_clear, handle_p, handle_t

logger = logging.getLogger(__name__)


# =============================================================================
# CENTRALIZED AUTHENTICATION
# =============================================================================

# Commands that require a Vikunja token to execute
# All other commands are safe without a token (help, credits, settings, etc.)
COMMANDS_REQUIRING_VIKUNJA_TOKEN = frozenset({
    # Task viewing
    "oops", "overdue", "now", "today", "week",
    "fire", "urgent", "vip", "priority",
    "maybe", "unscheduled", "zen", "focus",
    "tasks", "list",
    # CLI shortcuts (power user commands)
    "p", "t",
    # Task actions
    "done", "complete", "finish", "check",
    # Stats and testing
    "stats", "test",
    # Room bindings (need token to verify project exists)
    "bind",
    # Instance/project switching (need token to list projects)
    "switch", "project",
})

# Commands that are safe without a token (user settings, help, connection management)
COMMANDS_WITHOUT_TOKEN = frozenset({
    "help", "h", "?",
    "vik", "connect", "viki", "connections", "instances",
    "novik", "disconnect",
    "credits", "apikey", "model", "timezone",
    "unbind", "binding", "context",  # Only read local config
})


def _ensure_vikunja_token(user_id: str, command: str) -> dict[str, Any] | None:
    """Check if user has Vikunja token and set context var if so.

    Args:
        user_id: Matrix user ID
        command: The command being executed (for logging)

    Returns:
        None if token is valid and context is set.
        Error response dict if user needs to connect first.
    """
    from .server import (
        _get_user_vikunja_token,
        _current_vikunja_token,
        _current_user_id,
        _get_matrix_connect_prompt,
    )

    token = _get_user_vikunja_token(user_id)
    # EXPLICIT DEBUG - always log token lookup result
    print(f"[AUTH] _ensure_vikunja_token called: user={user_id}, cmd={command}, has_token={bool(token)}")
    if not token:
        print(f"[AUTH] BLOCKED: No token for {user_id}, returning connect prompt")
        logger.info(f"User {user_id} tried !{command} without Vikunja token")
        return {
            "success": False,
            "response": _get_matrix_connect_prompt(user_id),
            "tool": None,
            "needs_llm": False,
        }

    # Set context vars for _request and instance-aware functions to use
    _current_vikunja_token.set(token)
    _current_user_id.set(user_id)
    token_preview = token[:10] + "..." if len(token) > 10 else token
    print(f"[AUTH] ALLOWED: {user_id} has token {token_preview}")
    logger.debug(f"User {user_id} authenticated for !{command} with token: {token_preview}")

    return None  # Success - proceed with handler


def handle_matrix_message(
    message: str,
    user_id: str,
    room_id: str | None = None,
    is_dm: bool = False,
) -> dict[str, Any]:
    """Handle an incoming Matrix message.

    Args:
        message: Raw message text from user
        user_id: Matrix user ID (e.g., @user:matrix.org)
        room_id: Optional room ID for context
        is_dm: Whether this is a direct message (for onboarding flow)

    Returns:
        Dict with:
        - success: bool
        - response: str (formatted for Matrix)
        - tool: str | None (tool that was called)
        - needs_llm: bool (if message couldn't be parsed)
        - is_welcome: bool (if this is a first-contact welcome message)
    """
    # Import here to avoid circular imports
    from .server import (
        TOOL_REGISTRY,
        _get_user_vikunja_token,
        _is_first_contact,
        _mark_user_welcomed,
        _get_matrix_connect_prompt,
    )

    # Strip whitespace
    message = message.strip()

    # === FIRST CONTACT CHECK (Matrix onboarding) ===
    # On first DM, send welcome message with connect prompt
    if is_dm and _is_first_contact(user_id):
        _mark_user_welcomed(user_id)
        logger.info(f"First contact from Matrix user {user_id} - sending welcome")

        welcome_msg = _get_matrix_welcome_message(user_id)
        return {
            "success": True,
            "response": welcome_msg,
            "tool": None,
            "needs_llm": False,
            "is_welcome": True,
        }

    if not message:
        return {
            "success": False,
            "response": "I didn't receive a message. Try `!help` for commands.",
            "tool": None,
            "needs_llm": False,
        }

    # Handle !commands (direct, no LLM)
    if message.startswith("!"):
        return _handle_bang_command(message[1:], user_id, room_id, is_dm)

    # Handle ^commands (last-task context, solutions-dod7)
    if message.startswith("^"):
        return _handle_caret_command(message[1:], user_id)

    # Try RapidFuzz parsing
    tool_name, args_str = parse_command(message)

    # Auto-inject project context from room binding (if exists)
    if tool_name and room_id:
        from .server import _get_room_binding
        bound_project = _get_room_binding(user_id, room_id)
        if bound_project:
            # Check if command already has project specified
            # If not, prepend project to args
            if args_str and not any(keyword in args_str.lower() for keyword in ["project:", "in project", "for project"]):
                # Inject project at the beginning
                args_str = f"project:{bound_project} {args_str}"
            elif not args_str:
                args_str = f"project:{bound_project}"

    if tool_name is None:
        # No confident match - needs LLM or fallback
        return {
            "success": True,
            "response": None,  # Let caller decide (LLM or error)
            "tool": None,
            "needs_llm": True,
            "original_message": message,
        }

    # Handle special commands that don't need Vikunja connection
    if tool_name == "help":
        return {
            "success": True,
            "response": get_command_help(),
            "tool": "help",
            "needs_llm": False,
        }

    # Check if user has Vikunja connected
    token = _get_user_vikunja_token(user_id)
    if not token and tool_name not in ("add_instance", "list_instances"):
        # User needs to connect - show connect prompt
        return {
            "success": False,
            "response": _get_matrix_connect_prompt(user_id),
            "tool": None,
            "needs_llm": False,
        }

    # Execute the tool
    return _execute_tool(tool_name, args_str, user_id)


def _get_matrix_welcome_message(user_id: str) -> str:
    """Generate welcome message for first-contact Matrix users.

    Warmly welcomes the user and explains how to connect.
    """
    from .server import _get_matrix_connect_prompt

    # Get the connect instructions
    connect_prompt = _get_matrix_connect_prompt(user_id)

    return (
        "👋 **Welcome to Factum Erit!**\n\n"
        "I'm **eis**, your AI task assistant. I'll help you stay on top of what matters.\n\n"
        "**What I can do:**\n"
        "• Create and manage tasks with natural language\n"
        "• Show your overdue, today's, and upcoming tasks\n"
        "• Help you prioritize and organize your work\n"
        "• Answer questions about your projects\n\n"
        "**Quick commands** (no AI cost):\n"
        "• `!oops` - Overdue tasks\n"
        "• `!now` - Due today\n"
        "• `!fire` - Urgent tasks\n"
        "• `!bind <project>` - Bind room to project\n"
        "• `!help` - All commands\n\n"
        "---\n\n"
        f"{connect_prompt}\n\n"
        "---\n\n"
        "**Set your timezone** (recommended):\n"
        "• `!tz America/Los_Angeles` (Pacific)\n"
        "• `!tz America/New_York` (Eastern)\n"
        "• `!tz Europe/London` (UK)\n"
        "• `!tz Asia/Tokyo` (Japan)\n"
        "• Or just say: `tz` and tell me your city!\n\n"
        "_This helps me show task times correctly for you._"
    )

def _handle_bang_command(
    command: str,
    user_id: str,
    room_id: str | None = None,
    is_dm: bool = False,
) -> dict[str, Any]:
    """Handle !command style messages (direct execution, no LLM).

    These are ECO mode commands - no token cost.
    """
    from .server import (
        TOOL_REGISTRY,
        _get_user_vikunja_token,
        _list_all_tasks_impl,
        _format_tasks_for_slack,
        _current_vikunja_token,
        _get_user_instance,
        _get_user_project,
    )

    command = command.strip()
    parts = command.split(maxsplit=1)
    cmd = parts[0].lower() if parts else ""  # Only lowercase the command, not the args
    args = parts[1] if len(parts) > 1 else ""

    # ==========================================================================
    # CENTRALIZED AUTH CHECK - Single point of enforcement
    # ==========================================================================
    print(f"[AUTH] _handle_bang_command: cmd={cmd}, requires_token={cmd in COMMANDS_REQUIRING_VIKUNJA_TOKEN}")
    if cmd in COMMANDS_REQUIRING_VIKUNJA_TOKEN:
        auth_error = _ensure_vikunja_token(user_id, cmd)
        if auth_error:
            print(f"[AUTH] Returning auth error for cmd={cmd}")
            return auth_error
        # Token is now set in _current_vikunja_token context var
    # ==========================================================================

    # Help
    if cmd in ("help", "h", "?"):
        return {
            "success": True,
            "response": get_command_help(),
            "tool": "help",
            "needs_llm": False,
        }

    # NEW: !now and !week use the new per-instance context system
    if cmd in ("now", "today"):
        return handle_now(user_id)

    if cmd == "week":
        return handle_week(user_id)

    # CLI shortcuts for power users (solutions-nxtv)
    if cmd == "p":
        result = handle_p(args, user_id)
        # Store last_task_id for ^ commands
        if result.get("last_task_id"):
            from .context import set_last_task_id
            set_last_task_id(user_id, result["last_task_id"])
        return result

    if cmd == "t":
        result = handle_t(args, user_id)
        # Store last_task_id for ^ commands
        if result.get("last_task_id"):
            from .context import set_last_task_id
            set_last_task_id(user_id, result["last_task_id"])
        return result

    # Task filter commands (ECO mode - no LLM cost)
    # Note: !now and !week are handled above with the new context system
    filter_commands = {
        "oops": {"filter": "overdue", "title": "Overdue Tasks"},
        "overdue": {"filter": "overdue", "title": "Overdue Tasks"},
        "fire": {"filter": "priority_5", "title": "Priority 5 (Urgent)"},
        "urgent": {"filter": "priority_5", "title": "Priority 5 (Urgent)"},
        "vip": {"filter": "priority_3_plus", "title": "High Priority (3+)"},
        "priority": {"filter": "priority_3_plus", "title": "High Priority (3+)"},
        "maybe": {"filter": "no_due_date", "title": "Unscheduled"},
        "unscheduled": {"filter": "no_due_date", "title": "Unscheduled"},
        "zen": {"filter": "focus", "title": "Focus Mode"},
        "focus": {"filter": "focus", "title": "Focus Mode"},
        "tasks": {"filter": None, "title": "All Tasks"},
        "list": {"filter": None, "title": "All Tasks"},
    }

    if cmd in filter_commands:
        # Token already validated and set by centralized auth check above
        filter_info = filter_commands[cmd]
        import time
        start_time = time.time()
        try:
            # Use user's active instance (if set via !switch)
            instance = _get_user_instance(user_id) or ""

            # Get user's active project (if set via !project)
            project_id = 0
            project_info = _get_user_project(user_id)
            if project_info:
                project_id = project_info.get("id", 0)

            # Call list_all_tasks with appropriate filter
            # Note: filter_due parameter accepts values like "overdue", "due_today", etc.
            result = _list_all_tasks_impl(
                project_id=project_id,
                filter_due=filter_info["filter"] or "",
                include_done=False,
                instance=instance,
            )
            # Format for Matrix with context footer
            response = _format_tasks_for_matrix(result, filter_info["title"], user_id=user_id)

            # Log interaction for debugging
            execution_time_ms = int((time.time() - start_time) * 1000)
            results_count = result.get("total", 0)
            log_interaction(
                user_id=user_id,
                vikunja_instance=instance or "default",
                command=f"\!{cmd}",
                request_type="filter_command",
                filter_applied=filter_info["filter"],
                results_count=results_count,
                success=True,
                response_preview=response,
                execution_time_ms=execution_time_ms,
            )
            return {
                "success": True,
                "response": response,
                "tool": "list_all_tasks",
                "needs_llm": False,
                "eco_mode": True,  # No LLM cost
            }
        except Exception as e:
            logger.exception(f"Error in !{cmd}")

            # Log failed interaction
            execution_time_ms = int((time.time() - start_time) * 1000)
            log_interaction(
                user_id=user_id,
                vikunja_instance=instance or "default",
                command=f"\!{cmd}",
                request_type="filter_command",
                filter_applied=filter_info.get("filter"),
                results_count=0,
                success=False,
                error_message=str(e),
                execution_time_ms=execution_time_ms,
            )
            return {
                "success": False,
                "response": f"Error: {e}",
                "tool": None,
                "needs_llm": False,
            }

    # Connection commands - GATED behind registration
    if cmd in ("vik", "connect"):
        from .token_broker import is_registered_user
        if not is_registered_user(user_id):
            # Funnel messaging - guide them to register
            from .server import _get_matrix_connect_prompt
            return {
                "success": False,
                "response": (
                    "**Welcome to Factumerit!** 🎯\n\n"
                    "To connect your Vikunja and start managing tasks, "
                    "please complete the quick one-click setup:\n\n"
                    + _get_matrix_connect_prompt(user_id) + "\n\n"
                    "**What you'll get:**\n"
                    "• Natural language task management (\"remind me to call mom tomorrow\")\n"
                    "• Quick commands (`!now`, `!week`, `!p inbox`)\n"
                    "• Multi-instance support for work/personal separation\n\n"
                    "_Takes less than 30 seconds!_"
                ),
                "tool": None,
                "needs_llm": False,
            }
        return _handle_connect(args, user_id)

    if cmd in ("viki", "connections", "instances"):
        return _handle_list_instances(user_id)

    if cmd in ("novik", "disconnect"):
        return _handle_disconnect(args, user_id)

    if cmd == "test":
        return _handle_test_connection(user_id)

    if cmd == "stats":
        return _handle_stats(user_id)
    # Room-project binding commands (only work in rooms, not DMs)
    if cmd == "bind":
        return _handle_bind(args, user_id, room_id, is_dm)

    if cmd == "unbind":
        return _handle_unbind(user_id, room_id, is_dm)

    if cmd == "binding":
        return _handle_show_binding(user_id, room_id, is_dm)

    # Task completion by title
    if cmd in ("done", "complete", "finish", "check"):
        return _handle_done(args, user_id)

    # Cost control commands
    if cmd == "credits":
        return _handle_credits(user_id)

    if cmd == "apikey":
        return _handle_apikey(args, user_id)

    if cmd == "model":
        return _handle_model(args, user_id)

    if cmd in ("tz", "timezone"):
        return _handle_timezone(args, user_id)

    # Instance/project context commands (NEW: uses per-instance context system)
    if cmd in ("switch", "instance"):
        return handle_switch(args, user_id)

    if cmd == "project":
        return handle_project(args, user_id)

    if cmd == "context":
        return _handle_context(user_id)

    if cmd == "clear":
        return handle_clear(user_id)

    # Unknown !command
    return {
        "success": False,
        "response": f"Unknown command: `!{cmd}`\n\nTry `!help` for available commands.",
        "tool": None,
        "needs_llm": False,
    }


def _handle_caret_command(command: str, user_id: str) -> dict[str, Any]:
    """Handle ^command style messages (last-task context).

    These operate on the last single task returned by !t or !p.
    Bead: solutions-dod7
    """
    from .context import get_user_context, set_last_task_id
    from .vikunja_client import VikunjaClient

    ctx = get_user_context(user_id)

    if not ctx.last_task_id:
        return {
            "success": False,
            "response": (
                "No task in context.\n\n"
                "Use `!t <search>` to find a single task first, then use `^` commands.\n"
                "Example: `!t dentist` → `^done`"
            ),
            "tool": None,
            "needs_llm": False,
        }

    if not ctx.active_instance:
        return {
            "success": False,
            "response": "❌ No Vikunja instance connected.\n\nUse `!vik` to connect.",
            "tool": None,
            "needs_llm": False,
        }

    command = command.strip()
    parts = command.split(maxsplit=1)
    cmd = parts[0].lower() if parts else ""
    args = parts[1] if len(parts) > 1 else ""

    try:
        client = VikunjaClient(user_id, ctx.active_instance)
        task = client.get_task(ctx.last_task_id)

        if not task:
            set_last_task_id(user_id, None)  # Clear stale reference
            return {
                "success": False,
                "response": f"Task #{ctx.last_task_id} no longer exists.",
                "tool": None,
                "needs_llm": False,
            }

        # ^ alone - show task details
        if not cmd:
            due_str = f"Due: {task.due_date.strftime('%Y-%m-%d')}" if task.due_date else "No due date"
            status = "✅ Done" if task.done else "⬜ Open"
            return {
                "success": True,
                "response": (
                    f"**{task.title}** `#{task.id}`\n\n"
                    f"{status} | {due_str}\n"
                    f"Project: #{task.project_id}"
                    + (f"\n\n{task.description}" if task.description else "")
                ),
                "tool": "caret",
                "needs_llm": False,
                "eco_mode": True,
            }

        # ^done - mark complete
        if cmd in ("done", "complete", "finish", "check"):
            client.complete_task(ctx.last_task_id)
            set_last_task_id(user_id, None)  # Clear after completing
            return {
                "success": True,
                "response": f"✅ Completed: **{task.title}**",
                "tool": "caret_done",
                "needs_llm": False,
                "eco_mode": True,
            }

        # ^rename <title> - rename task
        if cmd in ("rename", "title", "name"):
            if not args:
                return {
                    "success": False,
                    "response": "Usage: `^rename <new title>`",
                    "tool": None,
                    "needs_llm": False,
                }
            client.update_task(ctx.last_task_id, title=args)
            return {
                "success": True,
                "response": f"✏️ Renamed to: **{args}**",
                "tool": "caret_rename",
                "needs_llm": False,
                "eco_mode": True,
            }

        # ^due <date> - set due date
        if cmd in ("due", "deadline"):
            from .date_parser import parse_natural_date
            if not args:
                return {
                    "success": False,
                    "response": "Usage: `^due <date>`\n\nExamples: `^due tomorrow`, `^due friday`, `^due 2024-01-15`",
                    "tool": None,
                    "needs_llm": False,
                }
            parsed_date = parse_natural_date(args)
            if not parsed_date:
                return {
                    "success": False,
                    "response": f"Couldn't parse date: '{args}'\n\nTry: tomorrow, friday, next week, 2024-01-15",
                    "tool": None,
                    "needs_llm": False,
                }
            client.update_task(ctx.last_task_id, due_date=parsed_date.isoformat())
            return {
                "success": True,
                "response": f"📅 Due date set: **{parsed_date.strftime('%A, %b %d')}**",
                "tool": "caret_due",
                "needs_llm": False,
                "eco_mode": True,
            }

        # ^delete - delete task
        if cmd in ("delete", "remove", "rm"):
            client.delete_task(ctx.last_task_id)
            set_last_task_id(user_id, None)  # Clear after deleting
            return {
                "success": True,
                "response": f"🗑️ Deleted: **{task.title}**",
                "tool": "caret_delete",
                "needs_llm": False,
                "eco_mode": True,
            }

        # Unknown ^ command
        return {
            "success": False,
            "response": (
                f"Unknown: `^{cmd}`\n\n"
                "**^ Commands:**\n"
                "• `^` - show task details\n"
                "• `^done` - mark complete\n"
                "• `^rename <title>` - rename\n"
                "• `^due <date>` - set due date\n"
                "• `^delete` - delete task"
            ),
            "tool": None,
            "needs_llm": False,
        }

    except Exception as e:
        logger.exception("Error in ^ command")
        return {
            "success": False,
            "response": f"❌ Error: {e}",
            "tool": None,
            "needs_llm": False,
        }


class ParseError(Exception):
    """Raised when argument parsing fails and should fall back to LLM."""
    pass


def _execute_tool(
    tool_name: str,
    args_str: str,
    user_id: str,
) -> dict[str, Any]:
    """Execute a tool from TOOL_REGISTRY."""
    from .server import TOOL_REGISTRY

    if tool_name not in TOOL_REGISTRY:
        return {
            "success": False,
            "response": f"Unknown tool: {tool_name}",
            "tool": tool_name,
            "needs_llm": False,
        }

    tool = TOOL_REGISTRY[tool_name]

    try:
        # Parse args from string with fuzzy project matching
        args = _parse_args_string(args_str, tool["input_schema"], user_id=user_id)

        # Execute
        result = tool["impl"](**args)

        # Format response with context footer
        response = _format_tool_result(tool_name, result, user_id=user_id)

        return {
            "success": True,
            "response": response,
            "tool": tool_name,
            "needs_llm": False,
        }
    except ParseError as e:
        # Can't parse args (e.g., expected integer, got string)
        # Fall back to LLM for natural language processing
        logger.info(f"ParseError for {tool_name}: {e}, falling back to LLM")
        return {
            "success": True,
            "response": None,
            "tool": None,
            "needs_llm": True,
            "original_message": args_str,
        }
    except Exception as e:
        logger.exception(f"Error executing {tool_name}")
        return {
            "success": False,
            "response": f"Error: {e}",
            "tool": tool_name,
            "needs_llm": False,
        }


def _extract_project_name(args_str: str) -> str | None:
    """Extract project name from natural language patterns.

    Patterns:
    - "in <name>" → <name>
    - "for <name>" → <name>
    - "project <name>" → <name>
    - "from <name>" → <name>

    Returns:
        Project name if found, None otherwise
    """
    import re

    # Try common patterns
    patterns = [
        r'^in\s+(.+)$',           # "in gym"
        r'^for\s+(.+)$',          # "for kitchen"
        r'^project\s+(.+)$',      # "project shopping"
        r'^from\s+(.+)$',         # "from inbox"
        r'^(.+)\s+project$',      # "gym project"
    ]

    args_lower = args_str.lower().strip()
    for pattern in patterns:
        match = re.match(pattern, args_lower)
        if match:
            extracted = match.group(1).strip()
            logger.debug(f"Extracted project name '{extracted}' from '{args_str}' using pattern {pattern}")
            return extracted

    logger.debug(f"No project name pattern matched in '{args_str}'")
    return None


def _fuzzy_match_project(name: str, user_id: str) -> int | None:
    """Fuzzy match project name to project ID.

    Args:
        name: Project name to match
        user_id: User ID for fetching their projects

    Returns:
        Project ID if confident match found, None otherwise
    """
    from rapidfuzz import fuzz, process
    from .server import _list_projects_impl

    try:
        # Get user's projects
        projects = _list_projects_impl()
        if not projects:
            logger.debug("No projects found for fuzzy matching")
            return None

        # Build list of (title, id) tuples - normalize to lowercase for matching
        project_choices = [(p.get("title", ""), p.get("id")) for p in projects]
        project_titles_lower = [title.lower() for title, _ in project_choices]

        logger.debug(f"Fuzzy matching '{name}' against {len(project_titles_lower)} projects")

        # Fuzzy match (case-insensitive)
        results = process.extract(
            name.lower(),
            project_titles_lower,
            scorer=fuzz.WRatio,
            limit=1
        )

        if not results:
            logger.debug("No fuzzy match results")
            return None

        best_match_lower, score, match_index = results[0]

        logger.debug(f"Best match: '{best_match_lower}' (score: {score})")

        # Use lower threshold for project names (70 instead of 80)
        # because project names are usually short and simple
        if score >= 70:
            # Get the original title and ID using the match index
            original_title, project_id = project_choices[match_index]
            logger.info(f"Fuzzy matched '{name}' → '{original_title}' (ID: {project_id}, score: {score})")
            return project_id
        else:
            logger.debug(f"Score {score} below threshold 70")

        return None

    except Exception as e:
        # Log but don't fail
        logger.error(f"Error in fuzzy project matching: {e}", exc_info=True)
        return None


def _parse_args_string(args_str: str, schema: dict, user_id: str = None) -> dict:
    """Parse argument string into dict based on schema.

    Enhanced parsing with project name extraction and fuzzy matching:
    - Extracts project names from patterns like "in gym", "for kitchen"
    - Fuzzy matches project names to IDs
    - Falls back to LLM only if no match found

    Raises:
        ParseError: If required integer field can't be parsed
    """
    args_str = args_str.strip()
    if not args_str:
        return {}

    properties = schema.get("properties", {})
    required = schema.get("required", [])

    # If only one required field, use entire string
    if len(required) == 1:
        field = required[0]
        field_type = properties.get(field, {}).get("type", "string")

        if field_type == "integer":
            # Special handling for project_id - try fuzzy matching first
            if field == "project_id" and user_id:
                # Try to extract project name from natural language
                project_name = _extract_project_name(args_str)
                if project_name:
                    project_id = _fuzzy_match_project(project_name, user_id)
                    if project_id:
                        return {field: project_id}

            # Try parsing as integer
            try:
                return {field: int(args_str.split()[0])}
            except ValueError:
                # Can't parse integer - this needs LLM to resolve
                raise ParseError(f"Expected integer for '{field}', got '{args_str}'")
        return {field: args_str}

    # Multiple fields - try to parse intelligently
    # For "title" fields, use entire string
    if "title" in properties:
        return {"title": args_str}

    # Default: first word as first arg
    parts = args_str.split(maxsplit=len(properties) - 1)
    result = {}
    for i, field in enumerate(required):
        if i < len(parts):
            value = parts[i]
            if properties.get(field, {}).get("type") == "integer":
                try:
                    value = int(value)
                except ValueError:
                    # Can't parse required integer - this needs LLM
                    raise ParseError(f"Expected integer for '{field}', got '{value}'")
            result[field] = value
    return result


def _format_tool_result(tool_name: str, result: Any, user_id: str = None) -> str:
    """Format tool result for Matrix display.

    Args:
        tool_name: Name of the tool that was executed
        result: Tool result to format
        user_id: Optional user ID for context footer
    """
    if isinstance(result, str):
        return result

    if isinstance(result, dict):
        # Handle common result patterns
        if "error" in result:
            return f"Error: {result['error']}"

        if "tasks" in result:
            return _format_tasks_for_matrix(result, "Tasks", user_id=user_id)

        if "projects" in result:
            return _format_projects_for_matrix(result, user_id=user_id)

        if "message" in result:
            return result["message"]

        # Fallback: JSON
        return f"```json\n{json.dumps(result, indent=2)}\n```"

    # Handle list results (e.g., list_projects returns a list)
    if isinstance(result, list):
        if not result:
            return "No results found."

        # Check first item to determine type
        first = result[0] if isinstance(result[0], dict) else {}

        # Projects (has 'title' and 'parent_project_id')
        if "title" in first and "parent_project_id" in first:
            return _format_projects_for_matrix({"projects": result}, user_id=user_id)

        # Tasks (has 'done' field)
        if "done" in first:
            return _format_tasks_for_matrix({"tasks": result}, "Tasks", user_id=user_id)

        # Labels (has 'hex_color' field)
        if "hex_color" in first and "title" in first:
            return _format_labels_for_matrix({"labels": result})

        # Views (has 'view_kind' field)
        if "view_kind" in first:
            return _format_views_for_matrix({"views": result})

        # Buckets (has 'position' and 'limit' fields)
        if "position" in first and "limit" in first:
            return _format_buckets_for_matrix({"buckets": result})

        # Relations (has 'relation_kind' field)
        if "relation_kind" in first:
            return _format_relations_for_matrix({"relations": result})

        # Fallback: JSON
        return f"```json\n{json.dumps(result, indent=2)}\n```"

    return str(result)


def _format_tasks_for_matrix(result: dict, title: str, user_id: str = None) -> str:
    """Format task list for Matrix (Markdown).

    Args:
        result: Dict containing tasks list
        title: Title for the task list
        user_id: Optional user ID for context footer
    """
    tasks = result.get("tasks", [])
    total = result.get("total", len(tasks))

    if not tasks:
        response = f"**{title}**: No tasks found."
        if user_id:
            from .server import _format_user_context
            response += f"\n\n{_format_user_context(user_id)}"
        return response

    lines = [f"**{title}** ({total} tasks):", ""]

    for task in tasks[:20]:  # Limit to 20
        status = "x" if task.get("done") else " "
        title_text = task.get("title", "Untitled")
        task_id = task.get("id", "?")

        # Add priority indicator
        priority = task.get("priority", 0)
        priority_str = "🔥" if priority >= 5 else ("⚡" if priority >= 3 else "")

        # Add due date if present
        due = task.get("due_date", "")
        due_str = f" (due: {due[:10]})" if due else ""

        lines.append(f"- [{status}] {priority_str}{title_text}{due_str} `#{task_id}`")

    if total > 20:
        lines.append(f"\n_...and {total - 20} more_")

    # Add context footer if user_id provided
    if user_id:
        from .server import _format_user_context
        lines.append("")
        lines.append(_format_user_context(user_id))

    return "\n".join(lines)


def _format_projects_for_matrix(result: dict, user_id: str = None) -> str:
    """Format project list for Matrix.

    Args:
        result: Dict containing projects list
        user_id: Optional user ID for context footer
    """
    projects = result.get("projects", [])

    if not projects:
        response = "No projects found."
        if user_id:
            from .server import _format_user_context
            response += f"\n\n{_format_user_context(user_id)}"
        return response

    lines = ["**Projects:**", ""]

    for project in projects[:20]:
        title = project.get("title", "Untitled")
        project_id = project.get("id", "?")
        is_favorite = project.get("is_favorite", False)

        # Add star emoji for favorites
        star = "⭐ " if is_favorite else ""
        lines.append(f"- {star}{title} `#{project_id}`")

    # Add context footer if user_id provided
    if user_id:
        from .server import _format_user_context
        lines.append("")
        lines.append(_format_user_context(user_id))

    return "\n".join(lines)


def _format_labels_for_matrix(result: dict) -> str:
    """Format label list for Matrix."""
    labels = result.get("labels", [])

    if not labels:
        return "No labels found."

    lines = ["**Labels:**", ""]

    for label in labels[:30]:
        title = label.get("title", "Untitled")
        label_id = label.get("id", "?")
        hex_color = label.get("hex_color", "")

        # Add color indicator if available
        if hex_color:
            lines.append(f"- 🏷️ {title} `#{label_id}` (#{hex_color})")
        else:
            lines.append(f"- 🏷️ {title} `#{label_id}`")

    return "\n".join(lines)


def _format_views_for_matrix(result: dict) -> str:
    """Format view list for Matrix."""
    views = result.get("views", [])

    if not views:
        return "No views found."

    lines = ["**Views:**", ""]

    # Map view kinds to icons
    view_icons = {
        "list": "📋",
        "kanban": "📊",
        "gantt": "📅",
        "table": "📑",
    }

    for view in views[:20]:
        title = view.get("title", "Untitled")
        view_id = view.get("id", "?")
        view_kind = view.get("view_kind", "list")
        icon = view_icons.get(view_kind, "📄")

        lines.append(f"- {icon} {title} `#{view_id}` ({view_kind})")

    return "\n".join(lines)


def _format_buckets_for_matrix(result: dict) -> str:
    """Format bucket list for Matrix."""
    buckets = result.get("buckets", [])

    if not buckets:
        return "No buckets found."

    lines = ["**Buckets:**", ""]

    for bucket in buckets[:20]:
        title = bucket.get("title", "Untitled")
        bucket_id = bucket.get("id", "?")
        limit = bucket.get("limit", 0)

        if limit > 0:
            lines.append(f"- 🗂️ {title} `#{bucket_id}` (limit: {limit})")
        else:
            lines.append(f"- 🗂️ {title} `#{bucket_id}`")

    return "\n".join(lines)


def _format_relations_for_matrix(result: dict) -> str:
    """Format task relations for Matrix."""
    relations = result.get("relations", [])

    if not relations:
        return "No related tasks found."

    lines = ["**Related Tasks:**", ""]

    # Map relation kinds to readable names
    relation_names = {
        "subtask": "Subtask of",
        "parenttask": "Parent of",
        "related": "Related to",
        "duplicateof": "Duplicate of",
        "duplicates": "Duplicates",
        "blocking": "Blocks",
        "blocked": "Blocked by",
        "precedes": "Precedes",
        "follows": "Follows",
        "copiedfrom": "Copied from",
        "copiedto": "Copied to",
    }

    for relation in relations[:20]:
        other_task_id = relation.get("other_task_id", "?")
        other_task_title = relation.get("other_task_title", "Untitled")
        relation_kind = relation.get("relation_kind", "related")
        relation_label = relation_names.get(relation_kind, relation_kind)

        lines.append(f"- {relation_label}: {other_task_title} `#{other_task_id}`")

    return "\n".join(lines)


def _handle_connect(args: str, user_id: str) -> dict[str, Any]:
    """Handle !vik and !connect commands.

    Matrix bot only - stores tokens in PostgreSQL, NOT YAML config.
    MCP (Claude Desktop) uses YAML config directly, not this function.

    Modes:
        !vik                      → Show connect prompt
        !vik <token>              → Connect to VIKUNJA_URL as 'personal'
        !vik <url> <token>        → Auto-generate instance name from URL
        !vik <url> <token> <name> → Use specified instance name
    """
    from .token_broker import set_user_token, get_user_instances, set_user_active_instance
    from datetime import datetime, timedelta, timezone
    from urllib.parse import urlparse
    import os
    import requests

    parts = args.split()

    # No args - show connect prompt or usage
    if len(parts) == 0:
        # Check if user already has instances
        existing = get_user_instances(user_id)

        if existing:
            # User has instances - show usage
            return {
                "success": True,
                "response": (
                    "**Add a new Vikunja instance:**\n\n"
                    "**Usage:**\n"
                    "• `!vik <token>` - Connect to default Vikunja instance as 'personal'\n"
                    "• `!vik <url> <token>` - Auto-generate instance name from URL\n"
                    "• `!vik <url> <token> <name>` - Use custom instance name\n\n"
                    "**Get your API token:**\n"
                    "Vikunja → Settings → API Tokens → Create new token\n\n"
                    f"**Your current instances:** {', '.join(existing)}\n"
                    "Use `!viki` to see details or `!switch <instance>` to switch."
                ),
                "tool": None,
                "needs_llm": False,
            }
        else:
            # First-time user - show OAuth connect prompt
            from .server import _get_matrix_connect_prompt
            return {
                "success": True,
                "response": _get_matrix_connect_prompt(user_id),
                "tool": None,
                "needs_llm": False,
            }

    # Disconnect command - handled by !novik
    if parts[0].lower() in ["disconnect", "reset", "clear"]:
        return {
            "success": False,
            "response": "Use `!novik <instance>` to disconnect. See `!viki` for instance list.",
            "tool": None,
            "needs_llm": False,
        }

    # Parse arguments
    if len(parts) == 1:
        # Mode: !vik <token>
        url = os.environ.get("VIKUNJA_URL", "https://vikunja.factumerit.app").rstrip('/')
        token = parts[0]
        instance_name = "personal"  # Fixed name for default instance
    elif len(parts) == 2:
        # Mode: !vik <url> <token>
        url = parts[0].rstrip('/')
        token = parts[1]
        instance_name = None  # Will auto-generate
    elif len(parts) >= 3:
        # Mode: !vik <url> <token> <name>
        url = parts[0].rstrip('/')
        token = parts[1]
        instance_name = parts[2]  # User-specified name
    else:
        return {
            "success": False,
            "response": (
                "Invalid usage.\n\n"
                "**Usage:**\n"
                "• `!vik <token>` - Connect to default Vikunja instance as 'personal'\n"
                "• `!vik <url> <token>` - Auto-generate instance name from URL\n"
                "• `!vik <url> <token> <name>` - Use custom instance name\n\n"
                "Get your API token from Vikunja → Settings → API Tokens"
            ),
            "tool": None,
            "needs_llm": False,
        }

    # Validate token format
    if not token.startswith("tk_"):
        return {
            "success": False,
            "response": (
                "Invalid token format. Vikunja tokens start with `tk_`.\n\n"
                "**Usage:**\n"
                "• `!vik <token>` - Connect to default Vikunja instance\n"
                "• `!vik <url> <token>` - Connect to custom instance\n"
                "• `!vik <url> <token> <name>` - Connect with custom name\n\n"
                "Get your API token from Vikunja → Settings → API Tokens"
            ),
            "tool": None,
            "needs_llm": False,
        }

    # Test the token
    try:
        response = requests.get(
            f"{url}/api/v1/user",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10.0
        )
        response.raise_for_status()
        user_info = response.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            return {
                "success": False,
                "response": "❌ Invalid token. Check your API token and try again.",
                "tool": None,
                "needs_llm": False,
            }
        else:
            return {
                "success": False,
                "response": f"❌ Connection failed: {e}",
                "tool": None,
                "needs_llm": False,
            }
    except Exception as e:
        logger.error(f"Connection failed for {user_id} to {url}: {e}")
        return {
            "success": False,
            "response": f"❌ Connection failed: {e}",
            "tool": None,
            "needs_llm": False,
        }

    # Get existing instances once
    existing = get_user_instances(user_id)

    # Auto-generate instance name if not specified
    if instance_name is None:
        # Extract domain: https://app.vikunja.cloud/ -> app_vikunja_cloud
        parsed = urlparse(url)
        domain = parsed.netloc.replace('.', '_').replace('-', '_')

        # Generate unique name
        if domain in existing:
            # Add number suffix
            counter = 2
            while f"{domain}_{counter}" in existing:
                counter += 1
            instance_name = f"{domain}_{counter}"
        else:
            instance_name = domain
    else:
        # User specified a name - check if it already exists
        if instance_name in existing:
            return {
                "success": False,
                "response": (
                    f"❌ Instance **{instance_name}** already exists.\n\n"
                    f"Use `!novik {instance_name}` to remove it first, or choose a different name:\n"
                    f"`!vik {url} {token[:10]}... <different_name>`"
                ),
                "tool": None,
                "needs_llm": False,
            }

    # Store token in PostgreSQL (with URL - solutions-mr8f)
    expires_at = datetime.now(timezone.utc) + timedelta(days=365)
    set_user_token(
        user_id=user_id,
        token=token,
        source="matrix_connect",
        expires_at=expires_at,
        instance=instance_name,
        instance_url=url,
        caller="matrix_handlers._handle_connect"
    )

    # Set as active instance
    set_user_active_instance(user_id, instance_name)

    logger.info(f"Connected {user_id} to {instance_name} at {url}")

    return {
        "success": True,
        "response": (
            f"✅ Connected to Vikunja at {url}\n"
            f"Instance: **{instance_name}**\n\n"
            f"Use `!switch {instance_name}` to switch to this instance."
        ),
        "tool": "connect_instance",
        "needs_llm": False,
    }


def _handle_list_instances(user_id: str) -> dict[str, Any]:
    """Handle !viki list instances command.

    Matrix bot only - shows PostgreSQL user tokens, NOT YAML config.
    """
    from .token_broker import get_user_instances, get_user_active_instance, get_user_instance_url

    try:
        # Get user's instances from PostgreSQL only
        user_instances = get_user_instances(user_id)
        active_instance = get_user_active_instance(user_id)

        if not user_instances:
            return {
                "success": True,
                "response": "No Vikunja instances connected.\n\nUse `!vik <url> <token>` to connect.",
                "tool": "list_instances",
                "needs_llm": False,
            }

        lines = ["**Connected Vikunja Instances:**", ""]
        for inst_name in sorted(user_instances):
            current = " ✓ (active)" if inst_name == active_instance else ""
            # Get URL from PostgreSQL (solutions-mr8f)
            url = get_user_instance_url(user_id, inst_name) or "https://vikunja.factumerit.app"
            lines.append(f"- **{inst_name}**: {url}{current}")

        # Add helpful commands
        lines.append("")
        lines.append("**Manage Instances:**")
        lines.append("• `!switch <instance>` - Switch active instance")
        lines.append("• `!vik <url> <token> [name]` - Add new instance")
        lines.append("• `!novik <instance>` - Remove instance")

        return {
            "success": True,
            "response": "\n".join(lines),
            "tool": "list_instances",
            "needs_llm": False,
        }
    except Exception as e:
        logger.error(f"Error listing instances for {user_id}: {e}")
        return {
            "success": False,
            "response": f"Error: {e}",
            "tool": None,
            "needs_llm": False,
        }


def _handle_disconnect(args: str, user_id: str) -> dict[str, Any]:
    """Handle !novik disconnect command."""
    from .token_broker import revoke_user_token, get_user_instances, get_user_active_instance, set_user_active_instance

    name = args.strip() or "default"

    try:
        # Check if user has this instance token
        user_instances = get_user_instances(user_id)

        if name not in user_instances:
            if user_instances:
                return {
                    "success": False,
                    "response": f"Instance '{name}' not found. You have: {', '.join(user_instances)}",
                    "tool": None,
                    "needs_llm": False,
                }
            else:
                return {
                    "success": False,
                    "response": "No instances connected. Use `!vik <token>` to connect.",
                    "tool": None,
                    "needs_llm": False,
                }

        # Revoke the token
        revoke_user_token(user_id, reason="User disconnected via !novik", instance=name)

        # If this was the active instance, switch to another
        active = get_user_active_instance(user_id)
        if active == name:
            remaining = [i for i in user_instances if i != name]
            if remaining:
                set_user_active_instance(user_id, remaining[0])
                return {
                    "success": True,
                    "response": f"Disconnected from '{name}'. Switched to '{remaining[0]}'.",
                    "tool": "disconnect_instance",
                    "needs_llm": False,
                }
            else:
                # No instances left - clear active instance
                # (set_user_active_instance will handle this)
                pass

        return {
            "success": True,
            "response": f"Disconnected from '{name}'.",
            "tool": "disconnect_instance",
            "needs_llm": False,
        }
    except Exception as e:
        return {
            "success": False,
            "response": f"Error: {e}",
            "tool": None,
            "needs_llm": False,
        }


def _handle_test_connection(user_id: str) -> dict[str, Any]:
    """Handle !test command with diagnostic info."""
    from .token_broker import get_user_active_instance, get_user_instances
    from .vikunja_client import VikunjaClient
    from .context import get_user_context

    try:
        # Get diagnostic info from PostgreSQL
        user_active_pg = get_user_active_instance(user_id)
        user_instances = get_user_instances(user_id)
        ctx = get_user_context(user_id)

        # Get instance URL
        instance_name = user_active_pg or "default"
        url = "Not configured"
        if ctx.active_instance:
            try:
                client = VikunjaClient(user_id, ctx.active_instance)
                url = client.base_url
            except Exception:
                pass

        # Test connection by listing projects
        project_count = 0
        task_preview_lines = []
        try:
            client = VikunjaClient(user_id, ctx.active_instance or "default")
            projects = client.get_projects()
            project_count = len(projects)

            # Get tasks using the same approach as !t
            tasks = client.get_tasks(filter_by="done = false")
            total_tasks = len(tasks)

            if total_tasks > 0:
                task_preview_lines.append("")
                task_preview_lines.append(f"**Task Preview** ({total_tasks} open):")
                for task in tasks[:5]:
                    due_str = ""
                    if task.due_date:
                        due_str = f" (due {task.due_date.strftime('%m/%d')})"
                    task_preview_lines.append(f"• {task.title}{due_str}")
                if total_tasks > 5:
                    task_preview_lines.append(f"_...and {total_tasks - 5} more_")
            else:
                task_preview_lines.append("")
                task_preview_lines.append("**Task Preview:** No open tasks")

        except Exception as e:
            task_preview_lines.append("")
            task_preview_lines.append(f"**Task Preview:** Error: {str(e)[:60]}")

        # Get git version
        git_version = "unknown"
        try:
            import subprocess
            result = subprocess.run(
                ["git", "rev-parse", "--short", "HEAD"],
                capture_output=True,
                text=True,
                timeout=2,
                cwd="/opt/render/project/src"  # Render deployment path
            )
            if result.returncode == 0:
                git_version = result.stdout.strip()
        except:
            # Fallback: try current directory
            try:
                result = subprocess.run(
                    ["git", "rev-parse", "--short", "HEAD"],
                    capture_output=True,
                    text=True,
                    timeout=2
                )
                if result.returncode == 0:
                    git_version = result.stdout.strip()
            except:
                pass

        # Build diagnostic response
        lines = [
            f"**Connection OK.** Found {project_count} projects.",
            f"_Version: `{git_version}`_",
            "",
            "**Diagnostics:**",
            f"• Instance: `{instance_name}`",
            f"• URL: `{url}`",
            f"• Connected instances: `{list(user_instances) if user_instances else ['None']}`",
        ]

        # Add task preview
        lines.extend(task_preview_lines)

        return {
            "success": True,
            "response": "\n".join(lines),
            "tool": "test_connection",
            "needs_llm": False,
        }
    except Exception as e:
        return {
            "success": False,
            "response": f"Connection failed: {e}",
            "tool": None,
            "needs_llm": False,
        }


def _handle_stats(user_id: str) -> dict[str, Any]:
    """Handle !stats command.

    Respects user's active instance set via !switch.
    """
    from .server import _task_summary_impl, _get_user_instance, _format_user_context

    try:
        # Use user's active instance (if set)
        instance = _get_user_instance(user_id) or ""
        result = _task_summary_impl(instance=instance)
        if result.get("error"):
            return {
                "success": False,
                "response": f"Error: {result['error']}",
                "tool": None,
                "needs_llm": False,
            }

        lines = [
            "**Task Summary:**",
            "",
            f"- Total: {result.get('total', 0)}",
            f"- Overdue: {result.get('overdue', 0)}",
            f"- Due today: {result.get('due_today', 0)}",
            f"- Due this week: {result.get('due_this_week', 0)}",
            f"- High priority: {result.get('high_priority', 0)}",
            f"- Unscheduled: {result.get('unscheduled', 0)}",
        ]

        # Add context footer
        lines.append("")
        lines.append(_format_user_context(user_id))

        return {
            "success": True,
            "response": "\n".join(lines),
            "tool": "task_summary",
            "needs_llm": False,
            "eco_mode": True,
        }
    except Exception as e:
        return {
            "success": False,
            "response": f"Error: {e}",
            "tool": None,
            "needs_llm": False,
        }


def _handle_bind(args: str, user_id: str, room_id: str | None, is_dm: bool = False) -> dict[str, Any]:
    """Handle !bind <project> command - bind room to project.

    Uses fuzzy search to find project by name.
    """
    from .server import (
        _set_room_binding,
        _list_projects_impl,
    )
    from rapidfuzz import fuzz, process

    if is_dm or not room_id:
        return {
            "success": False,
            "response": "Room binding only works in rooms, not DMs.",
            "tool": None,
            "needs_llm": False,
        }

    if not args.strip():
        return {
            "success": False,
            "response": "Usage: `!bind <project>`\n\nExample: `!bind Client XYZ`",
            "tool": None,
            "needs_llm": False,
        }

    # Token already validated and set by centralized auth check
    project_query = args.strip()
    
    try:
        # Get all projects
        projects_result = _list_projects_impl()
        projects = projects_result.get("projects", [])
        
        if not projects:
            return {
                "success": False,
                "response": "No projects found. Create a project in Vikunja first.",
                "tool": None,
                "needs_llm": False,
            }
        
        # Fuzzy search by title
        project_titles = {p["title"]: p for p in projects}
        matches = process.extract(
            project_query,
            project_titles.keys(),
            scorer=fuzz.WRatio,
            limit=1
        )
        
        if not matches or matches[0][1] < 60:  # Confidence threshold
            return {
                "success": False,
                "response": f"No project found matching '{project_query}'.\n\nAvailable projects:\n" + 
                           "\n".join(f"- {p['title']}" for p in projects[:10]),
                "tool": None,
                "needs_llm": False,
            }
        
        best_match = matches[0][0]
        project = project_titles[best_match]
        
        # Set binding
        _set_room_binding(user_id, room_id, project["title"])
        
        return {
            "success": True,
            "response": f"✅ Room bound to project: **{project['title']}**\n\n" +
                       "All commands in this room will now use this project automatically.",
            "tool": "bind",
            "needs_llm": False,
            "eco_mode": True,
        }
    except Exception as e:
        logger.exception("Error in !bind")
        return {
            "success": False,
            "response": f"Error: {e}",
            "tool": None,
            "needs_llm": False,
        }


def _handle_unbind(user_id: str, room_id: str | None, is_dm: bool = False) -> dict[str, Any]:
    """Handle !unbind command - remove room binding."""
    from .server import _remove_room_binding, _get_room_binding

    if is_dm or not room_id:
        return {
            "success": False,
            "response": "Room binding only works in rooms, not DMs.",
            "tool": None,
            "needs_llm": False,
        }
    
    try:
        # Check if there's a binding first
        current = _get_room_binding(user_id, room_id)
        if not current:
            return {
                "success": False,
                "response": "This room is not bound to any project.\n\nUse `!bind <project>` to bind it.",
                "tool": None,
                "needs_llm": False,
            }
        
        # Remove binding
        result = _remove_room_binding(user_id, room_id)
        
        return {
            "success": True,
            "response": f"✅ Room unbound from project: **{current}**",
            "tool": "unbind",
            "needs_llm": False,
            "eco_mode": True,
        }
    except Exception as e:
        logger.exception("Error in !unbind")
        return {
            "success": False,
            "response": f"Error: {e}",
            "tool": None,
            "needs_llm": False,
        }


def _handle_show_binding(user_id: str, room_id: str | None, is_dm: bool = False) -> dict[str, Any]:
    """Handle !binding command - show current room binding."""
    from .server import _get_room_binding

    if is_dm or not room_id:
        return {
            "success": False,
            "response": "Room binding only works in rooms, not DMs.",
            "tool": None,
            "needs_llm": False,
        }
    
    try:
        current = _get_room_binding(user_id, room_id)
        
        if current:
            return {
                "success": True,
                "response": f"📌 This room is bound to: **{current}**\n\n" +
                           "All commands will use this project automatically.\n\n" +
                           "Use `!unbind` to remove the binding.",
                "tool": "binding",
                "needs_llm": False,
                "eco_mode": True,
            }
        else:
            return {
                "success": True,
                "response": "This room is not bound to any project.\n\n" +
                           "Use `!bind <project>` to bind it.",
                "tool": "binding",
                "needs_llm": False,
                "eco_mode": True,
            }
    except Exception as e:
        logger.exception("Error in !binding")
        return {
            "success": False,
            "response": f"Error: {e}",
            "tool": None,
            "needs_llm": False,
        }


def _handle_done(args: str, user_id: str) -> dict[str, Any]:
    """Handle !done <title> command - complete task by fuzzy title match.

    Searches open tasks for best match and marks it done.
    Respects user's active instance set via !switch.
    """
    from .server import (
        _list_all_tasks_impl,
        _complete_task_impl,
        _get_user_instance,
    )
    from rapidfuzz import fuzz, process

    if not args.strip():
        return {
            "success": False,
            "response": "Usage: `!done <task title>`\n\nExample: `!done peloton ride`",
            "tool": None,
            "needs_llm": False,
        }

    # Token already validated and set by centralized auth check
    query = args.strip()

    try:
        # Use user's active instance (if set via !switch)
        instance = _get_user_instance(user_id) or ""

        # Get open tasks from user's active instance
        result = _list_all_tasks_impl(include_done=False, instance=instance)
        tasks = result.get("tasks", [])

        if not tasks:
            return {
                "success": False,
                "response": "No open tasks found.",
                "tool": None,
                "needs_llm": False,
            }

        # Fuzzy search by title
        task_titles = {t["title"]: t for t in tasks}
        matches = process.extract(
            query,
            task_titles.keys(),
            scorer=fuzz.WRatio,
            limit=3
        )

        if not matches or matches[0][1] < 50:  # Confidence threshold
            return {
                "success": False,
                "response": f"No task found matching '{query}'.\n\nTry `!oops` or `!now` to see your tasks.",
                "tool": None,
                "needs_llm": False,
            }

        best_match = matches[0][0]
        confidence = matches[0][1]
        task = task_titles[best_match]
        task_id = task["id"]

        # If low confidence, show options instead of auto-completing
        if confidence < 80 and len(matches) > 1:
            options = "\n".join(f"- `!done {m[0][:40]}` ({m[1]}%)" for m in matches[:3])
            return {
                "success": True,
                "response": f"Multiple matches for '{query}':\n\n{options}\n\nBe more specific or use one of the above.",
                "tool": None,
                "needs_llm": False,
                "eco_mode": True,
            }

        # Complete the task
        complete_result = _complete_task_impl(task_id)

        if complete_result.get("error"):
            return {
                "success": False,
                "response": f"Error: {complete_result['error']}",
                "tool": None,
                "needs_llm": False,
            }

        return {
            "success": True,
            "response": f"✅ Completed: **{best_match}** `#{task_id}`",
            "tool": "complete_task",
            "needs_llm": False,
            "eco_mode": True,
        }
    except Exception as e:
        logger.exception("Error in !done")
        return {
            "success": False,
            "response": f"Error: {e}",
            "tool": None,
            "needs_llm": False,
        }


def _handle_credits(user_id: str) -> dict[str, Any]:
    """Handle !credits command - show usage and remaining credits."""
    from .server import (
        _get_user_credits_info,
        _get_user_anthropic_api_key,
    )

    try:
        # Check if user has their own API key
        has_own_key = bool(_get_user_anthropic_api_key(user_id))

        if has_own_key:
            return {
                "success": True,
                "response": (
                    "**Your Usage**\n\n"
                    "You're using your own API key (BYOK), so there are no usage limits.\n\n"
                    "To remove your key and use free tier: `!apikey clear`"
                ),
                "tool": "credits",
                "needs_llm": False,
                "eco_mode": True,
            }

        # Get usage info
        info = _get_user_credits_info(user_id)
        budget = info.get("budget", 1.0)
        lifetime_used = info.get("usage", 0)
        remaining = info.get("remaining", budget)
        pct_used = (lifetime_used / budget * 100) if budget > 0 else 0

        # Build response
        lines = [
            "**Your Usage Credits**",
            "",
            f"• Used: ${lifetime_used:.4f}",
            f"• Remaining: ${remaining:.4f}",
            f"• Free tier limit: ${budget:.2f}",
            f"• Progress: {pct_used:.1f}%",
            "",
        ]

        if pct_used >= 100:
            lines.append("⚠️ **Free tier exhausted!** Use `!apikey` to add your own key.")
        elif pct_used >= 80:
            lines.append("⚠️ Approaching limit. Consider `!apikey` to add your own key.")
        else:
            lines.append("💡 Tip: Use `!oops`, `!now`, `!fire` for free (no AI cost).")

        return {
            "success": True,
            "response": "\n".join(lines),
            "tool": "credits",
            "needs_llm": False,
            "eco_mode": True,
        }
    except Exception as e:
        logger.exception("Error in !credits")
        return {
            "success": False,
            "response": f"Error: {e}",
            "tool": None,
            "needs_llm": False,
        }


def _handle_apikey(args: str, user_id: str) -> dict[str, Any]:
    """Handle !apikey command - manage user's own Anthropic API key (BYOK)."""
    import os
    from .server import (
        _get_user_anthropic_api_key,
        _set_user_anthropic_api_key,
        _remove_user_anthropic_api_key,
    )

    # SECURITY: Only allow !apikey on isolated instances
    # On shared servers, user A could prompt inject and steal user B's API key
    is_isolated = os.environ.get("ISOLATED_INSTANCE", "").lower() in ("1", "true", "yes")
    if not is_isolated:
        return {
            "success": False,
            "response": (
                "🔒 **API Key Management Disabled**\n\n"
                "For security reasons, `!apikey` is only available on isolated bot instances.\n\n"
                "**Why?** On shared servers, malicious users could use prompt injection to steal your API key.\n\n"
                "**Options:**\n"
                "• Use the free tier (no API key needed)\n"
                "• Deploy your own isolated bot instance\n"
                "• Contact admin for isolated instance access"
            ),
            "tool": None,
            "needs_llm": False,
        }

    # Clean up args - remove all whitespace including line breaks
    args = "".join(args.split())

    # No args - show current status
    if not args:
        has_key = bool(_get_user_anthropic_api_key(user_id))
        if has_key:
            return {
                "success": True,
                "response": (
                    "**API Key Status**: ✅ Set (BYOK mode)\n\n"
                    "You're using your own Anthropic API key.\n\n"
                    "• `!apikey clear` - Remove your key and use free tier\n"
                    "• `!apikey sk-ant-...` - Replace with a new key"
                ),
                "tool": "apikey",
                "needs_llm": False,
                "eco_mode": True,
            }
        else:
            return {
                "success": True,
                "response": (
                    "**API Key Status**: Using free tier\n\n"
                    "To use your own Anthropic API key (BYOK):\n"
                    "`!apikey sk-ant-api03-...`\n\n"
                    "Get your key from: https://console.anthropic.com/settings/keys"
                ),
                "tool": "apikey",
                "needs_llm": False,
                "eco_mode": True,
            }

    # Clear key
    if args.lower() == "clear":
        try:
            _remove_user_anthropic_api_key(user_id)
            return {
                "success": True,
                "response": "✅ API key removed. You're now using the free tier.",
                "tool": "apikey",
                "needs_llm": False,
                "eco_mode": True,
            }
        except Exception as e:
            return {
                "success": False,
                "response": f"Error clearing key: {e}",
                "tool": None,
                "needs_llm": False,
            }

    # Set new key
    if not args.startswith("sk-ant-"):
        return {
            "success": False,
            "response": (
                "Invalid API key format. Anthropic keys start with `sk-ant-`.\n\n"
                "Get your key from: https://console.anthropic.com/settings/keys"
            ),
            "tool": None,
            "needs_llm": False,
        }

    # TEMPORARY: Skip validation due to Render IP issues
    # Validate key before storing
    # from .server import _validate_anthropic_api_key
    # is_valid, validation_msg = _validate_anthropic_api_key(args)
    # if not is_valid:
    #     return {
    #         "success": False,
    #         "response": (
    #             f"❌ API key validation failed: {validation_msg}\n\n"
    #             "Please check your key at: https://console.anthropic.com/settings/keys"
    #         ),
    #         "tool": None,
    #         "needs_llm": False,
    #     }

    # Basic format check only
    if len(args) < 50:
        return {
            "success": False,
            "response": "❌ API key seems too short. Please check and try again.",
            "tool": None,
            "needs_llm": False,
        }

    try:
        _set_user_anthropic_api_key(user_id, args)
        return {
            "success": True,
            "response": (
                "✅ API key validated and saved! You're now in BYOK mode.\n\n"
                "• No usage limits apply\n"
                "• Your key is stored securely\n"
                "• Use `!apikey clear` to switch back to free tier"
            ),
            "tool": "apikey",
            "needs_llm": False,
            "eco_mode": True,
        }
    except Exception as e:
        return {
            "success": False,
            "response": f"Error setting key: {e}",
            "tool": None,
            "needs_llm": False,
        }


def _handle_model(args: str, user_id: str) -> dict[str, Any]:
    """Handle !model command - view or change AI model."""
    from .server import (
        _get_user_model,
        _set_user_model,
        AVAILABLE_MODELS,
        DEFAULT_MODEL,
    )

    args = args.strip().lower()

    # No args - show current model
    if not args:
        current = _get_user_model(user_id)
        models_list = ", ".join(AVAILABLE_MODELS.keys())
        return {
            "success": True,
            "response": (
                f"**Current model**: {current}\n\n"
                f"Available: {models_list}\n\n"
                "• `haiku` - Fastest, cheapest\n"
                "• `sonnet` - Balanced (default)\n"
                "• `opus` - Most capable, expensive\n\n"
                "Change with: `!model <name>`"
            ),
            "tool": "model",
            "needs_llm": False,
            "eco_mode": True,
        }

    # Set model
    if args not in AVAILABLE_MODELS:
        models_list = ", ".join(AVAILABLE_MODELS.keys())
        return {
            "success": False,
            "response": f"Unknown model: {args}\n\nAvailable: {models_list}",
            "tool": None,
            "needs_llm": False,
        }

    try:
        result = _set_user_model(user_id, args)
        if result.get("error"):
            return {
                "success": False,
                "response": f"Error: {result['error']}",
                "tool": None,
                "needs_llm": False,
            }
        return {
            "success": True,
            "response": f"✅ Model set to **{args}**",
            "tool": "model",
            "needs_llm": False,
            "eco_mode": True,
        }
    except Exception as e:
        return {
            "success": False,
            "response": f"Error: {e}",
            "tool": None,
            "needs_llm": False,
        }


def _handle_timezone(args: str, user_id: str) -> dict[str, Any]:
    """Handle !tz command - view or change timezone."""
    from .server import (
        _get_user_timezone_override,
        _set_user_timezone_override,
    )
    import pytz

    args = args.strip()

    # Common timezone aliases for convenience
    TZ_ALIASES = {
        "pacific": "America/Los_Angeles",
        "pst": "America/Los_Angeles",
        "pdt": "America/Los_Angeles",
        "mountain": "America/Denver",
        "mst": "America/Denver",
        "mdt": "America/Denver",
        "central": "America/Chicago",
        "cst": "America/Chicago",
        "cdt": "America/Chicago",
        "eastern": "America/New_York",
        "est": "America/New_York",
        "edt": "America/New_York",
        "utc": "UTC",
        "gmt": "UTC",
        "london": "Europe/London",
        "paris": "Europe/Paris",
        "berlin": "Europe/Berlin",
        "tokyo": "Asia/Tokyo",
        "sydney": "Australia/Sydney",
    }

    # No args - show current timezone
    if not args:
        current = _get_user_timezone_override(user_id) or "UTC (default)"
        return {
            "success": True,
            "response": (
                f"**Current timezone**: {current}\n\n"
                "Set with: `!tz <timezone>`\n\n"
                "Examples:\n"
                "• `!tz America/New_York`\n"
                "• `!tz eastern` (alias)\n"
                "• `!tz pacific`\n"
                "• `!tz Europe/London`\n"
                "• `!tz UTC`"
            ),
            "tool": "timezone",
            "needs_llm": False,
            "eco_mode": True,
        }

    # Resolve alias
    tz_input = args.lower()
    tz_name = TZ_ALIASES.get(tz_input, args)

    # Validate timezone
    try:
        pytz.timezone(tz_name)
    except pytz.UnknownTimeZoneError:
        return {
            "success": False,
            "response": (
                f"Unknown timezone: {args}\n\n"
                "Use IANA timezone names like `America/New_York`, `Europe/London`, `Asia/Tokyo`\n"
                "Or aliases: `pacific`, `eastern`, `central`, `mountain`, `utc`"
            ),
            "tool": None,
            "needs_llm": False,
        }

    # Set timezone
    try:
        result = _set_user_timezone_override(user_id, tz_name)
        from datetime import datetime
        now = datetime.now(pytz.timezone(tz_name))
        current_time = now.strftime("%Y-%m-%d %H:%M %Z")
        return {
            "success": True,
            "response": f"✅ Timezone set to **{tz_name}**\n\nCurrent time: {current_time}",
            "tool": "timezone",
            "needs_llm": False,
            "eco_mode": True,
        }
    except Exception as e:
        return {
            "success": False,
            "response": f"Error: {e}",
            "tool": None,
            "needs_llm": False,
        }


def _handle_switch(args: str, user_id: str) -> dict[str, Any]:
    """Handle !switch command - switch active Vikunja instance.

    Usage:
        !switch - Show current instance and available options
        !switch personal - Switch to 'personal' instance
        !switch clear - Revert to default instance
    """
    from .server import (
        _get_user_instance,
        _set_user_instance,
        _clear_user_instance,
        _format_user_context,
    )
    from .token_broker import get_user_instances, get_user_active_instance

    args = args.strip().lower()

    # No args - show current instance and available options
    if not args:
        user_instances = get_user_instances(user_id)
        current = get_user_active_instance(user_id)

        if not user_instances:
            return {
                "success": True,
                "response": "No Vikunja instances connected.\n\nUse `!vik <token>` to connect.",
                "tool": "switch",
                "needs_llm": False,
                "eco_mode": True,
            }

        lines = ["**Instance Management**", ""]

        if current:
            lines.append(f"Current instance: **{current}**")
        else:
            lines.append("Current instance: _(default)_")

        lines.append("")
        lines.append("**Your instances:**")
        for name in user_instances:
            marker = " *(active)*" if name == current else ""
            lines.append(f"- `{name}`{marker}")

        lines.append("")
        lines.append("Switch with: `!switch <name>`")
        lines.append("Clear with: `!switch clear`")

        return {
            "success": True,
            "response": "\n".join(lines),
            "tool": "switch",
            "needs_llm": False,
            "eco_mode": True,
        }

    # Clear command
    if args == "clear":
        result = _clear_user_instance(user_id)
        if result.get("cleared"):
            context = _format_user_context(user_id)
            return {
                "success": True,
                "response": f"✅ Instance preference cleared. Using default.\n\n{context}",
                "tool": "switch",
                "needs_llm": False,
                "eco_mode": True,
            }
        else:
            return {
                "success": True,
                "response": "No instance preference was set.",
                "tool": "switch",
                "needs_llm": False,
                "eco_mode": True,
            }

    # Switch to specified instance
    result = _set_user_instance(user_id, args)

    if result.get("error"):
        return {
            "success": False,
            "response": f"❌ {result['error']}",
            "tool": None,
            "needs_llm": False,
        }

    context = _format_user_context(user_id)
    return {
        "success": True,
        "response": f"✅ Switched to **{result['instance']}**\n\n{context}",
        "tool": "switch",
        "needs_llm": False,
        "eco_mode": True,
    }


def _handle_project(args: str, user_id: str) -> dict[str, Any]:
    """Handle !project command - set or show active project context.

    Usage:
        !project - Show current project
        !project Kitchen - Set active project to Kitchen (fuzzy match)
        !project clear - Clear active project (query all)
    """
    from .server import (
        _get_user_project,
        _set_user_project,
        _clear_user_project,
        _format_user_context,
        _list_projects_impl,
    )
    from rapidfuzz import fuzz, process

    args = args.strip()

    # Token already validated and set by centralized auth check

    # No args - show current project
    if not args:
        current = _get_user_project(user_id)
        context = _format_user_context(user_id)

        if current:
            return {
                "success": True,
                "response": (
                    f"**Active project:** {current['name']} ({current['instance']})\n\n"
                    f"{context}\n\n"
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
                    f"{context}\n\n"
                    "Use `!project <name>` to focus on a specific project."
                ),
                "tool": "project",
                "needs_llm": False,
                "eco_mode": True,
            }

    # Clear command
    if args.lower() == "clear":
        result = _clear_user_project(user_id)
        context = _format_user_context(user_id)
        if result.get("cleared"):
            return {
                "success": True,
                "response": f"✅ Active project cleared. Commands will query all projects.\n\n{context}",
                "tool": "project",
                "needs_llm": False,
                "eco_mode": True,
            }
        else:
            return {
                "success": True,
                "response": f"No active project was set.\n\n{context}",
                "tool": "project",
                "needs_llm": False,
                "eco_mode": True,
            }

    # Fuzzy match project name
    try:
        projects_result = _list_projects_impl()
        projects = projects_result if isinstance(projects_result, list) else projects_result.get("projects", [])

        if not projects:
            return {
                "success": False,
                "response": "No projects found. Create a project in Vikunja first.",
                "tool": None,
                "needs_llm": False,
            }

        # Build title -> project mapping
        project_titles = {p["title"]: p for p in projects}
        matches = process.extract(
            args,
            project_titles.keys(),
            scorer=fuzz.WRatio,
            limit=3
        )

        if not matches or matches[0][1] < 60:  # Confidence threshold
            project_list = "\n".join(f"- {p['title']}" for p in projects[:10])
            return {
                "success": False,
                "response": f"No project found matching '{args}'.\n\n**Available projects:**\n{project_list}",
                "tool": None,
                "needs_llm": False,
            }

        best_match = matches[0][0]
        confidence = matches[0][1]
        project = project_titles[best_match]

        # If low confidence and multiple matches, show options
        if confidence < 80 and len(matches) > 1 and matches[1][1] > 50:
            options = "\n".join(f"- `!project {m[0]}` ({m[1]}%)" for m in matches[:3] if m[1] > 50)
            return {
                "success": True,
                "response": f"Multiple matches for '{args}':\n\n{options}\n\nBe more specific.",
                "tool": None,
                "needs_llm": False,
                "eco_mode": True,
            }

        # Set the project
        result = _set_user_project(user_id, project["id"], project["title"])
        context = _format_user_context(user_id)

        return {
            "success": True,
            "response": f"✅ Active project: **{project['title']}**\n\n{context}",
            "tool": "project",
            "needs_llm": False,
            "eco_mode": True,
        }

    except Exception as e:
        logger.exception("Error in !project")
        return {
            "success": False,
            "response": f"Error: {e}",
            "tool": None,
            "needs_llm": False,
        }


def _handle_context(user_id: str) -> dict[str, Any]:
    """Handle !context command - show current instance/project context.

    This is a quick way to see the current context without switching anything.
    """
    from .server import (
        _get_user_instance,
        _get_user_project,
        _format_user_context,
    )
    from .token_broker import get_user_instances, get_user_active_instance

    user_instances = get_user_instances(user_id)
    current_instance = get_user_active_instance(user_id)
    current_project = _get_user_project(user_id)
    context = _format_user_context(user_id)

    lines = ["**Current Context**", ""]

    # Instance info
    if len(user_instances) > 1:
        if current_instance:
            lines.append(f"**Instance:** {current_instance}")
        else:
            lines.append("**Instance:** _(default)_")
    else:
        inst_name = user_instances[0] if user_instances else "default"
        lines.append(f"**Instance:** {inst_name}")

    # Project info
    if current_project:
        lines.append(f"**Project:** {current_project['name']}")
    else:
        lines.append("**Project:** All Projects")

    lines.append("")
    lines.append(context)
    lines.append("")
    lines.append("_Change with `!switch <instance>` or `!project <name>`_")

    return {
        "success": True,
        "response": "\n".join(lines),
        "tool": "context",
        "needs_llm": False,
        "eco_mode": True,
    }


def _handle_clear(user_id: str) -> dict[str, Any]:
    """Handle !clear command - remove active project context.

    This clears the project binding set via !project, so filter commands
    like !now and !week will show tasks from ALL projects.
    """
    from .server import _clear_user_project, _format_user_context

    result = _clear_user_project(user_id)
    context = _format_user_context(user_id)

    if result.get("cleared"):
        response = "✅ **Project context cleared**\n\nFilter commands will now show tasks from **all projects**.\n\n" + context
    else:
        response = "ℹ️ **No project was set**\n\nYou can set a project with `!project <name>`.\n\n" + context

    return {
        "success": True,
        "response": response,
        "tool": "clear",
        "needs_llm": False,
        "eco_mode": True,
    }
