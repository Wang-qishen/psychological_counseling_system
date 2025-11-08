"""
知识库模块
提供RAG功能，整合心理知识和用户知识
"""

from .base import BaseKnowledgeBase, Document, RetrievalResult
from .chroma_kb import ChromaKnowledgeBase
from .rag_manager import RAGManager, RAGResult, create_rag_manager_from_config

__all__ = [
    'BaseKnowledgeBase',
    'Document',
    'RetrievalResult',
    'ChromaKnowledgeBase',
    'RAGManager',
    'RAGResult',
    'create_rag_manager_from_config',
]
