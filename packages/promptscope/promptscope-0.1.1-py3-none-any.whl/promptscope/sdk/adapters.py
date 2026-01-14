import functools
import inspect
from typing import Callable

import openai

from promptscope.sdk.client import PromptScopeClient

_client = PromptScopeClient()

# Optional legacy OpenAI globals (present in v0.x, absent in v1.x client)
try:
	_original_chat_create = openai.ChatCompletion.create  # type: ignore[attr-defined]
	_original_chat_acreate = openai.ChatCompletion.acreate  # type: ignore[attr-defined]
	_original_completion_create = openai.Completion.create  # type: ignore[attr-defined]
	_original_completion_acreate = openai.Completion.acreate  # type: ignore[attr-defined]
except AttributeError:
	_original_chat_create = None
	_original_chat_acreate = None
	_original_completion_create = None
	_original_completion_acreate = None

def _get_prompt_name(offset=2) -> str:
    """
    Get the name of the calling function.
    This is a fragile way to get a prompt name, but it's a reasonable default.
    """
    try:
        frame = inspect.currentframe()
        if frame is None:
            return "unknown"
        for _ in range(offset):
            frame = frame.f_back
            if frame is None:
                return "unknown"
        return frame.f_code.co_name
    except Exception:
        return "unknown"


def _wrap_sync(func: Callable, prompt_name_prefix: str) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        prompt_name = f"{prompt_name_prefix}:{_get_prompt_name()}"
        content = kwargs.get("messages") or kwargs.get("prompt")
        model = kwargs.get("model")
        params = {k: v for k, v in kwargs.items() if k not in ["messages", "prompt"]}
        
        if content and model:
            _client.track(
                prompt_name=prompt_name,
                content=content,
                model=model,
                params=params,
                # allow duplicates because we want to record every API call
                allow_duplicate=True
            )
        return func(*args, **kwargs)
    return wrapper

def _wrap_async(func: Callable, prompt_name_prefix: str) -> Callable:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        prompt_name = f"{prompt_name_prefix}:{_get_prompt_name()}"
        content = kwargs.get("messages") or kwargs.get("prompt")
        model = kwargs.get("model")
        params = {k: v for k, v in kwargs.items() if k not in ["messages", "prompt"]}

        if content and model:
            _client.track(
                prompt_name=prompt_name,
                content=content,
                model=model,
                params=params,
                allow_duplicate=True
            )
        return await func(*args, **kwargs)
    return wrapper


def autoinstrument(prompt_name_prefix="openai"):
	"""
	Automatically instrument the OpenAI library to track prompts.
	This monkey-patches the OpenAI API client.
	"""
	# Legacy patching path (OpenAI v0.x). Newer v1 client uses OpenAI() instances; for those,
	# consumers should prefer PromptScopeOpenAI/PromptScopeAsyncOpenAI.
	legacy_chat = getattr(openai, "ChatCompletion", None)
	legacy_completion = getattr(openai, "Completion", None)

	if not legacy_chat or not legacy_completion:
		# Nothing to instrument; fail silently to avoid crashing when OpenAI globals are absent.
		return

	if getattr(legacy_chat, "_is_promptscope_instrumented", False):
		return

	if _original_chat_create:
		legacy_chat.create = _wrap_sync(_original_chat_create, prompt_name_prefix)
	if _original_chat_acreate:
		legacy_chat.acreate = _wrap_async(_original_chat_acreate, prompt_name_prefix)
	if _original_completion_create:
		legacy_completion.create = _wrap_sync(_original_completion_create, prompt_name_prefix)
	if _original_completion_acreate:
		legacy_completion.acreate = _wrap_async(_original_completion_acreate, prompt_name_prefix)

	setattr(legacy_chat, "_is_promptscope_instrumented", True)
	setattr(legacy_completion, "_is_promptscope_instrumented", True)
