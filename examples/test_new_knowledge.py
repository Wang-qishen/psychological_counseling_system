"""
测试新增的知识库 - 验证数据集集成效果
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import yaml
from dialogue.manager import create_dialogue_manager_from_config


def test_knowledge_retrieval():
    """测试知识检索功能"""
    
    print("\n" + "="*60)
    print("  测试新增知识库")
    print("="*60 + "\n")
    
    # 加载配置
    with open("configs/config.yaml", 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    # 使用原项目的方式创建管理器
    print("初始化对话管理器...")
    dialogue_manager = create_dialogue_manager_from_config(config)
    rag_manager = dialogue_manager.rag_manager
    print("✓ 初始化完成\n")
    
    # 获取统计信息
    try:
        stats = rag_manager.get_stats()
        psych_kb_stats = stats.get('psychological_kb', {})
        doc_count = psych_kb_stats.get('document_count', 0)
        print(f"当前知识库文档数: {doc_count:,}")
        print(f"目标文档数: 628,284")
        if doc_count > 0:
            progress = (doc_count / 628284) * 100
            print(f"完成度: {progress:.1f}%")
        print()
    except Exception as e:
        print(f"无法获取统计信息: {e}\n")
    
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


def test_simple():
    """简单测试 - 只测试基本功能"""
    
    print("\n" + "="*60)
    print("  快速验证测试")
    print("="*60 + "\n")
    
    # 加载配置
    with open("configs/config.yaml", 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    # 创建管理器
    print("初始化系统...")
    dialogue_manager = create_dialogue_manager_from_config(config)
    
    # 获取统计
    print("\n知识库状态:")
    print("-" * 60)
    stats = dialogue_manager.rag_manager.get_stats()
    psych_kb_stats = stats.get('psychological_kb', {})
    doc_count = psych_kb_stats.get('document_count', 0)
    
    print(f"文档数: {doc_count:,}")
    if doc_count > 0:
        progress = (doc_count / 628284) * 100
        print(f"完成度: {progress:.1f}%")
    print()
    
    # 单个测试查询
    print("测试检索:")
    print("-" * 60)
    test_query = "如何缓解焦虑?"
    print(f"查询: {test_query}\n")
    
    try:
        result = dialogue_manager.rag_manager.retrieve(query=test_query, top_k=3)
        
        if result.psychological_docs:
            print(f"✓ 成功! 检索到 {len(result.psychological_docs)} 条知识")
            
            # 显示第一条
            if result.psychological_docs:
                doc = result.psychological_docs[0]
                preview = doc['content'][:150] + "..." if len(doc['content']) > 150 else doc['content']
                print(f"\n示例结果:")
                print(f"  {preview}")
        else:
            print("✗ 未检索到知识")
            
    except Exception as e:
        print(f"✗ 检索失败: {e}")
    
    print("\n" + "="*60 + "\n")


def check_progress():
    """检查导入进度"""
    
    print("\n" + "="*60)
    print("  检查导入进度")
    print("="*60 + "\n")
    
    try:
        # 加载配置
        with open("configs/config.yaml", 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        # 创建管理器
        dialogue_manager = create_dialogue_manager_from_config(config)
        
        # 获取统计
        stats = dialogue_manager.rag_manager.get_stats()
        psych_kb_stats = stats.get('psychological_kb', {})
        doc_count = psych_kb_stats.get('document_count', 0)
        
        print(f"当前文档数: {doc_count:,}")
        print(f"目标文档数: 628,284")
        
        if doc_count > 0:
            progress = (doc_count / 628284) * 100
            print(f"\n完成度: {progress:.1f}%")
            
            if progress < 100:
                remaining = 628284 - doc_count
                print(f"剩余: {remaining:,} 条")
                print(f"\n状态: 🔄 正在导入中...")
            else:
                print(f"\n状态: ✅ 导入完成!")
        else:
            print(f"\n状态: ⚠️ 尚未开始导入")
        
        # 测试检索
        print("\n" + "-"*60)
        print("快速检索测试:")
        result = dialogue_manager.rag_manager.retrieve("测试", top_k=1)
        if result.psychological_docs:
            print("✓ 知识库可用")
        else:
            print("⚠️ 知识库为空或检索失败")
            
    except Exception as e:
        print(f"✗ 检查失败: {e}")
    
    print("\n" + "="*60 + "\n")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="测试新增知识库")
    parser.add_argument(
        "--mode",
        type=str,
        choices=['retrieval', 'simple', 'progress', 'all'],
        default='simple',
        help="测试模式"
    )
    
    args = parser.parse_args()
    
    if args.mode == 'progress':
        check_progress()
    elif args.mode == 'simple':
        test_simple()
    elif args.mode == 'retrieval':
        test_knowledge_retrieval()
    elif args.mode == 'all':
        check_progress()
        test_simple()
        test_knowledge_retrieval()


if __name__ == "__main__":
    main()