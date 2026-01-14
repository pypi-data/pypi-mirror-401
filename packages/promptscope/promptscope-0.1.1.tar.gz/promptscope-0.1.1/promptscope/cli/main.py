import argparse
import json
import os
from typing import Any, Dict, List

from promptscope.cli.diff import format_diff, run_diff
from promptscope.cli.replay import format_replay, run_replay
from promptscope.cli.stats import collect_stats, format_stats
from promptscope.cli.export import export_prompts, format_export
from promptscope.storage.sqlite import SQLiteStorage


def get_db_default() -> str:
	return os.environ.get("PROMPTSCOPE_DB", "promptscope.db")


def create_storage(db_path: str) -> SQLiteStorage:
	return SQLiteStorage(db_path)


def add_common_db_arg(parser: argparse.ArgumentParser) -> None:
	parser.add_argument("--db", default=get_db_default(), help="Path to SQLite database (PROMPTSCOPE_DB)")


def add_output_arg(parser: argparse.ArgumentParser, default: str = "table") -> None:
	parser.add_argument("--output", choices=["table", "json"], default=default, help="Output format")


def handle_diff(args: argparse.Namespace) -> None:
	storage = create_storage(args.db)
	result = run_diff(storage, args.prompt_id, args.from_version, args.to_version)
	print(format_diff(result, output=args.output, show_content=args.show_content))


def handle_replay(args: argparse.Namespace) -> None:
	storage = create_storage(args.db)
	result = run_replay(storage, args.prompt_id, args.version, args.model, args.params)
	print(format_replay(result, output=args.output))


def format_explain(result: Dict[str, Any], output: str = "table") -> str:
	if output == "json":
		return json.dumps(result, indent=2)
	lines = [
		f"Flow: {result['flow']}",
		f"Version: v{result['baseline_version']} -> v{result['target_version']}",
		f"Model: {result.get('baseline_model') or '-'} -> {result['target_model']}",
		f"Model changed: {'yes' if result['model_changed'] else 'no'}",
		"Parameter changes:",
		f"  added:   {json.dumps(result['parameters_diff']['added'], indent=2)}" if result["parameters_diff"]["added"] else "  added:   {}",
		f"  removed: {result['parameters_diff']['removed']}" if result["parameters_diff"]["removed"] else "  removed: []",
		f"  changed: {json.dumps(result['parameters_diff']['changed'], indent=2)}" if result["parameters_diff"]["changed"] else "  changed: {}",
		"Content diff:",
		f"  Added:    {result['content_diff']['added']}",
		f"  Removed:  {result['content_diff']['removed']}",
		f"  Modified: {result['content_diff']['modified']}",
		f"Target created at: {result['target_created_at']}",
	]
	return "\n".join(lines)


def handle_stats(args: argparse.Namespace) -> None:
	storage = create_storage(args.db)
	data = collect_stats(storage)
	print(format_stats(data, output=args.output))


def handle_list(args: argparse.Namespace) -> None:
	storage = create_storage(args.db)
	data: List[Dict[str, Any]] = storage.list_prompt_overviews()
	if args.output == "json":
		print(json.dumps({"prompts": data}, indent=2))
		return
	print("prompt_id            versions  latest  active")
	print("-----------------------------------------------")
	for item in data:
		print(f"{item['prompt_id']:<20} {item['versions']:<8} {item['latest']:<6} {str(item['active'] or '-'): <6}")


def handle_show(args: argparse.Namespace) -> None:
	from promptscope.cli.diff import resolve_version_label

	storage = create_storage(args.db)
	version = resolve_version_label(storage, args.prompt_id, args.version)
	if version is None:
		version = storage.get_active_version(args.prompt_id) or storage.get_latest_version(args.prompt_id)
	if version is None:
		raise ValueError(f"No versions found for prompt '{args.prompt_id}'.")
	prompt = storage.load_prompt_version(args.prompt_id, version)
	if not prompt:
		raise ValueError(f"Prompt '{args.prompt_id}' version {version} not found.")
	result = {
		"prompt_id": prompt.prompt_id,
		"version": prompt.version,
		"model": prompt.model,
		"parameters": prompt.parameters,
		"content": prompt.content,
		"created_at": str(prompt.created_at),
	}
	if args.output == "json":
		print(json.dumps(result, indent=2))
		return
	print(f"{prompt.prompt_id} v{prompt.version} (model={prompt.model})")
	print("Parameters:")
	print(json.dumps(prompt.parameters, indent=2))
	print("Content:")
	print(json.dumps(prompt.content, indent=2))


def handle_rollback(args: argparse.Namespace) -> None:
	from promptscope.core.versioning import rollback_prompt_version

	storage = create_storage(args.db)
	rollback_prompt_version(args.flow, args.to, storage=storage)


def handle_canary(args: argparse.Namespace) -> None:
	from promptscope.core.policies import canary_prompt_version

	storage = create_storage(args.db)
	canary_prompt_version(args.flow, args.version, args.traffic, storage=storage)


def handle_linter(args: argparse.Namespace) -> None:
	from promptscope.core.linter import lint_prompt

	storage = create_storage(args.db)
	lint_prompt(args.flow, args.version, storage=storage)


def handle_redact(args: argparse.Namespace) -> None:
	from promptscope.core.redaction import redact_fields

	storage = create_storage(args.db)
	redact_fields(args.flow, args.fields, storage=storage)


def handle_explain(args: argparse.Namespace) -> None:
	from promptscope.core.explain import explain_change

	storage = create_storage(args.db)
	result = explain_change(args.flow, args.id, storage=storage)
	print(format_explain(result, output=args.output))


def handle_export(args: argparse.Namespace) -> None:
	storage = create_storage(args.db)
	data = export_prompts(storage)
	payload = format_export(data, pretty=args.pretty)
	if args.out == "-" or not args.out:
		print(payload)
		return
	with open(args.out, "w", encoding="utf-8") as f:
		f.write(payload)
	print(f"[PromptScope] Exported prompts to {args.out}")


def build_parser() -> argparse.ArgumentParser:
	parser = argparse.ArgumentParser(description="PromptScope CLI")
	subparsers = parser.add_subparsers(dest="command")

	diff_parser = subparsers.add_parser("diff", help="Diff two prompt versions")
	diff_parser.add_argument("prompt_id", help="Prompt flow/prompt id")
	diff_parser.add_argument("--from-version", dest="from_version", help="From version number or keyword (latest, active, previous)")
	diff_parser.add_argument("--to-version", dest="to_version", help="To version number or keyword (latest, active)")
	diff_parser.add_argument("--show-content", action="store_true", help="Include full prompt contents")
	add_common_db_arg(diff_parser)
	add_output_arg(diff_parser)
	diff_parser.set_defaults(func=handle_diff)

	replay_parser = subparsers.add_parser("replay", help="Replay prompts with a model or params override")
	replay_parser.add_argument("prompt_id", help="Prompt flow/prompt id")
	replay_parser.add_argument("--version", help="Prompt version or keyword (latest, active)")
	replay_parser.add_argument("--model", type=str, help="Model to use for replay")
	replay_parser.add_argument("--params", help="Override params as JSON string")
	add_common_db_arg(replay_parser)
	add_output_arg(replay_parser)
	replay_parser.set_defaults(func=handle_replay)

	stats_parser = subparsers.add_parser("stats", help="Show prompt inventory and version counts")
	add_common_db_arg(stats_parser)
	add_output_arg(stats_parser)
	stats_parser.set_defaults(func=handle_stats)

	list_parser = subparsers.add_parser("list", help="List all prompts and their latest/active versions")
	add_common_db_arg(list_parser)
	add_output_arg(list_parser)
	list_parser.set_defaults(func=handle_list)

	show_parser = subparsers.add_parser("show", help="Show a specific prompt version (defaults to active/latest)")
	show_parser.add_argument("prompt_id", help="Prompt flow/prompt id")
	show_parser.add_argument("--version", help="Version number or keyword (latest, active)")
	add_common_db_arg(show_parser)
	add_output_arg(show_parser)
	show_parser.set_defaults(func=handle_show)

	rollback_parser = subparsers.add_parser("rollback", help="Rollback to a previous prompt version")
	rollback_parser.add_argument("flow", help="Prompt flow name")
	rollback_parser.add_argument("--to", type=int, required=True, help="Version number to rollback to")
	add_common_db_arg(rollback_parser)
	rollback_parser.set_defaults(func=handle_rollback)

	canary_parser = subparsers.add_parser("canary", help="Canary test a prompt version on a percentage of traffic")
	canary_parser.add_argument("flow", help="Prompt flow name")
	canary_parser.add_argument("--version", type=int, required=True, help="Prompt version to canary test")
	canary_parser.add_argument("--traffic", type=str, required=True, help="Traffic percentage, e.g. 5%")
	add_common_db_arg(canary_parser)
	canary_parser.set_defaults(func=handle_canary)

	linter_parser = subparsers.add_parser("linter", help="Lint a prompt for common issues")
	linter_parser.add_argument("flow", help="Prompt flow name")
	linter_parser.add_argument("--version", type=int, required=False, help="Prompt version to lint (default: latest)")
	add_common_db_arg(linter_parser)
	linter_parser.set_defaults(func=handle_linter)

	redact_parser = subparsers.add_parser("redact", help="Redact sensitive fields in prompts")
	redact_parser.add_argument("flow", help="Prompt flow name")
	redact_parser.add_argument("--fields", nargs="+", required=True, help="Fields to redact, e.g. email phone token")
	add_common_db_arg(redact_parser)
	redact_parser.set_defaults(func=handle_redact)

	explain_parser = subparsers.add_parser("explain", help="Explain why a prompt output changed")
	explain_parser.add_argument("flow", help="Prompt flow name")
	explain_parser.add_argument("--id", type=str, required=True, help="Prompt or output ID to explain")
	add_common_db_arg(explain_parser)
	add_output_arg(explain_parser)
	explain_parser.set_defaults(func=handle_explain)

	export_parser = subparsers.add_parser("export", help="Export all prompts and versions to JSON")
	add_common_db_arg(export_parser)
	export_parser.add_argument("--out", default="promptscope_export.json", help="Output file path ('-' for stdout)")
	export_parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
	export_parser.set_defaults(func=handle_export)

	return parser


def main() -> None:
	parser = build_parser()
	args = parser.parse_args()

	if not getattr(args, "command", None):
		parser.print_help()
		return

	try:
		args.func(args)
	except Exception as exc:
		print(f"[PromptScope] {args.command} failed: {exc}")


if __name__ == "__main__":
	main()
