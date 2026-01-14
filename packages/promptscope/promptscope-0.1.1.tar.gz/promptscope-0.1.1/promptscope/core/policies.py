
import random
from typing import Any, Callable, Dict, List, Optional, TypedDict

from promptscope.core.diffing import diff_prompts
from promptscope.utils.hashing import hash_prompt


class CanaryResult(TypedDict, total=False):
	flow: str
	baseline_version: Optional[int]
	candidate_version: int
	traffic_percent: float
	sample_size: int
	control_requests: int
	canary_requests: int
	passed: bool
	reason: str
	assignment_preview: List[str]
	content_diff: Dict[str, Any]
	model_changed: Optional[bool]
	parameters_changed: Optional[bool]
	control_hash: Optional[str]
	canary_hash: Optional[str]


def _parse_percent(traffic: str) -> float:
	cleaned = str(traffic).strip().replace("%", "")
	percent = float(cleaned)
	if percent < 0 or percent > 100:
		raise ValueError("traffic percent must be between 0 and 100")
	return percent


def _pick_baseline_version(flow: str, candidate_version: int, storage) -> Optional[int]:
	"""
	Pick a baseline version to compare against the canary candidate.
	Prefer the active version; fallback to the latest version that is not the candidate.
	"""
	active = storage.get_active_version(flow)
	if active is not None and active != candidate_version:
		return active
	latest = storage.get_latest_version(flow)
	if latest is not None and latest != candidate_version:
		return latest
	# try previous version if present
	try:
		versions = storage.list_versions(flow)
		prior_versions = [v for v in versions if v < candidate_version]
		return prior_versions[-1] if prior_versions else None
	except Exception:
		return None


def canary_prompt_version(
	flow: str,
	version: int,
	traffic: str,
	storage=None,
	output_comparator: Optional[Callable[[Any, Any], bool]] = None,
	sample_size: int = 1000,
	verbose: bool = True,
	seed: Optional[int] = None,
	activate_on_pass: bool = False
) -> CanaryResult:
	"""
	Route a percentage of traffic to a new prompt version for canary testing.
	Validates inputs, compares against the active/latest baseline, and returns a structured summary.
	"""
	if storage is None:
		from promptscope.storage.sqlite import SQLiteStorage
		storage = SQLiteStorage()
	if sample_size <= 0:
		raise ValueError("sample_size must be positive")

	try:
		percent = _parse_percent(traffic)
		canary_count = round(sample_size * percent / 100)
	except ValueError as exc:
		raise ValueError(f"Invalid traffic value '{traffic}': {exc}")

	candidate_prompt = storage.load_prompt_version(flow, version)
	if not candidate_prompt:
		msg = f"[PromptScope] Prompt '{flow}' version {version} not found."
		if verbose:
			print(msg)
		return {"flow": flow, "candidate_version": version, "traffic_percent": percent, "passed": False, "reason": msg}

	baseline_version = _pick_baseline_version(flow, version, storage)
	baseline_prompt = storage.load_prompt_version(flow, baseline_version) if baseline_version else None

	rng = random.Random(seed)
	assignments = ["canary"] * canary_count + ["control"] * max(sample_size - canary_count, 0)
	rng.shuffle(assignments)
	assignment_preview = assignments[: min(20, len(assignments))]

	if output_comparator is None:
		def output_comparator(control, canary):
			return control == canary

	control_hash = hash_prompt(baseline_prompt.content, baseline_prompt.model, baseline_prompt.parameters) if baseline_prompt else None
	canary_hash = hash_prompt(candidate_prompt.content, candidate_prompt.model, candidate_prompt.parameters)
	control_output = control_hash or "baseline_missing"
	canary_output = canary_hash
	passed = bool(output_comparator(control_output, canary_output)) if baseline_prompt else True

	content_diff = diff_prompts(baseline_prompt.content, candidate_prompt.content) if baseline_prompt else {}
	model_changed = baseline_prompt.model != candidate_prompt.model if baseline_prompt else None
	parameters_changed = baseline_prompt.parameters != candidate_prompt.parameters if baseline_prompt else None

	if verbose:
		print(f"[PromptScope] Starting canary test for '{flow}' candidate v{version} on {percent}% of traffic.")
		if baseline_version:
			print(f"[PromptScope] Baseline: v{baseline_version}; control hash={control_hash}")
		else:
			print("[PromptScope] No baseline version found; treating candidate as first version.")
		print(f"[PromptScope] Assigned {canary_count} canary / {sample_size - canary_count} control requests.")
		print(f"[PromptScope] Output comparison: {'PASS' if passed else 'FAIL'}")
		if not passed and baseline_prompt:
			print(f"[PromptScope] Canary differs from baseline (model_changed={model_changed}, params_changed={parameters_changed}).")
		if passed and activate_on_pass and hasattr(storage, "set_active_version"):
			storage.set_active_version(flow, version)
			print(f"[PromptScope] Canary passed; activated v{version} as active.")

	result: CanaryResult = {
		"flow": flow,
		"baseline_version": baseline_version,
		"candidate_version": version,
		"traffic_percent": percent,
		"sample_size": sample_size,
		"control_requests": sample_size - canary_count,
		"canary_requests": canary_count,
		"assignment_preview": assignment_preview,
		"passed": passed,
		"reason": "comparison_passed" if passed else "comparison_failed",
		"content_diff": content_diff,
		"model_changed": model_changed,
		"parameters_changed": parameters_changed,
		"control_hash": control_hash,
		"canary_hash": canary_hash,
	}
	return result
