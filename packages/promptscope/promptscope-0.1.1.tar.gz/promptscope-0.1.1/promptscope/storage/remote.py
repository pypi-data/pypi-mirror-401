
"""
Remote storage interface for PromptScope SaaS backend.
Provides an abstract base and example HTTP implementation stub.
"""


import abc
from typing import Any, Dict, Optional
import requests

class RemoteStorageBase(abc.ABC):
	"""
	Abstract base class for remote storage backends (e.g., SaaS, cloud).
	"""
	@abc.abstractmethod
	def save_prompt(self, flow: str, version: int, data: Dict[str, Any]) -> None:
		"""Save a prompt version remotely."""
		pass

	@abc.abstractmethod
	def load_prompt(self, flow: str, version: int) -> Optional[Dict[str, Any]]:
		"""Load a prompt version from remote storage."""
		pass

	@abc.abstractmethod
	def list_versions(self, flow: str) -> list:
		"""List all prompt versions for a flow."""
		pass

class HTTPRemoteStorage(RemoteStorageBase):
	"""
	HTTP-based remote storage implementation for PromptScope SaaS backend.
	"""
	def __init__(self, base_url: str, api_key: Optional[str] = None, timeout: int = 10):
		self.base_url = base_url.rstrip("/")
		self.api_key = api_key
		self.timeout = timeout

	def _headers(self) -> Dict[str, str]:
		headers = {"Content-Type": "application/json"}
		if self.api_key:
			headers["Authorization"] = f"Bearer {self.api_key}"
		return headers

	def save_prompt(self, flow: str, version: int, data: Dict[str, Any]) -> None:
		url = f"{self.base_url}/api/flows/{flow}/versions/{version}"
		try:
			resp = requests.put(url, json=data, headers=self._headers(), timeout=self.timeout)
			resp.raise_for_status()
		except requests.RequestException as e:
			raise RuntimeError(f"Failed to save prompt remotely: {e}")

	def load_prompt(self, flow: str, version: int) -> Optional[Dict[str, Any]]:
		url = f"{self.base_url}/api/flows/{flow}/versions/{version}"
		try:
			resp = requests.get(url, headers=self._headers(), timeout=self.timeout)
			if resp.status_code == 404:
				return None
			resp.raise_for_status()
			return resp.json()
		except requests.RequestException as e:
			raise RuntimeError(f"Failed to load prompt remotely: {e}")

	def list_versions(self, flow: str) -> list:
		url = f"{self.base_url}/api/flows/{flow}/versions"
		try:
			resp = requests.get(url, headers=self._headers(), timeout=self.timeout)
			resp.raise_for_status()
			return resp.json().get("versions", [])
		except requests.RequestException as e:
			raise RuntimeError(f"Failed to list prompt versions remotely: {e}")
