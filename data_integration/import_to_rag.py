"""
RAG知识库导入工具 - 将处理后的数据导入到ChromaDB
"""

import sys
import logging
from pathlib import Path
from typing import List, Dict
import yaml

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dialogue.manager import create_dialogue_manager_from_config

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
        
        # 使用原项目的方式创建对话管理器
        self.dialogue_manager = self._create_dialogue_manager()
        self.rag_manager = self.dialogue_manager.rag_manager
        
        self.stats = {
            'total_files': 0,
            'total_documents': 0,
            'failed_files': 0,
            'success_rate': 0.0
        }
    
    def _create_dialogue_manager(self):
        """
        创建对话管理器（使用原项目的方式）
        
        Returns:
            对话管理器实例
        """
        logger.info("初始化对话管理器...")
        
        # 使用原项目的工厂函数
        dialogue_manager = create_dialogue_manager_from_config(self.config)
        
        logger.info("✓ 对话管理器初始化完成")
        return dialogue_manager
    
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
        for idx, txt_file in enumerate(txt_files, 1):
            try:
                if idx % 100 == 0:  # 每100个文件打印一次进度
                    logger.info(f"进度: [{idx}/{len(txt_files)}]")
                
                count = self._import_file(txt_file)
                self.stats['total_documents'] += count
                
                if idx % 100 == 0:
                    logger.info(f"已导入 {self.stats['total_documents']} 条文档")
                
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
        from knowledge.base import Document
        
        docs_to_add = []
        
        for idx, doc_content in enumerate(documents):
            if len(doc_content) < 10:  # 过滤太短的文档
                continue
            
            # 创建Document对象
            doc = Document(
                content=doc_content,
                metadata={
                    'source_file': file_path.name,
                    'source_dir': file_path.parent.name,
                    'document_index': idx,
                    'type': 'knowledge_base'
                }
            )
            docs_to_add.append(doc)
        
        # 添加到知识库（使用原项目的方法）
        if docs_to_add:
            self.rag_manager.add_psychological_knowledge(docs_to_add)
        
        return len(docs_to_add)
    
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
                "失眠怎么办"
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
        "--verify",
        action="store_true",
        help="导入后验证"
    )
    
    args = parser.parse_args()
    
    print("\n" + "="*60)
    print("  RAG知识库导入工具")
    print("="*60 + "\n")
    
    # 创建导入器
    try:
        importer = RAGImporter(config_path=args.config)
    except Exception as e:
        logger.error(f"初始化失败: {e}")
        logger.error("请确保配置文件存在且格式正确")
        return
    
    # 导入数据
    logger.info("开始导入数据...\n")
    stats = importer.import_from_directory(data_dir=args.data_dir)
    
    # 打印摘要
    importer.print_summary()
    
    # 验证
    if args.verify and stats['total_documents'] > 0:
        logger.info("开始验证...")
        verify_results = importer.verify_import()
        
        success_count = sum(1 for r in verify_results.values() if r['success'])
        print(f"验证结果: {success_count}/{len(verify_results)} 个查询成功\n")


if __name__ == "__main__":
    main()