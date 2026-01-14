"""
Metadata Manager for @eis Smart Tasks.

Handles metadata in task descriptions for:
- Smart task identification
- Cost tier tracking
- Budget enforcement
- Schedule configuration

Supports two formats:
1. YAML frontmatter (for markdown descriptions)
2. HTML comment (for HTML descriptions): <!-- eis-meta: {...} -->

Based on: docs/factumerit/083-SMART_TASKS_DESIGN.md
Bead: solutions-hgwx.2
"""

import json
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

import yaml


# Cost tier configuration
COST_TIERS = {
    "$": {"max_calls": 30, "cost_per_call": 0.01, "max_budget": 0.30},
    "$$": {"max_calls": 150, "cost_per_call": 0.01, "max_budget": 1.50},
    "$$$": {"max_calls": 600, "cost_per_call": 0.01, "max_budget": 6.00},
}


@dataclass
class SmartTaskMetadata:
    """Metadata for a smart task stored in YAML frontmatter."""

    # Core identification
    smart_task: bool = True
    keyword: Optional[str] = None  # e.g., "weather", "stock", "news"

    # Cost tracking
    cost_tier: str = "$"  # "$", "$$", "$$$"
    llm_calls_used: int = 0
    llm_calls_limit: int = 30
    total_cost: float = 0.0

    # Task configuration
    prompt: Optional[str] = None  # Original user prompt
    schedule: Optional[str] = None  # e.g., "every morning at 6:30"
    handler_args: Optional[dict] = None  # Args for refresh (e.g., {"location": "Seattle"})

    # Timestamps
    created_at: Optional[str] = None
    last_updated: Optional[str] = None

    # Extra fields for extensibility
    extra: dict = field(default_factory=dict)

    def __post_init__(self):
        """Set defaults based on cost tier."""
        if self.cost_tier in COST_TIERS:
            tier_config = COST_TIERS[self.cost_tier]
            if self.llm_calls_limit == 30:  # Only set if using default
                self.llm_calls_limit = tier_config["max_calls"]

        if not self.created_at:
            self.created_at = datetime.now(timezone.utc).isoformat()

    @property
    def budget_remaining(self) -> int:
        """Return number of LLM calls remaining."""
        return max(0, self.llm_calls_limit - self.llm_calls_used)

    @property
    def budget_exhausted(self) -> bool:
        """Check if budget is exhausted."""
        return self.llm_calls_used >= self.llm_calls_limit

    @property
    def budget_percent_used(self) -> float:
        """Return percentage of budget used."""
        if self.llm_calls_limit == 0:
            return 100.0
        return (self.llm_calls_used / self.llm_calls_limit) * 100

    def increment_usage(self, calls: int = 1) -> bool:
        """Increment LLM usage counter.

        Args:
            calls: Number of calls to add

        Returns:
            True if increment succeeded (within budget), False if budget would be exceeded
        """
        if self.llm_calls_used + calls > self.llm_calls_limit:
            return False

        self.llm_calls_used += calls
        tier_config = COST_TIERS.get(self.cost_tier, COST_TIERS["$"])
        self.total_cost = self.llm_calls_used * tier_config["cost_per_call"]
        self.last_updated = datetime.now(timezone.utc).isoformat()
        return True

    def upgrade_tier(self, new_tier: str) -> bool:
        """Upgrade to a higher cost tier.

        Args:
            new_tier: New cost tier ("$", "$$", "$$$")

        Returns:
            True if upgrade succeeded, False if invalid tier
        """
        if new_tier not in COST_TIERS:
            return False

        tier_config = COST_TIERS[new_tier]
        self.cost_tier = new_tier
        self.llm_calls_limit = tier_config["max_calls"]
        self.last_updated = datetime.now(timezone.utc).isoformat()
        return True

    def reset_budget(self):
        """Reset the budget counter (for monthly resets or manual reset)."""
        self.llm_calls_used = 0
        self.total_cost = 0.0
        self.last_updated = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> dict:
        """Convert to dictionary for YAML serialization."""
        data = {
            "smart_task": self.smart_task,
            "cost_tier": self.cost_tier,
            "llm_calls_used": self.llm_calls_used,
            "llm_calls_limit": self.llm_calls_limit,
            "total_cost": round(self.total_cost, 2),
        }

        # Optional fields
        if self.keyword:
            data["keyword"] = self.keyword
        if self.prompt:
            data["prompt"] = self.prompt
        if self.schedule:
            data["schedule"] = self.schedule
        if self.handler_args:
            data["handler_args"] = self.handler_args
        if self.created_at:
            data["created_at"] = self.created_at
        if self.last_updated:
            data["last_updated"] = self.last_updated
        if self.extra:
            data.update(self.extra)

        return data

    @classmethod
    def from_dict(cls, data: dict) -> "SmartTaskMetadata":
        """Create from dictionary (YAML parsed data)."""
        known_keys = {
            "smart_task", "keyword", "cost_tier", "llm_calls_used",
            "llm_calls_limit", "total_cost", "prompt", "schedule",
            "handler_args", "created_at", "last_updated"
        }

        extra = {k: v for k, v in data.items() if k not in known_keys}

        return cls(
            smart_task=data.get("smart_task", True),
            keyword=data.get("keyword"),
            cost_tier=data.get("cost_tier", "$"),
            llm_calls_used=data.get("llm_calls_used", 0),
            llm_calls_limit=data.get("llm_calls_limit", 30),
            total_cost=data.get("total_cost", 0.0),
            prompt=data.get("prompt"),
            schedule=data.get("schedule"),
            handler_args=data.get("handler_args"),
            created_at=data.get("created_at"),
            last_updated=data.get("last_updated"),
            extra=extra,
        )


class MetadataManager:
    """Manage YAML frontmatter in task descriptions.

    Usage:
        manager = MetadataManager()

        # Extract metadata from description
        metadata, content = manager.extract(description)

        # Update metadata
        metadata.increment_usage()

        # Rebuild description with updated metadata
        new_description = manager.format(metadata, content)
    """

    # Pattern for HTML comment metadata: <!-- eis-meta: {...} -->
    HTML_META_PATTERN = re.compile(
        r'<!--\s*eis-meta:\s*(\{.*?\})\s*-->',
        re.DOTALL
    )

    # Pattern for hidden div: <div ... data-eis-meta='{...}'>
    DIV_META_PATTERN = re.compile(
        r'<div[^>]*data-eis-meta=[\'"](\{.*?\})[\'"][^>]*>',
        re.DOTALL
    )

    # Pattern for plaintext code: [eis:keyword:$:5/30:base64args] or legacy [eis:$:5/30]
    # New format: [eis:weather:$:0/30:eyJsb2NhdGlvbiI6IlRva3lvIn0]
    # Legacy format: [eis:$:0/30]
    CODE_META_PATTERN = re.compile(
        r'\[eis:(\w*):(\$+):(\d+)/(\d+)(?::([A-Za-z0-9_-]+))?\]'
    )
    CODE_META_LEGACY_PATTERN = re.compile(
        r'\[eis:(\$+):(\d+)/(\d+)\]'
    )

    @staticmethod
    def extract(description: str) -> tuple[Optional[SmartTaskMetadata], str]:
        """Extract metadata from description (tries multiple formats).

        Args:
            description: Task description (may include metadata)

        Returns:
            Tuple of (metadata or None, content without metadata)
        """
        if not description:
            return None, ""

        description = description.strip()

        # Try HTML comment format
        html_result = MetadataManager._extract_html(description)
        if html_result[0] is not None:
            return html_result

        # Try hidden div format
        div_result = MetadataManager._extract_div(description)
        if div_result[0] is not None:
            return div_result

        # Try plaintext code format
        code_result = MetadataManager._extract_code(description)
        if code_result[0] is not None:
            return code_result

        # Try YAML frontmatter (for markdown descriptions)
        return MetadataManager._extract_yaml(description)

    @staticmethod
    def _extract_html(description: str) -> tuple[Optional[SmartTaskMetadata], str]:
        """Extract metadata from HTML comment.

        Format: <!-- eis-meta: {"smart_task": true, ...} -->
        """
        match = MetadataManager.HTML_META_PATTERN.search(description)
        if not match:
            return None, description

        try:
            data = json.loads(match.group(1))
            if not isinstance(data, dict) or not data.get("smart_task"):
                return None, description

            metadata = SmartTaskMetadata.from_dict(data)
            # Remove the metadata comment from content
            content = description[:match.start()] + description[match.end():]
            content = content.strip()
            return metadata, content

        except json.JSONDecodeError:
            return None, description

    @staticmethod
    def _extract_div(description: str) -> tuple[Optional[SmartTaskMetadata], str]:
        """Extract metadata from hidden div with data attribute."""
        match = MetadataManager.DIV_META_PATTERN.search(description)
        if not match:
            return None, description

        try:
            data = json.loads(match.group(1))
            if not isinstance(data, dict) or not data.get("smart_task"):
                return None, description

            metadata = SmartTaskMetadata.from_dict(data)
            # Remove the div from content
            content = description[:match.start()] + description[match.end():]
            # Also remove closing </div> if present
            content = re.sub(r'</div>\s*', '', content, count=1)
            content = content.strip()
            return metadata, content

        except json.JSONDecodeError:
            return None, description

    @staticmethod
    def _extract_code(description: str) -> tuple[Optional[SmartTaskMetadata], str]:
        """Extract metadata from plaintext code.

        New format: [eis:weather:$:0/30:base64args]
        Legacy format: [eis:$:0/30]
        """
        import base64

        # Try new format first: [eis:keyword:tier:used/limit:args]
        match = MetadataManager.CODE_META_PATTERN.search(description)
        if match:
            keyword = match.group(1) or None  # Can be empty string
            cost_tier = match.group(2)  # $, $$, or $$$
            llm_calls_used = int(match.group(3))
            llm_calls_limit = int(match.group(4))
            args_b64 = match.group(5)  # Optional base64 args

            # Decode handler_args if present
            handler_args = None
            if args_b64:
                try:
                    # Add padding back for base64 decode
                    padded = args_b64 + '=' * (4 - len(args_b64) % 4)
                    args_json = base64.urlsafe_b64decode(padded).decode()
                    handler_args = json.loads(args_json)
                except (ValueError, json.JSONDecodeError):
                    pass  # Invalid base64 or JSON, ignore

            metadata = SmartTaskMetadata(
                smart_task=True,
                keyword=keyword,
                cost_tier=cost_tier,
                llm_calls_used=llm_calls_used,
                llm_calls_limit=llm_calls_limit,
                handler_args=handler_args,
            )

            # Remove the code from content
            content = re.sub(r'<p>\s*<small>\s*\[eis:[^\]]+\]\s*</small>\s*</p>', '', description)
            content = re.sub(r'\[eis:[^\]]+\]', '', content)
            content = content.strip()
            return metadata, content

        # Try legacy format: [eis:$:0/30]
        legacy_match = MetadataManager.CODE_META_LEGACY_PATTERN.search(description)
        if legacy_match:
            cost_tier = legacy_match.group(1)
            llm_calls_used = int(legacy_match.group(2))
            llm_calls_limit = int(legacy_match.group(3))

            metadata = SmartTaskMetadata(
                smart_task=True,
                cost_tier=cost_tier,
                llm_calls_used=llm_calls_used,
                llm_calls_limit=llm_calls_limit,
            )

            content = re.sub(r'<p>\s*<small>\s*\[eis:[^\]]+\]\s*</small>\s*</p>', '', description)
            content = re.sub(r'\[eis:[^\]]+\]', '', content)
            content = content.strip()
            return metadata, content

        return None, description

    @staticmethod
    def _extract_yaml(description: str) -> tuple[Optional[SmartTaskMetadata], str]:
        """Extract metadata from YAML frontmatter."""
        if not description.startswith("---"):
            return None, description

        # Find end of frontmatter
        parts = description.split("---", 2)
        if len(parts) < 3:
            return None, description

        yaml_content = parts[1].strip()
        content = parts[2].strip()

        try:
            data = yaml.safe_load(yaml_content)
            if not isinstance(data, dict):
                return None, description

            # Check if it's a smart task
            if not data.get("smart_task"):
                return None, description

            metadata = SmartTaskMetadata.from_dict(data)
            return metadata, content

        except yaml.YAMLError:
            return None, description

    @staticmethod
    def format(metadata: SmartTaskMetadata, content: str) -> str:
        """Format metadata and content as task description (YAML frontmatter).

        Args:
            metadata: SmartTaskMetadata instance
            content: Task content (without frontmatter)

        Returns:
            Full description with YAML frontmatter
        """
        yaml_content = yaml.dump(
            metadata.to_dict(),
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
        )

        return f"---\n{yaml_content}---\n\n{content}"

    @staticmethod
    def format_html(metadata: SmartTaskMetadata, html_content: str) -> str:
        """Format metadata and content as HTML description.

        Embeds metadata as plaintext code (survives Vikunja HTML processing).
        NOTE: HTML comments and hidden divs are stripped by Vikunja!

        Format: [eis:KEYWORD:TIER:USED/LIMIT:ARGS_JSON]
        - KEYWORD: weather, stock, news, etc (or empty)
        - TIER: $, $$, $$$
        - USED/LIMIT: LLM call counts
        - ARGS_JSON: URL-safe base64 encoded JSON (optional)

        Args:
            metadata: SmartTaskMetadata instance
            html_content: HTML content (task response)

        Returns:
            HTML with embedded metadata code
        """
        import base64

        keyword = metadata.keyword or ""

        # Encode handler_args as base64 JSON (URL-safe, no padding)
        args_part = ""
        if metadata.handler_args:
            args_json = json.dumps(metadata.handler_args, separators=(',', ':'))
            args_b64 = base64.urlsafe_b64encode(args_json.encode()).decode().rstrip('=')
            args_part = f":{args_b64}"

        # Format: [eis:keyword:tier:used/limit:args]
        meta_code = f"[eis:{keyword}:{metadata.cost_tier}:{metadata.llm_calls_used}/{metadata.llm_calls_limit}{args_part}]"

        return f"{html_content}\n<p><small>{meta_code}</small></p>"

    @staticmethod
    def create_initial(
        cost_tier: str,
        prompt: str,
        keyword: Optional[str] = None,
        schedule: Optional[str] = None,
        handler_args: Optional[dict] = None,
    ) -> SmartTaskMetadata:
        """Create initial metadata for a new smart task.

        Args:
            cost_tier: Cost tier ("$", "$$", "$$$")
            prompt: Original user prompt
            keyword: Optional keyword (e.g., "weather")
            schedule: Optional schedule string
            handler_args: Optional args for refresh (e.g., {"location": "Seattle"})

        Returns:
            SmartTaskMetadata instance with defaults set
        """
        tier_config = COST_TIERS.get(cost_tier, COST_TIERS["$"])

        return SmartTaskMetadata(
            smart_task=True,
            keyword=keyword,
            cost_tier=cost_tier,
            llm_calls_used=0,
            llm_calls_limit=tier_config["max_calls"],
            total_cost=0.0,
            prompt=prompt,
            schedule=schedule,
            handler_args=handler_args,
            created_at=datetime.now(timezone.utc).isoformat(),
        )

    @staticmethod
    def format_budget_warning(metadata: SmartTaskMetadata) -> str:
        """Format a budget exhaustion warning message.

        Args:
            metadata: SmartTaskMetadata with exhausted budget

        Returns:
            Warning message with upgrade options
        """
        return (
            f"Budget exhausted ({metadata.llm_calls_used}/{metadata.llm_calls_limit} calls, "
            f"${metadata.total_cost:.2f}).\n\n"
            f"**Options:**\n"
            f"1. Upgrade tier: `@eis !upgrade $$`\n"
            f"2. Reset counter: `@eis !reset-budget`\n"
            f"3. Disable auto-update: `@eis !disable`"
        )

    @staticmethod
    def format_cost_footer(metadata: SmartTaskMetadata) -> str:
        """Format cost tracking footer for task description.

        Args:
            metadata: SmartTaskMetadata instance

        Returns:
            Formatted footer with cost info
        """
        lines = []

        if metadata.last_updated:
            lines.append(f"*Last updated: {metadata.last_updated}*")

        lines.append(
            f"*LLM calls: {metadata.llm_calls_used}/{metadata.llm_calls_limit} "
            f"(${metadata.total_cost:.2f})*"
        )

        if metadata.budget_percent_used >= 80:
            remaining = metadata.budget_remaining
            lines.append(f"**{remaining} calls remaining**")

        return "\n".join(lines)

    # =========================================================================
    # Attachment-based metadata storage
    # =========================================================================

    METADATA_FILENAME = ".eis-meta.yaml"

    @staticmethod
    def to_yaml_bytes(metadata: SmartTaskMetadata) -> bytes:
        """Convert metadata to YAML bytes for attachment storage.

        Args:
            metadata: SmartTaskMetadata instance

        Returns:
            YAML content as bytes
        """
        yaml_content = yaml.dump(
            metadata.to_dict(),
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
        )
        return yaml_content.encode("utf-8")

    @staticmethod
    def from_yaml_bytes(content: bytes) -> Optional[SmartTaskMetadata]:
        """Parse metadata from YAML bytes.

        Args:
            content: YAML content as bytes

        Returns:
            SmartTaskMetadata or None if invalid
        """
        try:
            data = yaml.safe_load(content.decode("utf-8"))
            if not isinstance(data, dict) or not data.get("smart_task"):
                return None
            return SmartTaskMetadata.from_dict(data)
        except (yaml.YAMLError, UnicodeDecodeError):
            return None

    @staticmethod
    def find_metadata_attachment(attachments: list[dict]) -> Optional[int]:
        """Find the metadata attachment ID from a list of attachments.

        Args:
            attachments: List of attachment objects from Vikunja

        Returns:
            Attachment ID if found, None otherwise
        """
        for att in attachments:
            if att.get("file", {}).get("name") == MetadataManager.METADATA_FILENAME:
                return att.get("id")
        return None
