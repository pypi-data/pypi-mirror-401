"""
Command Registry for @eis Smart Tasks.

Single source of truth for all commands. Auto-generates:
- TIER3_COMMANDS dict for CommandParser
- Help documentation for help_handler

To add a new command:
1. Add entry to COMMAND_REGISTRY
2. Implement handler in keyword_handlers.py
3. Add arg extraction in command_parser.py (if needed)

That's it - help auto-updates!

Bead: solutions-6q17
"""

from dataclasses import dataclass, field
from typing import Optional

from .config import is_llm_enabled

# Categories/commands to hide when LLM features are disabled
LLM_CATEGORIES = {"llm", "budget"}
LLM_COMMANDS = {"ears", "model", "grant"}  # Commands that require LLM even if not in LLM category


@dataclass
class CommandDef:
    """Definition for a single command."""
    handler: str                          # Handler method name
    description: str                      # Short description (for overview table)
    usage: str                            # Usage pattern
    aliases: list[str] = field(default_factory=list)  # Command aliases
    examples: list[str] = field(default_factory=list) # Example commands
    notes: Optional[str] = None           # Additional notes
    category: str = "general"             # Category for grouping
    supports_schedule: bool = False       # Can use / schedule syntax
    supports_project: bool = False        # Can use | project syntax


# =============================================================================
# COMMAND REGISTRY - Single source of truth
# =============================================================================

COMMAND_REGISTRY: dict[str, CommandDef] = {
    # -------------------------------------------------------------------------
    # Info Commands (weather, stock, news)
    # -------------------------------------------------------------------------
    "weather": CommandDef(
        handler="weather_handler",
        description="Get weather for a location",
        usage="!w <location> [hourly|6h]",
        aliases=["!weather", "!w"],
        examples=[
            "@eis !w Tokyo",
            "@eis !w Seattle hourly",
            "@eis !w NYC every day +Dashboard",
        ],
        notes="Sub-daily: hourly, 1h, 2h, 4h, 6h, 12h. Daily+: use Vikunja's 'every day' syntax.",
        category="info",
        supports_schedule=True,
        supports_project=True,
    ),

    # DISABLED: Stock command - API rate limits (solutions-js3e)
    # "stock": CommandDef(
    #     handler="stock_handler",
    #     description="Get stock quote",
    #     usage="!s <TICKER> [hourly|6h]",
    #     aliases=["!stock", "!s"],
    #     examples=[
    #         "@eis !s AAPL",
    #         "@eis !s TSLA 4h",
    #         "@eis !s NVDA every day +Investments",
    #     ],
    #     notes="Sub-daily: hourly, 1h, 2h, 4h, 6h, 12h. Daily+: use Vikunja's 'every day' syntax.",
    #     category="info",
    #     supports_schedule=True,
    #     supports_project=True,
    # ),

    # DISABLED: News command - unreliable API (solutions-4sni)
    # "news": CommandDef(
    #     handler="news_handler",
    #     description="Get news headlines",
    #     usage="!n <query> or !n cat:<category>",
    #     aliases=["!news", "!n", "!headlines"],
    #     examples=[
    #         "@eis !n technology",
    #         "@eis !n cat:business",
    #         "@eis !n AI | News Feed",
    #     ],
    #     notes="Categories: business, entertainment, general, health, science, sports, technology",
    #     category="info",
    #     supports_schedule=False,
    #     supports_project=True,
    # ),

    "rss": CommandDef(
        handler="rss_handler",
        description="Fetch RSS/Atom feed",
        usage="!rss <url> [hourly|6h]",
        aliases=["!rss", "!feed"],
        examples=[
            "@eis !rss https://blog.example.com/feed.xml",
            "@eis !rss https://hnrss.org/frontpage 6h",
            "@eis !feed https://xkcd.com/rss.xml every day +Comics",
        ],
        notes="Sub-daily: hourly, 1h, 2h, 4h, 6h, 12h. Daily+: use Vikunja's 'every day' syntax.",
        category="info",
        supports_schedule=True,
        supports_project=True,
    ),

    # -------------------------------------------------------------------------
    # Action Commands
    # -------------------------------------------------------------------------
    "complete": CommandDef(
        handler="complete_task",
        description="Mark task(s) as complete",
        usage="!x <task_id> [task_id...]",
        aliases=["!complete", "!done", "!do", "!x"],
        examples=[
            "@eis !x 42",
            "@eis !done 123",
            "@eis !x 1 2 3",
        ],
        notes="Adds completion comment to target task. Command task is auto-deleted.",
        category="action",
    ),

    "delete": CommandDef(
        handler="delete_handler",
        description="Delete task(s) - project-scoped",
        usage="!delete [all|<id>|done]",
        aliases=["!delete", "!del", "!rm"],
        examples=[
            "@eis !delete",
            "@eis !delete all",
            "@eis !delete 42",
            "@eis !delete done",
        ],
        notes="Project-scoped for safety. 'all' deletes all tasks in current project. 'done' deletes completed tasks.",
        category="action",
    ),

    "remind": CommandDef(
        handler="set_reminder",
        description="Set a reminder (coming soon)",
        usage="!r <task_id> / <when>",
        aliases=["!remind", "!reminder", "!r"],
        examples=[
            "@eis !r 42 / tomorrow 3pm",
            "@eis !remind 123 / in 2 hours",
        ],
        notes="⚠️ Not yet implemented. Coming in Phase 2.",
        category="action",
    ),

    # -------------------------------------------------------------------------
    # AI/LLM Commands
    # -------------------------------------------------------------------------
    "llm": CommandDef(
        handler="llm_natural",
        description="AI-powered task creation",
        usage="$ <request> or $$ <request> or $$$ <request>",
        aliases=["$", "$$", "$$$"],
        examples=[
            "@eis $ plan a birthday party",
            "@eis $$ write a project proposal",
            "@eis $$$ create a detailed business plan",
        ],
        notes="Cost tiers: $ (3 calls), $$ (10 calls), $$$ (25 calls). Reply with @eis to refine.",
        category="llm",
    ),

    "llm_context": CommandDef(
        handler="llm_context",
        description="AI analysis of existing task",
        usage="$$ <task_id> / <instruction>",
        aliases=[],  # Uses $ prefix, handled specially
        examples=[
            "@eis $$ 42 / summarize comments",
            "@eis $$ 123 / suggest next steps",
        ],
        notes="Analyzes task content and comments with AI.",
        category="llm",
    ),

    # -------------------------------------------------------------------------
    # Budget Commands
    # -------------------------------------------------------------------------
    "upgrade": CommandDef(
        handler="upgrade_tier",
        description="Upgrade AI budget tier",
        usage="!upgrade <tier>",
        aliases=["!upgrade"],
        examples=[
            "@eis !upgrade $$",
            "@eis !upgrade $$$",
        ],
        notes="Use on a smart task to increase its LLM call budget.",
        category="budget",
    ),

    "reset": CommandDef(
        handler="reset_budget",
        description="Reset task's LLM counter (admin only)",
        usage="!reset",
        aliases=["!reset-budget", "!reset"],
        examples=[
            "@eis !reset",
        ],
        notes="Admin only. Resets task-level display counter (not user credit).",
        category="budget",
    ),

    "balance": CommandDef(
        handler="balance_handler",
        description="Check your AI credit balance",
        usage="!balance",
        aliases=["!balance", "!bal", "!credit"],
        examples=[
            "@eis !balance",
            "@eis !bal",
        ],
        notes="Shows remaining AI credit. New users get $1.00.",
        category="budget",
    ),

    "grant": CommandDef(
        handler="grant_credit",
        description="Grant AI credit to a user (admin only)",
        usage="!grant [username] $amount",
        aliases=["!grant", "!addcredit"],
        examples=[
            "@eis !grant $5",
            "@eis !grant ivan $10",
            "@eis !grant $10 ivan",
        ],
        notes="Admin only. Order flexible - 'ivan $5' or '$5 ivan'. Omit username to grant to self.",
        category="admin",
    ),

    # -------------------------------------------------------------------------
    # Meta Commands
    # -------------------------------------------------------------------------
    "model": CommandDef(
        handler="model_handler",
        description="Show AI models and capabilities",
        usage="!model [haiku|sonnet|opus]",
        aliases=["!model", "!models", "!ai"],
        examples=[
            "@eis !model",
            "@eis !model sonnet",
        ],
        notes="Shows available AI models, their strengths, and how to use them with $/$$/$$$ prefixes.",
        category="meta",
    ),

    "help": CommandDef(
        handler="help_handler",
        description="Show detailed help documentation",
        usage="!help [topic]",
        aliases=["!help", "!?"],
        examples=[
            "@eis !help",
            "@eis !help weather",
            "@eis !? schedule",
        ],
        notes="Verbose help. Topics: weather, stock, news, complete, llm, schedule, project, budget",
        category="meta",
    ),

    "cheatsheet": CommandDef(
        handler="cheatsheet_handler",
        description="Quick command reference card",
        usage="!h",
        aliases=["!h", "!quick", "!q"],
        examples=[
            "@eis !h",
            "@eis !quick",
        ],
        notes="Condensed command reference. Use !help for detailed docs.",
        category="meta",
    ),

    "whoami": CommandDef(
        handler="whoami_handler",
        description="Show your bot's username and display name",
        usage="!whoami",
        aliases=["!whoami", "!botinfo"],
        examples=[
            "@eis !whoami",
            "@eis !botinfo",
        ],
        notes="Shows your personal bot's username (for @mentions) and display name.",
        category="meta",
    ),

    # NOTE: !find reserved for smart search (solutions-lcit)
    # Will be: @eis !find devops → persistent saved search task

    # -------------------------------------------------------------------------
    # Ears Mode (renamed from capture - solutions-bx4t)
    # -------------------------------------------------------------------------
    "ears": CommandDef(
        handler="ears_handler",
        description="Listen to all new tasks in project",
        usage="!ears on|off",
        aliases=["!ears", "!listen"],
        examples=[
            "@eis !ears on",
            "@eis !ears off",
        ],
        notes="When on, @eis listens and processes all new tasks in this project without needing @mention.",
        category="meta",
    ),

    # -------------------------------------------------------------------------
    # Project Management
    # -------------------------------------------------------------------------
    "project": CommandDef(
        handler="project_handler",
        description="Manage projects (add/delete/rename)",
        usage="!project add|delete|rename <name> [to <target>]",
        aliases=["!project", "!proj", "!p"],
        examples=[
            "@eis !project add Ukulele to Music",
            "@eis !project add Travel",
            "@eis !project delete Ukulele",
            "@eis !project rename Music to Music Practice",
        ],
        notes="Uses 'to' for natural syntax. Fuzzy matches project names.",
        category="action",
    ),

    # -------------------------------------------------------------------------
    # Sharing Commands
    # -------------------------------------------------------------------------
    "share": CommandDef(
        handler="share_handler",
        description="Generate public share links for project",
        usage="!share [project_name]",
        aliases=["!share"],
        examples=[
            "@eis !share",
            "@eis !share Dashboard",
            "@eis !share Music",
        ],
        notes="Creates read-only share links for each project view. Links work without Vikunja account.",
        category="action",
    ),

    # -------------------------------------------------------------------------
    # Setup Commands
    # -------------------------------------------------------------------------
    "token": CommandDef(
        handler="token_handler",
        description="Generate MCP config for Claude Desktop",
        usage="!token",
        aliases=["!token", "!mcp", "!claude"],
        examples=[
            "@eis !token",
            "@eis !mcp",
        ],
        notes="Generates ready-to-paste JSON config for Claude Desktop's claude_desktop_config.json file.",
        category="meta",
    ),
}


# =============================================================================
# Auto-generated dictionaries
# =============================================================================

def build_tier3_commands() -> dict[str, str]:
    """Build TIER3_COMMANDS dict from registry."""
    commands = {}
    for name, cmd in COMMAND_REGISTRY.items():
        # Skip LLM commands (handled separately with $ prefix)
        if cmd.category == "llm":
            continue
        for alias in cmd.aliases:
            commands[alias] = cmd.handler
    return commands


def build_help_overview() -> str:
    """Generate help overview from registry."""
    llm_enabled = is_llm_enabled()

    lines = [
        "# @eis Command Reference",
        "",
        "**@eis** is your smart task assistant. Mention @eis in a task title to trigger commands.",
        "",
        "## Quick Reference",
        "",
        "| Command | Description |",
        "|---------|-------------|",
    ]

    # Group by category, show primary alias only
    seen_handlers = set()
    for name, cmd in COMMAND_REGISTRY.items():
        if cmd.handler in seen_handlers:
            continue
        # Skip LLM-related commands when LLM is disabled
        if not llm_enabled:
            if cmd.category in LLM_CATEGORIES or name in LLM_COMMANDS:
                continue
        seen_handlers.add(cmd.handler)
        primary = cmd.aliases[0] if cmd.aliases else f"!{name}"
        lines.append(f"| `{cmd.usage}` | {cmd.description} |")

    lines.extend([
        "",
        "## Syntax Modifiers",
        "",
        "- **`| project`** - Create task in specific project: `@eis !w Tokyo | Dashboard`",
        "- **`/ schedule`** - Auto-update schedule: `@eis !w Tokyo / hourly`",
        "",
        "## Help Topics",
        "",
        "Type `@eis !help <topic>` for details:",
        "",  # Blank line needed before list
    ])

    # List topics - skip LLM-related ones when disabled
    excluded = {"help", "llm_context"}
    if not llm_enabled:
        excluded.update(LLM_COMMANDS)
        excluded.update(name for name, cmd in COMMAND_REGISTRY.items() if cmd.category in LLM_CATEGORIES)
    topics = sorted(set(COMMAND_REGISTRY.keys()) - excluded)
    for topic in topics:
        cmd = COMMAND_REGISTRY[topic]
        lines.append(f"- `{topic}` - {cmd.description}")

    lines.extend([
        "- `schedule` - Auto-update schedule options",
        "- `project` - Target project syntax",
    ])
    # Only show budget topic when LLM is enabled
    if llm_enabled:
        lines.append("- `budget` - AI credit and billing")
    lines.append("")  # Blank line after list

    return "\n".join(lines)


def build_help_topic(topic: str) -> Optional[str]:
    """Generate help for a specific topic."""
    llm_enabled = is_llm_enabled()

    # Handle special topics
    if topic == "schedule":
        return _build_schedule_help()
    if topic == "project":
        return _build_project_help()
    if topic in ("budget", "credit", "balance"):
        # Budget topics require LLM features
        if not llm_enabled:
            return None
        return _build_budget_help()

    # Look up in registry
    cmd = COMMAND_REGISTRY.get(topic)
    if not cmd:
        return None

    # Hide LLM-related topics when disabled
    if not llm_enabled:
        if cmd.category in LLM_CATEGORIES or topic in LLM_COMMANDS:
            return None

    lines = [
        f"# {topic.title()} Commands",
        "",
        cmd.description,
        "",
        "## Usage",
        "",
        f"```",
        cmd.usage,
        "```",
        "",
    ]

    if cmd.aliases:
        lines.extend([
            "**Aliases:** " + ", ".join(f"`{a}`" for a in cmd.aliases),
            "",
        ])

    if cmd.examples:
        lines.extend([
            "## Examples",
            "",
        ])
        for ex in cmd.examples:
            lines.append(f"- `{ex}`")
        lines.append("")

    if cmd.supports_schedule or cmd.supports_project:
        lines.append("## Modifiers")
        lines.append("")
        if cmd.supports_project:
            lines.append("- **Target project:** `@eis " + cmd.usage.split()[0] + " ... | ProjectName`")
        if cmd.supports_schedule:
            lines.append("- **Auto-update:** `@eis " + cmd.usage.split()[0] + " ... / hourly`")
        lines.append("")

    if cmd.notes:
        lines.extend([
            "## Notes",
            "",
            cmd.notes,
        ])

    return "\n".join(lines)


def _build_schedule_help() -> str:
    """Build schedule topic help."""
    return """# Auto-Update Schedules

Make tasks automatically refresh on a schedule.

## Syntax

```
@eis !w <location> / <schedule>
@eis !s <ticker> / <schedule>
```

## Schedule Options

| Schedule | Meaning |
|----------|---------|
| `hourly` | Every hour |
| `daily` | Once per day |
| `6h` | Every 6 hours |
| `12h` | Every 12 hours |
| `weekly` | Once per week |

## Examples

- `@eis !w Tokyo / hourly` - Weather every hour
- `@eis !s AAPL / daily` - Stock quote daily
- `@eis !w NYC / 6h` - Weather every 6 hours

## How It Works

1. Task is created with initial data
2. Scheduler refreshes content on schedule
3. Task description updates automatically
4. Manual refresh: click "Refresh" link in task"""


def _build_project_help() -> str:
    """Build project topic help."""
    return """# Target Project Syntax

Create tasks in a specific project using `| project_name`.

## Syntax

```
@eis <command> | <project_name>
```

## Examples

- `@eis !w Tokyo | Dashboard`
- `@eis !s AAPL | Investments`
- `@eis !n tech | News Feed`
- `@eis $ plan vacation | Travel`

## Fuzzy Matching

Project names are fuzzy-matched:
- `| dash` matches "Dashboard"
- `| invest` matches "Investments"
- `| inbox` matches "Inbox"

## Multiple Matches

If multiple projects match, you'll see clickable links to choose.

## Combined with Schedule

```
@eis !w Seattle / hourly | Weather Board
```"""


def _build_budget_help() -> str:
    """Build budget/credit topic help."""
    return """# AI Credit & Budget

@eis uses AI (Claude) to understand natural language requests. Each AI call costs a small amount.

## Your Balance

Check your credit anytime:
```
@eis !balance
```

## How Billing Works

| Action | Cost |
|--------|------|
| ! commands (`!weather`, `!stock`, etc.) | **FREE** |
| Natural language (`@eis what's overdue?`) | ~$0.01-0.05 per request |
| Complex tasks (multiple tool calls) | ~$0.05-0.15 per request |

## Initial Credit

New users receive **$1.00** free credit - enough for dozens of AI requests.

## When Credit Runs Out

- AI commands will show "Out of AI credit"
- **! commands still work** (weather, stocks, news, RSS, etc.)
- Contact support to add more credit

## Commands

| Command | Description |
|---------|-------------|
| `!balance` | Check your current balance |
| `!bal` | Short alias for balance |
| `!credit` | Another alias for balance |

## Cost Display

After each AI response, you'll see:
```
~$0.02 | Balance: $0.85
```

This shows the cost of that request and your remaining balance.

## Tips to Save Credit

1. Use `!` commands when possible - they're free!
2. Be specific in requests to reduce back-and-forth
3. Use `!c` cheatsheet to find the right command"""


# Pre-build for import
TIER3_COMMANDS = build_tier3_commands()
