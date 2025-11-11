"""
RAG知识库导入工具 - 将处理后的数据导入到ChromaDB
"""

import sys
import logging
from pathlib import Path
from typing import List, Dict
import yaml

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from knowledge.rag_manager import RAGManager
from knowledge.chroma_kb import ChromaKnowledgeBase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RAGImporter:
    """RAG知识库导入器"""
    
    def __init__(self, config_path: str = "./configs/config.yaml"):
        """
        初始化导入器
        
        Args:
            config_path: 配置文件路径
        """
        # 加载配置
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        
        # 创建RAG管理器
        self.rag_manager = self._create_rag_manager()
        
        self.stats = {
            'total_files': 0,
            'total_documents': 0,
            'failed_files': 0,
            'success_rate': 0.0
        }
    
    def _create_rag_manager(self) -> RAGManager:
        """
        创建RAG管理器
        
        Returns:
            RAG管理器实例
        """
        logger.info("初始化RAG管理器...")
        
        # 创建心理知识库
        psych_kb = ChromaKnowledgeBase(
            collection_name="psychological_knowledge_extended",  # 新的集合名
            persist_directory=self.config['rag']['vector_store']['persist_directory'],
            embedding_model=self.config['rag']['embedding']['model_name']
        )
        
        # 创建RAG管理器
        rag_manager = RAGManager(
            psychological_kb=psych_kb,
            user_kb=None,  # 暂不使用用户知识库
            config=self.config['rag']
        )
        
        logger.info("✓ RAG管理器初始化完成")
        return rag_manager
    
    def import_from_directory(
        self, 
        data_dir: str,
        file_pattern: str = "*.txt"
    ) -> Dict:
        """
        从目录导入数据
        
        Args:
            data_dir: 数据目录
            file_pattern: 文件模式
            
        Returns:
            导入统计信息
        """
        logger.info(f"开始从目录导入: {data_dir}")
        
        data_path = Path(data_dir)
        if not data_path.exists():
            logger.error(f"目录不存在: {data_dir}")
            return self.stats
        
        # 查找所有TXT文件
        txt_files = list(data_path.rglob(file_pattern))
        
        if not txt_files:
            logger.warning(f"未找到任何 {file_pattern} 文件")
            return self.stats
        
        logger.info(f"找到 {len(txt_files)} 个文件")
        self.stats['total_files'] = len(txt_files)
        
        # 逐个文件导入
        for txt_file in txt_files:
            try:
                logger.info(f"导入: {txt_file.name}")
                count = self._import_file(txt_file)
                self.stats['total_documents'] += count
                logger.info(f"✓ {txt_file.name}: {count} 条文档")
                
            except Exception as e:
                logger.error(f"✗ {txt_file.name} 导入失败: {e}")
                self.stats['failed_files'] += 1
        
        # 计算成功率
        if self.stats['total_files'] > 0:
            success_files = self.stats['total_files'] - self.stats['failed_files']
            self.stats['success_rate'] = success_files / self.stats['total_files']
        
        return self.stats
    
    def _import_file(self, file_path: Path) -> int:
        """
        导入单个文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            导入的文档数量
        """
        # 读取文件
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 按分隔符分割文档
        documents = content.split("="*60)
        documents = [doc.strip() for doc in documents if doc.strip()]
        
        if not documents:
            return 0
        
        # 准备文档列表
        docs_to_add = []
        metadatas = []
        
        for idx, doc_content in enumerate(documents):
            if len(doc_content) < 10:  # 过滤太短的文档
                continue
            
            docs_to_add.append(doc_content)
            
            # 元数据
            metadata = {
                'source_file': file_path.name,
                'source_dir': file_path.parent.name,
                'document_index': idx,
                'type': 'knowledge_base'
            }
            metadatas.append(metadata)
        
        # 添加到知识库
        if docs_to_add:
            self.rag_manager.psychological_kb.add_documents(
                documents=docs_to_add,
                metadatas=metadatas
            )
        
        return len(docs_to_add)
    
    def import_with_chunking(
        self,
        data_dir: str,
        chunk_size: int = 500,
        chunk_overlap: int = 50
    ) -> Dict:
        """
        使用分块导入数据(适合长文本)
        
        Args:
            data_dir: 数据目录
            chunk_size: 分块大小
            chunk_overlap: 分块重叠
            
        Returns:
            导入统计信息
        """
        logger.info(f"使用分块导入 (chunk_size={chunk_size}, overlap={chunk_overlap})")
        
        data_path = Path(data_dir)
        txt_files = list(data_path.rglob("*.txt"))
        
        self.stats['total_files'] = len(txt_files)
        
        for txt_file in txt_files:
            try:
                logger.info(f"导入: {txt_file.name}")
                
                with open(txt_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 分块
                chunks = self._chunk_text(content, chunk_size, chunk_overlap)
                
                # 准备元数据
                metadatas = []
                for idx in range(len(chunks)):
                    metadatas.append({
                        'source_file': txt_file.name,
                        'source_dir': txt_file.parent.name,
                        'chunk_index': idx,
                        'total_chunks': len(chunks),
                        'type': 'knowledge_chunk'
                    })
                
                # 添加到知识库
                self.rag_manager.psychological_kb.add_documents(
                    documents=chunks,
                    metadatas=metadatas
                )
                
                self.stats['total_documents'] += len(chunks)
                logger.info(f"✓ {txt_file.name}: {len(chunks)} 个分块")
                
            except Exception as e:
                logger.error(f"✗ {txt_file.name} 导入失败: {e}")
                self.stats['failed_files'] += 1
        
        if self.stats['total_files'] > 0:
            success_files = self.stats['total_files'] - self.stats['failed_files']
            self.stats['success_rate'] = success_files / self.stats['total_files']
        
        return self.stats
    
    def _chunk_text(
        self, 
        text: str, 
        chunk_size: int, 
        overlap: int
    ) -> List[str]:
        """
        文本分块
        
        Args:
            text: 原始文本
            chunk_size: 分块大小
            overlap: 重叠大小
            
        Returns:
            分块列表
        """
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = start + chunk_size
            chunk = text[start:end]
            
            if chunk.strip():
                chunks.append(chunk)
            
            start = end - overlap
        
        return chunks
    
    def verify_import(self, test_queries: List[str] = None) -> Dict:
        """
        验证导入结果
        
        Args:
            test_queries: 测试查询列表
            
        Returns:
            验证结果
        """
        logger.info("\n验证导入结果...")
        
        if test_queries is None:
            test_queries = [
                "抑郁症的症状",
                "如何缓解焦虑",
                "失眠怎么办",
                "人际关系问题"
            ]
        
        results = {}
        
        for query in test_queries:
            logger.info(f"\n测试查询: {query}")
            
            try:
                rag_result = self.rag_manager.retrieve(
                    query=query,
                    top_k=3
                )
                
                results[query] = {
                    'success': True,
                    'retrieved_count': len(rag_result.psychological_docs),
                    'top_scores': [
                        doc.get('score', 0.0) 
                        for doc in rag_result.psychological_docs[:3]
                    ]
                }
                
                logger.info(f"✓ 检索到 {len(rag_result.psychological_docs)} 条相关知识")
                
                # 显示前2条
                for i, doc in enumerate(rag_result.psychological_docs[:2], 1):
                    preview = doc['content'][:100] + "..." if len(doc['content']) > 100 else doc['content']
                    logger.info(f"  [{i}] {preview}")
                
            except Exception as e:
                logger.error(f"✗ 查询失败: {e}")
                results[query] = {
                    'success': False,
                    'error': str(e)
                }
        
        return results
    
    def print_summary(self):
        """打印导入摘要"""
        print("\n" + "="*60)
        print("  导入摘要")
        print("="*60)
        print(f"\n总文件数: {self.stats['total_files']}")
        print(f"导入文档数: {self.stats['total_documents']}")
        print(f"失败文件数: {self.stats['failed_files']}")
        print(f"成功率: {self.stats['success_rate']*100:.2f}%")
        print("\n" + "="*60 + "\n")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="导入数据到RAG知识库")
    parser.add_argument(
        "--data-dir",
        type=str,
        default="./data/processed_knowledge",
        help="处理后的数据目录"
    )
    parser.add_argument(
        "--config",
        type=str,
        default="./configs/config.yaml",
        help="配置文件路径"
    )
    parser.add_argument(
        "--use-chunking",
        action="store_true",
        help="使用分块导入"
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=500,
        help="分块大小"
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="导入后验证"
    )
    
    args = parser.parse_args()
    
    print("\n" + "="*60)
    print("  RAG知识库导入工具")
    print("="*60 + "\n")
    
    # 创建导入器
    importer = RAGImporter(config_path=args.config)
    
    # 导入数据
    if args.use_chunking:
        stats = importer.import_with_chunking(
            data_dir=args.data_dir,
            chunk_size=args.chunk_size
        )
    else:
        stats = importer.import_from_directory(
            data_dir=args.data_dir
        )
    
    # 打印摘要
    importer.print_summary()
    
    # 验证
    if args.verify:
        logger.info("开始验证...")
        verify_results = importer.verify_import()
        
        success_count = sum(1 for r in verify_results.values() if r['success'])
        print(f"验证结果: {success_count}/{len(verify_results)} 个查询成功")


if __name__ == "__main__":
    main()
