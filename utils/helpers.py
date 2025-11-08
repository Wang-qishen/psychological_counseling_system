"""
工具函数
"""

import yaml
import os
from typing import Dict, Any


def load_config(config_path: str = './configs/config.yaml') -> Dict[str, Any]:
    """
    加载配置文件
    
    Args:
        config_path: 配置文件路径
        
    Returns:
        配置字典
    """
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    return config


def setup_directories(config: Dict[str, Any]) -> None:
    """
    创建必要的目录
    
    Args:
        config: 配置字典
    """
    paths = config.get('paths', {})
    
    dirs_to_create = [
        paths.get('data_dir', './data'),
        paths.get('logs_dir', './logs'),
        paths.get('cache_dir', './cache'),
        config['knowledge']['psychological_kb']['path'],
        config['knowledge']['user_kb']['path'],
        config['memory']['storage']['path'],
        config['rag']['vector_store']['persist_directory']
    ]
    
    for dir_path in dirs_to_create:
        os.makedirs(dir_path, exist_ok=True)
    
    print("Directories created successfully")


def format_dialogue_history(turns: list) -> str:
    """
    格式化对话历史为可读文本
    
    Args:
        turns: Turn对象列表
        
    Returns:
        格式化的文本
    """
    lines = []
    for i, turn in enumerate(turns, 1):
        lines.append(f"=== 第 {i} 轮 ===")
        lines.append(f"用户: {turn.user_message}")
        lines.append(f"咨询师: {turn.assistant_message}")
        if turn.emotion:
            emotion_str = ", ".join([f"{k}:{v:.2f}" for k, v in turn.emotion.items()])
            lines.append(f"情绪: {emotion_str}")
        lines.append("")
    
    return "\n".join(lines)
