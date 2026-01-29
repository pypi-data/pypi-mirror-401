"""Framework integrations for Monora.

This package provides first-class integrations with popular AI frameworks:
- LangChain (Python)
- OpenAI SDK
- Anthropic SDK
- Vercel AI SDK (coming soon)
"""

from typing import TYPE_CHECKING

from .anthropic_sdk import patch_anthropic
from .langchain import MonoraCallbackHandler
from .openai_sdk import patch_openai

if TYPE_CHECKING:
    from .anthropic_sdk import patch_anthropic as patch_anthropic
    from .langchain import MonoraCallbackHandler as MonoraCallbackHandler
    from .openai_sdk import patch_openai as patch_openai

__all__ = ["MonoraCallbackHandler", "patch_openai", "patch_anthropic"]
