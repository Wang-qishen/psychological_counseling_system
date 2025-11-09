"""
RAG (检索增强生成) 效果评估指标

关键指标：
1. Retrieval Precision: 检索精确率
2. Retrieval Recall: 检索召回率
3. Retrieval F1: 检索F1分数
4. Answer Relevance: 答案相关性
5. Faithfulness: 忠实度（答案是否基于检索内容）
6. Context Utilization: 上下文利用率
"""

import logging
from typing import List, Dict, Optional, Tuple
import numpy as np

logger = logging.getLogger(__name__)


class RAGMetrics:
    """RAG效果指标计算器"""
    
    def __init__(self, rag_manager=None):
        """
        初始化
        
        Args:
            rag_manager: RAG管理器实例
        """
        self.rag_manager = rag_manager
    
    def compute_retrieval_metrics(
        self,
        queries: List[str],
        retrieved_docs: List[List[str]],
        relevant_docs: List[List[str]],
        k: int = 5
    ) -> Dict[str, float]:
        """
        计算检索指标（Precision, Recall, F1）
        
        Args:
            queries: 查询列表
            retrieved_docs: 检索到的文档列表（每个查询对应一个文档列表）
            relevant_docs: 相关文档列表（每个查询对应一个文档列表）
            k: 考虑前k个检索结果
            
        Returns:
            检索指标字典
        """
        if len(queries) != len(retrieved_docs) or len(queries) != len(relevant_docs):
            raise ValueError("All input lists must have same length")
        
        precisions = []
        recalls = []
        f1_scores = []
        
        for i, (query, retrieved, relevant) in enumerate(
            zip(queries, retrieved_docs, relevant_docs)
        ):
            # 只考虑前k个检索结果
            retrieved_k = set(retrieved[:k])
            relevant_set = set(relevant)
            
            if not retrieved_k:
                precisions.append(0.0)
                recalls.append(0.0)
                f1_scores.append(0.0)
                continue
            
            # 计算交集
            intersection = retrieved_k & relevant_set
            
            # Precision: 检索到的文档中有多少是相关的
            precision = len(intersection) / len(retrieved_k) if retrieved_k else 0.0
            
            # Recall: 相关文档中有多少被检索到
            recall = len(intersection) / len(relevant_set) if relevant_set else 0.0
            
            # F1 Score
            if precision + recall > 0:
                f1 = 2 * (precision * recall) / (precision + recall)
            else:
                f1 = 0.0
            
            precisions.append(precision)
            recalls.append(recall)
            f1_scores.append(f1)
        
        return {
            "retrieval_precision": np.mean(precisions) if precisions else 0.0,
            "retrieval_recall": np.mean(recalls) if recalls else 0.0,
            "retrieval_f1": np.mean(f1_scores) if f1_scores else 0.0,
            "precision_std": np.std(precisions) if precisions else 0.0,
            "recall_std": np.std(recalls) if recalls else 0.0
        }
    
    def compute_answer_relevance(
        self,
        queries: List[str],
        answers: List[str],
        llm_evaluator=None
    ) -> Dict[str, float]:
        """
        计算答案相关性（使用LLM评估）
        
        Args:
            queries: 查询列表
            answers: 答案列表
            llm_evaluator: LLM评估器
            
        Returns:
            相关性得分
        """
        if len(queries) != len(answers):
            raise ValueError("queries and answers must have same length")
        
        if llm_evaluator is None:
            logger.warning("No LLM evaluator provided, using simple similarity")
            return self._compute_simple_relevance(queries, answers)
        
        relevance_scores = []
        
        for query, answer in zip(queries, answers):
            prompt = f"""请评估以下答案与问题的相关性（0-1分，保留2位小数）：

问题: {query}
答案: {answer}

评分标准：
0.0: 完全不相关
0.5: 部分相关
1.0: 高度相关

请只输出一个0-1之间的数字，不要有其他内容。"""
            
            try:
                result = llm_evaluator.generate(prompt)
                score = float(result.strip())
                score = max(0.0, min(1.0, score))
                relevance_scores.append(score)
            except Exception as e:
                logger.error(f"Error evaluating relevance: {e}")
                relevance_scores.append(0.5)
        
        return {
            "answer_relevance": np.mean(relevance_scores) if relevance_scores else 0.0,
            "relevance_std": np.std(relevance_scores) if relevance_scores else 0.0
        }
    
    def _compute_simple_relevance(
        self,
        queries: List[str],
        answers: List[str]
    ) -> Dict[str, float]:
        """计算简单相关性（基于关键词重叠）"""
        scores = []
        
        for query, answer in zip(queries, answers):
            query_tokens = set(query.split())
            answer_tokens = set(answer.split())
            
            if not query_tokens:
                scores.append(0.0)
                continue
            
            intersection = query_tokens & answer_tokens
            score = len(intersection) / len(query_tokens)
            scores.append(score)
        
        return {
            "answer_relevance": np.mean(scores) if scores else 0.0,
            "relevance_std": np.std(scores) if scores else 0.0
        }
    
    def compute_faithfulness(
        self,
        answers: List[str],
        retrieved_contexts: List[str],
        llm_evaluator=None
    ) -> Dict[str, float]:
        """
        计算忠实度（答案是否基于检索到的上下文）
        
        Args:
            answers: 答案列表
            retrieved_contexts: 检索到的上下文列表
            llm_evaluator: LLM评估器
            
        Returns:
            忠实度得分
        """
        if len(answers) != len(retrieved_contexts):
            raise ValueError("answers and contexts must have same length")
        
        if llm_evaluator is None:
            logger.warning("No LLM evaluator provided, using simple overlap")
            return self._compute_simple_faithfulness(answers, retrieved_contexts)
        
        faithfulness_scores = []
        
        for answer, context in zip(answers, retrieved_contexts):
            prompt = f"""请评估答案是否基于给定的上下文（0-1分，保留2位小数）：

上下文: {context}
答案: {answer}

评分标准：
0.0: 答案完全脱离上下文
0.5: 答案部分基于上下文
1.0: 答案完全基于上下文

请只输出一个0-1之间的数字，不要有其他内容。"""
            
            try:
                result = llm_evaluator.generate(prompt)
                score = float(result.strip())
                score = max(0.0, min(1.0, score))
                faithfulness_scores.append(score)
            except Exception as e:
                logger.error(f"Error evaluating faithfulness: {e}")
                faithfulness_scores.append(0.5)
        
        return {
            "faithfulness": np.mean(faithfulness_scores) if faithfulness_scores else 0.0,
            "faithfulness_std": np.std(faithfulness_scores) if faithfulness_scores else 0.0
        }
    
    def _compute_simple_faithfulness(
        self,
        answers: List[str],
        contexts: List[str]
    ) -> Dict[str, float]:
        """计算简单忠实度（基于文本重叠）"""
        scores = []
        
        for answer, context in zip(answers, contexts):
            answer_tokens = set(answer.split())
            context_tokens = set(context.split())
            
            if not answer_tokens:
                scores.append(0.0)
                continue
            
            intersection = answer_tokens & context_tokens
            score = len(intersection) / len(answer_tokens)
            scores.append(score)
        
        return {
            "faithfulness": np.mean(scores) if scores else 0.0,
            "faithfulness_std": np.std(scores) if scores else 0.0
        }
    
    def compute_context_utilization(
        self,
        answers_with_rag: List[str],
        answers_without_rag: List[str]
    ) -> Dict[str, float]:
        """
        计算上下文利用率（RAG vs 无RAG）
        
        Args:
            answers_with_rag: 使用RAG的答案列表
            answers_without_rag: 不使用RAG的答案列表
            
        Returns:
            利用率指标
        """
        if len(answers_with_rag) != len(answers_without_rag):
            raise ValueError("Answer lists must have same length")
        
        # 计算差异度
        diff_scores = []
        for ans_with, ans_without in zip(answers_with_rag, answers_without_rag):
            tokens_with = set(ans_with.split())
            tokens_without = set(ans_without.split())
            
            # 新增的内容比例
            new_tokens = tokens_with - tokens_without
            if tokens_with:
                diff = len(new_tokens) / len(tokens_with)
                diff_scores.append(diff)
        
        # 计算长度增加
        len_with = [len(a) for a in answers_with_rag]
        len_without = [len(a) for a in answers_without_rag]
        
        len_increase = (
            np.mean(len_with) - np.mean(len_without)
        ) / np.mean(len_without) if np.mean(len_without) > 0 else 0.0
        
        return {
            "context_utilization": np.mean(diff_scores) if diff_scores else 0.0,
            "length_increase": len_increase,
            "avg_length_with_rag": np.mean(len_with) if len_with else 0.0,
            "avg_length_without_rag": np.mean(len_without) if len_without else 0.0
        }
    
    def evaluate_rag_quality(
        self,
        query: str,
        top_k: int = 5
    ) -> Dict[str, any]:
        """
        评估单次RAG检索质量
        
        Args:
            query: 查询
            top_k: 返回top k个结果
            
        Returns:
            检索质量分析
        """
        if self.rag_manager is None:
            logger.error("RAG manager not set")
            return {}
        
        try:
            # 执行检索
            results = self.rag_manager.retrieve(query, top_k=top_k)
            
            # 分析检索结果
            if not results:
                return {
                    "retrieved_count": 0,
                    "avg_score": 0.0,
                    "quality": "poor"
                }
            
            scores = [r.get("score", 0.0) for r in results]
            
            return {
                "retrieved_count": len(results),
                "avg_score": np.mean(scores) if scores else 0.0,
                "min_score": np.min(scores) if scores else 0.0,
                "max_score": np.max(scores) if scores else 0.0,
                "score_std": np.std(scores) if scores else 0.0,
                "quality": self._assess_quality(np.mean(scores) if scores else 0.0)
            }
        except Exception as e:
            logger.error(f"Error evaluating RAG quality: {e}")
            return {}
    
    def _assess_quality(self, avg_score: float) -> str:
        """评估检索质量等级"""
        if avg_score >= 0.8:
            return "excellent"
        elif avg_score >= 0.6:
            return "good"
        elif avg_score >= 0.4:
            return "fair"
        else:
            return "poor"
    
    def run_comprehensive_rag_test(
        self,
        test_suite: Dict,
        llm_evaluator=None
    ) -> Dict[str, float]:
        """
        运行综合RAG测试
        
        Args:
            test_suite: 测试套件，包含：
                - retrieval_tests: 检索测试用例
                - relevance_tests: 相关性测试用例
                - faithfulness_tests: 忠实度测试用例
                - utilization_tests: 利用率测试用例
            llm_evaluator: LLM评估器
            
        Returns:
            综合评估结果
        """
        results = {}
        
        # 1. 检索指标测试
        if "retrieval_tests" in test_suite:
            logger.info("Running retrieval metrics tests...")
            retrieval_results = self.compute_retrieval_metrics(
                test_suite["retrieval_tests"]["queries"],
                test_suite["retrieval_tests"]["retrieved_docs"],
                test_suite["retrieval_tests"]["relevant_docs"],
                test_suite["retrieval_tests"].get("k", 5)
            )
            results.update(retrieval_results)
        
        # 2. 答案相关性测试
        if "relevance_tests" in test_suite:
            logger.info("Running answer relevance tests...")
            relevance_results = self.compute_answer_relevance(
                test_suite["relevance_tests"]["queries"],
                test_suite["relevance_tests"]["answers"],
                llm_evaluator
            )
            results.update(relevance_results)
        
        # 3. 忠实度测试
        if "faithfulness_tests" in test_suite:
            logger.info("Running faithfulness tests...")
            faithfulness_results = self.compute_faithfulness(
                test_suite["faithfulness_tests"]["answers"],
                test_suite["faithfulness_tests"]["contexts"],
                llm_evaluator
            )
            results.update(faithfulness_results)
        
        # 4. 上下文利用率测试
        if "utilization_tests" in test_suite:
            logger.info("Running context utilization tests...")
            utilization_results = self.compute_context_utilization(
                test_suite["utilization_tests"]["with_rag"],
                test_suite["utilization_tests"]["without_rag"]
            )
            results.update(utilization_results)
        
        return results


def evaluate_rag_performance(
    rag_manager,
    test_suite: Dict,
    llm_evaluator=None
) -> Dict[str, float]:
    """
    便捷函数：评估RAG性能
    
    Args:
        rag_manager: RAG管理器
        test_suite: 测试套件
        llm_evaluator: LLM评估器
        
    Returns:
        评估结果
    """
    metrics = RAGMetrics(rag_manager)
    return metrics.run_comprehensive_rag_test(test_suite, llm_evaluator)
