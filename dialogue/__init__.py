"""
对话管理模块
整合LLM、RAG和记忆系统
"""

from .manager import DialogueManager, create_dialogue_manager_from_config

__all__ = [
    'DialogueManager',
    'create_dialogue_manager_from_config',
]
