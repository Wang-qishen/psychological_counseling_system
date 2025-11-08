"""
对话管理器
整合LLM、RAG和记忆系统，提供完整的对话功能
"""

from typing import Optional, Dict, Any, List
from llm.base import BaseLLM, Message
from knowledge.rag_manager import RAGManager
from memory.manager import MemoryManager


class DialogueManager:
    """对话管理器"""
    
    def __init__(
        self,
        llm: BaseLLM,
        rag_manager: RAGManager,
        memory_manager: MemoryManager,
        config: Optional[Dict[str, Any]] = None
    ):
        """
        初始化对话管理器
        
        Args:
            llm: LLM实例
            rag_manager: RAG管理器
            memory_manager: 记忆管理器
            config: 配置参数
        """
        self.llm = llm
        self.rag_manager = rag_manager
        self.memory_manager = memory_manager
        self.config = config or {}
        
        # 系统提示词
        self.system_prompt = self.config.get('system_prompt', self._default_system_prompt())
        
        # 功能开关
        self.enable_rag = self.config.get('enable_rag', True)
        self.enable_memory = self.config.get('enable_memory', True)
        
        # 上下文管理
        self.max_context_length = self.config.get('max_context_length', 8000)
    
    def _default_system_prompt(self) -> str:
        """默认系统提示词"""
        return """你是一位专业、有同理心的心理咨询师。你的任务是：
1. 倾听用户的问题和感受
2. 提供专业的心理学见解和建议
3. 运用认知行为疗法(CBT)等技术帮助用户
4. 保持温暖、非评判的态度
5. 记住并关联用户的历史信息"""
    
    def chat(
        self,
        user_id: str,
        session_id: str,
        user_message: str,
        emotion: Optional[Dict[str, float]] = None
    ) -> str:
        """
        处理单轮对话
        
        Args:
            user_id: 用户ID
            session_id: 会话ID
            user_message: 用户消息
            emotion: 情绪状态（可选）
            
        Returns:
            助手回复
        """
        # 1. 构建上下文
        context = self._build_context(user_id, session_id, user_message)
        
        # 2. 构建消息列表
        messages = self._build_messages(context, user_message)
        
        # 3. 调用LLM生成回复
        response = self.llm.generate(messages)
        assistant_message = response.content
        
        # 4. 保存到记忆
        if self.enable_memory:
            self.memory_manager.add_turn(
                user_id=user_id,
                session_id=session_id,
                user_message=user_message,
                assistant_message=assistant_message,
                emotion=emotion
            )
        
        return assistant_message
    
    def _build_context(
        self,
        user_id: str,
        session_id: str,
        user_message: str
    ) -> Dict[str, Any]:
        """
        构建对话上下文
        
        Args:
            user_id: 用户ID
            session_id: 会话ID
            user_message: 用户消息
            
        Returns:
            上下文字典
        """
        context = {
            'rag_context': None,
            'memory_context': None,
            'session_history': []
        }
        
        # RAG检索
        if self.enable_rag:
            rag_result = self.rag_manager.retrieve(
                query=user_message,
                user_id=user_id
            )
            context['rag_context'] = rag_result.combined_context
        
        # 记忆检索
        if self.enable_memory:
            memory_context = self.memory_manager.retrieve_relevant_memory(
                user_id=user_id,
                current_context=user_message
            )
            context['memory_context'] = memory_context
            
            # 获取当前会话历史
            user_memory = self.memory_manager.get_user_memory(user_id)
            if user_memory:
                session = next(
                    (s for s in user_memory.sessions if s.session_id == session_id),
                    None
                )
                if session:
                    context['session_history'] = session.turns[-10:]  # 最近10轮
        
        return context
    
    def _build_messages(
        self,
        context: Dict[str, Any],
        user_message: str
    ) -> List[Message]:
        """
        构建LLM消息列表
        
        Args:
            context: 上下文字典
            user_message: 用户消息
            
        Returns:
            消息列表
        """
        messages = []
        
        # 1. 系统消息
        system_content_parts = [self.system_prompt]
        
        # 添加用户档案信息
        if context.get('memory_context'):
            memory_ctx = context['memory_context']
            profile = memory_ctx.get('profile', {})
            
            if profile:
                profile_text = self._format_profile(profile)
                system_content_parts.append(f"\n\n### 用户档案\n{profile_text}")
            
            # 添加历史摘要
            recent_sessions = memory_ctx.get('recent_sessions', [])
            if recent_sessions:
                summary_text = self._format_session_summaries(recent_sessions)
                system_content_parts.append(f"\n\n### 历史会话摘要\n{summary_text}")
            
            # 添加情绪趋势
            emotion_trend = memory_ctx.get('emotion_trend', {})
            if emotion_trend:
                trend_text = self._format_emotion_trend(emotion_trend)
                system_content_parts.append(f"\n\n### 情绪趋势\n{trend_text}")
        
        # 添加RAG检索的知识
        if context.get('rag_context'):
            system_content_parts.append(f"\n\n### 相关知识\n{context['rag_context']}")
        
        messages.append(Message(
            role="system",
            content="\n".join(system_content_parts)
        ))
        
        # 2. 对话历史
        session_history = context.get('session_history', [])
        for turn in session_history:
            messages.append(Message(role="user", content=turn.user_message))
            messages.append(Message(role="assistant", content=turn.assistant_message))
        
        # 3. 当前用户消息
        messages.append(Message(role="user", content=user_message))
        
        # 4. 检查长度并截断（如果需要）
        messages = self._truncate_messages(messages)
        
        return messages
    
    def _format_profile(self, profile: Dict[str, Any]) -> str:
        """格式化用户档案"""
        parts = []
        
        if profile.get('age'):
            parts.append(f"年龄: {profile['age']}")
        if profile.get('gender'):
            parts.append(f"性别: {profile['gender']}")
        if profile.get('occupation'):
            parts.append(f"职业: {profile['occupation']}")
        if profile.get('main_issues'):
            parts.append(f"主要问题: {', '.join(profile['main_issues'])}")
        
        return "\n".join(parts) if parts else "暂无档案信息"
    
    def _format_session_summaries(self, sessions: List[Dict[str, Any]]) -> str:
        """格式化会话摘要"""
        summaries = []
        for session in sessions:
            if session.get('summary'):
                summaries.append(f"- {session['summary']}")
        
        return "\n".join(summaries) if summaries else "暂无历史摘要"
    
    def _format_emotion_trend(self, trend: Dict[str, Any]) -> str:
        """格式化情绪趋势"""
        avg_emotions = trend.get('average_emotions', {})
        if not avg_emotions:
            return "暂无情绪数据"
        
        emotion_strs = [
            f"{emotion}: {value:.2f}"
            for emotion, value in avg_emotions.items()
        ]
        
        return "平均情绪状态: " + ", ".join(emotion_strs)
    
    def _truncate_messages(self, messages: List[Message]) -> List[Message]:
        """
        截断消息以适应上下文长度限制
        
        Args:
            messages: 消息列表
            
        Returns:
            截断后的消息列表
        """
        # 简单实现：保留系统消息和最后几轮对话
        # 可以使用更智能的策略
        
        total_length = sum(
            self.llm.count_tokens(msg.content)
            for msg in messages
        )
        
        if total_length <= self.max_context_length:
            return messages
        
        # 保留系统消息和最后的用户消息
        system_msg = messages[0]
        user_msg = messages[-1]
        
        # 从倒数第二条开始向前取
        truncated = [system_msg]
        current_length = self.llm.count_tokens(system_msg.content) + \
                        self.llm.count_tokens(user_msg.content)
        
        for msg in reversed(messages[1:-1]):
            msg_length = self.llm.count_tokens(msg.content)
            if current_length + msg_length <= self.max_context_length:
                truncated.insert(1, msg)
                current_length += msg_length
            else:
                break
        
        truncated.append(user_msg)
        
        return truncated
    
    def start_session(self, user_id: str) -> str:
        """
        开始新会话
        
        Args:
            user_id: 用户ID
            
        Returns:
            会话ID
        """
        return self.memory_manager.start_session(user_id)
    
    def end_session(self, user_id: str, session_id: str) -> None:
        """
        结束会话
        
        Args:
            user_id: 用户ID
            session_id: 会话ID
        """
        self.memory_manager.end_session(user_id, session_id)


def create_dialogue_manager_from_config(config: Dict[str, Any]) -> DialogueManager:
    """
    从配置创建对话管理器
    
    Args:
        config: 配置字典
        
    Returns:
        DialogueManager实例
    """
    from llm import create_llm_from_config
    from knowledge import create_rag_manager_from_config
    from memory import create_memory_manager_from_config
    
    # 创建LLM
    main_llm = create_llm_from_config(config)
    
    # 创建摘要用的LLM（如果配置了使用本地模型）
    summarizer = None
    if config['memory']['update']['auto_summarize']:
        summarize_backend = config['memory']['update'].get('summarize_backend', 'api')
        if summarize_backend == 'local' and config['llm']['backend'] == 'api':
            # 使用本地模型做摘要
            from llm import LocalLLM
            summarizer = LocalLLM(config['llm']['local'])
        else:
            # 使用主LLM
            summarizer = main_llm
    
    # 创建RAG管理器
    rag_manager = create_rag_manager_from_config(config)
    
    # 创建记忆管理器
    memory_manager = create_memory_manager_from_config(config, summarizer)
    
    # 创建对话管理器
    dialogue_config = {
        'system_prompt': config['dialogue']['system_prompt'],
        'max_context_length': config['dialogue']['max_context_length'],
        'enable_rag': config['dialogue']['generation']['enable_rag'],
        'enable_memory': config['dialogue']['generation']['enable_memory']
    }
    
    return DialogueManager(
        llm=main_llm,
        rag_manager=rag_manager,
        memory_manager=memory_manager,
        config=dialogue_config
    )
