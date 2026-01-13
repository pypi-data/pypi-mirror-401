"""
Wrappers for automatic usage tracking with AI provider SDKs.

This module provides wrapper classes that intercept API calls to various AI providers
and automatically send usage data to Paygent for tracking and billing.
"""

from .openai_wrapper import PaygentOpenAI
from .anthropic_wrapper import PaygentAnthropic
from .mistral_wrapper import PaygentMistral
from .gemini_wrapper import PaygentGemini

# LangChain integration (optional dependency)
try:
    from .langchain_wrapper import PaygentLangChainCallback
    __all__ = [
        "PaygentOpenAI",
        "PaygentAnthropic",
        "PaygentMistral",
        "PaygentGemini",
        "PaygentLangChainCallback",
    ]
except ImportError:
    # LangChain not installed
    __all__ = [
        "PaygentOpenAI",
        "PaygentAnthropic",
        "PaygentMistral",
        "PaygentGemini",
    ]
