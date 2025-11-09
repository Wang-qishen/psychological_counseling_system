"""
数据集管理模块

提供各种评估数据集的加载和生成功能：
- MentalChatLoader: MentalChat16K数据集加载器
- MemoryTestGenerator: 记忆测试数据生成器
- DatasetLoader: 通用数据集加载器
"""

from .dataset_loader import (
    BaseDatasetLoader,
    LocalDatasetLoader,
    HuggingFaceDatasetLoader,
    create_dataset_loader
)
from .mentalchat_loader import (
    MentalChatLoader,
    load_mentalchat,
    create_mentalchat_evaluation_set
)
from .memory_test_generator import (
    MemoryTestGenerator,
    generate_memory_tests
)

__all__ = [
    "BaseDatasetLoader",
    "LocalDatasetLoader",
    "HuggingFaceDatasetLoader",
    "create_dataset_loader",
    "MentalChatLoader",
    "load_mentalchat",
    "create_mentalchat_evaluation_set",
    "MemoryTestGenerator",
    "generate_memory_tests"
]
