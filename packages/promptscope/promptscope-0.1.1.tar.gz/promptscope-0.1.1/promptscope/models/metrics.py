from dataclasses import dataclass

@dataclass
class OutputScore:
	execution_id: str
	score_type: str
	value: float
	passed: bool
	details: str

