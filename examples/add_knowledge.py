#!/usr/bin/env python3
"""
知识库添加工具
用于将心理学知识和用户档案添加到RAG系统中
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dialogue.manager import create_dialogue_manager_from_config
from knowledge.base import Document
import yaml


def load_config():
    """加载配置文件"""
    config_path = project_root / "configs" / "config.yaml"
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def ensure_directories(config):
    """确保必要的目录存在"""
    dirs_to_create = [
        config['rag']['vector_store']['persist_directory'],
        config['memory']['storage']['path'],
    ]
    
    for dir_path in dirs_to_create:
        os.makedirs(dir_path, exist_ok=True)
    
    print("Directories created successfully")


def load_text_file(file_path):
    """
    加载文本文件
    
    Args:
        file_path: 文件路径
        
    Returns:
        文件内容字符串
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except Exception as e:
        print(f"错误: 无法读取文件 {file_path}: {e}")
        return None


def add_psychological_knowledge(dialogue_manager, knowledge_dir):
    """
    添加心理学知识到知识库
    
    Args:
        dialogue_manager: 对话管理器实例
        knowledge_dir: 知识文件目录
    """
    print("\n" + "=" * 60)
    print("添加心理学专业知识到知识库...")
    print("=" * 60)
    
    # 查找所有.txt文件
    knowledge_path = Path(knowledge_dir)
    if not knowledge_path.exists():
        print(f"错误: 目录 {knowledge_dir} 不存在")
        return
    
    txt_files = list(knowledge_path.glob("*.txt"))
    
    if not txt_files:
        print(f"警告: 在 {knowledge_dir} 中未找到任何 .txt 文件")
        return
    
    documents = []
    for file_path in txt_files:
        filename = os.path.basename(file_path)
        content = load_text_file(file_path)
        
        if content:
            doc = Document(
                content=content,
                metadata={
                    "source": filename,
                    "type": "psychological_knowledge"
                }
            )
            documents.append(doc)
            print(f"✓ 已加载: {filename} ({len(content)} 字符)")
    
    # 添加到知识库
    if documents:
        dialogue_manager.rag_manager.add_psychological_knowledge(documents)
        print(f"\n成功添加 {len(documents)} 个心理学知识文档到知识库！")
    else:
        print("\n未添加任何文档")


def add_user_knowledge(dialogue_manager, user_info_dir):
    """
    添加用户信息到知识库
    
    Args:
        dialogue_manager: 对话管理器实例
        user_info_dir: 用户信息文件目录
    """
    print("\n" + "=" * 60)
    print("添加用户个人信息到知识库...")
    print("=" * 60)
    
    # 查找所有.txt文件
    user_info_path = Path(user_info_dir)
    if not user_info_path.exists():
        print(f"错误: 目录 {user_info_dir} 不存在")
        return
    
    txt_files = list(user_info_path.glob("*.txt"))
    
    if not txt_files:
        print(f"警告: 在 {user_info_dir} 中未找到任何 .txt 文件")
        return
    
    added_count = 0
    for file_path in txt_files:
        filename = os.path.basename(file_path)
        content = load_text_file(file_path)
        
        if content:
            # 从文件名提取用户ID (例如: user_a_profile.txt -> a)
            user_id = filename.replace('_profile.txt', '').replace('user_', '')
            
            print(f"✓ 已加载: {filename} ({len(content)} 字符)")
            
            # 使用正确的方法签名
            dialogue_manager.rag_manager.add_user_knowledge(
                user_id=user_id,
                content=content,
                metadata={
                    "source": filename,
                    "type": "user_profile"
                }
            )
            added_count += 1
    
    if added_count > 0:
        print(f"\n成功添加 {added_count} 个用户档案到知识库！")
    else:
        print("\n未添加任何文档")


def main():
    """主函数"""
    print("=" * 60)
    print("知识库添加工具")
    print("=" * 60)
    
    # 1. 加载配置
    print("[1/4] 加载配置...")
    config = load_config()
    
    # 2. 创建必要的目录
    print("[2/4] 创建必要的目录...")
    ensure_directories(config)
    
    # 3. 初始化对话管理器
    print("[3/4] 初始化系统...")
    dialogue_manager = create_dialogue_manager_from_config(config)
    
    # 4. 添加知识
    print("[4/4] 添加知识文件...")
    
    # 添加心理学知识
    knowledge_dir = project_root / "data" / "sample_knowledge"
    add_psychological_knowledge(dialogue_manager, knowledge_dir)
    
    # 添加用户信息
    user_info_dir = project_root / "data" / "sample_user_info"
    add_user_knowledge(dialogue_manager, user_info_dir)
    
    # 显示统计信息
    print("\n" + "=" * 60)
    print("知识库统计信息")
    print("=" * 60)
    stats = dialogue_manager.rag_manager.get_stats()
    print(f"\n心理知识库:")
    print(f"  - 文档数: {stats['psychological_kb'].get('document_count', 0)}")
    print(f"\n用户知识库:")
    print(f"  - 文档数: {stats['user_kb'].get('document_count', 0)}")
    
    print("\n" + "=" * 60)
    print("✅ 知识库添加完成！")
    print("=" * 60)
    print("\n提示: 现在可以运行对比实验了:")
    print("  python examples/comparison_experiment.py")


if __name__ == "__main__":
    main()