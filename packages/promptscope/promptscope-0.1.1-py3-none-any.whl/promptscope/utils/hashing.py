
"""
Serious hashing utilities for PromptScope.
Provides robust hashing for prompts, objects, and files.
"""

import hashlib
import json
from typing import Any, Optional

from promptscope.utils.serialization import canonical_json


def _hash_bytes(raw: bytes, algo: str = "sha256") -> str:
	h = hashlib.new(algo)
	h.update(raw)
	return h.hexdigest()


def hash_prompt(content: dict, model: str, params: dict, algo: str = "sha256") -> str:
	"""
	Hash a prompt definition (content, model, params) using the specified algorithm.
	Args:
		content: Prompt content dict.
		model: Model name.
		params: Model parameters dict.
		algo: Hash algorithm (default: sha256).
	Returns:
		str: Hex digest of the hash.
	"""
	payload = {"content": content or {}, "model": model, "params": params or {}}
	return _hash_bytes(canonical_json(payload).encode(), algo=algo)

def hash_object(obj: Any, algo: str = "sha256") -> str:
	"""
	Hash a generic Python object (via JSON serialization).
	Args:
		obj: The object to hash.
		algo: Hash algorithm (default: sha256).
	Returns:
		str: Hex digest of the hash.
	"""
	return _hash_bytes(canonical_json(obj).encode(), algo=algo)

def hash_file(path: str, algo: str = "sha256", chunk_size: int = 65536) -> str:
	"""
	Hash the contents of a file.
	Args:
		path: Path to the file.
		algo: Hash algorithm (default: sha256).
		chunk_size: Read chunk size in bytes.
	Returns:
		str: Hex digest of the hash.
	"""
	h = hashlib.new(algo)
	with open(path, "rb") as f:
		while True:
			chunk = f.read(chunk_size)
			if not chunk:
				break
			h.update(chunk)
	return h.hexdigest()
