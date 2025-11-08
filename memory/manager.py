"""
记忆管理器
实现三层记忆架构的核心逻辑
"""

import uuid
from typing import Optional, Dict, Any, List
from datetime import datetime
import math

from .models import (
    UserMemory, UserProfile, SessionMemory,
    Turn, LongTermTrends
)
from .storage import BaseMemoryStorage
from llm.base import BaseLLM, Message


class MemoryManager:
    """记忆管理器"""
    
    def __init__(
        self,
        storage: BaseMemoryStorage,
        summarizer: Optional[BaseLLM] = None,
        config: Optional[Dict[str, Any]] = None
    ):
        """
        初始化记忆管理器
        
        Args:
            storage: 存储后端
            summarizer: 用于摘要的LLM（可选）
            config: 配置参数
        """
        self.storage = storage
        self.summarizer = summarizer
        self.config = config or {}
        
        # 配置参数
        self.max_turns = self.config.get('max_turns', 50)
        self.time_decay_factor = self.config.get('time_decay_factor', 0.95)
        self.max_history_sessions = self.config.get('max_history_sessions', 10)
        self.auto_summarize = self.config.get('auto_summarize', True)
    
    def create_user(
        self,
        user_id: str,
        age: Optional[int] = None,
        gender: Optional[str] = None,
        occupation: Optional[str] = None,
        **kwargs
    ) -> UserMemory:
        """
        创建新用户
        
        Args:
            user_id: 用户ID
            age: 年龄
            gender: 性别
            occupation: 职业
            **kwargs: 其他用户信息
            
        Returns:
            用户记忆对象
        """
        if self.storage.user_exists(user_id):
            raise ValueError(f"User {user_id} already exists")
        
        # 创建用户档案
        profile = UserProfile(
            user_id=user_id,
            age=age,
            gender=gender,
            occupation=occupation,
            **{k: v for k, v in kwargs.items() if hasattr(UserProfile, k)}
        )
        
        # 创建用户记忆
        user_memory = UserMemory(
            user_id=user_id,
            profile=profile
        )
        
        # 保存
        self.storage.save_user_memory(user_memory)
        
        return user_memory
    
    def get_user_memory(self, user_id: str) -> Optional[UserMemory]:
        """
        获取用户记忆
        
        Args:
            user_id: 用户ID
            
        Returns:
            用户记忆对象，如果不存在则返回None
        """
        return self.storage.load_user_memory(user_id)
    
    def start_session(self, user_id: str) -> str:
        """
        开始新会话
        
        Args:
            user_id: 用户ID
            
        Returns:
            会话ID
        """
        user_memory = self.get_user_memory(user_id)
        if not user_memory:
            raise ValueError(f"User {user_id} does not exist")
        
        # 创建新会话
        session_id = str(uuid.uuid4())
        session = SessionMemory(
            session_id=session_id,
            user_id=user_id
        )
        
        user_memory.sessions.append(session)
        
        # 保存
        self.storage.save_user_memory(user_memory)
        
        return session_id
    
    def end_session(self, user_id: str, session_id: str) -> None:
        """
        结束会话
        
        Args:
            user_id: 用户ID
            session_id: 会话ID
        """
        user_memory = self.get_user_memory(user_id)
        if not user_memory:
            return
        
        # 找到会话
        session = next(
            (s for s in user_memory.sessions if s.session_id == session_id),
            None
        )
        
        if not session:
            return
        
        # 设置结束时间
        session.end_time = datetime.now().isoformat()
        
        # 生成摘要
        if self.auto_summarize and self.summarizer and session.turns:
            session.session_summary = self._generate_summary(session)
            session.main_topics = self._extract_topics(session)
        
        # 保存
        self.storage.save_user_memory(user_memory)
    
    def add_turn(
        self,
        user_id: str,
        session_id: str,
        user_message: str,
        assistant_message: str,
        emotion: Optional[Dict[str, float]] = None
    ) -> None:
        """
        添加对话轮次
        
        Args:
            user_id: 用户ID
            session_id: 会话ID
            user_message: 用户消息
            assistant_message: 助手消息
            emotion: 情绪状态
        """
        user_memory = self.get_user_memory(user_id)
        if not user_memory:
            return
        
        # 找到会话
        session = next(
            (s for s in user_memory.sessions if s.session_id == session_id),
            None
        )
        
        if not session:
            return
        
        # 添加轮次
        session.add_turn(user_message, assistant_message, emotion)
        
        # 更新情绪轨迹
        if emotion:
            session.emotion_trajectory.append({
                'timestamp': datetime.now().isoformat(),
                'emotion': emotion
            })
            
            # 更新长期趋势
            if user_memory.trends:
                user_memory.trends.add_emotion_record(
                    session_id=session_id,
                    emotions=emotion,
                    context=user_message[:100]  # 保存部分上下文
                )
        
        # 保存
        self.storage.save_user_memory(user_memory)
    
    def retrieve_relevant_memory(
        self,
        user_id: str,
        current_context: str,
        top_k: int = 3
    ) -> Dict[str, Any]:
        """
        检索相关记忆
        
        Args:
            user_id: 用户ID
            current_context: 当前上下文
            top_k: 返回top-k个相关会话
            
        Returns:
            相关记忆字典
        """
        user_memory = self.get_user_memory(user_id)
        if not user_memory:
            return {}
        
        # 获取最近的会话
        recent_sessions = user_memory.get_recent_sessions(self.max_history_sessions)
        
        # 计算相关性分数（简单实现：基于时间衰减）
        scored_sessions = []
        for i, session in enumerate(reversed(recent_sessions)):
            # 时间衰减分数
            time_score = self.time_decay_factor ** i
            
            # 可以添加更复杂的相关性计算
            # 例如：基于主题匹配、情绪相似度等
            
            scored_sessions.append((session, time_score))
        
        # 排序并取top-k
        scored_sessions.sort(key=lambda x: x[1], reverse=True)
        top_sessions = scored_sessions[:top_k]
        
        # 构建记忆上下文
        memory_context = {
            'profile': user_memory.profile.to_dict(),
            'recent_sessions': [
                {
                    'session_id': s.session_id,
                    'summary': s.session_summary,
                    'main_topics': s.main_topics,
                    'score': score
                }
                for s, score in top_sessions if s.session_summary
            ],
            'emotion_trend': self._get_emotion_trend(user_memory),
            'main_issues': user_memory.profile.main_issues
        }
        
        return memory_context
    
    def _generate_summary(self, session: SessionMemory) -> str:
        """
        生成会话摘要
        
        Args:
            session: 会话对象
            
        Returns:
            摘要文本
        """
        if not self.summarizer or not session.turns:
            return ""
        
        # 构建对话历史
        dialogue = []
        for turn in session.turns:
            dialogue.append(f"用户: {turn.user_message}")
            dialogue.append(f"咨询师: {turn.assistant_message}")
        
        dialogue_text = "\n".join(dialogue)
        
        # 生成摘要
        messages = [
            Message(
                role="system",
                content="你是一个专业的心理咨询记录摘要助手。请简洁地总结以下咨询对话的核心内容。"
            ),
            Message(
                role="user",
                content=f"请总结以下对话（100字以内）:\n\n{dialogue_text}"
            )
        ]
        
        try:
            response = self.summarizer.generate(messages, max_tokens=200)
            return response.content.strip()
        except Exception as e:
            print(f"Summary generation failed: {e}")
            return ""
    
    def _extract_topics(self, session: SessionMemory) -> List[str]:
        """
        提取会话主题
        
        Args:
            session: 会话对象
            
        Returns:
            主题列表
        """
        # 简单实现：从摘要中提取
        # 可以用更复杂的NLP方法
        if session.session_summary:
            # 简单的关键词提取
            keywords = ['工作', '家庭', '焦虑', '抑郁', '压力', '睡眠', '关系']
            topics = [kw for kw in keywords if kw in session.session_summary]
            return topics[:3]
        return []
    
    def _get_emotion_trend(self, user_memory: UserMemory) -> Dict[str, Any]:
        """
        获取情绪趋势
        
        Args:
            user_memory: 用户记忆
            
        Returns:
            情绪趋势数据
        """
        if not user_memory.trends or not user_memory.trends.emotion_history:
            return {}
        
        # 获取最近的情绪记录
        recent_emotions = user_memory.trends.emotion_history[-10:]
        
        # 计算平均情绪
        emotion_avg = {}
        for record in recent_emotions:
            for emotion, value in record.emotions.items():
                if emotion not in emotion_avg:
                    emotion_avg[emotion] = []
                emotion_avg[emotion].append(value)
        
        # 计算均值
        for emotion in emotion_avg:
            emotion_avg[emotion] = sum(emotion_avg[emotion]) / len(emotion_avg[emotion])
        
        return {
            'average_emotions': emotion_avg,
            'record_count': len(recent_emotions)
        }
    
    def update_user_profile(self, user_id: str, **kwargs) -> None:
        """
        更新用户档案
        
        Args:
            user_id: 用户ID
            **kwargs: 要更新的字段
        """
        user_memory = self.get_user_memory(user_id)
        if not user_memory:
            return
        
        user_memory.profile.update(**kwargs)
        self.storage.save_user_memory(user_memory)


def create_memory_manager_from_config(
    config: Dict[str, Any],
    summarizer: Optional[BaseLLM] = None
) -> MemoryManager:
    """
    从配置创建记忆管理器
    
    Args:
        config: 配置字典
        summarizer: 摘要LLM（可选）
        
    Returns:
        MemoryManager实例
    """
    from .storage import create_memory_storage
    
    memory_config = config['memory']
    
    # 创建存储后端
    storage = create_memory_storage(
        storage_type=memory_config['storage']['type'],
        config=memory_config['storage']
    )
    
    # 创建记忆管理器
    manager_config = {
        'max_turns': memory_config['layers']['session']['max_turns'],
        'time_decay_factor': memory_config['retrieval']['time_decay_factor'],
        'max_history_sessions': memory_config['retrieval']['max_history_sessions'],
        'auto_summarize': memory_config['update']['auto_summarize']
    }
    
    return MemoryManager(
        storage=storage,
        summarizer=summarizer,
        config=manager_config
    )
