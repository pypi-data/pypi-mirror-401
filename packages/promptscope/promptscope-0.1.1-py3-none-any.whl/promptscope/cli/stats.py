import argparse
import json
from typing import Any, Dict, List

from promptscope.storage.sqlite import SQLiteStorage


def collect_stats(storage: SQLiteStorage) -> Dict[str, Any]:
	results: List[Dict[str, Any]] = storage.list_prompt_overviews()
	return {
		"prompts": results,
		"totals": {
			"prompt_count": len(results),
			"version_count": sum(item["versions"] for item in results),
			"stale_count": sum(1 for item in results if item["stale"]),
		},
	}


def format_stats(data: Dict[str, Any], output: str = "table") -> str:
	if output == "json":
		return json.dumps(data, indent=2)

	lines = [
		f"Prompts: {data['totals']['prompt_count']}  Versions: {data['totals']['version_count']}  Stale active: {data['totals']['stale_count']}",
		"",
		"prompt_id            versions  latest  active  status",
		"------------------------------------------------------",
	]
	for item in data["prompts"]:
		status = "stale" if item["stale"] else "fresh"
		lines.append(
			f"{item['prompt_id']:<20} {item['versions']:<8} {item['latest']:<6} {str(item['active'] or '-'): <7} {status}"
		)
	return "\n".join(lines)


def main():
	parser = argparse.ArgumentParser("promptscope-stats")
	parser.add_argument("--db", default="promptscope.db", help="Path to SQLite database")
	parser.add_argument("--output", choices=["table", "json"], default="table", help="Output format")
	args = parser.parse_args()

	storage = SQLiteStorage(args.db)
	data = collect_stats(storage)
	print(format_stats(data, args.output))


if __name__ == "__main__":
	main()
