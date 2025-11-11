"""
数据集处理器 - 将下载的数据集转换为RAG系统可用格式
"""

import json
import logging
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ProcessedDocument:
    """处理后的文档"""
    content: str
    metadata: Dict
    source: str


class DatasetProcessor:
    """数据集处理器"""
    
    def __init__(
        self,
        input_dir: str = "./data/downloaded_datasets",
        output_dir: str = "./data/processed_knowledge"
    ):
        """
        初始化处理器
        
        Args:
            input_dir: 下载数据集的目录
            output_dir: 处理后数据的输出目录
        """
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 统计信息
        self.stats = {
            'smilechat': {'total': 0, 'processed': 0},
            'psyqa': {'total': 0, 'processed': 0},
            'cpyscoun': {'total': 0, 'processed': 0}
        }
    
    def process_smilechat(self) -> List[ProcessedDocument]:
        """
        处理SmileChat数据集 - 支持任意命名的JSON文件
        
        Returns:
            处理后的文档列表
        """
        logger.info("开始处理SmileChat数据集...")
        
        smilechat_dir = self.input_dir / "smilechat"
        if not smilechat_dir.exists():
            logger.warning(f"SmileChat数据集不存在: {smilechat_dir}")
            return []
        
        documents = []
        
        # 查找所有JSON文件（支持任意命名）
        json_files = list(smilechat_dir.glob("*.json"))
        
        if not json_files:
            logger.warning(f"SmileChat目录下未找到任何JSON文件")
            return []
        
        logger.info(f"找到 {len(json_files)} 个JSON文件")
        
        # 处理所有JSON文件
        for json_file in json_files:
            logger.info(f"处理文件: {json_file.name}")
            
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # 处理数据（可能是列表或字典）
                if isinstance(data, list):
                    items = data
                elif isinstance(data, dict):
                    # 如果是字典，尝试提取data字段
                    if 'data' in data:
                        items = data['data']
                    else:
                        items = [data]
                else:
                    logger.warning(f"未知的数据格式: {json_file.name}")
                    continue
                
                # 处理每个item
                for idx, item in enumerate(items):
                    self.stats['smilechat']['total'] += 1
                    
                    doc = self._process_smilechat_item(item, json_file.stem, idx)
                    if doc:
                        documents.append(doc)
                        self.stats['smilechat']['processed'] += 1
                
                logger.info(f"✓ {json_file.name} 处理完成: {len(items)} 条")
                
            except Exception as e:
                logger.error(f"处理{json_file.name}时出错: {e}")
        
        logger.info(f"SmileChat总计: {self.stats['smilechat']['processed']}/{self.stats['smilechat']['total']} 条")
        return documents
    
    def _process_smilechat_item(
        self, 
        item: Dict, 
        file_name: str, 
        idx: int
    ) -> Optional[ProcessedDocument]:
        """
        处理SmileChat单条数据
        
        Args:
            item: 数据项
            file_name: 文件名
            idx: 索引
            
        Returns:
            处理后的文档
        """
        try:
            # SmileChat可能的格式1: {question: str, answer: List[str]}
            # SmileChat可能的格式2: {instruction: str, output: str}
            # SmileChat可能的格式3: 其他格式
            
            content_parts = []
            
            # 尝试提取问题
            question = None
            if 'question' in item:
                question = item['question']
            elif 'instruction' in item:
                question = item['instruction']
            elif 'input' in item:
                question = item['input']
            elif 'query' in item:
                question = item['query']
            
            if question:
                content_parts.append(f"问题: {question.strip()}")
            
            # 尝试提取回答
            answers = []
            if 'answer' in item:
                answer_data = item['answer']
                if isinstance(answer_data, list):
                    answers = answer_data
                elif isinstance(answer_data, str):
                    answers = [answer_data]
            elif 'output' in item:
                answers = [item['output']]
            elif 'response' in item:
                answers = [item['response']]
            
            # 构建完整对话
            if answers:
                for i, ans in enumerate(answers, 1):
                    if ans and ans.strip():
                        if len(answers) > 1:
                            content_parts.append(f"回复{i}: {ans.strip()}")
                        else:
                            content_parts.append(f"回复: {ans.strip()}")
            
            if not content_parts:
                # 如果上述都没提取到，尝试将整个item转为文本
                content_str = json.dumps(item, ensure_ascii=False)
                if len(content_str) > 50:  # 至少有一些内容
                    content_parts.append(content_str)
            
            if not content_parts:
                return None
            
            content = "\n\n".join(content_parts)
            
            # 元数据
            metadata = {
                'source': 'SmileChat',
                'file': file_name,
                'index': idx,
                'dialogue_length': len(answers),
                'has_multi_turn': len(answers) > 1,
                'type': 'dialogue'
            }
            
            return ProcessedDocument(
                content=content,
                metadata=metadata,
                source='smilechat'
            )
            
        except Exception as e:
            logger.warning(f"处理SmileChat项目失败: {e}")
            return None
    
    def process_psyqa(self) -> List[ProcessedDocument]:
        """
        处理PsyQA数据集
        
        Returns:
            处理后的文档列表
        """
        logger.info("检查PsyQA数据集...")
        
        psyqa_dir = self.input_dir / "psyqa"
        if not psyqa_dir.exists():
            logger.warning("PsyQA数据集未下载")
            return []
        
        # 查找JSON文件
        json_files = list(psyqa_dir.glob("*.json"))
        if not json_files:
            logger.warning("PsyQA目录下未找到JSON文件")
            return []
        
        documents = []
        
        for file_path in json_files:
            logger.info(f"处理PsyQA文件: {file_path.name}")
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                if isinstance(data, list):
                    items = data
                elif isinstance(data, dict) and 'data' in data:
                    items = data['data']
                else:
                    items = [data]
                
                for idx, item in enumerate(items):
                    self.stats['psyqa']['total'] += 1
                    
                    doc = self._process_psyqa_item(item, idx)
                    if doc:
                        documents.append(doc)
                        self.stats['psyqa']['processed'] += 1
                
                logger.info(f"✓ {file_path.name} 处理完成: {len(documents)} 条")
                
            except Exception as e:
                logger.error(f"处理PsyQA文件{file_path.name}时出错: {e}")
        
        logger.info(f"PsyQA总计: {self.stats['psyqa']['processed']}/{self.stats['psyqa']['total']} 条")
        return documents
    
    def _process_psyqa_item(
        self, 
        item: Dict, 
        idx: int
    ) -> Optional[ProcessedDocument]:
        """
        处理PsyQA单条数据
        
        Args:
            item: 数据项
            idx: 索引
            
        Returns:
            处理后的文档
        """
        try:
            question = item.get('question', '').strip()
            description = item.get('description', '').strip()
            answer = item.get('answer', '').strip()
            
            if not question or not answer:
                return None
            
            content_parts = [f"问题: {question}"]
            
            if description:
                content_parts.append(f"问题描述: {description}")
            
            content_parts.append(f"专业回答: {answer}")
            
            content = "\n\n".join(content_parts)
            
            metadata = {
                'source': 'PsyQA',
                'index': idx,
                'has_description': bool(description),
                'strategy': item.get('strategy', []),
                'type': 'qa_with_strategy'
            }
            
            if 'keywords' in item:
                metadata['keywords'] = item['keywords']
            
            return ProcessedDocument(
                content=content,
                metadata=metadata,
                source='psyqa'
            )
            
        except Exception as e:
            logger.warning(f"处理PsyQA项目失败: {e}")
            return None
    
    def clean_text(self, text: str) -> str:
        """清理文本"""
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9，。！？、；：""''（）《》\s]', '', text)
        return text.strip()
    
    def save_to_txt_files(
        self, 
        documents: List[ProcessedDocument],
        chunk_size: int = 100
    ) -> List[str]:
        """
        保存为TXT文件(用于RAG系统)
        
        Args:
            documents: 文档列表
            chunk_size: 每个文件的文档数量
            
        Returns:
            保存的文件路径列表
        """
        logger.info("保存为TXT格式...")
        
        saved_files = []
        
        # 按来源分组
        by_source = {}
        for doc in documents:
            if doc.source not in by_source:
                by_source[doc.source] = []
            by_source[doc.source].append(doc)
        
        # 为每个来源创建文件
        for source, docs in by_source.items():
            source_dir = self.output_dir / source
            source_dir.mkdir(exist_ok=True)
            
            # 分块保存
            for i in range(0, len(docs), chunk_size):
                chunk = docs[i:i+chunk_size]
                chunk_num = i // chunk_size + 1
                
                file_path = source_dir / f"{source}_part{chunk_num:03d}.txt"
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    for doc in chunk:
                        f.write(doc.content)
                        f.write("\n\n" + "="*60 + "\n\n")
                
                saved_files.append(str(file_path))
                logger.info(f"✓ 保存: {file_path.name} ({len(chunk)} 条)")
        
        return saved_files
    
    def save_to_json(
        self, 
        documents: List[ProcessedDocument]
    ) -> str:
        """
        保存为JSON格式(用于备份和分析)
        
        Args:
            documents: 文档列表
            
        Returns:
            JSON文件路径
        """
        logger.info("保存为JSON格式...")
        
        json_path = self.output_dir / "processed_all.json"
        
        data = []
        for doc in documents:
            data.append({
                'content': doc.content,
                'metadata': doc.metadata,
                'source': doc.source
            })
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"✓ JSON保存完成: {json_path}")
        return str(json_path)
    
    def generate_summary(self) -> Dict:
        """生成处理摘要"""
        summary = {
            'total_processed': sum(s['processed'] for s in self.stats.values()),
            'total_attempted': sum(s['total'] for s in self.stats.values()),
            'by_source': self.stats,
            'success_rate': 0.0
        }
        
        if summary['total_attempted'] > 0:
            summary['success_rate'] = summary['total_processed'] / summary['total_attempted']
        
        return summary
    
    def save_summary(self, summary: Dict) -> str:
        """保存处理摘要"""
        summary_path = self.output_dir / "processing_summary.json"
        
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        
        # 同时生成可读版本
        readable_path = self.output_dir / "processing_summary.txt"
        with open(readable_path, 'w', encoding='utf-8') as f:
            f.write("="*60 + "\n")
            f.write("  数据集处理摘要\n")
            f.write("="*60 + "\n\n")
            
            f.write(f"总计处理: {summary['total_processed']} / {summary['total_attempted']} 条\n")
            f.write(f"成功率: {summary['success_rate']*100:.2f}%\n\n")
            
            f.write("各数据集统计:\n")
            for source, stats in summary['by_source'].items():
                if stats['total'] > 0:
                    f.write(f"  - {source}: {stats['processed']} / {stats['total']} 条\n")
            
            f.write("\n" + "="*60 + "\n")
        
        logger.info(f"✓ 摘要保存: {summary_path}")
        return str(summary_path)


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="处理下载的数据集")
    parser.add_argument(
        "--input-dir",
        type=str,
        default="./data/downloaded_datasets",
        help="下载数据集的目录"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="./data/processed_knowledge",
        help="处理后数据的输出目录"
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=100,
        help="每个TXT文件的文档数量"
    )
    
    args = parser.parse_args()
    
    print("\n" + "="*60)
    print("  数据集处理工具")
    print("="*60 + "\n")
    
    processor = DatasetProcessor(
        input_dir=args.input_dir,
        output_dir=args.output_dir
    )
    
    all_documents = []
    
    # 处理SmileChat
    smilechat_docs = processor.process_smilechat()
    all_documents.extend(smilechat_docs)
    
    # 处理PsyQA
    psyqa_docs = processor.process_psyqa()
    all_documents.extend(psyqa_docs)
    
    if not all_documents:
        logger.warning("没有处理任何文档!")
        return
    
    logger.info(f"\n总计处理 {len(all_documents)} 条文档\n")
    
    # 保存为TXT文件
    txt_files = processor.save_to_txt_files(all_documents, chunk_size=args.chunk_size)
    
    # 保存为JSON
    json_file = processor.save_to_json(all_documents)
    
    # 生成摘要
    summary = processor.generate_summary()
    summary_file = processor.save_summary(summary)
    
    print("\n" + "="*60)
    print("  ✓ 处理完成!")
    print("="*60)
    print(f"\n处理文档数: {len(all_documents)}")
    print(f"TXT文件数: {len(txt_files)}")
    print(f"输出目录: {args.output_dir}")
    print(f"摘要文件: {summary_file}\n")


if __name__ == "__main__":
    main()