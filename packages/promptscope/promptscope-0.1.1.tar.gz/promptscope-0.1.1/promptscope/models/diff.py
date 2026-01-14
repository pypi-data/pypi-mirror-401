from dataclasses import dataclass
from typing import List

@dataclass
class PromptDiff:
    prompt_id: str
    from_version: int
    to_version: int
    added: List[str]
    removed: List[str]
    modified: List[str]

    added: List[str]
    removed: List[str]
    modified: List[str]
