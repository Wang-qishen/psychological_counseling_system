"""
临床质量评估指标

基于MentalChat16K论文的7个临床维度：
1. Empathy (共情能力)
2. Supportiveness (支持性)
3. Guidance (指导性)
4. Reflectiveness (反思性)
5. Reassurance (安慰性)
6. Professionalism (专业性)
7. Information (信息量)

使用LLM作为评审员进行评分（1-5分制）
"""

import json
import logging
from typing import List, Dict, Optional
import numpy as np

logger = logging.getLogger(__name__)


class ClinicalMetrics:
    """临床质量指标计算器"""
    
    # 7个临床维度的定义
    DIMENSIONS = {
        "empathy": {
            "name": "共情能力 (Empathy)",
            "description": "理解和回应用户情感的能力",
            "prompt_template": """请评估以下心理咨询回复的共情能力（1-5分）：

用户问题: {question}
AI回复: {response}

评分标准：
1分：完全没有共情，忽视用户情感
2分：有限的共情，仅表面认可
3分：中等共情，能识别基本情感
4分：良好共情，深入理解情感
5分：卓越共情，准确捕捉并回应细微情感

请只输出一个1-5的数字分数，不要有其他内容。"""
        },
        "supportiveness": {
            "name": "支持性 (Supportiveness)",
            "description": "提供情感支持和鼓励的程度",
            "prompt_template": """请评估以下心理咨询回复的支持性（1-5分）：

用户问题: {question}
AI回复: {response}

评分标准：
1分：无支持，可能使用户感到孤立
2分：轻微支持，缺乏实质性鼓励
3分：中等支持，提供一些鼓励
4分：良好支持，给予充分的情感支持
5分：卓越支持，提供强大的情感支持和陪伴

请只输出一个1-5的数字分数，不要有其他内容。"""
        },
        "guidance": {
            "name": "指导性 (Guidance)",
            "description": "提供实用建议和解决方案的能力",
            "prompt_template": """请评估以下心理咨询回复的指导性（1-5分）：

用户问题: {question}
AI回复: {response}

评分标准：
1分：无指导，没有提供任何建议
2分：模糊指导，建议不具体
3分：中等指导，提供一些可行建议
4分：良好指导，建议具体且实用
5分：卓越指导，提供系统化、可操作的解决方案

请只输出一个1-5的数字分数，不要有其他内容。"""
        },
        "reflectiveness": {
            "name": "反思性 (Reflectiveness)",
            "description": "引导用户自我反思和洞察的能力",
            "prompt_template": """请评估以下心理咨询回复的反思性（1-5分）：

用户问题: {question}
AI回复: {response}

评分标准：
1分：无反思引导，直接给答案
2分：轻微反思，仅提出表面问题
3分：中等反思，引导用户思考
4分：良好反思，促进深层次思考
5分：卓越反思，帮助用户获得深刻洞察

请只输出一个1-5的数字分数，不要有其他内容。"""
        },
        "reassurance": {
            "name": "安慰性 (Reassurance)",
            "description": "缓解焦虑和提供心理安慰的能力",
            "prompt_template": """请评估以下心理咨询回复的安慰性（1-5分）：

用户问题: {question}
AI回复: {response}

评分标准：
1分：无安慰，可能加重焦虑
2分：轻微安慰，效果有限
3分：中等安慰，能缓解部分焦虑
4分：良好安慰，有效缓解焦虑
5分：卓越安慰，显著减轻心理负担

请只输出一个1-5的数字分数，不要有其他内容。"""
        },
        "professionalism": {
            "name": "专业性 (Professionalism)",
            "description": "心理咨询的专业水平和准确性",
            "prompt_template": """请评估以下心理咨询回复的专业性（1-5分）：

用户问题: {question}
AI回复: {response}

评分标准：
1分：不专业，有明显错误
2分：勉强专业，知识不够准确
3分：中等专业，基本符合专业标准
4分：良好专业，展现专业知识和技巧
5分：卓越专业，高水平的专业咨询

请只输出一个1-5的数字分数，不要有其他内容。"""
        },
        "information": {
            "name": "信息量 (Information)",
            "description": "提供有价值信息的丰富程度",
            "prompt_template": """请评估以下心理咨询回复的信息量（1-5分）：

用户问题: {question}
AI回复: {response}

评分标准：
1分：几乎无信息，空洞无内容
2分：信息量少，内容单薄
3分：中等信息量，提供基本信息
4分：信息丰富，内容充实
5分：信息量大，内容深入全面

请只输出一个1-5的数字分数，不要有其他内容。"""
        }
    }
    
    def __init__(self, llm_evaluator=None):
        """
        初始化
        
        Args:
            llm_evaluator: LLM评估器（需要实现generate方法）
        """
        self.llm_evaluator = llm_evaluator
    
    def evaluate_single_dimension(
        self,
        dimension: str,
        question: str,
        response: str
    ) -> Optional[float]:
        """
        评估单个维度
        
        Args:
            dimension: 维度名称（empathy, supportiveness等）
            question: 用户问题
            response: AI回复
            
        Returns:
            1-5的评分，失败返回None
        """
        if dimension not in self.DIMENSIONS:
            logger.error(f"Unknown dimension: {dimension}")
            return None
        
        if self.llm_evaluator is None:
            logger.error("LLM evaluator not set")
            return None
        
        # 生成评估prompt
        prompt = self.DIMENSIONS[dimension]["prompt_template"].format(
            question=question,
            response=response
        )
        
        try:
            # 调用LLM评估
            result = self.llm_evaluator.generate(prompt)
            
            # 提取分数（尝试从结果中解析数字）
            score = self._extract_score(result)
            
            if score is None:
                logger.warning(f"Failed to extract score from: {result}")
                return None
            
            # 确保分数在1-5范围内
            score = max(1.0, min(5.0, score))
            
            return score
            
        except Exception as e:
            logger.error(f"Error evaluating dimension {dimension}: {e}")
            return None
    
    def _extract_score(self, text: str) -> Optional[float]:
        """从文本中提取分数"""
        import re
        
        # 移除空白字符
        text = text.strip()
        
        # 尝试直接转换
        try:
            score = float(text)
            if 1 <= score <= 5:
                return score
        except ValueError:
            pass
        
        # 尝试正则提取
        patterns = [
            r'(\d+\.?\d*)分',  # "4.5分"
            r'(\d+\.?\d*)/5',  # "4/5"
            r'评分[:：]\s*(\d+\.?\d*)',  # "评分: 4"
            r'^(\d+\.?\d*)$',  # 纯数字
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                try:
                    score = float(match.group(1))
                    if 1 <= score <= 5:
                        return score
                except ValueError:
                    continue
        
        return None
    
    def evaluate_all_dimensions(
        self,
        question: str,
        response: str
    ) -> Dict[str, float]:
        """
        评估所有7个维度
        
        Args:
            question: 用户问题
            response: AI回复
            
        Returns:
            所有维度的评分字典
        """
        results = {}
        
        for dimension in self.DIMENSIONS.keys():
            logger.info(f"Evaluating {dimension}...")
            score = self.evaluate_single_dimension(dimension, question, response)
            if score is not None:
                results[dimension] = score
        
        return results
    
    def evaluate_batch(
        self,
        questions: List[str],
        responses: List[str],
        dimensions: Optional[List[str]] = None
    ) -> Dict[str, float]:
        """
        批量评估（返回平均分）
        
        Args:
            questions: 用户问题列表
            responses: AI回复列表
            dimensions: 要评估的维度列表（None表示全部）
            
        Returns:
            各维度的平均分字典
        """
        if len(questions) != len(responses):
            raise ValueError("questions and responses must have same length")
        
        if dimensions is None:
            dimensions = list(self.DIMENSIONS.keys())
        
        # 初始化结果存储
        dimension_scores = {dim: [] for dim in dimensions}
        
        # 遍历所有样本
        for i, (question, response) in enumerate(zip(questions, responses)):
            logger.info(f"Evaluating sample {i+1}/{len(questions)}...")
            
            for dimension in dimensions:
                score = self.evaluate_single_dimension(dimension, question, response)
                if score is not None:
                    dimension_scores[dimension].append(score)
        
        # 计算平均分
        avg_scores = {}
        for dimension, scores in dimension_scores.items():
            if scores:
                avg_scores[f"{dimension}_avg"] = np.mean(scores)
                avg_scores[f"{dimension}_std"] = np.std(scores)
            else:
                avg_scores[f"{dimension}_avg"] = 0.0
                avg_scores[f"{dimension}_std"] = 0.0
        
        # 计算总体平均分
        valid_avgs = [v for k, v in avg_scores.items() if k.endswith('_avg') and v > 0]
        if valid_avgs:
            avg_scores["overall_avg"] = np.mean(valid_avgs)
        else:
            avg_scores["overall_avg"] = 0.0
        
        return avg_scores


def evaluate_clinical_quality(
    questions: List[str],
    responses: List[str],
    llm_evaluator,
    dimensions: Optional[List[str]] = None
) -> Dict[str, float]:
    """
    便捷函数：评估临床质量
    
    Args:
        questions: 用户问题列表
        responses: AI回复列表
        llm_evaluator: LLM评估器
        dimensions: 要评估的维度列表
        
    Returns:
        评估结果字典
    """
    metrics = ClinicalMetrics(llm_evaluator)
    return metrics.evaluate_batch(questions, responses, dimensions)
