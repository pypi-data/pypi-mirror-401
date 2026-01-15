# fireprompt/__init__.py
# SPDX-License-Identifier: MIT

"""
FirePrompt - Turn Python functions into LLM prompts.

A lightweight Python library for building type-safe LLM prompts with Jinja2
templating and Pydantic validation.
"""

# imports
import warnings

from fireprompt.types import LLM
from fireprompt.api import prompt
from fireprompt.types import LLMConfig
from fireprompt.types import LLMConfigPreset
from fireprompt.logger import set_debug_mode

# suppress litellm cleanup warnings
warnings.filterwarnings(
    "ignore",
    category=RuntimeWarning,
    message=".*coroutine.*was never awaited.*"
)


warnings.filterwarnings(
    "ignore",
    category=UserWarning,
    message=r"^Pydantic serializer warnings:.*",
)


# exports public APIs
__all__ = [
    "prompt",
    "LLM",
    "LLMConfig",
    "LLMConfigPreset",
    "enable_logging",
    "disable_logging"
]

# version
__version__ = "0.1.9"


# logging
def enable_logging() -> None:
    """Enable logging."""
    set_debug_mode(True)


def disable_logging() -> None:
    """Disable logging."""
    set_debug_mode(False)
