"""
系统评估器

提供完整的系统评估流程，整合所有评估指标：
- 技术性能评估
- 临床质量评估
- 记忆系统评估
- RAG效果评估
- 安全性评估
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import numpy as np

from ..metrics import (
    TechnicalMetrics,
    ClinicalMetrics,
    MemoryMetrics,
    RAGMetrics,
    SafetyMetrics
)

logger = logging.getLogger(__name__)


class SystemEvaluator:
    """系统评估器"""
    
    def __init__(
        self,
        dialogue_manager,
        llm_evaluator=None,
        output_dir: str = "./evaluation_results"
    ):
        """
        初始化
        
        Args:
            dialogue_manager: 对话管理器实例
            llm_evaluator: LLM评估器（用于临床质量评估）
            output_dir: 结果输出目录
        """
        self.dialogue_manager = dialogue_manager
        self.llm_evaluator = llm_evaluator
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 初始化各评估模块
        self.technical_metrics = TechnicalMetrics()
        self.clinical_metrics = ClinicalMetrics(llm_evaluator)
        self.memory_metrics = MemoryMetrics(dialogue_manager.memory_manager)
        self.rag_metrics = RAGMetrics(dialogue_manager.rag_manager)
        self.safety_metrics = SafetyMetrics(llm_evaluator)
    
    def evaluate_technical_performance(
        self,
        predictions: List[str],
        references: List[str],
        lang: str = "zh"
    ) -> Dict[str, float]:
        """
        评估技术性能
        
        Args:
            predictions: 预测结果列表
            references: 参考答案列表
            lang: 语言
            
        Returns:
            技术指标字典
        """
        logger.info("=" * 50)
        logger.info("Evaluating Technical Performance")
        logger.info("=" * 50)
        
        results = self.technical_metrics.compute_all_metrics(
            predictions, references, lang
        )
        
        # 打印结果
        logger.info("\nTechnical Metrics:")
        for key, value in results.items():
            logger.info(f"  {key}: {value:.4f}")
        
        return results
    
    def evaluate_clinical_quality(
        self,
        questions: List[str],
        responses: List[str],
        sample_size: Optional[int] = None
    ) -> Dict[str, float]:
        """
        评估临床质量
        
        Args:
            questions: 问题列表
            responses: 回复列表
            sample_size: 采样大小（None表示全部）
            
        Returns:
            临床质量指标字典
        """
        logger.info("=" * 50)
        logger.info("Evaluating Clinical Quality")
        logger.info("=" * 50)
        
        # 采样（临床评估成本较高）
        if sample_size and sample_size < len(questions):
            indices = np.random.choice(len(questions), sample_size, replace=False)
            questions = [questions[i] for i in indices]
            responses = [responses[i] for i in indices]
            logger.info(f"Sampling {sample_size} cases for clinical evaluation")
        
        results = self.clinical_metrics.evaluate_batch(questions, responses)
        
        # 打印结果
        logger.info("\nClinical Quality Metrics:")
        for key, value in results.items():
            logger.info(f"  {key}: {value:.4f}")
        
        return results
    
    def evaluate_memory_system(
        self,
        test_suite: Dict
    ) -> Dict[str, float]:
        """
        评估记忆系统
        
        Args:
            test_suite: 记忆测试套件
            
        Returns:
            记忆系统指标字典
        """
        logger.info("=" * 50)
        logger.info("Evaluating Memory System")
        logger.info("=" * 50)
        
        results = self.memory_metrics.run_comprehensive_memory_test(test_suite)
        
        # 打印结果
        logger.info("\nMemory System Metrics:")
        for key, value in results.items():
            if isinstance(value, float):
                logger.info(f"  {key}: {value:.4f}")
            else:
                logger.info(f"  {key}: {value}")
        
        return results
    
    def evaluate_rag_performance(
        self,
        test_suite: Dict
    ) -> Dict[str, float]:
        """
        评估RAG性能
        
        Args:
            test_suite: RAG测试套件
            
        Returns:
            RAG指标字典
        """
        logger.info("=" * 50)
        logger.info("Evaluating RAG Performance")
        logger.info("=" * 50)
        
        results = self.rag_metrics.run_comprehensive_rag_test(
            test_suite, self.llm_evaluator
        )
        
        # 打印结果
        logger.info("\nRAG Performance Metrics:")
        for key, value in results.items():
            if isinstance(value, float):
                logger.info(f"  {key}: {value:.4f}")
            else:
                logger.info(f"  {key}: {value}")
        
        return results
    
    def evaluate_safety(
        self,
        test_suite: Dict
    ) -> Dict[str, float]:
        """
        评估安全性
        
        Args:
            test_suite: 安全测试套件
            
        Returns:
            安全性指标字典
        """
        logger.info("=" * 50)
        logger.info("Evaluating Safety")
        logger.info("=" * 50)
        
        results = self.safety_metrics.run_comprehensive_safety_test(test_suite)
        
        # 打印结果
        logger.info("\nSafety Metrics:")
        for key, value in results.items():
            if isinstance(value, float):
                logger.info(f"  {key}: {value:.4f}")
            else:
                logger.info(f"  {key}: {value}")
        
        return results
    
    def run_full_evaluation(
        self,
        test_data: Dict,
        clinical_sample_size: int = 50
    ) -> Dict[str, any]:
        """
        运行完整评估
        
        Args:
            test_data: 测试数据，包含：
                - questions: 问题列表
                - reference_answers: 参考答案列表
                - memory_test_suite: 记忆测试套件
                - rag_test_suite: RAG测试套件
                - safety_test_suite: 安全测试套件
            clinical_sample_size: 临床评估采样大小
            
        Returns:
            完整评估结果
        """
        logger.info("=" * 70)
        logger.info(" STARTING FULL SYSTEM EVALUATION ")
        logger.info("=" * 70)
        logger.info(f"Evaluation Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 70)
        
        results = {
            "evaluation_time": datetime.now().isoformat(),
            "test_data_info": {
                "num_questions": len(test_data.get("questions", [])),
                "clinical_sample_size": clinical_sample_size
            }
        }
        
        # 1. 生成回复
        logger.info("\nStep 1: Generating responses...")
        questions = test_data.get("questions", [])
        predictions = []
        
        for i, question in enumerate(questions):
            if i % 10 == 0:
                logger.info(f"  Processing {i}/{len(questions)}...")
            
            try:
                response = self.dialogue_manager.chat(
                    user_id="eval_user",
                    message=question
                )
                predictions.append(response)
            except Exception as e:
                logger.error(f"Error generating response: {e}")
                predictions.append("")
        
        logger.info(f"Generated {len(predictions)} responses")
        
        # 2. 技术性能评估
        references = test_data.get("reference_answers", [])
        if references and len(references) == len(predictions):
            results["technical_metrics"] = self.evaluate_technical_performance(
                predictions, references
            )
        
        # 3. 临床质量评估
        if self.llm_evaluator:
            results["clinical_metrics"] = self.evaluate_clinical_quality(
                questions, predictions, clinical_sample_size
            )
        else:
            logger.warning("No LLM evaluator provided, skipping clinical evaluation")
        
        # 4. 记忆系统评估
        if "memory_test_suite" in test_data:
            results["memory_metrics"] = self.evaluate_memory_system(
                test_data["memory_test_suite"]
            )
        
        # 5. RAG性能评估
        if "rag_test_suite" in test_data:
            results["rag_metrics"] = self.evaluate_rag_performance(
                test_data["rag_test_suite"]
            )
        
        # 6. 安全性评估
        if "safety_test_suite" in test_data:
            # 添加生成的回复到安全测试中
            if "harmful_content_tests" not in test_data["safety_test_suite"]:
                test_data["safety_test_suite"]["harmful_content_tests"] = predictions
            
            results["safety_metrics"] = self.evaluate_safety(
                test_data["safety_test_suite"]
            )
        
        # 计算总体得分
        results["overall_score"] = self._compute_overall_score(results)
        
        # 保存结果
        self._save_results(results, predictions, questions)
        
        logger.info("=" * 70)
        logger.info(" EVALUATION COMPLETED ")
        logger.info("=" * 70)
        logger.info(f"\nOverall Score: {results['overall_score']:.4f}")
        logger.info(f"Results saved to: {self.output_dir}")
        
        return results
    
    def _compute_overall_score(self, results: Dict) -> float:
        """计算总体得分"""
        scores = []
        
        # 技术指标
        if "technical_metrics" in results:
            tech = results["technical_metrics"]
            if "bert_f1" in tech:
                scores.append(tech["bert_f1"])
        
        # 临床指标
        if "clinical_metrics" in results:
            clin = results["clinical_metrics"]
            if "overall_avg" in clin:
                scores.append(clin["overall_avg"] / 5.0)  # 归一化到0-1
        
        # 记忆指标
        if "memory_metrics" in results:
            mem = results["memory_metrics"]
            if "memory_recall_accuracy" in mem:
                scores.append(mem["memory_recall_accuracy"])
        
        # RAG指标
        if "rag_metrics" in results:
            rag = results["rag_metrics"]
            if "retrieval_f1" in rag:
                scores.append(rag["retrieval_f1"])
        
        # 安全指标
        if "safety_metrics" in results:
            safety = results["safety_metrics"]
            if "overall_safety_score" in safety:
                scores.append(safety["overall_safety_score"])
        
        return np.mean(scores) if scores else 0.0
    
    def _save_results(
        self,
        results: Dict,
        predictions: List[str],
        questions: List[str]
    ):
        """保存评估结果"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 保存完整结果
        results_file = self.output_dir / f"evaluation_results_{timestamp}.json"
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        # 保存预测结果
        predictions_file = self.output_dir / f"predictions_{timestamp}.json"
        with open(predictions_file, 'w', encoding='utf-8') as f:
            json.dump({
                "questions": questions,
                "predictions": predictions
            }, f, ensure_ascii=False, indent=2)
        
        # 生成简报
        self._generate_summary_report(results, timestamp)
    
    def _generate_summary_report(self, results: Dict, timestamp: str):
        """生成评估简报"""
        report_file = self.output_dir / f"evaluation_summary_{timestamp}.txt"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write(" EVALUATION SUMMARY REPORT \n")
            f.write("=" * 70 + "\n\n")
            f.write(f"Evaluation Time: {results['evaluation_time']}\n\n")
            
            # 技术指标
            if "technical_metrics" in results:
                f.write("Technical Performance:\n")
                f.write("-" * 40 + "\n")
                for key, value in results["technical_metrics"].items():
                    f.write(f"  {key}: {value:.4f}\n")
                f.write("\n")
            
            # 临床指标
            if "clinical_metrics" in results:
                f.write("Clinical Quality:\n")
                f.write("-" * 40 + "\n")
                for key, value in results["clinical_metrics"].items():
                    f.write(f"  {key}: {value:.4f}\n")
                f.write("\n")
            
            # 记忆指标
            if "memory_metrics" in results:
                f.write("Memory System:\n")
                f.write("-" * 40 + "\n")
                for key, value in results["memory_metrics"].items():
                    if isinstance(value, float):
                        f.write(f"  {key}: {value:.4f}\n")
                f.write("\n")
            
            # RAG指标
            if "rag_metrics" in results:
                f.write("RAG Performance:\n")
                f.write("-" * 40 + "\n")
                for key, value in results["rag_metrics"].items():
                    if isinstance(value, float):
                        f.write(f"  {key}: {value:.4f}\n")
                f.write("\n")
            
            # 安全指标
            if "safety_metrics" in results:
                f.write("Safety Metrics:\n")
                f.write("-" * 40 + "\n")
                for key, value in results["safety_metrics"].items():
                    if isinstance(value, float):
                        f.write(f"  {key}: {value:.4f}\n")
                f.write("\n")
            
            # 总体得分
            f.write("=" * 70 + "\n")
            f.write(f"OVERALL SCORE: {results['overall_score']:.4f}\n")
            f.write("=" * 70 + "\n")
