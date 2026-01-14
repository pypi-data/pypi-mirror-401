import json
from typing import Any, Dict, List

from promptscope.storage.sqlite import SQLiteStorage


def export_prompts(storage: SQLiteStorage) -> Dict[str, Any]:
	data: List[Dict[str, Any]] = []
	for prompt_id in storage.list_prompts():
		versions: List[Dict[str, Any]] = []
		for version in storage.list_versions(prompt_id):
			prompt = storage.load_prompt_version(prompt_id, version)
			if not prompt:
				continue
			versions.append(
				{
					"prompt_id": prompt.prompt_id,
					"version": prompt.version,
					"model": prompt.model,
					"parameters": prompt.parameters,
					"content": prompt.content,
					"created_at": str(prompt.created_at),
					"response": prompt.response,
					"response_ms": prompt.response_ms,
					"cost": prompt.cost,
				}
			)
		data.append(
			{
				"prompt_id": prompt_id,
				"active_version": storage.get_active_version(prompt_id),
				"versions": versions,
			}
		)
	return {"prompts": data}


def format_export(data: Dict[str, Any], pretty: bool = True) -> str:
	if pretty:
		return json.dumps(data, indent=2)
	return json.dumps(data, separators=(",", ":"))
