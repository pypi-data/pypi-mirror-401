from dataclasses import dataclass
from typing import Optional

@dataclass
class ReplayRequest:
    prompt_id: str
    version: int
    target_model: Optional[str] = None
    override_params: Optional[dict] = None
