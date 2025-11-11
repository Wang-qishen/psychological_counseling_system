#!/usr/bin/env python3
"""
快速测试MentalChat16K集成效果

运行此脚本验证数据集是否成功集成到RAG系统

使用方法：
    python test_integration.py
"""

import os
import sys
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def test_data_loading():
    """测试1：数据加载"""
    print("\n" + "="*70)
    print("测试1：数据加载")
    print("="*70)
    
    try:
        from knowledge.data_loaders import DataLoader
        
        csv_path = 'data/datasets/MentalChat16K_train.csv'
        
        if not os.path.exists(csv_path):
            print(f"❌ 数据文件不存在: {csv_path}")
            print("   请先运行: python scripts/download_datasets.py --dataset mentalchat16k")
            return False
        
        print(f"✅ 数据文件存在: {csv_path}")
        
        # 测试加载
        print("\n加载数据...")
        loader = DataLoader()
        documents = loader.load_csv(
            csv_path,
            question_col='question',
            answer_col='answer'
        )
        
        print(f"✅ 成功加载 {len(documents)} 个文档")
        
        # 显示示例
        if documents:
            doc = documents[0]
            print(f"\n第一个文档示例:")
            print(f"  问题: {doc.metadata.get('question', 'N/A')[:60]}...")
            print(f"  内容: {doc.content[:80]}...")
            print(f"  长度: {len(doc.content)} 字符")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_rag_manager():
    """测试2：RAG Manager初始化"""
    print("\n" + "="*70)
    print("测试2：RAG Manager初始化")
    print("="*70)
    
    try:
        from knowledge.rag_manager import RAGManager
        import yaml
        
        # 检查配置文件
        config_path = 'configs/config.yaml'
        if not os.path.exists(config_path):
            print(f"❌ 配置文件不存在: {config_path}")
            return False
        
        print(f"✅ 配置文件存在: {config_path}")
        
        # 加载配置
        print("\n加载配置...")
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        print("✅ 配置加载成功")
        
        # 初始化RAG Manager
        print("\n初始化RAG Manager...")
        print("（这可能需要1-2分钟，请耐心等待...）")
        rag_manager = RAGManager(config)
        
        print("✅ RAG Manager初始化成功")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_rag_retrieval():
    """测试3：RAG检索功能"""
    print("\n" + "="*70)
    print("测试3：RAG检索功能")
    print("="*70)
    
    try:
        from knowledge.rag_manager import RAGManager
        import yaml
        
        # 初始化
        with open('configs/config.yaml') as f:
            config = yaml.safe_load(f)
        
        rag_manager = RAGManager(config)
        
        # 测试查询
        test_queries = [
            "我失眠怎么办？",
            "如何应对焦虑？",
            "感到很抑郁",
        ]
        
        print("\n测试RAG检索:")
        all_success = True
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n[{i}/{len(test_queries)}] 查询: {query}")
            
            try:
                result = rag_manager.retrieve(
                    query=query,
                    user_id="test_user",
                    top_k=3
                )
                
                print(f"  ✅ 检索到 {len(result.documents)} 个文档")
                
                # 显示第一个结果
                if result.documents:
                    doc = result.documents[0]
                    print(f"  最相关文档:")
                    print(f"    相似度: {doc.similarity:.3f}")
                    print(f"    内容: {doc.content[:60]}...")
                    print(f"    来源: {doc.metadata.get('source', 'N/A')}")
                
            except Exception as e:
                print(f"  ❌ 检索失败: {str(e)}")
                all_success = False
        
        return all_success
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_full_dialogue():
    """测试4：完整对话系统"""
    print("\n" + "="*70)
    print("测试4：完整对话系统")
    print("="*70)
    
    try:
        from dialogue.dialogue_manager import DialogueManager
        import yaml
        
        # 初始化
        print("\n初始化对话系统...")
        with open('configs/config.yaml') as f:
            config = yaml.safe_load(f)
        
        dialogue_manager = DialogueManager(config)
        print("✅ 对话系统初始化成功")
        
        # 测试对话
        test_messages = [
            "你好，我最近总是失眠",
            "具体应该怎么做？",
        ]
        
        print("\n测试对话:")
        user_id = "test_user"
        session_id = "test_session"
        
        for i, message in enumerate(test_messages, 1):
            print(f"\n[{i}/{len(test_messages)}] 用户: {message}")
            
            try:
                response = dialogue_manager.chat(
                    user_id=user_id,
                    session_id=session_id,
                    user_message=message
                )
                
                print(f"  咨询师: {response[:100]}...")
                print("  ✅ 对话成功")
                
            except Exception as e:
                print(f"  ❌ 对话失败: {str(e)}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主测试流程"""
    print("\n" + "="*70)
    print("MentalChat16K集成测试")
    print("="*70)
    
    results = {}
    
    # 运行所有测试
    print("\n开始测试...")
    
    results['data_loading'] = test_data_loading()
    
    if results['data_loading']:
        results['rag_manager'] = test_rag_manager()
    else:
        results['rag_manager'] = False
        print("\n⚠️  跳过RAG Manager测试（数据加载失败）")
    
    if results['rag_manager']:
        results['rag_retrieval'] = test_rag_retrieval()
        results['full_dialogue'] = test_full_dialogue()
    else:
        results['rag_retrieval'] = False
        results['full_dialogue'] = False
        print("\n⚠️  跳过后续测试（RAG Manager初始化失败）")
    
    # 显示测试结果
    print("\n" + "="*70)
    print("测试结果总结")
    print("="*70)
    
    test_names = {
        'data_loading': '数据加载',
        'rag_manager': 'RAG Manager初始化',
        'rag_retrieval': 'RAG检索功能',
        'full_dialogue': '完整对话系统',
    }
    
    passed = 0
    total = len(results)
    
    for key, name in test_names.items():
        status = "✅ 通过" if results[key] else "❌ 失败"
        print(f"{name}: {status}")
        if results[key]:
            passed += 1
    
    print(f"\n总计: {passed}/{total} 测试通过")
    
    if passed == total:
        print("\n" + "="*70)
        print("🎉 恭喜！所有测试通过！")
        print("="*70)
        print("\n✅ MentalChat16K已成功集成到你的RAG系统")
        print("✅ 系统运行正常，可以开始使用")
        print("\n下一步:")
        print("  1. 运行对话示例: python examples/basic_rag_chat.py")
        print("  2. 运行评估实验: python evaluation/scripts/run_full_evaluation.py")
        print("  3. 对比实验: python examples/comparison_experiment.py")
    else:
        print("\n" + "="*70)
        print("⚠️  部分测试失败")
        print("="*70)
        print("\n请检查:")
        print("  1. 是否已下载MentalChat16K: python scripts/download_datasets.py")
        print("  2. 是否已添加data_loaders.py到knowledge/目录")
        print("  3. 配置文件是否正确: configs/config.yaml")
        print("  4. 查看错误信息并修复问题")


if __name__ == '__main__':
    main()
