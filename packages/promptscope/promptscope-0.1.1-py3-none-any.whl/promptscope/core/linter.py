
from typing import Any, Dict, List, Optional, TypedDict

SEVERITY_ORDER = {"error": 3, "warning": 2, "info": 1}


class LintWarning(TypedDict, total=False):
	code: str
	message: str
	severity: str
	path: str
	hint: str


def _count_by_severity(warnings: List[LintWarning]) -> Dict[str, int]:
	counts = {"error": 0, "warning": 0, "info": 0}
	for w in warnings:
		sev = w.get("severity", "warning")
		if sev in counts:
			counts[sev] += 1
	return counts


def _sort_warnings(warnings: List[LintWarning]) -> List[LintWarning]:
	return sorted(
		warnings,
		key=lambda w: (-SEVERITY_ORDER.get(w.get("severity", "warning"), 0), w.get("code", "")),
	)


def _warn(warnings: List[LintWarning], code: str, message: str, severity: str = "warning", path: Optional[str] = None, hint: Optional[str] = None):
	entry: LintWarning = {"code": code, "message": message, "severity": severity}
	if path:
		entry["path"] = path
	if hint:
		entry["hint"] = hint
	warnings.append(entry)


def _check_system_prompt(content: Dict[str, Any], warnings: List[LintWarning]) -> None:
	system_prompt = content.get("system", "")
	if not system_prompt:
		_warn(warnings, "missing_system", "System prompt missing or empty.", "error", path="content.system")
		return
	if len(system_prompt) < 20:
		_warn(warnings, "short_system", "System prompt is very short (<20 chars).", "warning", path="content.system")
	lowered = system_prompt.lower()
	if "summarize" in lowered and "bullet" not in lowered and "json" not in lowered:
		_warn(warnings, "ambiguous_summary", "Summary instruction is ambiguous; specify bullets, JSON, or another format.", "warning", path="content.system")
	if "contradict" in lowered or "conflict" in lowered:
		_warn(warnings, "conflict", "Conflicting directives detected in system prompt.", "warning", path="content.system")
	for vague in ["maybe", "possibly", "etc", "as needed"]:
		if vague in lowered:
			_warn(warnings, "vague_instruction", f"Vague phrasing ('{vague}') found; tighten instructions.", "info", path="content.system")
			break
	if "todo" in lowered or "tbd" in lowered:
		_warn(warnings, "incomplete_instruction", "System prompt contains TODO/TBD text; finalize instructions.", "warning", path="content.system")


def _check_output_format(content: Dict[str, Any], warnings: List[LintWarning]) -> None:
	if "output_format" not in content:
		_warn(warnings, "missing_output_format", "Missing explicit output format instruction.", "error", path="content.output_format")
		return
	output_format = content.get("output_format")
	if not output_format:
		_warn(warnings, "empty_output_format", "Output format is empty.", "error", path="content.output_format")
	elif not isinstance(output_format, (str, dict)):
		_warn(warnings, "invalid_output_format", "Output format should be a string or JSON template.", "error", path="content.output_format")


def _check_examples(content: Dict[str, Any], warnings: List[LintWarning]) -> None:
	if "examples" not in content:
		_warn(warnings, "missing_examples", "Few-shot examples missing; add examples for stability.", "info", path="content.examples")
		return
	examples = content.get("examples")
	if not isinstance(examples, list):
		_warn(warnings, "invalid_examples", "Examples should be a list of example dicts.", "error", path="content.examples")
		return
	if len(examples) == 0:
		_warn(warnings, "empty_examples", "Examples list is empty; add at least one example.", "warning", path="content.examples")
	for i, example in enumerate(examples):
		if not isinstance(example, dict):
			_warn(warnings, "invalid_example_entry", f"Example #{i} is not a dict.", "warning", path=f"content.examples[{i}]")
			continue
		if "input" not in example or "output" not in example:
			_warn(warnings, "incomplete_example", f"Example #{i} missing 'input' or 'output'.", "warning", path=f"content.examples[{i}]")


def _check_parameters(params: Any, warnings: List[LintWarning]) -> None:
	if not isinstance(params, dict):
		_warn(warnings, "invalid_params", "Parameters should be a dictionary.", "warning", path="parameters")
		return
	temperature = params.get("temperature")
	if temperature is not None and not (0 <= temperature <= 1):
		_warn(warnings, "temperature_range", "Temperature should be between 0 and 1.", "warning", path="parameters.temperature")
	top_p = params.get("top_p")
	if top_p is not None and not (0 <= top_p <= 1):
		_warn(warnings, "top_p_range", "top_p should be between 0 and 1.", "warning", path="parameters.top_p")
	max_tokens = params.get("max_tokens")
	if max_tokens is not None and (not isinstance(max_tokens, int) or max_tokens <= 0):
		_warn(warnings, "max_tokens_invalid", "max_tokens should be a positive integer.", "warning", path="parameters.max_tokens")


def _check_content_shape(content: Any, warnings: List[LintWarning]) -> bool:
	if content is None:
		_warn(warnings, "missing_content", "Prompt content is missing.", "error", path="content")
		return False
	if not isinstance(content, dict):
		_warn(warnings, "invalid_content_type", "Prompt content is not a dict; cannot lint.", "error", path="content")
		return False
	return True


def lint_prompt(flow: str, version: int | None = None, storage=None):
	"""
	Lint a prompt for common issues (ambiguity, missing instructions, incomplete examples, parameter ranges).
	Returns structured results while still printing a summary for CLI use.
	"""
	if storage is None:
		from promptscope.storage.sqlite import SQLiteStorage
		storage = SQLiteStorage()
	if version is None:
		version = storage.get_active_version(flow) or storage.get_latest_version(flow)

	prompt = storage.load_prompt_version(flow, version) if version else None
	if not prompt:
		msg = f"[PromptScope] Prompt '{flow}' version {version} not found."
		print(msg)
		return {
			"prompt_id": flow,
			"version": version,
			"warnings": [{"code": "not_found", "message": msg, "severity": "error"}],
			"ok": False,
		}

	warnings: List[LintWarning] = []
	if not _check_content_shape(prompt.content, warnings):
		print(f"[PromptScope] Lint findings for '{flow}' v{version}:")
		for w in warnings:
			print(f"- ({w['severity']}) {w['message']}")
		return {"prompt_id": flow, "version": version, "warnings": warnings, "ok": False}

	content: Dict[str, Any] = prompt.content or {}
	_check_system_prompt(content, warnings)
	_check_output_format(content, warnings)
	_check_examples(content, warnings)
	_check_parameters(getattr(prompt, "parameters", None), warnings)

	ok = not any(w.get("severity") == "error" for w in warnings)
	if warnings:
		counts = _count_by_severity(warnings)
		print(f"[PromptScope] Lint findings for '{flow}' v{version} "
		      f"(errors={counts['error']}, warnings={counts['warning']}, info={counts['info']}):")
		for w in _sort_warnings(warnings):
			path_note = f" [{w['path']}]" if "path" in w else ""
			hint_note = f" Hint: {w['hint']}" if "hint" in w else ""
			print(f"- ({w['severity']}) [{w['code']}] {w['message']}{path_note}{hint_note}")
	else:
		print(f"[PromptScope] No common prompt bugs detected for '{flow}' v{version}.")
	return {"prompt_id": flow, "version": version, "warnings": warnings, "ok": ok}
