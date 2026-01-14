from typing import Any, Callable, Dict, Optional, TypedDict

from promptscope.models.replay import ReplayRequest


class ReplayResult(TypedDict, total=False):
	flow: str
	version: int
	source_model: str
	target_model: str
	parameters: Dict[str, Any]
	content: Dict[str, Any]
	original_output: Any
	swapped_output: Any
	differs: bool
	reason: str
	ran_with_override: bool


def _ensure_runner(model_runner: Optional[Callable[[Any, str, Dict[str, Any]], Any]]) -> Callable[[Any, str, Dict[str, Any]], Any]:
	if model_runner is None:
		def model_runner(content, model, params):
			# Stub runner: replace with a real model call in production
			return f"[Simulated output for model={model}]"
	return model_runner


def _merge_params(base: Any, override: Optional[Dict[str, Any]]) -> Dict[str, Any]:
	base_dict = base if isinstance(base, dict) else {}
	if override is None:
		return dict(base_dict)
	if not isinstance(override, dict):
		raise ValueError("override_params must be a dictionary when provided.")
	merged = dict(base_dict)
	merged.update(override)
	return merged


def replay_with_model_swap(
	flow: str,
	version: int,
	model: str,
	storage=None,
	model_runner: Optional[Callable[[Any, str, Dict[str, Any]], Any]] = None,
	params_override: Optional[Dict[str, Any]] = None,
	verbose: bool = True
) -> ReplayResult:
	"""
	Replay a prompt version with an alternate model (and optional params override) to compare outputs.
	Returns a structured result with original vs. swapped outputs.
	"""
	if storage is None:
		from promptscope.storage.sqlite import SQLiteStorage
		storage = SQLiteStorage()
	if not model:
		raise ValueError("A target model is required for replay.")

	runner = _ensure_runner(model_runner)
	prompt = storage.load_prompt_version(flow, version)
	if not prompt:
		msg = f"[PromptScope] No prompt found for flow '{flow}' version {version}"
		if verbose:
			print(msg)
		return {"flow": flow, "version": version, "target_model": model, "differs": False, "reason": msg}

	params = _merge_params(prompt.parameters, params_override)
	content = prompt.content or {}

	original_output = runner(content, prompt.model, params)
	swapped_output = runner(content, model, params)

	result: ReplayResult = {
		"flow": flow,
		"version": version,
		"source_model": prompt.model,
		"target_model": model,
		"parameters": params,
		"content": content,
		"original_output": original_output,
		"swapped_output": swapped_output,
		"differs": original_output != swapped_output,
		"ran_with_override": params_override is not None,
		"reason": "comparison_complete",
	}

	if verbose:
		print(f"[PromptScope] Replaying '{flow}' v{version} with model swap: {prompt.model} -> {model}")
		if params_override:
			print("[PromptScope] Parameters overridden for replay.")
		print("--- Original Output ---")
		print(original_output)
		print("--- Swapped Model Output ---")
		print(swapped_output)
		if result["differs"]:
			print("[PromptScope] Output differs between models.")
		else:
			print("[PromptScope] Outputs are identical.")
	return result


def replay_prompt(storage, request: ReplayRequest):
	"""
	Replay a prompt with possible model/param override.
	Args:
		storage: Storage backend instance.
		request: ReplayRequest object.
	Returns:
		Dict with model, content, params and metadata.
	"""
	prompt = storage.load_prompt_version(request.prompt_id, request.version)
	if not prompt:
		raise ValueError(f"Prompt {request.prompt_id} v{request.version} not found.")
	model = request.target_model or prompt.model
	params = _merge_params(prompt.parameters, request.override_params)
	return {
		"prompt_id": request.prompt_id,
		"version": request.version,
		"source_model": prompt.model,
		"model": model,
		"content": prompt.content or {},
		"params": params
	}
