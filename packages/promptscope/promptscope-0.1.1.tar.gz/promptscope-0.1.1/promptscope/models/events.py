from dataclasses import dataclass
from datetime import datetime

@dataclass
class DriftEvent:
    prompt_id: str
    from_version: int
    to_version: int

    metric: str
    severity: str     # low | medium | high
    description: str
    created_at: datetime
