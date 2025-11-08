"""
本地GGUF模型实现
使用llama-cpp-python加载和运行GGUF格式模型
"""

from typing import List, Optional, Dict, Any
from llama_cpp import Llama

from .base import BaseLLM, Message, LLMResponse


class LocalLLM(BaseLLM):
    """本地GGUF模型实现"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        初始化本地模型
        
        Args:
            config: 配置字典，包含model_path, n_ctx等
        """
        super().__init__(config)
        
        model_path = config.get('model_path')
        if not model_path:
            raise ValueError("model_path is required for local LLM")
        
        # 初始化Llama模型
        self.model = Llama(
            model_path=model_path,
            n_ctx=config.get('n_ctx', 4096),
            n_threads=config.get('n_threads', 8),
            n_gpu_layers=config.get('n_gpu_layers', 35),
            verbose=False
        )
        
        self.temperature = config.get('temperature', 0.7)
        self.max_tokens = config.get('max_tokens', 2000)
        self.model_name = "TinyLlama-1.1B-Chat"
    
    def generate(
        self,
        messages: List[Message],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> LLMResponse:
        """
        使用本地模型生成回复
        
        Args:
            messages: 对话消息列表
            temperature: 温度参数（覆盖配置）
            max_tokens: 最大token数（覆盖配置）
            **kwargs: 其他参数
            
        Returns:
            LLMResponse对象
        """
        # 构建prompt（TinyLlama的格式）
        prompt = self._format_prompt(messages)
        
        try:
            # 调用模型
            response = self.model(
                prompt,
                temperature=temperature or self.temperature,
                max_tokens=max_tokens or self.max_tokens,
                stop=["</s>", "User:", "用户:"],  # 停止词
                **kwargs
            )
            
            # 提取内容
            content = response['choices'][0]['text'].strip()
            
            # 提取使用信息
            usage = {
                'prompt_tokens': response['usage']['prompt_tokens'],
                'completion_tokens': response['usage']['completion_tokens'],
                'total_tokens': response['usage']['total_tokens']
            }
            
            return LLMResponse(
                content=content,
                model=self.model_name,
                usage=usage,
                metadata={'finish_reason': response['choices'][0]['finish_reason']}
            )
            
        except Exception as e:
            raise RuntimeError(f"Local model generation failed: {str(e)}")
    
    def _format_prompt(self, messages: List[Message]) -> str:
        """
        将消息列表格式化为TinyLlama的prompt格式
        
        TinyLlama格式:
        <|system|>
        {system_message}</s>
        <|user|>
        {user_message}</s>
        <|assistant|>
        
        Args:
            messages: 消息列表
            
        Returns:
            格式化的prompt字符串
        """
        prompt_parts = []
        
        for msg in messages:
            if msg.role == 'system':
                prompt_parts.append(f"<|system|>\n{msg.content}</s>")
            elif msg.role == 'user':
                prompt_parts.append(f"<|user|>\n{msg.content}</s>")
            elif msg.role == 'assistant':
                prompt_parts.append(f"<|assistant|>\n{msg.content}</s>")
        
        # 添加assistant标记以引导模型生成
        prompt_parts.append("<|assistant|>")
        
        return "\n".join(prompt_parts)
    
    def count_tokens(self, text: str) -> int:
        """
        计算文本的token数量
        
        Args:
            text: 输入文本
            
        Returns:
            token数量（近似值）
        """
        # llama-cpp-python的tokenize方法
        tokens = self.model.tokenize(text.encode('utf-8'))
        return len(tokens)
    
    def __del__(self):
        """清理资源"""
        if hasattr(self, 'model'):
            del self.model
