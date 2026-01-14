
"""
Serialization utilities for PromptScope.
Provides helpers for serializing and deserializing objects, prompts, and results.
"""
import json
import pickle
from typing import Any, Tuple


def canonical_json(obj: Any) -> str:
	"""
	Serialize to JSON with sorted keys and no extra whitespace (stable for hashing/compare).
	"""
	return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str)


def to_json(obj: Any, *, indent: int = 2, sort_keys: bool = False) -> str:
	"""
	Serialize an object to a JSON string (pretty-print friendly).
	"""
	return json.dumps(obj, indent=indent, sort_keys=sort_keys, default=str)


def to_json_bytes(obj: Any, *, sort_keys: bool = True) -> bytes:
	"""
	Serialize an object to UTF-8 JSON bytes (sorted by default for deterministic output).
	"""
	return json.dumps(obj, sort_keys=sort_keys, default=str).encode("utf-8")


def from_json(data: str) -> Any:
	"""
	Deserialize a JSON string to a Python object.
	"""
	return json.loads(data)


def try_from_json(data: str) -> Tuple[Any, str | None]:
	"""
	Attempt to deserialize JSON, returning (value, error_message).
	"""
	try:
		return json.loads(data), None
	except Exception as exc:
		return None, str(exc)


def to_pickle(obj: Any) -> bytes:
	"""
	Serialize an object to a pickle byte stream.
	"""
	return pickle.dumps(obj)


def from_pickle(data: bytes) -> Any:
	"""
	Deserialize a pickle byte stream to a Python object.
	"""
	return pickle.loads(data)


def safe_serialize(obj: Any) -> str:
	"""
	Try to serialize an object to JSON, fallback to string if it fails.
	"""
	try:
		return to_json(obj)
	except Exception:
		return str(obj)
