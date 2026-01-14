import inspect
from functools import wraps
from typing import Any, Callable

from promptscope.sdk.client import PromptScopeClient

# Default client instance
client = PromptScopeClient()

def track_prompt(prompt_name: str) -> Callable:
    """
    Decorator to automatically track a function call as a prompt version.

    This decorator inspects the keyword arguments of the decorated function
    to find prompt content ("messages" or "prompt") and other parameters.
    """
    def wrapper(fn: Callable) -> Callable:
        @wraps(fn)
        def inner(*args, **kwargs):
            content = kwargs.get("messages") or kwargs.get("prompt")
            model = kwargs.get("model")
            
            # Exclude prompt content from params
            params = {k: v for k, v in kwargs.items() if k not in ["messages", "prompt"]}

            if content and model:
                client.track(
                    prompt_name=prompt_name,
                    content=content,
                    model=model,
                    params=params
                )
            return fn(*args, **kwargs)
        return inner
    return wrapper
