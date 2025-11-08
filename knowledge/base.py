"""
知识库基类
定义统一的知识库接口
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class Document:
    """文档数据结构"""
    content: str
    metadata: Dict[str, Any]
    doc_id: Optional[str] = None
    score: Optional[float] = None  # 检索时的相似度分数


@dataclass
class RetrievalResult:
    """检索结果"""
    documents: List[Document]
    query: str
    total_retrieved: int


class BaseKnowledgeBase(ABC):
    """知识库基类"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        初始化知识库
        
        Args:
            config: 知识库配置
        """
        self.config = config
        self.collection_name = config.get('collection_name', 'default')
    
    @abstractmethod
    def add_documents(self, documents: List[Document]) -> None:
        """
        添加文档到知识库
        
        Args:
            documents: 文档列表
        """
        pass
    
    @abstractmethod
    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        filter_dict: Optional[Dict[str, Any]] = None
    ) -> RetrievalResult:
        """
        检索相关文档
        
        Args:
            query: 查询文本
            top_k: 返回top-k个结果
            filter_dict: 元数据过滤条件
            
        Returns:
            检索结果
        """
        pass
    
    @abstractmethod
    def update_document(self, doc_id: str, document: Document) -> None:
        """
        更新文档
        
        Args:
            doc_id: 文档ID
            document: 新的文档内容
        """
        pass
    
    @abstractmethod
    def delete_document(self, doc_id: str) -> None:
        """
        删除文档
        
        Args:
            doc_id: 文档ID
        """
        pass
    
    @abstractmethod
    def clear(self) -> None:
        """清空知识库"""
        pass
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(collection={self.collection_name})"
