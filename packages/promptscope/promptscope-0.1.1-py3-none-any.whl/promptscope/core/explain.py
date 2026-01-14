from typing import Any, Dict, Optional, TypedDict

from promptscope.core.diffing import DiffResult, diff_prompts


class ExplainResult(TypedDict, total=False):
	flow: str
	target_version: Optional[int]
	baseline_version: Optional[int]
	target_model: Optional[str]
	baseline_model: Optional[str]
	model_changed: Optional[bool]
	parameters_diff: Dict[str, Any]
	content_diff: DiffResult
	target_created_at: Optional[str]
	ok: bool
	reason: str


def _resolve_version_label(storage, flow: str, label: Optional[str]) -> Optional[int]:
	"""
	Accepts numeric strings or keywords: latest, active, previous.
	Returns resolved version or None if it cannot be determined.
	"""
	if label is None:
		return None
	if isinstance(label, int):
		return label
	label_lower = str(label).lower()
	if label_lower == "latest":
		return storage.get_latest_version(flow)
	if label_lower == "active":
		return storage.get_active_version(flow) or storage.get_latest_version(flow)
	if label_lower in {"prev", "previous"}:
		latest = storage.get_latest_version(flow)
		return latest - 1 if latest and latest > 1 else None
	try:
		return int(label)
	except ValueError:
		return None


def _diff_params(before: Dict[str, Any], after: Dict[str, Any]) -> Dict[str, Any]:
	added = {k: after[k] for k in after.keys() - before.keys()}
	removed = [k for k in before.keys() - after.keys()]
	changed = {
		k: {"from": before[k], "to": after[k]}
		for k in before.keys() & after.keys()
		if before[k] != after[k]
	}
	return {
		"added": added,
		"removed": removed,
		"changed": changed,
	}


def explain_change(flow: str, output_id: str, storage=None) -> Dict[str, Any]:
	"""
	Explain why a prompt output changed by comparing a target version to its previous version.
	Args:
		flow (str): The prompt flow name.
		output_id (str): The prompt/output identifier; accepts version numbers or keywords (latest, active, previous).
		storage: Storage backend instance.
	Returns:
		Structured explanation with model, parameters, and content diffs.
	"""
	if storage is None:
		from promptscope.storage.sqlite import SQLiteStorage
		storage = SQLiteStorage()

	target_version = _resolve_version_label(storage, flow, output_id)
	if target_version is None:
		target_version = storage.get_active_version(flow) or storage.get_latest_version(flow)
	if target_version is None:
		raise ValueError(f"No versions found for flow '{flow}'.")

	baseline_version = target_version - 1 if target_version and target_version > 1 else target_version
	target_prompt = storage.load_prompt_version(flow, target_version)
	baseline_prompt = storage.load_prompt_version(flow, baseline_version) if baseline_version else None
	if not target_prompt:
		raise ValueError(f"Prompt '{flow}' version {target_version} not found.")

	content_diff = diff_prompts(baseline_prompt.content if baseline_prompt else {}, target_prompt.content or {})
	params_diff = _diff_params(baseline_prompt.parameters if baseline_prompt else {}, target_prompt.parameters or {})
	model_changed = baseline_prompt.model != target_prompt.model if baseline_prompt else None

	return ExplainResult(
		flow=flow,
		target_version=target_version,
		baseline_version=baseline_prompt.version if baseline_prompt else None,
		model_changed=model_changed,
		baseline_model=baseline_prompt.model if baseline_prompt else None,
		target_model=target_prompt.model,
		parameters_diff=params_diff,
		content_diff=content_diff,
		target_created_at=str(target_prompt.created_at) if target_prompt.created_at else None,
		ok=True,
		reason="comparison_complete",
	)
