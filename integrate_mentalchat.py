#!/usr/bin/env python3
"""
MentalChat16K数据集集成脚本
将MentalChat16K数据加载到现有的RAG系统中

使用方法：
    python integrate_mentalchat.py

选择集成方式：
    1. 仅加载数据（不添加到数据库）
    2. 添加到ChromaDB
    3. 通过RAGManager集成（推荐）⭐
    4. 全部执行
"""

import os
import sys
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from knowledge.data_loaders import DataLoader


def integrate_mentalchat_to_rag():
    """
    将MentalChat16K数据集集成到RAG系统
    """
    print("=" * 70)
    print("MentalChat16K数据集集成到RAG系统")
    print("=" * 70)
    
    # Step 1: 初始化数据加载器
    print("\n[1/4] 初始化数据加载器...")
    loader = DataLoader(
        chunk_size=600,      # 参考Mentalic Net的设置
        chunk_overlap=0,     # 无重叠
        min_length=50        # 过滤短文本
    )
    print("✅ 数据加载器初始化完成")
    
    # Step 2: 加载MentalChat16K数据
    print("\n[2/4] 加载MentalChat16K数据集...")
    csv_path = 'data/datasets/MentalChat16K_train.csv'
    
    if not os.path.exists(csv_path):
        print(f"❌ 错误：找不到数据文件 {csv_path}")
        print("   请先运行: python scripts/download_datasets.py --dataset mentalchat16k")
        return None
    
    documents = loader.load_csv(
        csv_path,
        question_col='question',
        answer_col='answer',
        min_length=50
    )
    
    print(f"✅ 成功加载 {len(documents)} 个文档")
    
    # Step 3: 显示数据统计
    print("\n[3/4] 数据统计信息...")
    print(f"  总文档数: {len(documents)}")
    
    # 按来源统计
    sources = {}
    for doc in documents:
        source = doc.metadata.get('source', 'unknown')
        sources[source] = sources.get(source, 0) + 1
    
    print(f"  数据来源:")
    for source, count in sources.items():
        print(f"    - {source}: {count} 个文档")
    
    # 显示示例文档
    print(f"\n  示例文档:")
    if documents:
        doc = documents[0]
        question = doc.metadata.get('question', 'N/A')
        print(f"    问题: {question[:60]}...")
        print(f"    内容: {doc.content[:80]}...")
        print(f"    长度: {len(doc.content)} 字符")
    
    # Step 4: 返回文档供后续使用
    print("\n[4/4] 准备集成到RAG系统...")
    print("✅ 数据准备完成，可以添加到RAG知识库")
    
    return documents


def add_to_chroma_db(documents):
    """
    将文档添加到ChromaDB向量数据库
    
    Args:
        documents: Document对象列表
    """
    from knowledge.chroma_kb import ChromaKnowledgeBase
    
    print("\n" + "=" * 70)
    print("添加到ChromaDB向量数据库")
    print("=" * 70)
    
    # 初始化ChromaDB
    print("\n初始化ChromaDB...")
    kb = ChromaKnowledgeBase(
        collection_name="psychology",
        persist_directory="data/chroma_db"
    )
    
    # 批量添加文档
    print(f"添加 {len(documents)} 个文档到向量数据库...")
    
    batch_size = 100
    total_batches = (len(documents) + batch_size - 1) // batch_size
    
    for i in range(0, len(documents), batch_size):
        batch = documents[i:i+batch_size]
        batch_num = i // batch_size + 1
        
        # 添加文档
        for doc in batch:
            kb.add_document(
                content=doc.content,
                metadata=doc.metadata
            )
        
        print(f"  进度: [{batch_num}/{total_batches}] 已添加 {min(i+batch_size, len(documents))}/{len(documents)} 个文档")
    
    print(f"\n✅ 成功添加 {len(documents)} 个文档到ChromaDB")
    
    # 测试检索
    print("\n测试检索功能...")
    results = kb.search("我失眠怎么办？", top_k=3)
    
    print(f"检索到 {len(results)} 个相关文档:")
    for i, result in enumerate(results, 1):
        print(f"\n  结果 {i}:")
        print(f"    内容: {result.content[:100]}...")
        print(f"    相似度: {result.similarity:.3f}")
        print(f"    来源: {result.metadata.get('source', 'N/A')}")
    
    return kb


def integrate_with_rag_manager():
    """
    方法2：通过RAGManager集成（推荐）
    """
    from knowledge.rag_manager import RAGManager
    import yaml
    
    print("\n" + "=" * 70)
    print("方法2：通过RAGManager集成（推荐）")
    print("=" * 70)
    
    # 加载配置
    print("\n加载配置文件...")
    with open('configs/config.yaml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    # 初始化RAG Manager
    print("初始化RAG Manager...")
    # rag_manager = RAGManager(config)
    rag_manager = RAGManager(config, user_kb="mentalchat")  # 或其他合适的用户知识库名称
    
    # 加载MentalChat16K数据
    print("\n加载MentalChat16K数据...")
    loader = DataLoader(chunk_size=600, chunk_overlap=0)
    documents = loader.load_csv(
        'data/datasets/MentalChat16K_train.csv',
        question_col='question',
        answer_col='answer'
    )
    
    print(f"✅ 加载了 {len(documents)} 个文档")
    
    # 添加到心理学知识库
    print("\n添加到心理学知识库...")
    for i, doc in enumerate(documents):
        rag_manager.psych_kb.add_document(
            content=doc.content,
            metadata=doc.metadata
        )
        
        if (i + 1) % 1000 == 0:
            print(f"  进度: 已添加 {i+1}/{len(documents)} 个文档")
    
    print(f"\n✅ 完成！共添加 {len(documents)} 个文档到RAG系统")
    
    # 测试RAG检索
    print("\n测试RAG检索...")
    test_query = "我最近感到很焦虑，应该怎么办？"
    print(f"测试查询: {test_query}")
    
    result = rag_manager.retrieve(
        query=test_query,
        user_id="test_user",
        top_k=3
    )
    
    print(f"\n检索到 {len(result.documents)} 个相关文档:")
    for i, doc in enumerate(result.documents, 1):
        print(f"\n  文档 {i}:")
        print(f"    内容: {doc.content[:100]}...")
        print(f"    相似度: {doc.similarity:.3f}")
        print(f"    来源: {doc.metadata.get('source', 'N/A')}")
    
    return rag_manager


def main():
    """
    主函数：提供多种集成方式
    """
    print("\n" + "=" * 70)
    print("MentalChat16K集成工具")
    print("=" * 70)
    print("\n选择集成方式:")
    print("  1. 仅加载数据（不添加到数据库）")
    print("  2. 添加到ChromaDB")
    print("  3. 通过RAGManager集成（推荐）⭐")
    print("  4. 全部执行")
    
    try:
        choice = input("\n请选择 (1-4): ").strip()
    except:
        choice = "3"  # 默认选项
    
    if choice == "1":
        print("\n执行选项1: 仅加载数据")
        documents = integrate_mentalchat_to_rag()
        if documents:
            print(f"\n✅ 成功加载 {len(documents)} 个文档")
            print("   可以使用 add_to_chroma_db(documents) 添加到数据库")
        
    elif choice == "2":
        print("\n执行选项2: 添加到ChromaDB")
        documents = integrate_mentalchat_to_rag()
        if documents:
            kb = add_to_chroma_db(documents)
            print(f"\n✅ 集成完成！数据已保存到 data/chroma_db")
        
    elif choice == "3":
        print("\n执行选项3: 通过RAGManager集成（推荐）")
        rag_manager = integrate_with_rag_manager()
        print(f"\n✅ 集成完成！RAG系统已准备就绪")
        
    elif choice == "4":
        print("\n执行选项4: 全部执行")
        
        # Step 1: 加载数据
        documents = integrate_mentalchat_to_rag()
        
        if documents:
            # Step 2: 添加到ChromaDB
            kb = add_to_chroma_db(documents)
            
            # Step 3: 通过RAGManager集成
            rag_manager = integrate_with_rag_manager()
            
            print("\n" + "=" * 70)
            print("✅ 所有步骤完成！")
            print("=" * 70)
            print("\n知识库状态:")
            print(f"  - ChromaDB文档数: {len(documents)}")
            print(f"  - RAG系统: 已就绪")
            print(f"  - 存储位置: data/chroma_db")
    
    else:
        print("❌ 无效选择，请输入1-4")
        return
    
    print("\n" + "=" * 70)
    print("集成完成！")
    print("=" * 70)
    print("\n下一步:")
    print("  1. 测试对话: python examples/basic_rag_chat.py")
    print("  2. 运行评估: python evaluation/scripts/run_full_evaluation.py")
    print("  3. 对比实验: python examples/comparison_experiment.py")


if __name__ == '__main__':
    main()
