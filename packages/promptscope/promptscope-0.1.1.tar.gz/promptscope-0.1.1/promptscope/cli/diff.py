import argparse
import json
from typing import Any, Dict, Optional

from promptscope.core.diffing import diff_prompts
from promptscope.storage.sqlite import SQLiteStorage


def resolve_version_label(storage: SQLiteStorage, prompt_id: str, label: Optional[str]) -> Optional[int]:
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
		return storage.get_latest_version(prompt_id)
	if label_lower == "active":
		return storage.get_active_version(prompt_id) or storage.get_latest_version(prompt_id)
	if label_lower in {"prev", "previous"}:
		latest = storage.get_latest_version(prompt_id)
		return latest - 1 if latest and latest > 1 else None
	return int(label)


def run_diff(storage: SQLiteStorage, prompt_id: str, from_version: Optional[str], to_version: Optional[str]) -> Dict[str, Any]:
	latest = storage.get_latest_version(prompt_id)
	if latest is None:
		raise ValueError(f"No versions found for prompt '{prompt_id}'.")

	resolved_to = resolve_version_label(storage, prompt_id, to_version) or latest
	resolved_from = resolve_version_label(storage, prompt_id, from_version)
	if resolved_from is None:
		resolved_from = resolved_to - 1 if resolved_to > 1 else resolved_to

	p1 = storage.load_prompt_version(prompt_id, resolved_from)
	p2 = storage.load_prompt_version(prompt_id, resolved_to)
	if not p1 or not p2:
		raise ValueError(f"Unable to load versions {resolved_from} and {resolved_to} for prompt '{prompt_id}'.")

	diff = diff_prompts(p1.content, p2.content)
	return {
		"prompt_id": prompt_id,
		"from_version": resolved_from,
		"to_version": resolved_to,
		"from_model": p1.model,
		"to_model": p2.model,
		"diff": diff,
		"from_params": p1.parameters,
		"to_params": p2.parameters,
		"from_content": p1.content,
		"to_content": p2.content,
	}


def format_diff(result: Dict[str, Any], output: str = "table", show_content: bool = False) -> str:
	if output == "json":
		serializable = {**result, "diff": result["diff"]}
		return json.dumps(serializable, indent=2)

	lines = [
		f"Prompt: {result['prompt_id']}",
		f"From v{result['from_version']} (model={result['from_model']}) -> To v{result['to_version']} (model={result['to_model']})",
		"Diff:",
		f"  Added:    {result['diff']['added']}",
		f"  Removed:  {result['diff']['removed']}",
		f"  Modified: {result['diff']['modified']}",
	]
	if show_content:
		lines.append("From content:")
		lines.append(json.dumps(result["from_content"], indent=2))
		lines.append("To content:")
		lines.append(json.dumps(result["to_content"], indent=2))
	return "\n".join(lines)


def main():
	parser = argparse.ArgumentParser("promptscope-diff")
	parser.add_argument("prompt_id", help="Prompt ID")
	parser.add_argument("--from-version", dest="from_version", help="From version number or keyword (latest, active, previous)")
	parser.add_argument("--to-version", dest="to_version", help="To version number or keyword (latest, active)")
	parser.add_argument("--db", default="promptscope.db", help="Path to SQLite database")
	parser.add_argument("--output", choices=["table", "json"], default="table", help="Output format")
	parser.add_argument("--show-content", action="store_true", help="Include prompt contents in output")
	args = parser.parse_args()

	storage = SQLiteStorage(args.db)
	try:
		result = run_diff(storage, args.prompt_id, args.from_version, args.to_version)
		print(format_diff(result, output=args.output, show_content=args.show_content))
	except Exception as exc:
		print(f"[PromptScope] diff failed: {exc}")


if __name__ == "__main__":
	main()
