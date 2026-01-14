from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, Optional

@dataclass(frozen=True)
class PromptVersion:
    prompt_id: str
    version: int
    content: Dict[str, Any]
    model: str
    parameters: Dict[str, Any]
    content_hash: str
    created_at: datetime
    response: Optional[Dict[str, Any]] = field(default=None)
    response_ms: Optional[int] = field(default=None)
    cost: Optional[float] = field(default=None)