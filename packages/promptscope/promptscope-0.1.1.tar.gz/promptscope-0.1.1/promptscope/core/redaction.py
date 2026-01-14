from copy import deepcopy
from typing import Any, Iterable, List, Sequence, Tuple

from promptscope.core.versioning import next_version
from promptscope.models.prompt import PromptVersion
from promptscope.utils.hashing import hash_prompt
from promptscope.utils.time import now_utc


def _parse_field_path(field: str) -> List[str | int]:
	"""
	Convert a dotted path like "user.email" or "items.0.token" into segments.
	Numeric segments are treated as list indices.
	"""
	parts: List[str | int] = []
	for part in field.split("."):
		if part == "":
			continue
		if part.isdigit():
			parts.append(int(part))
		else:
			parts.append(part)
	return parts


def _redact_path(target: Any, path: Sequence[str | int], placeholder: Any) -> bool:
	"""
	Redact a single path inside a nested dict/list structure.
	Returns True if something was redacted.
	"""
	cursor = target
	for i, segment in enumerate(path):
		is_last = i == len(path) - 1
		if isinstance(cursor, dict):
			if segment not in cursor:
				return False
			if is_last:
				cursor[segment] = placeholder
				return True
			cursor = cursor[segment]
		elif isinstance(cursor, list):
			if not isinstance(segment, int) or segment < 0 or segment >= len(cursor):
				return False
			if is_last:
				cursor[segment] = placeholder
				return True
			cursor = cursor[segment]
		else:
			return False
	return False


def _apply_redactions(content: dict, fields: Iterable[str], placeholder: Any) -> Tuple[dict, set[str], set[str]]:
	"""
	Apply redactions to the provided content and report successes and misses.
	Returns (redacted_content, redacted_fields, missing_fields).
	"""
	redacted_content = deepcopy(content)
	redacted_fields: set[str] = set()
	missing_fields: set[str] = set()

	for raw_field in fields:
		path = _parse_field_path(raw_field)
		if not path:
			missing_fields.add(raw_field)
			continue
		if _redact_path(redacted_content, path, placeholder):
			redacted_fields.add(raw_field)
		else:
			missing_fields.add(raw_field)
	return redacted_content, redacted_fields, missing_fields


def redact_fields(flow: str, fields: list[str], storage=None, placeholder: Any = "[REDACTED]", activate: bool = True):
	"""
	Redact sensitive fields in prompts for a given flow (supports dotted paths and list indices)
	and save as a new version. Returns the new prompt version number or None when nothing changed.
	"""
	if storage is None:
		from promptscope.storage.sqlite import SQLiteStorage
		storage = SQLiteStorage()

	version = storage.get_active_version(flow) or storage.get_latest_version(flow)
	prompt = storage.load_prompt_version(flow, version) if version else None
	if not prompt:
		print(f"[PromptScope] Prompt '{flow}' version {version} not found.")
		return None
	if not isinstance(prompt.content, dict):
		print(f"[PromptScope] Prompt '{flow}' v{version} content is not a dict; skipping redaction.")
		return None

	redacted_content, redacted_fields, missing_fields = _apply_redactions(prompt.content, fields, placeholder)
	if not redacted_fields:
		print(f"[PromptScope] No fields redacted for flow '{flow}'. Missing: {sorted(missing_fields)}")
		return None

	content_hash = hash_prompt(redacted_content, prompt.model, prompt.parameters)
	new_version = next_version(version)
	redacted_prompt = PromptVersion(
		prompt_id=prompt.prompt_id,
		version=new_version,
		content=redacted_content,
		model=prompt.model,
		parameters=prompt.parameters,
		content_hash=content_hash,
		created_at=now_utc()
	)
	storage.save_prompt_version(redacted_prompt)
	if activate and hasattr(storage, "set_active_version"):
		storage.set_active_version(flow, new_version)

	missing_note = f" (not found: {sorted(missing_fields)})" if missing_fields else ""
	print(f"[PromptScope] Redacted fields {sorted(redacted_fields)} in flow '{flow}'. New version: {new_version}{missing_note}")
	return new_version
