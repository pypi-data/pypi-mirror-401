"""
Configuration helpers for vikunja-mcp.

Bead: fa-86im
"""

import os


def is_llm_enabled() -> bool:
    """Check if LLM features are enabled.

    LLM features ($, $, $$, natural language, !ears) are gated behind
    this flag. When disabled, natural language is fuzzy-matched to ! commands.

    Default: False (disabled for API cost reasons, pending local LLM)
    """
    return os.environ.get("ENABLE_LLM_FEATURES", "").lower() in ("true", "1", "yes")
