"""
LLM抽象基类
定义统一的LLM接口，支持多种后端实现
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any
from dataclasses import dataclass


@dataclass
class Message:
    """对话消息"""
    role: str  # 'system', 'user', 'assistant'
    content: str


@dataclass
class LLMResponse:
    """LLM响应"""
    content: str
    model: str
    usage: Optional[Dict[str, int]] = None  # Token使用情况
    metadata: Optional[Dict[str, Any]] = None


class BaseLLM(ABC):
    """LLM基类，定义统一接口"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        初始化LLM
        
        Args:
            config: LLM配置字典
        """
        self.config = config
        self.model_name = config.get('model', 'unknown')
        
    @abstractmethod
    def generate(
        self,
        messages: List[Message],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> LLMResponse:
        """
        生成回复
        
        Args:
            messages: 对话消息列表
            temperature: 温度参数
            max_tokens: 最大生成token数
            **kwargs: 其他参数
            
        Returns:
            LLMResponse对象
        """
        pass
    
    @abstractmethod
    def count_tokens(self, text: str) -> int:
        """
        计算文本的token数量
        
        Args:
            text: 输入文本
            
        Returns:
            token数量
        """
        pass
    
    def format_messages(self, messages: List[Message]) -> List[Dict[str, str]]:
        """
        将Message对象转换为字典格式
        
        Args:
            messages: Message对象列表
            
        Returns:
            字典格式的消息列表
        """
        return [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(model={self.model_name})"
