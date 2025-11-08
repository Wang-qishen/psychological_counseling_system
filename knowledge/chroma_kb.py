"""
基于ChromaDB的向量知识库实现
"""

import os
import uuid
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

from .base import BaseKnowledgeBase, Document, RetrievalResult


class ChromaKnowledgeBase(BaseKnowledgeBase):
    """基于ChromaDB的向量知识库"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        初始化ChromaDB知识库
        
        Args:
            config: 配置字典
        """
        super().__init__(config)
        
        # 初始化embedding模型
        embedding_config = config.get('embedding', {})
        model_name = embedding_config.get(
            'model_name',
            'sentence-transformers/paraphrase-multilingual-mpnet-base-v2'
        )
        device = embedding_config.get('device', 'cuda')
        
        self.embedding_model = SentenceTransformer(model_name, device=device)
        
        # 初始化ChromaDB客户端
        persist_dir = config.get('persist_directory', './data/vector_db')
        os.makedirs(persist_dir, exist_ok=True)
        
        self.client = chromadb.PersistentClient(
            path=persist_dir,
            settings=Settings(anonymized_telemetry=False)
        )
        
        # 获取或创建collection
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"description": config.get('description', '')}
        )
    
    def add_documents(self, documents: List[Document]) -> None:
        """
        添加文档到知识库
        
        Args:
            documents: 文档列表
        """
        if not documents:
            return
        
        # 准备数据
        ids = []
        embeddings = []
        texts = []
        metadatas = []
        
        for doc in documents:
            # 生成ID
            doc_id = doc.doc_id or str(uuid.uuid4())
            ids.append(doc_id)
            
            # 生成embedding
            embedding = self.embedding_model.encode(
                doc.content,
                convert_to_numpy=True
            ).tolist()
            embeddings.append(embedding)
            
            texts.append(doc.content)
            metadatas.append(doc.metadata)
        
        # 批量添加
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas
        )
    
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
        # 生成query embedding
        query_embedding = self.embedding_model.encode(
            query,
            convert_to_numpy=True
        ).tolist()
        
        # 执行检索
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=filter_dict  # 元数据过滤
        )
        
        # 解析结果
        documents = []
        if results['documents'] and results['documents'][0]:
            for i in range(len(results['documents'][0])):
                doc = Document(
                    content=results['documents'][0][i],
                    metadata=results['metadatas'][0][i] if results['metadatas'] else {},
                    doc_id=results['ids'][0][i] if results['ids'] else None,
                    score=1.0 - results['distances'][0][i] if results['distances'] else None
                )
                documents.append(doc)
        
        return RetrievalResult(
            documents=documents,
            query=query,
            total_retrieved=len(documents)
        )
    
    def update_document(self, doc_id: str, document: Document) -> None:
        """
        更新文档
        
        Args:
            doc_id: 文档ID
            document: 新的文档内容
        """
        # 生成新的embedding
        embedding = self.embedding_model.encode(
            document.content,
            convert_to_numpy=True
        ).tolist()
        
        # 更新
        self.collection.update(
            ids=[doc_id],
            embeddings=[embedding],
            documents=[document.content],
            metadatas=[document.metadata]
        )
    
    def delete_document(self, doc_id: str) -> None:
        """
        删除文档
        
        Args:
            doc_id: 文档ID
        """
        self.collection.delete(ids=[doc_id])
    
    def clear(self) -> None:
        """清空知识库"""
        self.client.delete_collection(name=self.collection_name)
        self.collection = self.client.create_collection(
            name=self.collection_name,
            metadata=self.collection.metadata
        )
    
    def get_stats(self) -> Dict[str, Any]:
        """
        获取知识库统计信息
        
        Returns:
            统计信息字典
        """
        count = self.collection.count()
        return {
            'collection_name': self.collection_name,
            'document_count': count,
            'embedding_model': self.embedding_model.get_sentence_embedding_dimension()
        }
