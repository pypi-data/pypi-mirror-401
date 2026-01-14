import importlib.metadata
from typing import Dict, Union

# Default version for when the package is not installed (e.g., in development)
__dev_version__ = "0.1.0.dev"

try:
    # This will work when the package is installed via pip
    __version__ = importlib.metadata.version("promptscope")
except importlib.metadata.PackageNotFoundError:
    # Fallback for development mode
    __version__ = __dev_version__

VERSION = __version__.split('.')

def get_version_info() -> Dict[str, Union[str, int]]:
    """
    Returns a dictionary of version information.
    """
    major, minor, patch, *extra = VERSION
    return {
        "major": int(major),
        "minor": int(minor),
        "patch": int(patch),
        "extra": '.'.join(extra),
        "full": __version__,
    }

def get_user_agent() -> str:
    """
    Returns a user-agent string for API requests.
    """
    return f"promptscope-py/{__version__}"