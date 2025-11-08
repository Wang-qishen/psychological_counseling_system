"""
记忆存储后端
支持多种存储方式（JSON, SQLite等）
"""

import os
import json
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any

from .models import UserMemory, UserProfile


class BaseMemoryStorage(ABC):
    """记忆存储基类"""
    
    @abstractmethod
    def save_user_memory(self, user_memory: UserMemory) -> None:
        """保存用户记忆"""
        pass
    
    @abstractmethod
    def load_user_memory(self, user_id: str) -> Optional[UserMemory]:
        """加载用户记忆"""
        pass
    
    @abstractmethod
    def user_exists(self, user_id: str) -> bool:
        """检查用户是否存在"""
        pass
    
    @abstractmethod
    def delete_user_memory(self, user_id: str) -> None:
        """删除用户记忆"""
        pass


class JSONMemoryStorage(BaseMemoryStorage):
    """基于JSON文件的记忆存储"""
    
    def __init__(self, storage_path: str):
        """
        初始化JSON存储
        
        Args:
            storage_path: 存储目录路径
        """
        self.storage_path = storage_path
        os.makedirs(storage_path, exist_ok=True)
    
    def _get_user_file(self, user_id: str) -> str:
        """获取用户文件路径"""
        return os.path.join(self.storage_path, f"{user_id}.json")
    
    def save_user_memory(self, user_memory: UserMemory) -> None:
        """
        保存用户记忆到JSON文件
        
        Args:
            user_memory: 用户记忆对象
        """
        file_path = self._get_user_file(user_memory.user_id)
        
        # 转换为字典并保存
        data = user_memory.to_dict()
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load_user_memory(self, user_id: str) -> Optional[UserMemory]:
        """
        从JSON文件加载用户记忆
        
        Args:
            user_id: 用户ID
            
        Returns:
            用户记忆对象，如果不存在则返回None
        """
        file_path = self._get_user_file(user_id)
        
        if not os.path.exists(file_path):
            return None
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            return UserMemory.from_dict(data)
        
        except Exception as e:
            print(f"Error loading user memory for {user_id}: {e}")
            return None
    
    def user_exists(self, user_id: str) -> bool:
        """
        检查用户是否存在
        
        Args:
            user_id: 用户ID
            
        Returns:
            是否存在
        """
        file_path = self._get_user_file(user_id)
        return os.path.exists(file_path)
    
    def delete_user_memory(self, user_id: str) -> None:
        """
        删除用户记忆
        
        Args:
            user_id: 用户ID
        """
        file_path = self._get_user_file(user_id)
        
        if os.path.exists(file_path):
            os.remove(file_path)
    
    def list_users(self) -> list:
        """
        列出所有用户ID
        
        Returns:
            用户ID列表
        """
        files = os.listdir(self.storage_path)
        return [f.replace('.json', '') for f in files if f.endswith('.json')]


def create_memory_storage(storage_type: str, config: Dict[str, Any]) -> BaseMemoryStorage:
    """
    创建记忆存储后端
    
    Args:
        storage_type: 存储类型 ('json', 'sqlite'等)
        config: 配置字典
        
    Returns:
        存储后端实例
    """
    if storage_type == 'json':
        storage_path = config.get('path', './data/memory_db')
        return JSONMemoryStorage(storage_path)
    else:
        raise ValueError(f"Unsupported storage type: {storage_type}")
