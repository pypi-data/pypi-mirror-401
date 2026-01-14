from typing import Any, Dict, TypedDict


class ScoreResult(TypedDict, total=False):
	score_type: str
	value: float
	passed: bool
	details: Dict[str, Any]
	reason: str


def score_length(output: str, max_len: int = 1000, min_len: int = 0) -> ScoreResult:
	"""
	Simple length-based quality score with optional min/max bounds.
	Returns normalized value (0-1), pass flag, and metadata.
	"""
	if max_len <= 0:
		raise ValueError("max_len must be positive")
	if min_len < 0:
		raise ValueError("min_len cannot be negative")
	if min_len > max_len:
		raise ValueError("min_len cannot exceed max_len")

	length = len(output or "")
	passed = min_len <= length <= max_len
	if length <= max_len:
		value = min(1.0, length / max_len)
	else:
		over_ratio = (length - max_len) / max_len
		value = max(0.0, 1 - over_ratio)

	reason = "within_bounds" if passed else ("too_short" if length < min_len else "too_long")
	return {
		"score_type": "length",
		"value": round(value, 4),
		"passed": passed,
		"details": {"length": length, "min_len": min_len, "max_len": max_len},
		"reason": reason,
	}
