"""
LLM模块
提供统一的LLM接口，支持多种后端
"""

from .base import BaseLLM, Message, LLMResponse
from .openai_llm import OpenAILLM
from .local_llm import LocalLLM
from .factory import LLMFactory, create_llm_from_config

__all__ = [
    'BaseLLM',
    'Message',
    'LLMResponse',
    'OpenAILLM',
    'LocalLLM',
    'LLMFactory',
    'create_llm_from_config',
]
