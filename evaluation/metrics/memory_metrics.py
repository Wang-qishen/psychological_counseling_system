"""
记忆系统评估指标

评估三层记忆架构的性能：
1. 短期记忆 (Short-term Memory)
2. 工作记忆 (Working Memory)  
3. 长期记忆 (Long-term Memory)

关键指标：
- Memory Recall Accuracy: 记忆召回准确率
- Memory Consistency: 记忆一致性
- Personalization Score: 个性化得分
- Context Utilization: 上下文利用率
"""

import logging
from typing import List, Dict, Optional, Tuple
import numpy as np
from datetime import datetime

logger = logging.getLogger(__name__)


class MemoryMetrics:
    """记忆系统指标计算器"""
    
    def __init__(self, memory_manager=None):
        """
        初始化
        
        Args:
            memory_manager: 记忆管理器实例
        """
        self.memory_manager = memory_manager
    
    def test_memory_recall(
        self,
        test_cases: List[Dict]
    ) -> Dict[str, float]:
        """
        测试记忆召回能力
        
        Args:
            test_cases: 测试用例列表，每个包含：
                - user_id: 用户ID
                - query: 查询内容
                - expected_info: 期望召回的信息
                - memory_type: 记忆类型（short/working/long）
                
        Returns:
            召回准确率等指标
        """
        if self.memory_manager is None:
            logger.error("Memory manager not set")
            return {}
        
        total = len(test_cases)
        correct_recalls = 0
        recall_scores = []
        
        for case in test_cases:
            user_id = case.get("user_id")
            query = case.get("query")
            expected = case.get("expected_info", "")
            memory_type = case.get("memory_type", "all")
            
            # 获取记忆内容
            if memory_type == "short":
                memory_content = self.memory_manager.get_short_term_context(user_id)
            elif memory_type == "working":
                memory_content = self.memory_manager.get_working_memory_context(user_id)
            elif memory_type == "long":
                memory_content = self.memory_manager.get_long_term_context(user_id)
            else:
                memory_content = self.memory_manager.get_full_context(user_id)
            
            # 检查期望信息是否被召回
            if expected in memory_content:
                correct_recalls += 1
                recall_scores.append(1.0)
            else:
                # 计算部分匹配得分
                partial_score = self._compute_partial_match(expected, memory_content)
                recall_scores.append(partial_score)
                if partial_score > 0.7:
                    correct_recalls += 1
        
        accuracy = correct_recalls / total if total > 0 else 0.0
        avg_score = np.mean(recall_scores) if recall_scores else 0.0
        
        return {
            "memory_recall_accuracy": accuracy,
            "memory_recall_score": avg_score,
            "total_tests": total,
            "correct_recalls": correct_recalls
        }
    
    def _compute_partial_match(self, expected: str, actual: str) -> float:
        """计算部分匹配得分"""
        if not expected or not actual:
            return 0.0
        
        # 简单的字符串包含检查
        expected_tokens = set(expected.split())
        actual_tokens = set(actual.split())
        
        if not expected_tokens:
            return 0.0
        
        intersection = expected_tokens & actual_tokens
        return len(intersection) / len(expected_tokens)
    
    def test_memory_consistency(
        self,
        user_id: str,
        session_count: int = 3
    ) -> Dict[str, float]:
        """
        测试记忆一致性（跨会话）
        
        Args:
            user_id: 用户ID
            session_count: 测试会话数
            
        Returns:
            一致性指标
        """
        if self.memory_manager is None:
            logger.error("Memory manager not set")
            return {}
        
        # 获取多个时间点的记忆快照
        snapshots = []
        for _ in range(session_count):
            context = self.memory_manager.get_full_context(user_id)
            snapshots.append(context)
        
        # 计算相似度
        if len(snapshots) < 2:
            return {"consistency_score": 1.0}
        
        similarities = []
        for i in range(len(snapshots) - 1):
            sim = self._compute_text_similarity(snapshots[i], snapshots[i+1])
            similarities.append(sim)
        
        avg_consistency = np.mean(similarities) if similarities else 0.0
        
        return {
            "consistency_score": avg_consistency,
            "snapshot_count": len(snapshots)
        }
    
    def _compute_text_similarity(self, text1: str, text2: str) -> float:
        """计算文本相似度（简单实现）"""
        if not text1 or not text2:
            return 0.0
        
        tokens1 = set(text1.split())
        tokens2 = set(text2.split())
        
        if not tokens1 or not tokens2:
            return 0.0
        
        intersection = tokens1 & tokens2
        union = tokens1 | tokens2
        
        return len(intersection) / len(union) if union else 0.0
    
    def test_personalization(
        self,
        user_id: str,
        generic_response: str,
        personalized_response: str,
        ground_truth: Optional[str] = None
    ) -> Dict[str, float]:
        """
        测试个性化效果
        
        Args:
            user_id: 用户ID
            generic_response: 通用回复（无记忆）
            personalized_response: 个性化回复（有记忆）
            ground_truth: 真实标准答案（可选）
            
        Returns:
            个性化提升指标
        """
        # 计算差异度
        difference_score = 1.0 - self._compute_text_similarity(
            generic_response, 
            personalized_response
        )
        
        results = {
            "personalization_difference": difference_score
        }
        
        # 如果有ground truth，计算准确性提升
        if ground_truth:
            generic_sim = self._compute_text_similarity(generic_response, ground_truth)
            personalized_sim = self._compute_text_similarity(personalized_response, ground_truth)
            improvement = personalized_sim - generic_sim
            
            results["personalization_improvement"] = improvement
            results["generic_similarity"] = generic_sim
            results["personalized_similarity"] = personalized_sim
        
        return results
    
    def test_context_utilization(
        self,
        responses_with_context: List[str],
        responses_without_context: List[str],
        evaluation_criteria: Optional[str] = "relevance"
    ) -> Dict[str, float]:
        """
        测试上下文利用率
        
        Args:
            responses_with_context: 使用上下文的回复列表
            responses_without_context: 不使用上下文的回复列表
            evaluation_criteria: 评估标准
            
        Returns:
            上下文利用指标
        """
        if len(responses_with_context) != len(responses_without_context):
            raise ValueError("Response lists must have same length")
        
        # 计算长度差异（使用上下文的回复通常更长更详细）
        len_with = [len(r) for r in responses_with_context]
        len_without = [len(r) for r in responses_without_context]
        
        avg_len_improvement = (
            np.mean(len_with) - np.mean(len_without)
        ) / np.mean(len_without) if np.mean(len_without) > 0 else 0.0
        
        # 计算差异度（使用上下文的回复应该更个性化）
        diff_scores = []
        for r_with, r_without in zip(responses_with_context, responses_without_context):
            diff = 1.0 - self._compute_text_similarity(r_with, r_without)
            diff_scores.append(diff)
        
        return {
            "context_utilization_score": np.mean(diff_scores) if diff_scores else 0.0,
            "length_improvement": avg_len_improvement,
            "avg_length_with_context": np.mean(len_with) if len_with else 0.0,
            "avg_length_without_context": np.mean(len_without) if len_without else 0.0
        }
    
    def evaluate_memory_efficiency(
        self,
        user_id: str
    ) -> Dict[str, float]:
        """
        评估记忆系统效率
        
        Args:
            user_id: 用户ID
            
        Returns:
            效率指标
        """
        if self.memory_manager is None:
            logger.error("Memory manager not set")
            return {}
        
        # 获取记忆统计
        short_term = self.memory_manager.get_short_term_context(user_id)
        working = self.memory_manager.get_working_memory_context(user_id)
        long_term = self.memory_manager.get_long_term_context(user_id)
        
        return {
            "short_term_size": len(short_term),
            "working_memory_size": len(working),
            "long_term_size": len(long_term),
            "total_memory_size": len(short_term) + len(working) + len(long_term)
        }
    
    def run_comprehensive_memory_test(
        self,
        test_suite: Dict
    ) -> Dict[str, float]:
        """
        运行综合记忆测试
        
        Args:
            test_suite: 测试套件，包含：
                - recall_tests: 召回测试用例
                - consistency_tests: 一致性测试配置
                - personalization_tests: 个性化测试用例
                - context_tests: 上下文测试用例
                
        Returns:
            综合评估结果
        """
        results = {}
        
        # 1. 记忆召回测试
        if "recall_tests" in test_suite:
            logger.info("Running memory recall tests...")
            recall_results = self.test_memory_recall(test_suite["recall_tests"])
            results.update(recall_results)
        
        # 2. 记忆一致性测试
        if "consistency_tests" in test_suite:
            logger.info("Running memory consistency tests...")
            for test_config in test_suite["consistency_tests"]:
                user_id = test_config.get("user_id")
                session_count = test_config.get("session_count", 3)
                consistency_results = self.test_memory_consistency(user_id, session_count)
                results.update({
                    f"consistency_{user_id}": consistency_results["consistency_score"]
                })
        
        # 3. 个性化测试
        if "personalization_tests" in test_suite:
            logger.info("Running personalization tests...")
            personalization_scores = []
            for test_case in test_suite["personalization_tests"]:
                p_results = self.test_personalization(**test_case)
                personalization_scores.append(p_results.get("personalization_difference", 0))
            if personalization_scores:
                results["avg_personalization_score"] = np.mean(personalization_scores)
        
        # 4. 上下文利用测试
        if "context_tests" in test_suite:
            logger.info("Running context utilization tests...")
            context_results = self.test_context_utilization(
                test_suite["context_tests"]["with_context"],
                test_suite["context_tests"]["without_context"]
            )
            results.update(context_results)
        
        return results


def evaluate_memory_system(
    memory_manager,
    test_suite: Dict
) -> Dict[str, float]:
    """
    便捷函数：评估记忆系统
    
    Args:
        memory_manager: 记忆管理器
        test_suite: 测试套件
        
    Returns:
        评估结果
    """
    metrics = MemoryMetrics(memory_manager)
    return metrics.run_comprehensive_memory_test(test_suite)
