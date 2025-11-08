"""
OpenAI API实现
支持GPT-4, GPT-3.5等模型
"""

import os
from typing import List, Optional, Dict, Any
from openai import OpenAI
import tiktoken

from .base import BaseLLM, Message, LLMResponse


class OpenAILLM(BaseLLM):
    """OpenAI API实现"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        初始化OpenAI客户端
        
        Args:
            config: 配置字典，包含api_key, model等
        """
        super().__init__(config)
        
        # 获取API密钥
        api_key = os.environ.get(config.get('api_key_env', 'OPENAI_API_KEY'))
        if not api_key:
            raise ValueError(
                f"API key not found in environment variable: "
                f"{config.get('api_key_env', 'OPENAI_API_KEY')}"
            )
        
        # 初始化客户端
        self.client = OpenAI(api_key=api_key)
        self.model = config.get('model', 'gpt-4o-mini')
        self.temperature = config.get('temperature', 0.7)
        self.max_tokens = config.get('max_tokens', 2000)
        
        # 初始化tokenizer
        try:
            self.encoding = tiktoken.encoding_for_model(self.model)
        except KeyError:
            # 如果模型不支持，使用默认编码
            self.encoding = tiktoken.get_encoding("cl100k_base")
    
    def generate(
        self,
        messages: List[Message],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> LLMResponse:
        """
        调用OpenAI API生成回复
        
        Args:
            messages: 对话消息列表
            temperature: 温度参数（覆盖配置）
            max_tokens: 最大token数（覆盖配置）
            **kwargs: 其他OpenAI API参数
            
        Returns:
            LLMResponse对象
        """
        # 转换消息格式
        formatted_messages = self.format_messages(messages)
        
        # 调用API
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=formatted_messages,
                temperature=temperature or self.temperature,
                max_tokens=max_tokens or self.max_tokens,
                **kwargs
            )
            
            # 提取响应内容
            content = response.choices[0].message.content
            
            # 提取使用信息
            usage = None
            if hasattr(response, 'usage') and response.usage:
                usage = {
                    'prompt_tokens': response.usage.prompt_tokens,
                    'completion_tokens': response.usage.completion_tokens,
                    'total_tokens': response.usage.total_tokens
                }
            
            return LLMResponse(
                content=content,
                model=self.model,
                usage=usage,
                metadata={'finish_reason': response.choices[0].finish_reason}
            )
            
        except Exception as e:
            raise RuntimeError(f"OpenAI API call failed: {str(e)}")
    
    def count_tokens(self, text: str) -> int:
        """
        计算文本的token数量
        
        Args:
            text: 输入文本
            
        Returns:
            token数量
        """
        return len(self.encoding.encode(text))
