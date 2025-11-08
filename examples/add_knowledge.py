"""
知识库添加工具
用于将本地文本文件添加到系统的知识库中
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import load_config, setup_directories
from dialogue import create_dialogue_manager_from_config
from knowledge import Document
import glob


def load_text_file(file_path):
    """
    读取文本文件
    
    Args:
        file_path: 文件路径
        
    Returns:
        文件内容
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None


def add_psychological_knowledge(dialogue_manager, knowledge_dir):
    """
    添加心理学专业知识
    
    Args:
        dialogue_manager: 对话管理器实例
        knowledge_dir: 知识文件目录
    """
    print("\n" + "="*60)
    print("添加心理学专业知识到知识库...")
    print("="*60)
    
    # 获取所有文本文件
    txt_files = glob.glob(os.path.join(knowledge_dir, "*.txt"))
    
    if not txt_files:
        print(f"警告: 在 {knowledge_dir} 中未找到任何 .txt 文件")
        return
    
    documents = []
    for file_path in txt_files:
        filename = os.path.basename(file_path)
        content = load_text_file(file_path)
        
        if content:
            # 从文件名提取类别
            category = filename.replace('.txt', '').replace('_', ' ')
            
            doc = Document(
                content=content,
                metadata={
                    "source": filename,
                    "category": category,
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
    添加用户个人信息
    
    Args:
        dialogue_manager: 对话管理器实例
        user_info_dir: 用户信息文件目录
    """
    print("\n" + "="*60)
    print("添加用户个人信息到知识库...")
    print("="*60)
    
    # 获取所有文本文件
    txt_files = glob.glob(os.path.join(user_info_dir, "*.txt"))
    
    if not txt_files:
        print(f"警告: 在 {user_info_dir} 中未找到任何 .txt 文件")
        return
    
    documents = []
    for file_path in txt_files:
        filename = os.path.basename(file_path)
        content = load_text_file(file_path)
        
        if content:
            # 从文件名提取用户ID
            user_id = filename.replace('_profile.txt', '').replace('user_', '')
            
            doc = Document(
                content=content,
                metadata={
                    "source": filename,
                    "user_id": user_id,
                    "type": "user_profile"
                }
            )
            documents.append(doc)
            print(f"✓ 已加载: {filename} ({len(content)} 字符)")
    
    # 添加到知识库
    if documents:
        dialogue_manager.rag_manager.add_user_knowledge(documents)
        print(f"\n成功添加 {len(documents)} 个用户档案到知识库！")
    else:
        print("\n未添加任何文档")


def main():
    """主函数"""
    print("="*60)
    print("知识库添加工具")
    print("="*60)
    
    # 1. 加载配置
    print("\n[1/4] 加载配置...")
    config = load_config()
    
    # 2. 创建目录
    print("[2/4] 创建必要的目录...")
    setup_directories(config)
    
    # 3. 创建对话管理器
    print("[3/4] 初始化系统...")
    dialogue_manager = create_dialogue_manager_from_config(config)
    
    # 4. 添加知识
    print("[4/4] 添加知识文件...")
    
    # 心理学知识库
    psych_knowledge_dir = "./data/sample_knowledge"
    if os.path.exists(psych_knowledge_dir):
        add_psychological_knowledge(dialogue_manager, psych_knowledge_dir)
    else:
        print(f"\n警告: 未找到目录 {psych_knowledge_dir}")
        print("请确保已创建该目录并放入心理学知识文件")
    
    # 用户信息知识库
    user_info_dir = "./data/sample_user_info"
    if os.path.exists(user_info_dir):
        add_user_knowledge(dialogue_manager, user_info_dir)
    else:
        print(f"\n警告: 未找到目录 {user_info_dir}")
        print("请确保已创建该目录并放入用户信息文件")
    
    print("\n" + "="*60)
    print("知识库添加完成！")
    print("="*60)
    print("\n提示：")
    print("- 知识库已保存在向量数据库中")
    print("- 下次运行时会自动加载")
    print("- 可以运行 examples/basic_rag_chat.py 测试知识检索")
    print("- 可以运行 examples/comparison_experiment.py 进行对比实验")


if __name__ == "__main__":
    main()
