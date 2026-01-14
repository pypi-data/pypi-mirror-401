"""
PromptScope SDK
"""

from .client import PromptScopeClient
from .adapters import autoinstrument
from .decorators import track_prompt

__all__ = [
    "PromptScopeClient",
    "autoinstrument",
    "track_prompt",
    "track"
]

_default_client = PromptScopeClient()

def track(prompt_name: str, content: any, model: str, params: dict, **kwargs):
    """
    Track a prompt using the default client.

    :param prompt_name: The name of the prompt.
    :param content: The content of the prompt (e.g., a string or a list of messages).
    :param model: The model used to generate the output.
    :param params: A dictionary of parameters used for the generation.
    """
    return _default_client.track(prompt_name, content, model, params, **kwargs)
