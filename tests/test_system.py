"""
系统测试脚本
验证各个模块是否正常工作
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_config():
    """测试配置加载"""
    print("Testing config loading...")
    try:
        from utils import load_config, setup_directories
        config = load_config()
        setup_directories(config)
        print("✅ Config loading: PASSED")
        return config
    except Exception as e:
        print(f"❌ Config loading: FAILED - {e}")
        return None


def test_llm(config):
    """测试LLM"""
    print("\nTesting LLM...")
    try:
        from llm import create_llm_from_config, Message
        
        llm = create_llm_from_config(config)
        
        # 简单测试
        messages = [
            Message(role="system", content="你是一个助手。"),
            Message(role="user", content="你好，请用一句话介绍自己。")
        ]
        
        response = llm.generate(messages, max_tokens=100)
        print(f"   Response: {response.content[:100]}...")
        print("✅ LLM: PASSED")
        return llm
    except Exception as e:
        print(f"❌ LLM: FAILED - {e}")
        return None


def test_knowledge(config):
    """测试知识库"""
    print("\nTesting knowledge base...")
    try:
        from knowledge import create_rag_manager_from_config, Document
        
        rag_manager = create_rag_manager_from_config(config)
        
        # 添加测试文档
        test_docs = [
            Document(
                content="焦虑是一种情绪状态。",
                metadata={"test": "yes"}
            )
        ]
        rag_manager.add_psychological_knowledge(test_docs)
        
        # 测试检索
        result = rag_manager.retrieve("什么是焦虑")
        print(f"   Retrieved {len(result.psychological_docs)} documents")
        print("✅ Knowledge base: PASSED")
        return rag_manager
    except Exception as e:
        print(f"❌ Knowledge base: FAILED - {e}")
        return None


def test_memory(config, llm):
    """测试记忆系统"""
    print("\nTesting memory system...")
    try:
        from memory import create_memory_manager_from_config
        
        memory_manager = create_memory_manager_from_config(config, llm)
        
        # 创建测试用户
        test_user_id = "test_user_999"
        
        # 删除旧数据（如果存在）
        if memory_manager.storage.user_exists(test_user_id):
            memory_manager.storage.delete_user_memory(test_user_id)
        
        # 创建用户
        user_memory = memory_manager.create_user(
            user_id=test_user_id,
            age=25,
            gender="测试"
        )
        print(f"   Created user: {user_memory.user_id}")
        
        # 开始会话
        session_id = memory_manager.start_session(test_user_id)
        print(f"   Started session: {session_id}")
        
        # 添加对话
        memory_manager.add_turn(
            user_id=test_user_id,
            session_id=session_id,
            user_message="测试消息",
            assistant_message="测试回复",
            emotion={"test": 0.5}
        )
        
        # 结束会话
        memory_manager.end_session(test_user_id, session_id)
        
        # 验证
        loaded_memory = memory_manager.get_user_memory(test_user_id)
        assert loaded_memory is not None
        assert len(loaded_memory.sessions) > 0
        
        # 清理
        memory_manager.storage.delete_user_memory(test_user_id)
        
        print("✅ Memory system: PASSED")
        return memory_manager
    except Exception as e:
        print(f"❌ Memory system: FAILED - {e}")
        import traceback
        traceback.print_exc()
        return None


def test_dialogue(config):
    """测试对话管理器"""
    print("\nTesting dialogue manager...")
    try:
        from dialogue import create_dialogue_manager_from_config
        
        dialogue_manager = create_dialogue_manager_from_config(config)
        
        # 创建测试用户
        test_user_id = "test_user_998"
        
        # 删除旧数据
        if dialogue_manager.memory_manager.storage.user_exists(test_user_id):
            dialogue_manager.memory_manager.storage.delete_user_memory(test_user_id)
        
        # 创建用户
        dialogue_manager.memory_manager.create_user(
            user_id=test_user_id,
            age=30
        )
        
        # 开始会话
        session_id = dialogue_manager.start_session(test_user_id)
        
        # 进行对话
        response = dialogue_manager.chat(
            user_id=test_user_id,
            session_id=session_id,
            user_message="你好"
        )
        
        print(f"   Response: {response[:100]}...")
        
        # 结束会话
        dialogue_manager.end_session(test_user_id, session_id)
        
        # 清理
        dialogue_manager.memory_manager.storage.delete_user_memory(test_user_id)
        
        print("✅ Dialogue manager: PASSED")
        return True
    except Exception as e:
        print(f"❌ Dialogue manager: FAILED - {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    print("="*60)
    print("Psychological Counseling System - Test Suite")
    print("="*60)
    
    # 测试配置
    config = test_config()
    if not config:
        print("\n❌ Critical failure: Cannot load config")
        return
    
    # 测试LLM
    llm = test_llm(config)
    if not llm:
        print("\n⚠️  Warning: LLM test failed, some features may not work")
    
    # 测试知识库
    rag = test_knowledge(config)
    if not rag:
        print("\n⚠️  Warning: Knowledge base test failed")
    
    # 测试记忆系统
    memory = test_memory(config, llm)
    if not memory:
        print("\n⚠️  Warning: Memory system test failed")
    
    # 测试对话管理器
    if llm and rag and memory:
        dialogue_ok = test_dialogue(config)
        if not dialogue_ok:
            print("\n⚠️  Warning: Dialogue manager test failed")
    
    print("\n" + "="*60)
    print("Test Summary:")
    print("="*60)
    print(f"Config:    {'✅ PASSED' if config else '❌ FAILED'}")
    print(f"LLM:       {'✅ PASSED' if llm else '❌ FAILED'}")
    print(f"Knowledge: {'✅ PASSED' if rag else '❌ FAILED'}")
    print(f"Memory:    {'✅ PASSED' if memory else '❌ FAILED'}")
    
    if config and llm and rag and memory:
        print("\n🎉 All core components are working!")
        print("You can now run the examples:")
        print("  python examples/basic_rag_chat.py")
        print("  python examples/multi_session_chat.py")
    else:
        print("\n⚠️  Some components failed. Please check the errors above.")
    
    print("="*60)


if __name__ == "__main__":
    main()
