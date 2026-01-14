"""
PromptScope
-----------

A Python library for prompt observability, versioning, diffing, and replay for LLMs.
"""

from .sdk import (
    autoinstrument,
    track,
    PromptScopeClient,
    track_prompt
)
from .telemetry import initialize, shutdown_telemetry

__all__ = [
    "autoinstrument",
    "track",
    "PromptScopeClient",
    "track_prompt",
    "initialize",
    "shutdown_telemetry"
]
