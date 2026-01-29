"""
Joule SDK for Python

Track AI API usage with automatic monitoring of costs, tokens, and performance.
Works with OpenAI and Anthropic SDKs.
"""

from .client import JouleClient
from .openai_wrapper import JouleOpenAI
from .anthropic_wrapper import JouleAnthropic

__version__ = "0.1.0"
__all__ = ["JouleClient", "JouleOpenAI", "JouleAnthropic"]
