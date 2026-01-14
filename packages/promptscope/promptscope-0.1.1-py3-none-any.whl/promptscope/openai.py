"""
This module provides enhanced OpenAI clients with features like caching, retries,
and automatic prompt tracking for PromptScope.
"""
import warnings
import openai
from openai import OpenAI, AsyncOpenAI, RateLimitError, APITimeoutError, APIConnectionError, InternalServerError
import time
import asyncio
import functools
import hashlib
import json
from typing import Callable, Any, Dict, Optional

from promptscope.sdk.client import PromptScopeClient
from promptscope.core.cost import calculate_cost

# --- PromptScope client for tracking ---
_ps_client = PromptScopeClient()


class BudgetExceededError(RuntimeError):
    """Raised when a response cost exceeds the configured maximum."""
    pass

# --- In-memory cache ---
_CACHE: Dict[str, Any] = {}


def _get_cache_key(model: str, messages: list, **kwargs) -> str:
    """Creates a consistent hash key for caching based on request parameters."""
    hasher = hashlib.sha256()
    hasher.update(model.encode())
    hasher.update(json.dumps(messages, sort_keys=True).encode())
    # Include other relevant parameters that affect the response
    for key, value in sorted(kwargs.items()):
        if key not in ["user", "api_key", "base_url", "timeout", "extra_body"]:  # Exclude transient/auth keys
            try:
                hasher.update(f"{key}:{json.dumps(value, sort_keys=True)}".encode())
            except TypeError:
                # For non-serializable values, use a string representation
                hasher.update(f"{key}:{str(value)}".encode())
    return hasher.hexdigest()


def _clear_cache():
    """Clears the in-memory cache."""
    _CACHE.clear()


# --- Retry logic ---
def _retry_with_exponential_backoff(
    func: Callable,
    retries: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0,
):
    """Decorator for retrying a function with exponential backoff."""
    
    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs):
        delay = initial_delay
        for i in range(retries + 1):
            try:
                return await func(*args, **kwargs)
            except (RateLimitError, APITimeoutError, APIConnectionError, InternalServerError) as e:
                if i == retries:
                    raise
                warnings.warn(
                    f"API call failed with {e}, retrying in {delay:.2f} seconds...",
                    UserWarning,
                )
                await asyncio.sleep(delay)
                delay *= backoff_factor

    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs):
        delay = initial_delay
        for i in range(retries + 1):
            try:
                return func(*args, **kwargs)
            except (RateLimitError, APITimeoutError, APIConnectionError, InternalServerError) as e:
                if i == retries:
                    raise
                warnings.warn(
                    f"API call failed with {e}, retrying in {delay:.2f} seconds...",
                    UserWarning,
                )
                time.sleep(delay)
                delay *= backoff_factor

    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    return sync_wrapper


class PromptScopeOpenAI(OpenAI):
    """
    An enhanced OpenAI client with caching, retries, and automatic prompt tracking.
    """

    def __init__(
        self,
        *args,
        enable_cache: bool = True,
        retries: int = 3,
        storage: Any = None,
        max_cost: Optional[float] = None,
        **kwargs,
    ):
        """
        Initializes the PromptScopeOpenAI client.

        Args:
            enable_cache (bool): Whether to enable in-memory caching for responses.
            retries (int): Number of times to retry on API failure.
            storage: (BaseStorage, optional): A PromptScope storage backend.
                If not provided, the default SQLite backend will be used.
            max_cost (float, optional): If set, raise when a response cost exceeds this USD threshold.
        """
        # Disable the SDK's built-in retries so we can handle retries ourselves
        # and emit warnings when failures occur.
        kwargs.setdefault("max_retries", 0)
        super().__init__(*args, **kwargs)
        self.enable_cache = enable_cache
        self.retries = retries
        self.max_cost = max_cost
        self._ps_client = PromptScopeClient(storage=storage) if storage else _ps_client
        # Override the chat completions create method with our retry/caching/tracking logic.
        original_create = self.chat.completions.create
        self.chat.completions.create = self._create_wrapper(original_create)

    def _create_wrapper(self, original_create_func: Callable) -> Callable:
        @functools.wraps(original_create_func)
        def wrapper(*, model: str, messages: list, **kwargs):
            prompt_name = kwargs.get("extra_body", {}).get("prompt_name")
            params = {k: v for k, v in kwargs.items() if k not in ["extra_body"]}

            if self.enable_cache:
                if kwargs.get("stream", False):
                    warnings.warn("Caching is not supported for streaming requests.", UserWarning)
                else:
                    cache_key = _get_cache_key(model, messages, **params)
                    if cache_key in _CACHE:
                        return _CACHE[cache_key]

            delay = 1.0
            response = None
            for attempt in range(self.retries + 1):
                try:
                    start_time = time.perf_counter()
                    response = original_create_func(model=model, messages=messages, **kwargs)
                    end_time = time.perf_counter()
                    break
                except (RateLimitError, APITimeoutError, APIConnectionError, InternalServerError) as e:
                    if attempt == self.retries:
                        raise
                    warnings.warn(
                        f"API call failed with {e}, retrying in {delay:.2f} seconds...",
                        UserWarning,
                    )
                    time.sleep(delay)
                    delay *= 2.0

            if response is None:
                raise RuntimeError("Failed to obtain response after retries")
            response_ms = round((end_time - start_time) * 1000)
            
            # Optional budget guard
            usage = getattr(response, "usage", None)
            if usage and self.max_cost is not None:
                cost = calculate_cost(model, usage.get("prompt_tokens", 0), usage.get("completion_tokens", 0))
                if cost > self.max_cost:
                    raise BudgetExceededError(
                        f"Response cost {cost:.6f} exceeds configured max_cost {self.max_cost:.6f}"
                    )
            
            if prompt_name:
                self._ps_client.track(
                    prompt_name=prompt_name,
                    content=messages,
                    model=model,
                    params=params,
                    allow_duplicate=True,
                    response=response.model_dump(),
                    response_ms=response_ms
                )
            
            if self.enable_cache and not kwargs.get("stream", False):
                cache_key = _get_cache_key(model, messages, **params)
                _CACHE[cache_key] = response
            
            return response

        return wrapper


class PromptScopeAsyncOpenAI(AsyncOpenAI):
    """
    An enhanced AsyncOpenAI client with caching, retries, and automatic prompt tracking.
    """

    def __init__(
        self,
        *args,
        enable_cache: bool = True,
        retries: int = 3,
        storage: Any = None,
        max_cost: Optional[float] = None,
        **kwargs,
    ):
        """
        Initializes the PromptScopeAsyncOpenAI client.

        Args:
            enable_cache (bool): Whether to enable in-memory caching for responses.
            retries (int): Number of times to retry on API failure.
            storage: (BaseStorage, optional): A PromptScope storage backend.
                If not provided, the default SQLite backend will be used.
            max_cost (float, optional): If set, raise when a response cost exceeds this USD threshold.
        """
        # Disable built-in retries to rely on our own retry handler (emits warnings).
        kwargs.setdefault("max_retries", 0)
        super().__init__(*args, **kwargs)
        self.enable_cache = enable_cache
        self.retries = retries
        self.max_cost = max_cost
        self._ps_client = PromptScopeClient(storage=storage) if storage else _ps_client

        # Override the chat completions create method
        original_create = self.chat.completions.create
        self.chat.completions.create = self._create_wrapper(original_create)

    def _create_wrapper(self, original_create_func: Callable) -> Callable:
        @functools.wraps(original_create_func)
        async def wrapper(*, model: str, messages: list, **kwargs):
            prompt_name = kwargs.get("extra_body", {}).get("prompt_name")
            params = {k: v for k, v in kwargs.items() if k not in ["extra_body"]}

            if self.enable_cache:
                if kwargs.get("stream", False):
                    warnings.warn("Caching is not supported for streaming requests.", UserWarning)
                else:
                    cache_key = _get_cache_key(model, messages, **params)
                    if cache_key in _CACHE:
                        return _CACHE[cache_key]

            delay = 1.0
            response = None
            for attempt in range(self.retries + 1):
                try:
                    start_time = time.perf_counter()
                    response = await original_create_func(model=model, messages=messages, **kwargs)
                    end_time = time.perf_counter()
                    break
                except (RateLimitError, APITimeoutError, APIConnectionError, InternalServerError) as e:
                    if attempt == self.retries:
                        raise
                    warnings.warn(
                        f"API call failed with {e}, retrying in {delay:.2f} seconds...",
                        UserWarning,
                    )
                    await asyncio.sleep(delay)
                    delay *= 2.0

            if response is None:
                raise RuntimeError("Failed to obtain response after retries")
            response_ms = round((end_time - start_time) * 1000)

            # Optional budget guard
            usage = getattr(response, "usage", None)
            if usage and self.max_cost is not None:
                cost = calculate_cost(model, usage.get("prompt_tokens", 0), usage.get("completion_tokens", 0))
                if cost > self.max_cost:
                    raise BudgetExceededError(
                        f"Response cost {cost:.6f} exceeds configured max_cost {self.max_cost:.6f}"
                    )
            
            if prompt_name:
                self._ps_client.track(
                    prompt_name=prompt_name,
                    content=messages,
                    model=model,
                    params=params,
                    allow_duplicate=True,
                    response=response.model_dump(),
                    response_ms=response_ms
                )

            if self.enable_cache and not kwargs.get("stream", False):
                cache_key = _get_cache_key(model, messages, **params)
                _CACHE[cache_key] = response

            return response

        return wrapper

# --- Deprecated ---
class DeprecatedOpenAI(OpenAI):
    """
    This class is for backward compatibility. New code should use `promptscope.autoinstrument()`
    at the start of the application, or use the more advanced `PromptScopeOpenAI` client.
    """
    def __init__(self, *args, **kwargs):
        from promptscope.sdk import autoinstrument
        warnings.warn(
            "'promptscope.openai.OpenAI' is deprecated and will be removed in a future version. "
            "Use `import openai` and call `promptscope.autoinstrument()` once at the start of your application. "
            "For advanced features like caching and retries, use `from promptscope.openai import PromptScopeOpenAI`.",
            DeprecationWarning,
            stacklevel=2,
        )
        autoinstrument()
        super().__init__(*args, **kwargs)

# For backward compatibility, alias the class to OpenAI if the user wants a true drop-in
OpenAI = DeprecatedOpenAI
