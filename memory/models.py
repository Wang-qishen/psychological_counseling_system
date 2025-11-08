"""
记忆系统数据模型
定义三层记忆架构的数据结构
"""

from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional
from datetime import datetime
import json


@dataclass
class Turn:
    """单轮对话"""
    user_message: str
    assistant_message: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    emotion: Optional[Dict[str, float]] = None  # 情绪状态


@dataclass
class SessionMemory:
    """会话级记忆（短期）"""
    session_id: str
    user_id: str
    start_time: str = field(default_factory=lambda: datetime.now().isoformat())
    end_time: Optional[str] = None
    turns: List[Turn] = field(default_factory=list)
    session_summary: Optional[str] = None
    main_topics: List[str] = field(default_factory=list)
    emotion_trajectory: List[Dict[str, Any]] = field(default_factory=list)
    
    def add_turn(self, user_msg: str, assistant_msg: str, emotion: Optional[Dict[str, float]] = None):
        """添加一轮对话"""
        turn = Turn(
            user_message=user_msg,
            assistant_message=assistant_msg,
            emotion=emotion
        )
        self.turns.append(turn)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return asdict(self)


@dataclass
class UserProfile:
    """用户档案（中期）"""
    user_id: str
    age: Optional[int] = None
    gender: Optional[str] = None
    occupation: Optional[str] = None
    main_issues: List[str] = field(default_factory=list)
    life_events: List[Dict[str, Any]] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def update(self, **kwargs):
        """更新档案"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return asdict(self)


@dataclass
class EmotionRecord:
    """情绪记录"""
    timestamp: str
    session_id: str
    emotions: Dict[str, float]  # 例如: {'anxiety': 0.7, 'stress': 0.8}
    context: Optional[str] = None


@dataclass
class TopicRecord:
    """话题记录"""
    timestamp: str
    session_id: str
    topics: List[str]
    importance: float = 0.5


@dataclass
class InterventionRecord:
    """干预记录"""
    timestamp: str
    session_id: str
    intervention_type: str  # CBT, mindfulness, etc.
    effectiveness: Optional[float] = None
    notes: Optional[str] = None


@dataclass
class LongTermTrends:
    """长期趋势（长期）"""
    user_id: str
    emotion_history: List[EmotionRecord] = field(default_factory=list)
    topic_history: List[TopicRecord] = field(default_factory=list)
    intervention_history: List[InterventionRecord] = field(default_factory=list)
    
    def add_emotion_record(self, session_id: str, emotions: Dict[str, float], context: Optional[str] = None):
        """添加情绪记录"""
        record = EmotionRecord(
            timestamp=datetime.now().isoformat(),
            session_id=session_id,
            emotions=emotions,
            context=context
        )
        self.emotion_history.append(record)
    
    def add_topic_record(self, session_id: str, topics: List[str], importance: float = 0.5):
        """添加话题记录"""
        record = TopicRecord(
            timestamp=datetime.now().isoformat(),
            session_id=session_id,
            topics=topics,
            importance=importance
        )
        self.topic_history.append(record)
    
    def add_intervention_record(
        self,
        session_id: str,
        intervention_type: str,
        effectiveness: Optional[float] = None,
        notes: Optional[str] = None
    ):
        """添加干预记录"""
        record = InterventionRecord(
            timestamp=datetime.now().isoformat(),
            session_id=session_id,
            intervention_type=intervention_type,
            effectiveness=effectiveness,
            notes=notes
        )
        self.intervention_history.append(record)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'user_id': self.user_id,
            'emotion_history': [asdict(r) for r in self.emotion_history],
            'topic_history': [asdict(r) for r in self.topic_history],
            'intervention_history': [asdict(r) for r in self.intervention_history]
        }


@dataclass
class UserMemory:
    """完整的用户记忆"""
    user_id: str
    profile: UserProfile
    sessions: List[SessionMemory] = field(default_factory=list)
    trends: Optional[LongTermTrends] = None
    
    def __post_init__(self):
        """初始化后处理"""
        if self.trends is None:
            self.trends = LongTermTrends(user_id=self.user_id)
    
    def get_current_session(self) -> Optional[SessionMemory]:
        """获取当前会话"""
        if self.sessions:
            return self.sessions[-1]
        return None
    
    def get_recent_sessions(self, n: int = 5) -> List[SessionMemory]:
        """获取最近的n个会话"""
        return self.sessions[-n:] if len(self.sessions) >= n else self.sessions
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'user_id': self.user_id,
            'profile': self.profile.to_dict(),
            'sessions': [s.to_dict() for s in self.sessions],
            'trends': self.trends.to_dict() if self.trends else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserMemory':
        """从字典创建"""
        profile = UserProfile(**data['profile'])
        
        sessions = []
        for s_data in data.get('sessions', []):
            turns = [Turn(**t) for t in s_data.get('turns', [])]
            session = SessionMemory(
                session_id=s_data['session_id'],
                user_id=s_data['user_id'],
                start_time=s_data['start_time'],
                end_time=s_data.get('end_time'),
                turns=turns,
                session_summary=s_data.get('session_summary'),
                main_topics=s_data.get('main_topics', []),
                emotion_trajectory=s_data.get('emotion_trajectory', [])
            )
            sessions.append(session)
        
        trends_data = data.get('trends')
        trends = None
        if trends_data:
            emotion_hist = [EmotionRecord(**r) for r in trends_data.get('emotion_history', [])]
            topic_hist = [TopicRecord(**r) for r in trends_data.get('topic_history', [])]
            interv_hist = [InterventionRecord(**r) for r in trends_data.get('intervention_history', [])]
            
            trends = LongTermTrends(
                user_id=trends_data['user_id'],
                emotion_history=emotion_hist,
                topic_history=topic_hist,
                intervention_history=interv_hist
            )
        
        return cls(
            user_id=data['user_id'],
            profile=profile,
            sessions=sessions,
            trends=trends
        )
