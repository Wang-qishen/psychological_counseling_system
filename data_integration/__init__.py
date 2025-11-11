"""
数据集集成模块

提供中文心理咨询数据集的下载、处理和导入功能
"""

from .dataset_downloader import DatasetDownloader
from .process_datasets import DatasetProcessor

__version__ = '1.0.0'
__all__ = ['DatasetDownloader', 'DatasetProcessor']
