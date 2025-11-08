"""
RAG管理器
整合心理知识库和用户知识库，提供统一的检索接口
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from .base import BaseKnowledgeBase, Document, RetrievalResult
from .chroma_kb import ChromaKnowledgeBase


@dataclass
class RAGResult:
    """RAG检索结果"""
    psychological_docs: List[Document]
    user_docs: List[Document]
    combined_context: str
    metadata: Dict[str, Any]


class RAGManager:
    """RAG管理器，整合多个知识库"""
    
    def __init__(
        self,
        psychological_kb: BaseKnowledgeBase,
        user_kb: BaseKnowledgeBase,
        config: Optional[Dict[str, Any]] = None
    ):
        """
        初始化RAG管理器
        
        Args:
            psychological_kb: 心理知识库
            user_kb: 用户知识库
            config: 配置参数
        """
        self.psychological_kb = psychological_kb
        self.user_kb = user_kb
        self.config = config or {}
        
        # 检索参数
        self.top_k = self.config.get('top_k', 5)
        self.score_threshold = self.config.get('score_threshold', 0.5)
        
        # 知识源权重
        weights = self.config.get('weights', {})
        self.psych_weight = weights.get('psychological_knowledge', 0.6)
        self.user_weight = weights.get('user_knowledge', 0.4)
    
    def retrieve(
        self,
        query: str,
        user_id: Optional[str] = None,
        top_k: Optional[int] = None,
        enable_rerank: bool = True
    ) -> RAGResult:
        """
        从两个知识库检索相关信息
        
        Args:
            query: 查询文本
            user_id: 用户ID（用于过滤用户知识库）
            top_k: 每个知识库返回的文档数
            enable_rerank: 是否重排序
            
        Returns:
            RAG检索结果
        """
        k = top_k or self.top_k
        
        # 从心理知识库检索
        psych_result = self.psychological_kb.retrieve(
            query=query,
            top_k=k
        )
        
        # 从用户知识库检索
        user_filter = {'user_id': user_id} if user_id else None
        user_result = self.user_kb.retrieve(
            query=query,
            top_k=k,
            filter_dict=user_filter
        )
        
        # 过滤低分文档
        psych_docs = [
            doc for doc in psych_result.documents
            if doc.score is None or doc.score >= self.score_threshold
        ]
        
        user_docs = [
            doc for doc in user_result.documents
            if doc.score is None or doc.score >= self.score_threshold
        ]
        
        # 重排序（如果启用）
        if enable_rerank:
            psych_docs = self._rerank(query, psych_docs)
            user_docs = self._rerank(query, user_docs)
        
        # 构建组合上下文
        combined_context = self._build_context(psych_docs, user_docs)
        
        # 元数据
        metadata = {
            'psych_doc_count': len(psych_docs),
            'user_doc_count': len(user_docs),
            'query': query,
            'user_id': user_id
        }
        
        return RAGResult(
            psychological_docs=psych_docs,
            user_docs=user_docs,
            combined_context=combined_context,
            metadata=metadata
        )
    
    def _rerank(self, query: str, documents: List[Document]) -> List[Document]:
        """
        重排序文档（简单实现，基于分数）
        
        Args:
            query: 查询文本
            documents: 文档列表
            
        Returns:
            重排序后的文档列表
        """
        # 简单的基于分数的排序
        # 更复杂的可以使用cross-encoder模型
        return sorted(
            documents,
            key=lambda x: x.score if x.score is not None else 0.0,
            reverse=True
        )
    
    def _build_context(
        self,
        psych_docs: List[Document],
        user_docs: List[Document]
    ) -> str:
        """
        构建组合上下文
        
        Args:
            psych_docs: 心理知识文档
            user_docs: 用户知识文档
            
        Returns:
            格式化的上下文字符串
        """
        context_parts = []
        
        # 添加心理知识
        if psych_docs:
            context_parts.append("=== 相关心理学知识 ===")
            for i, doc in enumerate(psych_docs, 1):
                context_parts.append(f"{i}. {doc.content}")
            context_parts.append("")
        
        # 添加用户信息
        if user_docs:
            context_parts.append("=== 用户相关信息 ===")
            for i, doc in enumerate(user_docs, 1):
                context_parts.append(f"{i}. {doc.content}")
            context_parts.append("")
        
        return "\n".join(context_parts)
    
    def add_psychological_knowledge(self, documents: List[Document]) -> None:
        """
        添加心理知识
        
        Args:
            documents: 文档列表
        """
        self.psychological_kb.add_documents(documents)
    
    def add_user_knowledge(
        self,
        user_id: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        添加用户知识
        
        Args:
            user_id: 用户ID
            content: 内容
            metadata: 额外元数据
        """
        doc_metadata = metadata or {}
        doc_metadata['user_id'] = user_id
        
        document = Document(
            content=content,
            metadata=doc_metadata
        )
        
        self.user_kb.add_documents([document])
    
    def get_stats(self) -> Dict[str, Any]:
        """
        获取统计信息
        
        Returns:
            统计信息字典
        """
        return {
            'psychological_kb': self.psychological_kb.get_stats(),
            'user_kb': self.user_kb.get_stats(),
            'config': {
                'top_k': self.top_k,
                'score_threshold': self.score_threshold,
                'weights': {
                    'psychological': self.psych_weight,
                    'user': self.user_weight
                }
            }
        }


def create_rag_manager_from_config(config: Dict[str, Any]) -> RAGManager:
    """
    从配置创建RAG管理器
    
    Args:
        config: 配置字典
        
    Returns:
        RAGManager实例
    """
    # 创建心理知识库
    psych_config = config['knowledge']['psychological_kb']
    psych_config['embedding'] = config['rag']['embedding']
    psych_config['persist_directory'] = config['rag']['vector_store']['persist_directory']
    
    psychological_kb = ChromaKnowledgeBase(psych_config)
    
    # 创建用户知识库
    user_config = config['knowledge']['user_kb']
    user_config['embedding'] = config['rag']['embedding']
    user_config['persist_directory'] = config['rag']['vector_store']['persist_directory']
    
    user_kb = ChromaKnowledgeBase(user_config)
    
    # 创建RAG管理器
    rag_config = {
        'top_k': config['rag']['retrieval']['top_k'],
        'score_threshold': config['rag']['retrieval']['score_threshold'],
        'weights': config['dialogue']['generation']['weights']
    }
    
    return RAGManager(
        psychological_kb=psychological_kb,
        user_kb=user_kb,
        config=rag_config
    )
