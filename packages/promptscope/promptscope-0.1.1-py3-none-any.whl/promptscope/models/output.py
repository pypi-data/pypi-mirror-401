from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class PromptExecution:
	execution_id: str
	prompt_id: str
	version: int
	model: str
	parameters: dict
	input_tokens: int
	output_tokens: int
	latency_ms: float
	output: str
	error: Optional[str]
	created_at: datetime
