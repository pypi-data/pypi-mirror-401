from typing import Any, Dict, List, TypedDict


class DiffResult(TypedDict, total=False):
	added: Dict[str, Any]
	removed: Dict[str, Any]
	modified: List[str]
	changed: Dict[str, Dict[str, Any]]
	unchanged: List[str]
	type_mismatches: Dict[str, str]


def _make_path(parent: str, key: str) -> str:
	return f"{parent}.{key}" if parent else key


def _make_index_path(parent: str, idx: int) -> str:
	return f"{parent}[{idx}]" if parent else f"[{idx}]"


def _accumulate_diff(old: Any, new: Any, parent: str, out: Dict[str, Any]) -> None:
	# Same type and both dicts: recurse per key
	if isinstance(old, dict) and isinstance(new, dict):
		for key in old.keys() - new.keys():
			path = _make_path(parent, key)
			out["removed"][path] = old[key]
		for key in new.keys() - old.keys():
			path = _make_path(parent, key)
			out["added"][path] = new[key]
		for key in old.keys() & new.keys():
			path = _make_path(parent, key)
			_accumulate_diff(old[key], new[key], path, out)
		return

	# Lists: compare by index
	if isinstance(old, list) and isinstance(new, list):
		max_len = max(len(old), len(new))
		for idx in range(max_len):
			path = _make_index_path(parent, idx)
			if idx >= len(old):
				out["added"][path] = new[idx]
			elif idx >= len(new):
				out["removed"][path] = old[idx]
			else:
				_accumulate_diff(old[idx], new[idx], path, out)
		return

	# Type mismatch
	if type(old) is not type(new):
		out["type_mismatches"][parent or "$"] = f"{type(old).__name__} -> {type(new).__name__}"
		out["changed"][parent or "$"] = {"from": old, "to": new}
		out["modified"].append(parent or "$")
		return

	# Primitive equality
	if old == new:
		out["unchanged"].append(parent or "$")
	else:
		out["changed"][parent or "$"] = {"from": old, "to": new}
		out["modified"].append(parent or "$")


def diff_prompts(old: Dict[str, Any], new: Dict[str, Any]) -> DiffResult:
	"""
	Deep diff between two prompt payloads (dict/list/primitive).
	Returns added/removed/modified paths plus change details.
	"""
	out: DiffResult = {
		"added": {},
		"removed": {},
		"modified": [],
		"changed": {},
		"unchanged": [],
		"type_mismatches": {},
	}
	_accumulate_diff(old, new, parent="", out=out)  # type: ignore[arg-type]
	# Keep modified paths sorted for stable output
	out["modified"] = sorted(out["modified"])
	out["unchanged"] = sorted(out["unchanged"])
	return out
