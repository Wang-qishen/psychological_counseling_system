"""
数据集加载器

提供统一的数据集加载接口，支持：
- MentalChat16K
- Empathetic Dialogues
- Counsel Chat
- 自定义记忆测试集
- 自定义RAG测试集
"""

import json
import logging
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class BaseDatasetLoader(ABC):
    """数据集加载器基类"""
    
    def __init__(self, data_dir: str = "./data"):
        """
        初始化
        
        Args:
            data_dir: 数据目录路径
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    @abstractmethod
    def load(self) -> List[Dict]:
        """
        加载数据集
        
        Returns:
            数据样本列表
        """
        pass
    
    @abstractmethod
    def get_test_split(self, num_samples: Optional[int] = None) -> List[Dict]:
        """
        获取测试集
        
        Args:
            num_samples: 样本数量（None表示全部）
            
        Returns:
            测试样本列表
        """
        pass
    
    def save_to_json(self, data: List[Dict], filepath: str):
        """保存数据到JSON文件"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"Saved {len(data)} samples to {filepath}")
    
    def load_from_json(self, filepath: str) -> List[Dict]:
        """从JSON文件加载数据"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.info(f"Loaded {len(data)} samples from {filepath}")
        return data


class LocalDatasetLoader(BaseDatasetLoader):
    """本地数据集加载器"""
    
    def __init__(self, data_dir: str = "./data", dataset_name: str = "custom"):
        """
        初始化
        
        Args:
            data_dir: 数据目录
            dataset_name: 数据集名称
        """
        super().__init__(data_dir)
        self.dataset_name = dataset_name
        self.dataset_path = self.data_dir / f"{dataset_name}.json"
    
    def load(self) -> List[Dict]:
        """加载本地数据集"""
        if not self.dataset_path.exists():
            logger.error(f"Dataset not found: {self.dataset_path}")
            return []
        
        return self.load_from_json(str(self.dataset_path))
    
    def get_test_split(self, num_samples: Optional[int] = None) -> List[Dict]:
        """获取测试集"""
        data = self.load()
        
        if num_samples is None:
            return data
        
        return data[:num_samples] if num_samples <= len(data) else data


class HuggingFaceDatasetLoader(BaseDatasetLoader):
    """HuggingFace数据集加载器"""
    
    def __init__(
        self,
        dataset_name: str,
        data_dir: str = "./data",
        cache_dir: Optional[str] = None
    ):
        """
        初始化
        
        Args:
            dataset_name: HuggingFace数据集名称
            data_dir: 本地数据目录
            cache_dir: 缓存目录
        """
        super().__init__(data_dir)
        self.dataset_name = dataset_name
        self.cache_dir = cache_dir
        self._dataset = None
    
    def load(self) -> List[Dict]:
        """加载HuggingFace数据集"""
        try:
            from datasets import load_dataset
            
            logger.info(f"Loading dataset from HuggingFace: {self.dataset_name}")
            self._dataset = load_dataset(
                self.dataset_name,
                cache_dir=self.cache_dir
            )
            
            # 转换为标准格式
            data = []
            for split in self._dataset.keys():
                for item in self._dataset[split]:
                    data.append(dict(item))
            
            logger.info(f"Loaded {len(data)} samples from HuggingFace")
            return data
            
        except ImportError:
            logger.error("datasets library not installed. Install with: pip install datasets")
            return []
        except Exception as e:
            logger.error(f"Error loading dataset from HuggingFace: {e}")
            return []
    
    def get_test_split(self, num_samples: Optional[int] = None) -> List[Dict]:
        """获取测试集"""
        if self._dataset is None:
            self.load()
        
        if self._dataset is None:
            return []
        
        # 尝试获取test split
        if 'test' in self._dataset:
            test_data = [dict(item) for item in self._dataset['test']]
        elif 'validation' in self._dataset:
            test_data = [dict(item) for item in self._dataset['validation']]
        else:
            # 使用部分训练数据
            train_data = [dict(item) for item in self._dataset['train']]
            test_size = min(200, len(train_data) // 10)
            test_data = train_data[-test_size:]
        
        if num_samples is None:
            return test_data
        
        return test_data[:num_samples] if num_samples <= len(test_data) else test_data


def create_dataset_loader(
    dataset_name: str,
    source: str = "local",
    data_dir: str = "./data",
    **kwargs
) -> BaseDatasetLoader:
    """
    创建数据集加载器
    
    Args:
        dataset_name: 数据集名称
        source: 数据源（"local" 或 "huggingface"）
        data_dir: 数据目录
        **kwargs: 其他参数
        
    Returns:
        数据集加载器实例
    """
    if source == "local":
        return LocalDatasetLoader(data_dir, dataset_name)
    elif source == "huggingface":
        return HuggingFaceDatasetLoader(dataset_name, data_dir, **kwargs)
    else:
        raise ValueError(f"Unknown source: {source}")
