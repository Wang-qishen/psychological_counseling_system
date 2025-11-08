"""
多会话对话示例
展示跨会话的记忆系统功能
"""

import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import load_config, setup_directories, format_dialogue_history
from dialogue import create_dialogue_manager_from_config
from knowledge import Document


def run_session(dialogue_manager, user_id: str, session_num: int, conversations: list):
    """运行单个会话"""
    print(f"\n{'='*60}")
    print(f"Session {session_num}")
    print(f"{'='*60}\n")
    
    # 开始会话
    session_id = dialogue_manager.start_session(user_id)
    
    # 进行对话
    for i, conv in enumerate(conversations, 1):
        print(f"\n--- Turn {i} ---")
        print(f"用户: {conv['user']}")
        
        response = dialogue_manager.chat(
            user_id=user_id,
            session_id=session_id,
            user_message=conv['user'],
            emotion=conv.get('emotion')
        )
        
        print(f"咨询师: {response}")
        
        # 模拟真实对话的时间间隔
        time.sleep(0.5)
    
    # 结束会话
    dialogue_manager.end_session(user_id, session_id)
    
    return session_id


def main():
    # 1. 初始化
    print("Initializing system...")
    config = load_config()
    setup_directories(config)
    dialogue_manager = create_dialogue_manager_from_config(config)
    
    # 2. 添加心理知识
    sample_knowledge = [
        Document(
            content="工作倦怠的表现包括：情绪耗竭、去人格化、个人成就感降低。应对方法包括设置边界、寻求支持、培养兴趣爱好。",
            metadata={"source": "职业心理", "category": "burnout"}
        ),
        Document(
            content="社交焦虑的认知行为治疗包括：识别负面自动思维、暴露疗法、社交技能训练。",
            metadata={"source": "社交焦虑", "category": "social_anxiety"}
        ),
    ]
    dialogue_manager.rag_manager.add_psychological_knowledge(sample_knowledge)
    
    # 3. 创建用户
    user_id = "test_user_002"
    
    if not dialogue_manager.memory_manager.get_user_memory(user_id):
        dialogue_manager.memory_manager.create_user(
            user_id=user_id,
            age=25,
            gender="男",
            occupation="产品经理"
        )
        print(f"Created user: {user_id}")
    
    # 4. 第一次会话 - 讨论工作压力
    session1_conversations = [
        {
            "user": "最近工作压力特别大，感觉快要崩溃了。",
            "emotion": {"stress": 0.9, "anxiety": 0.7}
        },
        {
            "user": "老板总是给我安排紧急任务，我连休息的时间都没有。",
            "emotion": {"stress": 0.8, "frustration": 0.7}
        },
        {
            "user": "我试着和老板沟通过，但是没什么效果。",
            "emotion": {"helplessness": 0.6, "stress": 0.7}
        }
    ]
    
    run_session(dialogue_manager, user_id, 1, session1_conversations)
    
    print("\n[模拟时间流逝...]\n")
    time.sleep(2)
    
    # 5. 第二次会话 - 继续讨论，系统会记住之前的内容
    session2_conversations = [
        {
            "user": "你好，我是上次来咨询的那个人。",
            "emotion": {"stress": 0.6, "anxiety": 0.5}
        },
        {
            "user": "上次你给的建议我试了，但是工作压力还是很大。",
            "emotion": {"stress": 0.7, "disappointment": 0.5}
        },
        {
            "user": "而且我发现自己最近社交也有问题，不想和人交流。",
            "emotion": {"anxiety": 0.6, "withdrawal": 0.7}
        }
    ]
    
    print("\n💡 注意：系统会记住第一次会话的内容并在回复中体现\n")
    run_session(dialogue_manager, user_id, 2, session2_conversations)
    
    # 6. 查看完整记忆
    print(f"\n{'='*60}")
    print("Complete Memory Analysis")
    print(f"{'='*60}\n")
    
    user_memory = dialogue_manager.memory_manager.get_user_memory(user_id)
    
    if user_memory:
        # 用户档案
        print("### 用户档案")
        print(f"ID: {user_memory.user_id}")
        print(f"年龄: {user_memory.profile.age}")
        print(f"性别: {user_memory.profile.gender}")
        print(f"职业: {user_memory.profile.occupation}")
        
        # 会话历史
        print(f"\n### 会话历史 (共 {len(user_memory.sessions)} 个会话)")
        for i, session in enumerate(user_memory.sessions, 1):
            print(f"\n会话 {i}:")
            print(f"  ID: {session.session_id}")
            print(f"  时间: {session.start_time}")
            print(f"  轮次: {len(session.turns)}")
            print(f"  摘要: {session.session_summary or '未生成'}")
            print(f"  话题: {', '.join(session.main_topics) if session.main_topics else '未提取'}")
        
        # 情绪趋势
        if user_memory.trends and user_memory.trends.emotion_history:
            print(f"\n### 情绪趋势 (共 {len(user_memory.trends.emotion_history)} 条记录)")
            
            # 计算平均情绪
            emotion_totals = {}
            for record in user_memory.trends.emotion_history:
                for emotion, value in record.emotions.items():
                    if emotion not in emotion_totals:
                        emotion_totals[emotion] = []
                    emotion_totals[emotion].append(value)
            
            print("平均情绪状态:")
            for emotion, values in emotion_totals.items():
                avg = sum(values) / len(values)
                print(f"  {emotion}: {avg:.2f}")
    
    print(f"\n{'='*60}")
    print("Multi-session demo completed!")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
