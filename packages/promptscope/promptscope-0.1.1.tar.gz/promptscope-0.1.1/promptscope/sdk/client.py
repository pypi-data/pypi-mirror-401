from typing import Any, Dict

from promptscope.core.tracker import track_prompt
from promptscope.storage.base import BaseStorage


class PromptScopeClient:
    def __init__(self, storage: BaseStorage = None):
        self._storage = storage

    @property
    def storage(self) -> BaseStorage:
        if self._storage is None:
            # Lazy initialization of default storage
            from promptscope.storage.sqlite import SQLiteStorage
            self._storage = SQLiteStorage()
        return self._storage

    def track(self, prompt_name: str, content: Any, model: str, params: Dict[str, Any], **kwargs):
        return track_prompt(
            self.storage,
            prompt_name,
            content,
            model,
            params,
            **kwargs
        )
