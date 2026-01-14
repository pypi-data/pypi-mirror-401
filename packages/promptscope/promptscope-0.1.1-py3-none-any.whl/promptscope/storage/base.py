from abc import ABC, abstractmethod
from typing import Optional, List
from promptscope.models.prompt import PromptVersion

class BaseStorage(ABC):
    """
    Abstract base class for all PromptScope storage backends.
    Defines the required interface for versioned prompt storage.
    """

    @abstractmethod
    def get_latest_version(self, prompt_id: str) -> Optional[int]:
        """
        Get the latest version number for a prompt flow.
        Args:
            prompt_id: The prompt flow identifier.
        Returns:
            The latest version number, or None if not found.
        """
        pass

    @abstractmethod
    def list_versions(self, prompt_id: str) -> List[int]:
        """
        List all version numbers for a prompt flow.
        Args:
            prompt_id: The prompt flow identifier.
        Returns:
            List of version numbers (ascending).
        """
        pass

    @abstractmethod
    def save_prompt_version(self, prompt: PromptVersion) -> None:
        """
        Save a new prompt version.
        Args:
            prompt: The PromptVersion object to save.
        """
        pass

    @abstractmethod
    def load_prompt_version(self, prompt_id: str, version: int) -> Optional[PromptVersion]:
        """
        Load a specific prompt version.
        Args:
            prompt_id: The prompt flow identifier.
            version: The version number to load.
        Returns:
            The PromptVersion object, or None if not found.
        """
        pass

    def close(self):
        """Optional: Close any open resources (default: no-op)."""
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()