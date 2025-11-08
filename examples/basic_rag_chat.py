"""
基础RAG对话示例
演示如何使用系统进行简单的心理咨询对话
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import load_config, setup_directories
from dialogue import create_dialogue_manager_from_config
from memory import MemoryManager
from knowledge import Document


def main():
    # 1. 加载配置
    print("Loading configuration...")
    config = load_config()
    
    # 2. 创建目录
    setup_directories(config)
    
    # 3. 创建对话管理器
    print("Initializing dialogue manager...")
    dialogue_manager = create_dialogue_manager_from_config(config)
    
    # 4. 添加一些示例心理知识（可选）
    print("Adding sample psychological knowledge...")
    sample_knowledge = [
        Document(
            content="认知行为疗法(CBT)是一种心理治疗方法，通过识别和改变负面思维模式来改善情绪和行为。",
            metadata={"source": "CBT基础", "category": "therapy_method"}
        ),
        Document(
            content="焦虑是一种对未来的过度担忧。应对焦虑的方法包括深呼吸、渐进性肌肉放松和认知重构。",
            metadata={"source": "焦虑管理", "category": "anxiety"}
        ),
        Document(
            content="失眠的认知行为疗法(CBT-I)包括：睡眠限制、刺激控制、睡眠卫生教育和认知重构。",
            metadata={"source": "睡眠障碍", "category": "sleep"}
        ),
    ]
    
    dialogue_manager.rag_manager.add_psychological_knowledge(sample_knowledge)
    
    # 5. 创建用户
    user_id = "test_user_001"
    
    # 检查用户是否存在
    user_memory = dialogue_manager.memory_manager.get_user_memory(user_id)
    if not user_memory:
        print(f"Creating new user: {user_id}")
        dialogue_manager.memory_manager.create_user(
            user_id=user_id,
            age=28,
            gender="女",
            occupation="软件工程师"
        )
    else:
        print(f"User {user_id} already exists")
    
    # 6. 开始会话
    print("\n" + "="*50)
    print("Starting counseling session...")
    print("="*50 + "\n")
    
    session_id = dialogue_manager.start_session(user_id)
    
    # 7. 进行对话
    test_conversations = [
        {
            "user": "你好，我最近工作压力很大，经常睡不着觉。",
            "emotion": {"anxiety": 0.7, "stress": 0.8}
        },
        {
            "user": "我试过数羊，但是效果不好。有什么更好的方法吗？",
            "emotion": {"anxiety": 0.6, "stress": 0.7}
        },
        {
            "user": "好的，我会尝试的。谢谢你的建议。",
            "emotion": {"anxiety": 0.4, "stress": 0.5}
        }
    ]
    
    for i, conv in enumerate(test_conversations, 1):
        print(f"\n--- Turn {i} ---")
        print(f"用户: {conv['user']}")
        
        # 生成回复
        response = dialogue_manager.chat(
            user_id=user_id,
            session_id=session_id,
            user_message=conv['user'],
            emotion=conv.get('emotion')
        )
        
        print(f"咨询师: {response}")
    
    # 8. 结束会话
    print("\n" + "="*50)
    print("Ending session...")
    dialogue_manager.end_session(user_id, session_id)
    
    # 9. 查看记忆
    print("\n" + "="*50)
    print("Memory Summary:")
    print("="*50)
    
    user_memory = dialogue_manager.memory_manager.get_user_memory(user_id)
    if user_memory:
        current_session = user_memory.get_current_session()
        if current_session:
            print(f"\nSession ID: {current_session.session_id}")
            print(f"Total turns: {len(current_session.turns)}")
            print(f"Summary: {current_session.session_summary or 'Not generated yet'}")
            print(f"Topics: {current_session.main_topics or 'Not extracted yet'}")
    
    print("\n" + "="*50)
    print("Demo completed successfully!")
    print("="*50)


if __name__ == "__main__":
    main()
