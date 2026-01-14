from typing import Any, Dict, Optional, Tuple
from promptscope.core.cost import calculate_cost

from promptscope.utils.hashing import hash_prompt
from promptscope.utils.time import now_utc
from promptscope.core.versioning import next_version
from promptscope.models.prompt import PromptVersion


def track_prompt(storage, 
                 prompt_id: str, 
                 content: Any, 
                 model: str, 
                 params: Dict[str, Any], 
                 activate: bool = True, 
                 allow_duplicate: bool = False,
                 response: Optional[Dict[str, Any]] = None,
                 response_ms: Optional[int] = None) -> Tuple[PromptVersion, bool]:
    """
    Track and persist a new prompt version if content changed (or if forced).
    Returns (PromptVersion, created_flag).
    """
    if storage is None:
        from promptscope.storage.sqlite import SQLiteStorage
        storage = SQLiteStorage()

    latest_version = storage.get_latest_version(prompt_id)
    content_hash = hash_prompt(content, model, params)

    if latest_version and not allow_duplicate:
        latest_prompt = storage.load_prompt_version(prompt_id, latest_version)
        if latest_prompt and latest_prompt.content_hash == content_hash:
            return latest_prompt, False

    version = next_version(latest_version)
    
    cost = None
    if response and response.get("usage"):
        usage = response["usage"]
        cost = calculate_cost(model, usage.get("prompt_tokens", 0), usage.get("completion_tokens", 0))

    prompt = PromptVersion(
        prompt_id=prompt_id,
        version=version,
        content=content,
        model=model,
        parameters=params,
        content_hash=content_hash,
        created_at=now_utc(),
        response=response,
        response_ms=response_ms,
        cost=cost
    )
    storage.save_prompt_version(prompt)
    if activate and hasattr(storage, "set_active_version"):
        storage.set_active_version(prompt_id, version)
    return prompt, True