"""
Tool Registry for Vikunja-native @eis.

Defines which MCP tools are available when @eis operates within a project.

Principle: @eis can do anything WITHIN a project it's invited to,
but cannot access other projects or perform admin operations.

Bead: solutions-2gvm
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class ToolCategory(Enum):
    """Tool categories for grouping and display."""
    TASK = "task"           # Task CRUD
    BATCH = "batch"         # Bulk operations
    LABEL = "label"         # Label management
    BUCKET = "bucket"       # Kanban bucket operations
    VIEW = "view"           # View management
    RELATION = "relation"   # Task relations
    ASSIGNMENT = "assign"   # User assignment
    QUERY = "query"         # Read-only queries
    POSITION = "position"   # Ordering/positioning


class ConfirmLevel(Enum):
    """Confirmation level required for tool execution."""
    NONE = "none"           # Execute immediately
    COUNT = "count"         # Confirm if affects >N items
    ALWAYS = "always"       # Always require confirmation


@dataclass
class ToolDef:
    """Definition for a tool available to @eis."""
    name: str                           # Function name
    category: ToolCategory              # Category for grouping
    description: str                    # Short description
    confirm: ConfirmLevel = ConfirmLevel.NONE
    confirm_threshold: int = 5          # For COUNT level: confirm if > N items
    cost_estimate: str = "free"         # Estimated cost: "free", "~1¢", etc.
    min_tier: str = "$"                 # Minimum cost tier: "$", "$$", "$$$" (fa-qld6)


# =============================================================================
# VIKUNJA-NATIVE TOOL REGISTRY
# =============================================================================

VIKUNJA_TOOLS: dict[str, ToolDef] = {
    # -------------------------------------------------------------------------
    # Task CRUD
    # -------------------------------------------------------------------------
    "create_task": ToolDef(
        name="create_task",
        category=ToolCategory.TASK,
        description="Create a new task in the project",
        min_tier="$$",  # fa-qld6: Haiku creates duplicates
    ),
    "get_task": ToolDef(
        name="get_task",
        category=ToolCategory.TASK,
        description="Get task details by ID",
    ),
    "complete_task": ToolDef(
        name="complete_task",
        category=ToolCategory.TASK,
        description="Mark a task as complete",
    ),
    "delete_task": ToolDef(
        name="delete_task",
        category=ToolCategory.TASK,
        description="Delete a task",
        # confirm disabled - see solutions-jjih
    ),
    "batch_delete_tasks": ToolDef(
        name="batch_delete_tasks",
        category=ToolCategory.BATCH,
        description="Delete multiple tasks at once",
        # Same destructiveness as delete_project, so allowed for bot
    ),
    "set_reminders": ToolDef(
        name="set_reminders",
        category=ToolCategory.TASK,
        description="Set reminder times for a task",
    ),

    # -------------------------------------------------------------------------
    # Batch Operations
    # -------------------------------------------------------------------------
    "batch_create_tasks": ToolDef(
        name="batch_create_tasks",
        category=ToolCategory.BATCH,
        description="Create multiple tasks at once",
        confirm=ConfirmLevel.COUNT,
        confirm_threshold=10,
        min_tier="$$",  # fa-qld6: Haiku creates duplicates
    ),
    "batch_update_tasks": ToolDef(
        name="batch_update_tasks",
        category=ToolCategory.BATCH,
        description="Update multiple tasks at once",
        confirm=ConfirmLevel.COUNT,
        confirm_threshold=5,
    ),
    "complete_tasks_by_label": ToolDef(
        name="complete_tasks_by_label",
        category=ToolCategory.BATCH,
        description="Complete all tasks with a specific label",
        # confirm disabled - see solutions-jjih
    ),

    # -------------------------------------------------------------------------
    # Labels
    # -------------------------------------------------------------------------
    "add_label_to_task": ToolDef(
        name="add_label_to_task",
        category=ToolCategory.LABEL,
        description="Add a label to a task",
    ),
    "create_label": ToolDef(
        name="create_label",
        category=ToolCategory.LABEL,
        description="Create a new label",
        min_tier="$$",  # fa-qld6: Haiku creates duplicates
    ),
    "delete_label": ToolDef(
        name="delete_label",
        category=ToolCategory.LABEL,
        description="Delete a label",
        # confirm disabled - see solutions-jjih
    ),
    "list_labels": ToolDef(
        name="list_labels",
        category=ToolCategory.LABEL,
        description="List all labels in the project",
    ),
    "bulk_create_labels": ToolDef(
        name="bulk_create_labels",
        category=ToolCategory.LABEL,
        description="Create multiple labels at once",
        min_tier="$$",  # fa-qld6: Haiku creates duplicates
    ),
    "bulk_relabel_tasks": ToolDef(
        name="bulk_relabel_tasks",
        category=ToolCategory.LABEL,
        description="Add/remove labels from multiple tasks",
        confirm=ConfirmLevel.COUNT,
        confirm_threshold=5,
    ),

    # -------------------------------------------------------------------------
    # Buckets (Kanban)
    # -------------------------------------------------------------------------
    "create_bucket": ToolDef(
        name="create_bucket",
        category=ToolCategory.BUCKET,
        description="Create a new kanban bucket",
        min_tier="$$",  # fa-qld6: Haiku creates duplicates
    ),
    "delete_bucket": ToolDef(
        name="delete_bucket",
        category=ToolCategory.BUCKET,
        description="Delete a bucket (moves tasks to default)",
        # confirm disabled - see solutions-jjih
    ),
    "list_buckets": ToolDef(
        name="list_buckets",
        category=ToolCategory.BUCKET,
        description="List all buckets in a view",
    ),
    "sort_bucket": ToolDef(
        name="sort_bucket",
        category=ToolCategory.BUCKET,
        description="Sort tasks within a bucket",
    ),
    "move_tasks_by_label_to_buckets": ToolDef(
        name="move_tasks_by_label_to_buckets",
        category=ToolCategory.BUCKET,
        description="Move tasks to buckets based on labels",
        confirm=ConfirmLevel.COUNT,
        confirm_threshold=5,
    ),
    "list_tasks_by_bucket": ToolDef(
        name="list_tasks_by_bucket",
        category=ToolCategory.BUCKET,
        description="List tasks grouped by bucket",
    ),

    # -------------------------------------------------------------------------
    # Views
    # -------------------------------------------------------------------------
    "create_view": ToolDef(
        name="create_view",
        category=ToolCategory.VIEW,
        description="Create a new view (list, kanban, etc.)",
        min_tier="$$",  # fa-qld6: Haiku creates duplicates
    ),
    "create_filtered_view": ToolDef(
        name="create_filtered_view",
        category=ToolCategory.VIEW,
        description="Create a view with filters",
        min_tier="$$",  # fa-qld6: Haiku creates duplicates
    ),
    "delete_view": ToolDef(
        name="delete_view",
        category=ToolCategory.VIEW,
        description="Delete a view",
        # confirm disabled - see solutions-jjih
    ),
    "list_views": ToolDef(
        name="list_views",
        category=ToolCategory.VIEW,
        description="List all views in the project",
    ),
    "get_view_tasks": ToolDef(
        name="get_view_tasks",
        category=ToolCategory.VIEW,
        description="Get tasks from a specific view",
    ),
    "get_kanban_view": ToolDef(
        name="get_kanban_view",
        category=ToolCategory.VIEW,
        description="Get kanban board layout",
    ),
    "setup_kanban_board": ToolDef(
        name="setup_kanban_board",
        category=ToolCategory.VIEW,
        description="Set up a kanban board with buckets",
        min_tier="$$",  # fa-qld6: Haiku creates duplicates
    ),

    # -------------------------------------------------------------------------
    # Task Relations
    # -------------------------------------------------------------------------
    "create_task_relation": ToolDef(
        name="create_task_relation",
        category=ToolCategory.RELATION,
        description="Create a relation between tasks (subtask, blocks, etc.)",
        min_tier="$$",  # fa-qld6: Haiku creates duplicates
    ),
    "list_task_relations": ToolDef(
        name="list_task_relations",
        category=ToolCategory.RELATION,
        description="List relations for a task",
    ),

    # -------------------------------------------------------------------------
    # Assignment
    # -------------------------------------------------------------------------
    "assign_user": ToolDef(
        name="assign_user",
        category=ToolCategory.ASSIGNMENT,
        description="Assign a user to a task",
    ),
    "unassign_user": ToolDef(
        name="unassign_user",
        category=ToolCategory.ASSIGNMENT,
        description="Remove a user from a task",
    ),

    # -------------------------------------------------------------------------
    # Projects (allow full access for single-user parity with Claude Desktop)
    # -------------------------------------------------------------------------
    "create_project": ToolDef(
        name="create_project",
        category=ToolCategory.TASK,  # Reusing TASK category
        description="Create a new project or subproject",
        min_tier="$$",  # fa-qld6: Haiku creates duplicates
    ),
    "list_projects": ToolDef(
        name="list_projects",
        category=ToolCategory.QUERY,
        description="List all projects",
    ),
    "get_project": ToolDef(
        name="get_project",
        category=ToolCategory.QUERY,
        description="Get project details by ID",
    ),
    "share_project": ToolDef(
        name="share_project",
        category=ToolCategory.TASK,
        description="Share a project with a user",
    ),
    "get_project_users": ToolDef(
        name="get_project_users",
        category=ToolCategory.QUERY,
        description="List users with access to a project",
    ),
    "delete_project": ToolDef(
        name="delete_project",
        category=ToolCategory.TASK,
        description="Delete a project and all its tasks",
        # Note: Confirmation disabled - no state persistence between messages
        # User explicitly asking to delete is already confirmation enough
    ),

    # -------------------------------------------------------------------------
    # Queries (read-only)
    # -------------------------------------------------------------------------
    "list_tasks": ToolDef(
        name="list_tasks",
        category=ToolCategory.QUERY,
        description="List tasks in the project",
    ),
    "due_today": ToolDef(
        name="due_today",
        category=ToolCategory.QUERY,
        description="Get tasks due today",
    ),
    "due_this_week": ToolDef(
        name="due_this_week",
        category=ToolCategory.QUERY,
        description="Get tasks due this week",
    ),
    "overdue_tasks": ToolDef(
        name="overdue_tasks",
        category=ToolCategory.QUERY,
        description="Get overdue tasks",
    ),
    "high_priority_tasks": ToolDef(
        name="high_priority_tasks",
        category=ToolCategory.QUERY,
        description="Get high priority tasks",
    ),
    "upcoming_deadlines": ToolDef(
        name="upcoming_deadlines",
        category=ToolCategory.QUERY,
        description="Get tasks with upcoming deadlines",
    ),
    "unscheduled_tasks": ToolDef(
        name="unscheduled_tasks",
        category=ToolCategory.QUERY,
        description="Get tasks without due dates",
    ),
    # Note: task_summary uses cross-project query, not available in Vikunja-native
    # Use list_tasks with project_id instead
    "focus_now": ToolDef(
        name="focus_now",
        category=ToolCategory.QUERY,
        description="Get suggested task to focus on",
    ),

    # -------------------------------------------------------------------------
    # Positioning
    # -------------------------------------------------------------------------
    "set_task_position": ToolDef(
        name="set_task_position",
        category=ToolCategory.POSITION,
        description="Set task position in a view",
    ),
    "bulk_set_task_positions": ToolDef(
        name="bulk_set_task_positions",
        category=ToolCategory.POSITION,
        description="Set positions for multiple tasks",
    ),
    "batch_set_positions": ToolDef(
        name="batch_set_positions",
        category=ToolCategory.POSITION,
        description="Batch update task positions",
    ),
    "set_view_position": ToolDef(
        name="set_view_position",
        category=ToolCategory.POSITION,
        description="Set view position in project",
    ),
}


# =============================================================================
# EXCLUDED TOOLS (and why)
# =============================================================================

EXCLUDED_TOOLS = {
    # Cross-project operations
    "move_task_to_project": "Cross-project move not allowed",
    "move_task_to_project_by_name": "Cross-project move not allowed",
    "move_tasks_by_label": "Cross-project move not allowed",
    "list_all_projects": "Cross-project access not allowed",
    "list_all_tasks": "Cross-project access not allowed",
    "search_all": "Cross-project search not allowed",
    "export_all_projects": "Admin operation",

    # Project-level operations (some now allowed for single-user parity)
    # delete_project - NOW ALLOWED with confirmation (ConfirmLevel.ALWAYS)
    "update_project": "Project modification not allowed",
    "setup_project": "Admin operation",
    # create_project, list_projects, get_project - NOW ALLOWED

    # Instance management
    "connect_instance": "Instance management not allowed",
    "disconnect_instance": "Instance management not allowed",
    "list_instances": "Instance management not allowed",
    "rename_instance": "Instance management not allowed",
    "switch_instance": "Instance management not allowed",

    # Context (Claude Code specific)
    "get_context": "Claude Code specific",
    "get_active_context": "Claude Code specific",
    "set_active_context": "Claude Code specific",

    # Calendar integration
    "add_to_calendar": "External integration",
    "get_calendar_url": "External integration",
    "get_ics_feed": "External integration",

    # Project config
    "get_project_config": "Admin operation",
    "set_project_config": "Admin operation",
    "delete_project_config": "Admin operation",
    "list_project_configs": "Admin operation",

    # Templates
    "create_from_template": "Template management not allowed",

    # XQ (queue management)
    "check_xq": "XQ not available in Vikunja-native",
    "claim_xq_task": "XQ not available in Vikunja-native",
    "complete_xq_task": "XQ not available in Vikunja-native",
    "setup_xq": "XQ not available in Vikunja-native",

    # Token/health
    "check_token_health": "Admin operation",

    # Analysis (requires cross-project or expensive)
    "analyze_project_dimensions": "Expensive analysis, use task_summary instead",
}


# =============================================================================
# Helper functions
# =============================================================================

def get_tool(name: str) -> Optional[ToolDef]:
    """Get tool definition by name."""
    return VIKUNJA_TOOLS.get(name)


def is_allowed(name: str) -> bool:
    """Check if a tool is allowed in Vikunja-native mode."""
    return name in VIKUNJA_TOOLS


def is_excluded(name: str) -> tuple[bool, Optional[str]]:
    """Check if a tool is excluded and get the reason."""
    if name in EXCLUDED_TOOLS:
        return True, EXCLUDED_TOOLS[name]
    return False, None


def needs_confirmation(name: str, item_count: int = 1) -> bool:
    """Check if a tool needs confirmation before execution.

    Args:
        name: Tool name
        item_count: Number of items the operation affects

    Returns:
        True if confirmation required
    """
    tool = VIKUNJA_TOOLS.get(name)
    if not tool:
        return False

    if tool.confirm == ConfirmLevel.ALWAYS:
        return True
    if tool.confirm == ConfirmLevel.COUNT:
        return item_count > tool.confirm_threshold
    return False


def get_tools_by_category(category: ToolCategory) -> list[ToolDef]:
    """Get all tools in a category."""
    return [t for t in VIKUNJA_TOOLS.values() if t.category == category]


def list_all_tools() -> list[str]:
    """Get list of all allowed tool names."""
    return list(VIKUNJA_TOOLS.keys())


# Model tier hierarchy for comparisons (fa-qld6)
TIER_ORDER = {"$": 0, "$$": 1, "$$$": 2}
MODEL_TO_TIER = {
    "haiku": "$",
    "sonnet": "$$",
    "opus": "$$$",
}


def meets_tier_requirement(model: str, min_tier: str) -> bool:
    """Check if a model meets the minimum tier requirement.

    Args:
        model: Model name ("haiku", "sonnet", "opus")
        min_tier: Minimum required tier ("$", "$$", "$$$")

    Returns:
        True if model meets or exceeds the tier requirement

    Bead: fa-qld6
    """
    model_tier = MODEL_TO_TIER.get(model, "$")
    model_level = TIER_ORDER.get(model_tier, 0)
    min_level = TIER_ORDER.get(min_tier, 0)
    return model_level >= min_level


def check_tier_for_tool(name: str, model: str) -> tuple[bool, Optional[str]]:
    """Check if a model can use a tool based on tier requirements.

    Args:
        name: Tool name
        model: Model name ("haiku", "sonnet", "opus")

    Returns:
        Tuple of (allowed, error_message)
        - allowed: True if tool can be used
        - error_message: Explanation if blocked, None if allowed

    Bead: fa-qld6
    """
    tool = VIKUNJA_TOOLS.get(name)
    if not tool:
        return True, None  # Unknown tools pass through

    if meets_tier_requirement(model, tool.min_tier):
        return True, None

    model_tier = MODEL_TO_TIER.get(model, "$")
    return False, (
        f"Tool '{name}' requires {tool.min_tier} tier (Sonnet or better). "
        f"Current model: {model} ({model_tier}). "
        f"Reply with `@eis $$` or `@eis $$$` to upgrade."
    )
