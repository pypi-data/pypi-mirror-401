import argparse
import json
from typing import Any, Dict, Optional

from promptscope.core.replay import replay_prompt
from promptscope.models.replay import ReplayRequest
from promptscope.storage.sqlite import SQLiteStorage


def resolve_version_label(storage: SQLiteStorage, prompt_id: str, version_label: Optional[str]) -> Optional[int]:
	if version_label is None:
		return None
	if isinstance(version_label, int):
		return version_label
	label_lower = str(version_label).lower()
	if label_lower == "latest":
		return storage.get_latest_version(prompt_id)
	if label_lower == "active":
		return storage.get_active_version(prompt_id) or storage.get_latest_version(prompt_id)
	return int(version_label)


def run_replay(storage: SQLiteStorage, prompt_id: str, version_label: Optional[str], model: Optional[str], params_raw: Optional[str]) -> Dict[str, Any]:
	version = resolve_version_label(storage, prompt_id, version_label)
	if version is None:
		version = storage.get_active_version(prompt_id) or storage.get_latest_version(prompt_id)
	if version is None:
		raise ValueError(f"No versions found for prompt '{prompt_id}'.")

	override_params = None
	if params_raw:
		override_params = json.loads(params_raw)

	request = ReplayRequest(
		prompt_id=prompt_id,
		version=version,
		target_model=model,
		override_params=override_params,
	)
	return replay_prompt(storage, request)


def format_replay(result: Dict[str, Any], output: str) -> str:
	if output == "json":
		return json.dumps(result, indent=2)
	lines = [
		f"Model: {result['model']}",
		"Parameters:",
		json.dumps(result["params"], indent=2),
		"Content:",
		json.dumps(result["content"], indent=2),
	]
	return "\n".join(lines)


def main():
	parser = argparse.ArgumentParser("promptscope-replay")
	parser.add_argument("prompt_id", help="Prompt ID")
	parser.add_argument("--version", help="Prompt version or keyword (latest, active)")
	parser.add_argument("--model", help="Target model override", default=None)
	parser.add_argument("--params", help="Override params as JSON string", default=None)
	parser.add_argument("--db", default="promptscope.db", help="Path to SQLite database")
	parser.add_argument("--output", choices=["table", "json"], default="table", help="Output format")
	args = parser.parse_args()

	storage = SQLiteStorage(args.db)
	try:
		result = run_replay(storage, args.prompt_id, args.version, args.model, args.params)
		print(format_replay(result, args.output))
	except Exception as exc:
		print(f"[PromptScope] replay failed: {exc}")


if __name__ == "__main__":
	main()
