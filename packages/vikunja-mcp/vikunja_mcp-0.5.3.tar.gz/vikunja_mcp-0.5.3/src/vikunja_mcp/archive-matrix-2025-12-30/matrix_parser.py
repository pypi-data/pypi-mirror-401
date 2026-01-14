"""RapidFuzz command parser for Matrix bot.

Fuzzy command matching with 70+ threshold. Maps natural language
variations to MCP tool names.

Based on research: 1.002 (rapidfuzz discovery)
Spec: analyses/factumerit/28-MVP_SCOPE.md
"""

from rapidfuzz import process, fuzz


# Command aliases -> MCP tool function names
# Keys are natural language variations, values are tool names
# NOTE: Must match keys in TOOL_REGISTRY in server.py
COMMANDS: dict[str, str] = {
    # Task listing (use list_tasks, not list_all_tasks - matches TOOL_REGISTRY)
    "list tasks": "list_tasks",
    "show tasks": "list_tasks",
    "tasks": "list_tasks",
    "my tasks": "list_tasks",
    "what's due": "list_tasks",
    "whats due": "list_tasks",
    "due today": "list_tasks",
    "today": "list_tasks",
    "overdue": "list_tasks",

    # Task creation
    "add": "create_task",
    "add task": "create_task",
    "create task": "create_task",
    "new task": "create_task",
    "todo": "create_task",

    # Task completion
    "done": "complete_task",
    "complete": "complete_task",
    "finish": "complete_task",
    "check": "complete_task",
    "mark done": "complete_task",

    # Task details
    "show": "get_task",
    "get task": "get_task",
    "task details": "get_task",
    "details": "get_task",

    # Task update
    "update": "update_task",
    "edit": "update_task",
    "change": "update_task",
    "modify": "update_task",

    # Task deletion
    "delete": "delete_task",
    "remove": "delete_task",
    "del": "delete_task",

    # Projects
    "projects": "list_projects",
    "list projects": "list_projects",
    "show projects": "list_projects",

    # Labels
    "labels": "list_labels",
    "list labels": "list_labels",
    "tags": "list_labels",

    # Configuration
    "config": "list_instances",
    "config list": "list_instances",
    "instances": "list_instances",
    "config add": "add_instance",
    "connect": "add_instance",
    "config test": "test_connection",
    "test": "test_connection",
    "switch": "switch_instance",
    "use": "switch_instance",

    # Help
    "help": "help",
    "commands": "help",
    "?": "help",
}

# Threshold for fuzzy matching (0-100)
# 80+ = confident match (reduces false positives like "hello" -> "help")
# Below 80 = pass to fallback handler (LLM or "I don't understand")
MATCH_THRESHOLD = 80


def parse_command(user_input: str) -> tuple[str | None, str]:
    """Parse user input into command and arguments.

    Args:
        user_input: Raw message from user

    Returns:
        Tuple of (tool_name, remaining_args) if match found with score >= 70
        Tuple of (None, original_input) if no confident match

    Examples:
        >>> parse_command("whats due today")
        ('list_all_tasks', 'today')

        >>> parse_command("add buy groceries")
        ('create_task', 'buy groceries')

        >>> parse_command("done 42")
        ('complete_task', '42')

        >>> parse_command("hello there")
        (None, 'hello there')
    """
    if not user_input or not user_input.strip():
        return None, user_input

    # Strip whitespace for matching, but preserve original for arg extraction
    input_lower = user_input.lower().strip()
    input_stripped = user_input.strip()

    # First try exact prefix matching for multi-word commands
    # This ensures "config add" beats "config" when input starts with "config add"
    # FIX: Check for word boundaries to avoid "show me" matching "show"
    best_match = None
    best_match_len = 0
    for cmd in COMMANDS.keys():
        # Check if input starts with command followed by space or end of string
        if input_lower == cmd or input_lower.startswith(cmd + " "):
            if len(cmd) > best_match_len:
                best_match = cmd
                best_match_len = len(cmd)

    if best_match:
        # Use stripped input for arg extraction
        args = input_stripped[best_match_len:].strip()
        return COMMANDS[best_match], args

    # Fall back to fuzzy matching for typos
    # Get all matches above threshold, prefer longer matches
    results = process.extract(
        input_lower,
        COMMANDS.keys(),
        scorer=fuzz.WRatio,
        limit=5  # Get top 5 matches
    )

    if not results:
        return None, user_input

    # Filter by threshold and prefer longer matches for same score
    valid_matches = [(match, score) for match, score, _ in results if score >= MATCH_THRESHOLD]
    
    if not valid_matches:
        return None, user_input

    # Sort by score (desc), then by length (desc) for ties
    valid_matches.sort(key=lambda x: (x[1], len(x[0])), reverse=True)
    match, score = valid_matches[0]

    # Extract arguments after the matched command
    match_words = match.split()
    input_words = input_stripped.split()

    # Use word-based extraction for fuzzy matches
    if len(input_words) > len(match_words):
        args = ' '.join(input_words[len(match_words):])
    else:
        args = ""

    return COMMANDS[match], args


def get_command_help() -> str:
    """Return formatted help text listing available commands."""
    # Group commands by tool
    tools: dict[str, list[str]] = {}
    for alias, tool in COMMANDS.items():
        if tool not in tools:
            tools[tool] = []
        tools[tool].append(alias)

    lines = ["**Available Commands:**", ""]

    # ECO mode commands (no AI cost)
    lines.append("**Quick Commands** (free, no AI cost):")
    lines.append("- `!t [search]` - List tasks (or search)")
    lines.append("- `!p [search]` - List projects (or search)")
    lines.append("- `!oops` - Overdue tasks")
    lines.append("- `!now` - Due today")
    lines.append("- `!fire` - Urgent (priority 5)")
    lines.append("- `!vip` - High priority (3+)")
    lines.append("- `!week` - Due this week")
    lines.append("- `!maybe` - Unscheduled")
    lines.append("- `!zen` - Focus mode")
    lines.append("- `!done <title>` - Complete task by name")
    lines.append("- `!stats` - Task summary")
    lines.append("")

    # Cost control & preferences
    lines.append("**Settings:**")
    lines.append("- `!tz` - View/set timezone")
    lines.append("- `!model` - View/change AI model")
    lines.append("- `!credits` - Check usage/remaining credits")
    lines.append("- `!apikey` - Manage your API key")
    lines.append("- `!clear` - Clear conversation memory")
    lines.append("")

    # Connection commands
    lines.append("**Connection:**")
    lines.append("- `!vik <token>` - Connect Vikunja")
    lines.append("- `!viki` - List connections")
    lines.append("- `!novik <name>` - Remove instance")
    lines.append("- `!test` - Test connection")
    lines.append("")

    # Room binding
    lines.append("**Room Binding** (rooms only):")
    lines.append("- `!bind <project>` - Bind room to project")
    lines.append("- `!unbind` - Remove binding")
    lines.append("- `!binding` - Show current binding")
    lines.append("")

    # Instance/Project context
    lines.append("**Context:**")
    lines.append("- `!switch` - View/change Vikunja instance")
    lines.append("- `!project` - View/set active project")
    lines.append("- `!context` - Show current context")
    lines.append("")

    # Last-task commands
    lines.append("**Last Task** (after `!t` returns one task):")
    lines.append("- `^` - Show task details")
    lines.append("- `^done` - Mark complete")
    lines.append("- `^rename <title>` - Rename task")
    lines.append("- `^due <date>` - Set due (tomorrow, friday, 1/15)")
    lines.append("- `^delete` - Delete task")
    lines.append("")

    lines.append("_Or just type naturally - AI handles the rest!_")

    return "\n".join(lines)
