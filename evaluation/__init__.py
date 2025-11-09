"""
心理咨询系统测评模块

提供完整的评估框架，包括：
- 技术性能评估（BERT Score、ROUGE、BLEU等）
- 专业质量评估（共情、支持、指导等7个临床指标）
- 安全性评估（有害内容检测、隐私保护等）
- 用户体验评估（响应时间、满意度）
- 临床效果评估（情绪改善、问题解决）
- 系统特色评估（RAG效果、记忆系统性能）

使用方法：
    from evaluation import EvaluationFramework
    
    evaluator = EvaluationFramework(config)
    results = evaluator.run_full_evaluation()
"""

from .framework import EvaluationFramework
from .metrics import *
from .evaluators import *

__version__ = "1.0.0"
__all__ = ["EvaluationFramework"]
