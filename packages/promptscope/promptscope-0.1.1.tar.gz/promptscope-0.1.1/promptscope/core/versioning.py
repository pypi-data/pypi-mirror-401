from typing import Optional, Union


def resolve_version_label(storage, flow: str, label: Union[str, int, None]) -> Optional[int]:
	"""
	Resolve a version label (int, 'latest', 'active', 'previous') to a concrete version number.
	Returns None if it cannot be determined.
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


def rollback_prompt_version(flow: str, to_version: int, storage=None) -> bool:
	"""
	Mark an older prompt version as active for the given flow.
	Returns True when successful.
	"""
	if storage is None:
		from promptscope.storage.sqlite import SQLiteStorage
		storage = SQLiteStorage()
	if to_version is None or to_version <= 0:
		print(f"[PromptScope] Invalid version '{to_version}' for rollback.")
		return False
	prompt = storage.load_prompt_version(flow, to_version)
	if not prompt:
		print(f"[PromptScope] Version {to_version} does not exist for flow '{flow}'")
		return False
	storage.set_active_version(flow, to_version)
	print(f"[PromptScope] Rolled back '{flow}' to version {to_version}. Now active.")
	return True


def next_version(latest: int | None) -> int:
	return 1 if latest is None else latest + 1
