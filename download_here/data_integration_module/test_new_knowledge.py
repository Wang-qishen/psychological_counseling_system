"""
测试新增的知识库 - 验证数据集集成效果
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import yaml
from knowledge.rag_manager import RAGManager
from knowledge.chroma_kb import ChromaKnowledgeBase


def test_knowledge_retrieval():
    """测试知识检索功能"""
    
    print("\n" + "="*60)
    print("  测试新增知识库")
    print("="*60 + "\n")
    
    # 加载配置
    with open("configs/config.yaml", 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    # 创建知识库
    print("初始化RAG管理器...")
    psych_kb = ChromaKnowledgeBase(
        collection_name="psychological_knowledge_extended",
        persist_directory=config['rag']['vector_store']['persist_directory'],
        embedding_model=config['rag']['embedding']['model_name']
    )
    
    rag_manager = RAGManager(
        psychological_kb=psych_kb,
        user_kb=None,
        config=config['rag']
    )
    print("✓ 初始化完成\n")
    
    # 测试查询
    test_queries = [
        "抑郁症有哪些症状?",
        "如何应对焦虑情绪?",
        "失眠的认知行为疗法",
        "如何改善人际关系?",
        "压力管理的方法",
        "情感问题咨询"
    ]
    
    print("开始测试检索...\n")
    
    for i, query in enumerate(test_queries, 1):
        print(f"[测试 {i}/{len(test_queries)}] 查询: {query}")
        print("-" * 60)
        
        try:
            # 检索
            result = rag_manager.retrieve(query=query, top_k=3)
            
            if result.psychological_docs:
                print(f"✓ 检索到 {len(result.psychological_docs)} 条相关知识\n")
                
                # 显示前2条结果
                for j, doc in enumerate(result.psychological_docs[:2], 1):
                    content = doc['content']
                    metadata = doc.get('metadata', {})
                    
                    # 截取预览
                    preview = content[:200] + "..." if len(content) > 200 else content
                    
                    print(f"  结果 {j}:")
                    print(f"    来源: {metadata.get('source_file', 'unknown')}")
                    print(f"    相关度: {doc.get('score', 0.0):.3f}")
                    print(f"    内容预览: {preview}")
                    print()
            else:
                print("✗ 未检索到相关知识\n")
            
        except Exception as e:
            print(f"✗ 检索失败: {e}\n")
        
        print()
    
    print("="*60)
    print("  测试完成!")
    print("="*60 + "\n")


def test_comparison():
    """对比新旧知识库"""
    
    print("\n" + "="*60)
    print("  对比新旧知识库")
    print("="*60 + "\n")
    
    with open("configs/config.yaml", 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    # 旧知识库
    print("1. 测试旧知识库(sample_knowledge)...")
    old_kb = ChromaKnowledgeBase(
        collection_name="psych_knowledge",
        persist_directory=config['rag']['vector_store']['persist_directory'],
        embedding_model=config['rag']['embedding']['model_name']
    )
    
    # 新知识库
    print("2. 测试新知识库(downloaded_datasets)...\n")
    new_kb = ChromaKnowledgeBase(
        collection_name="psychological_knowledge_extended",
        persist_directory=config['rag']['vector_store']['persist_directory'],
        embedding_model=config['rag']['embedding']['model_name']
    )
    
    # 测试查询
    test_query = "如何缓解焦虑?"
    
    print(f"测试查询: {test_query}\n")
    
    # 旧库检索
    print("旧知识库结果:")
    print("-" * 60)
    try:
        old_result = old_kb.retrieve(query=test_query, top_k=3)
        if old_result.documents:
            print(f"✓ 检索到 {len(old_result.documents)} 条")
            for i, doc in enumerate(old_result.documents[:2], 1):
                preview = doc[:150] + "..." if len(doc) > 150 else doc
                print(f"  [{i}] {preview}\n")
        else:
            print("✗ 无结果\n")
    except Exception as e:
        print(f"✗ 检索失败: {e}\n")
    
    # 新库检索
    print("\n新知识库结果:")
    print("-" * 60)
    try:
        new_result = new_kb.retrieve(query=test_query, top_k=3)
        if new_result.documents:
            print(f"✓ 检索到 {len(new_result.documents)} 条")
            for i, doc in enumerate(new_result.documents[:2], 1):
                preview = doc[:150] + "..." if len(doc) > 150 else doc
                print(f"  [{i}] {preview}\n")
        else:
            print("✗ 无结果\n")
    except Exception as e:
        print(f"✗ 检索失败: {e}\n")
    
    print("\n" + "="*60)
    print("  对比完成!")
    print("="*60 + "\n")


def check_stats():
    """检查知识库统计信息"""
    
    print("\n" + "="*60)
    print("  知识库统计信息")
    print("="*60 + "\n")
    
    with open("configs/config.yaml", 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    try:
        # 新知识库
        new_kb = ChromaKnowledgeBase(
            collection_name="psychological_knowledge_extended",
            persist_directory=config['rag']['vector_store']['persist_directory'],
            embedding_model=config['rag']['embedding']['model_name']
        )
        
        # 获取统计
        collection = new_kb.collection
        count = collection.count()
        
        print(f"新知识库文档数: {count}")
        
        # 尝试获取一些样本
        if count > 0:
            sample = collection.peek(limit=3)
            print(f"\n样本文档:")
            for i, doc in enumerate(sample['documents'][:3], 1):
                preview = doc[:100] + "..." if len(doc) > 100 else doc
                print(f"  [{i}] {preview}")
        
    except Exception as e:
        print(f"✗ 获取统计信息失败: {e}")
    
    print("\n" + "="*60 + "\n")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="测试新增知识库")
    parser.add_argument(
        "--mode",
        type=str,
        choices=['retrieval', 'comparison', 'stats', 'all'],
        default='all',
        help="测试模式"
    )
    
    args = parser.parse_args()
    
    if args.mode == 'retrieval' or args.mode == 'all':
        test_knowledge_retrieval()
    
    if args.mode == 'comparison' or args.mode == 'all':
        test_comparison()
    
    if args.mode == 'stats' or args.mode == 'all':
        check_stats()


if __name__ == "__main__":
    main()
