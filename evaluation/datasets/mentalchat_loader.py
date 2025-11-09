"""
MentalChat16K数据集加载器

MentalChat16K是Mentalic Net论文使用的标准评估数据集
包含16,113个心理健康相关的问答对和200个测试问题
支持7个临床维度的评估
"""

import logging
from typing import List, Dict, Optional, Tuple
from pathlib import Path
from .dataset_loader import HuggingFaceDatasetLoader

logger = logging.getLogger(__name__)


class MentalChatLoader(HuggingFaceDatasetLoader):
    """MentalChat16K数据集加载器"""
    
    # 数据集信息
    DATASET_NAME = "ShenLab/MentalChat16K"
    DATASET_SIZE = 16113
    TEST_SIZE = 200
    
    # 7个临床评估维度
    CLINICAL_DIMENSIONS = [
        "empathy",           # 共情能力
        "supportiveness",    # 支持性
        "guidance",          # 指导性
        "reflectiveness",    # 反思性
        "reassurance",       # 安慰性
        "professionalism",   # 专业性
        "information"        # 信息量
    ]
    
    def __init__(
        self,
        data_dir: str = "./data/mentalchat",
        cache_dir: Optional[str] = None,
        download: bool = True
    ):
        """
        初始化
        
        Args:
            data_dir: 本地数据目录
            cache_dir: 缓存目录
            download: 是否自动下载
        """
        super().__init__(
            dataset_name=self.DATASET_NAME,
            data_dir=data_dir,
            cache_dir=cache_dir
        )
        self.download = download
    
    def load(self) -> List[Dict]:
        """
        加载MentalChat16K数据集
        
        Returns:
            数据样本列表，每个样本包含：
                - question: 用户问题
                - answer: 参考答案
                - context: 对话上下文（可选）
        """
        logger.info("Loading MentalChat16K dataset...")
        
        data = super().load()
        
        if not data and self.download:
            logger.info("Dataset not found locally, will download on first use")
        
        # 标准化格式
        standardized_data = []
        for item in data:
            standardized_item = {
                "question": item.get("question", item.get("input", "")),
                "answer": item.get("answer", item.get("output", "")),
                "context": item.get("context", ""),
                "source": "MentalChat16K"
            }
            standardized_data.append(standardized_item)
        
        logger.info(f"Loaded {len(standardized_data)} samples from MentalChat16K")
        return standardized_data
    
    def get_test_split(self, num_samples: Optional[int] = 200) -> List[Dict]:
        """
        获取测试集（默认200个样本，与论文一致）
        
        Args:
            num_samples: 样本数量
            
        Returns:
            测试样本列表
        """
        data = self.load()
        
        if not data:
            logger.warning("No data loaded, returning empty list")
            return []
        
        # 使用最后200个样本作为测试集（与论文一致）
        test_size = num_samples if num_samples is not None else self.TEST_SIZE
        test_data = data[-test_size:] if len(data) >= test_size else data
        
        logger.info(f"Created test split with {len(test_data)} samples")
        return test_data
    
    def get_training_split(self) -> List[Dict]:
        """
        获取训练集
        
        Returns:
            训练样本列表
        """
        data = self.load()
        
        if not data:
            return []
        
        # 训练集是除去最后200个样本的数据
        train_data = data[:-self.TEST_SIZE] if len(data) >= self.TEST_SIZE else []
        
        logger.info(f"Created training split with {len(train_data)} samples")
        return train_data
    
    def get_samples_by_category(
        self,
        category: str,
        num_samples: Optional[int] = None
    ) -> List[Dict]:
        """
        按类别获取样本（如果数据集支持）
        
        Args:
            category: 类别名称
            num_samples: 样本数量
            
        Returns:
            样本列表
        """
        data = self.load()
        
        # 筛选特定类别的样本
        filtered_data = [
            item for item in data 
            if item.get("category") == category
        ]
        
        if num_samples is not None:
            filtered_data = filtered_data[:num_samples]
        
        logger.info(f"Found {len(filtered_data)} samples for category: {category}")
        return filtered_data
    
    def create_evaluation_set(
        self,
        num_samples: int = 200,
        include_dimensions: bool = True
    ) -> Dict[str, any]:
        """
        创建评估集
        
        Args:
            num_samples: 样本数量
            include_dimensions: 是否包含临床维度标注
            
        Returns:
            评估集字典，包含：
                - questions: 问题列表
                - answers: 参考答案列表
                - dimensions: 临床维度列表（如果include_dimensions=True）
        """
        test_data = self.get_test_split(num_samples)
        
        evaluation_set = {
            "questions": [item["question"] for item in test_data],
            "reference_answers": [item["answer"] for item in test_data],
            "contexts": [item.get("context", "") for item in test_data]
        }
        
        if include_dimensions:
            evaluation_set["clinical_dimensions"] = self.CLINICAL_DIMENSIONS
        
        return evaluation_set
    
    def get_dataset_info(self) -> Dict[str, any]:
        """
        获取数据集信息
        
        Returns:
            数据集信息字典
        """
        return {
            "name": "MentalChat16K",
            "source": self.DATASET_NAME,
            "total_samples": self.DATASET_SIZE,
            "test_samples": self.TEST_SIZE,
            "clinical_dimensions": self.CLINICAL_DIMENSIONS,
            "description": "心理健康对话数据集，包含16,113个问答对和200个测试问题"
        }


def load_mentalchat(
    data_dir: str = "./data/mentalchat",
    num_test_samples: int = 200
) -> Tuple[List[Dict], List[Dict]]:
    """
    便捷函数：加载MentalChat数据集
    
    Args:
        data_dir: 数据目录
        num_test_samples: 测试样本数量
        
    Returns:
        (训练集, 测试集)元组
    """
    loader = MentalChatLoader(data_dir=data_dir)
    train_data = loader.get_training_split()
    test_data = loader.get_test_split(num_test_samples)
    
    return train_data, test_data


def create_mentalchat_evaluation_set(
    data_dir: str = "./data/mentalchat",
    num_samples: int = 200
) -> Dict[str, any]:
    """
    便捷函数：创建MentalChat评估集
    
    Args:
        data_dir: 数据目录
        num_samples: 样本数量
        
    Returns:
        评估集字典
    """
    loader = MentalChatLoader(data_dir=data_dir)
    return loader.create_evaluation_set(num_samples)
