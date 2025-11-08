"""
LLM工厂类
根据配置自动创建相应的LLM实例
"""

from typing import Dict, Any
from .base import BaseLLM
from .openai_llm import OpenAILLM
from .local_llm import LocalLLM


class LLMFactory:
    """LLM工厂类"""
    
    # 注册的LLM实现
    _registry = {
        'openai': OpenAILLM,
        'local': LocalLLM,
        # 可以轻松添加新的实现
        # 'anthropic': AnthropicLLM,
        # 'azure': AzureOpenAILLM,
    }
    
    @classmethod
    def create(cls, backend: str, config: Dict[str, Any]) -> BaseLLM:
        """
        创建LLM实例
        
        Args:
            backend: 后端类型 ('openai', 'local', 'anthropic'等)
            config: 配置字典
            
        Returns:
            BaseLLM实例
            
        Raises:
            ValueError: 如果backend类型不支持
        """
        if backend not in cls._registry:
            raise ValueError(
                f"Unsupported LLM backend: {backend}. "
                f"Available options: {list(cls._registry.keys())}"
            )
        
        llm_class = cls._registry[backend]
        return llm_class(config)
    
    @classmethod
    def register(cls, name: str, llm_class: type):
        """
        注册新的LLM实现
        
        Args:
            name: 后端名称
            llm_class: LLM类（必须继承自BaseLLM）
            
        Example:
            >>> LLMFactory.register('custom', CustomLLM)
        """
        if not issubclass(llm_class, BaseLLM):
            raise TypeError(f"{llm_class} must inherit from BaseLLM")
        
        cls._registry[name] = llm_class
    
    @classmethod
    def list_backends(cls) -> list:
        """
        列出所有可用的后端
        
        Returns:
            后端名称列表
        """
        return list(cls._registry.keys())


def create_llm_from_config(config: Dict[str, Any]) -> BaseLLM:
    """
    从配置字典创建LLM实例的便捷函数
    
    Args:
        config: 完整的配置字典（包含llm部分）
        
    Returns:
        BaseLLM实例
        
    Example:
        >>> config = yaml.safe_load(open('config.yaml'))
        >>> llm = create_llm_from_config(config)
    """
    llm_config = config.get('llm', {})
    backend = llm_config.get('backend', 'api')
    
    if backend == 'api':
        # API模式，使用provider指定的服务
        provider = llm_config.get('api', {}).get('provider', 'openai')
        backend_config = llm_config.get('api', {})
        return LLMFactory.create(provider, backend_config)
    
    elif backend == 'local':
        # 本地模式
        backend_config = llm_config.get('local', {})
        return LLMFactory.create('local', backend_config)
    
    else:
        raise ValueError(f"Unknown backend mode: {backend}")
