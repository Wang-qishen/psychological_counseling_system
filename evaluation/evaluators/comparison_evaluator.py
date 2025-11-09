"""
对比评估器

用于对比不同系统配置的性能：
- 裸LLM（Bare LLM）
- LLM + RAG
- 完整系统（LLM + RAG + Memory）

这是验证记忆系统和RAG效果的关键实验
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import numpy as np

from ..metrics import TechnicalMetrics, ClinicalMetrics

logger = logging.getLogger(__name__)


class ComparisonEvaluator:
    """对比评估器"""
    
    def __init__(
        self,
        output_dir: str = "./evaluation_results/comparisons"
    ):
        """
        初始化
        
        Args:
            output_dir: 结果输出目录
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.technical_metrics = TechnicalMetrics()
    
    def compare_systems(
        self,
        questions: List[str],
        reference_answers: List[str],
        bare_llm_responses: List[str],
        llm_rag_responses: List[str],
        full_system_responses: List[str],
        llm_evaluator=None
    ) -> Dict[str, any]:
        """
        对比三种系统配置
        
        Args:
            questions: 问题列表
            reference_answers: 参考答案列表
            bare_llm_responses: 裸LLM的回复
            llm_rag_responses: LLM+RAG的回复
            full_system_responses: 完整系统的回复
            llm_evaluator: LLM评估器（用于临床评估）
            
        Returns:
            对比结果字典
        """
        logger.info("=" * 70)
        logger.info(" SYSTEM COMPARISON EVALUATION ")
        logger.info("=" * 70)
        
        results = {
            "evaluation_time": datetime.now().isoformat(),
            "num_samples": len(questions),
            "systems": {}
        }
        
        # 1. 评估裸LLM
        logger.info("\n1. Evaluating Bare LLM...")
        results["systems"]["bare_llm"] = self._evaluate_single_system(
            "Bare LLM",
            questions,
            reference_answers,
            bare_llm_responses,
            llm_evaluator
        )
        
        # 2. 评估LLM+RAG
        logger.info("\n2. Evaluating LLM + RAG...")
        results["systems"]["llm_rag"] = self._evaluate_single_system(
            "LLM + RAG",
            questions,
            reference_answers,
            llm_rag_responses,
            llm_evaluator
        )
        
        # 3. 评估完整系统
        logger.info("\n3. Evaluating Full System...")
        results["systems"]["full_system"] = self._evaluate_single_system(
            "Full System (LLM + RAG + Memory)",
            questions,
            reference_answers,
            full_system_responses,
            llm_evaluator
        )
        
        # 4. 计算提升
        results["improvements"] = self._calculate_improvements(results["systems"])
        
        # 5. 保存结果
        self._save_comparison_results(results)
        
        # 6. 打印总结
        self._print_comparison_summary(results)
        
        logger.info("=" * 70)
        logger.info(" COMPARISON COMPLETED ")
        logger.info("=" * 70)
        
        return results
    
    def _evaluate_single_system(
        self,
        system_name: str,
        questions: List[str],
        references: List[str],
        predictions: List[str],
        llm_evaluator=None
    ) -> Dict[str, float]:
        """评估单个系统"""
        logger.info(f"\nEvaluating: {system_name}")
        logger.info("-" * 50)
        
        results = {}
        
        # 技术指标
        tech_metrics = self.technical_metrics.compute_all_metrics(
            predictions, references
        )
        results["technical"] = tech_metrics
        
        logger.info("Technical Metrics:")
        for key, value in tech_metrics.items():
            logger.info(f"  {key}: {value:.4f}")
        
        # 临床指标（采样评估）
        if llm_evaluator:
            sample_size = min(30, len(questions))
            indices = np.random.choice(len(questions), sample_size, replace=False)
            
            sampled_questions = [questions[i] for i in indices]
            sampled_responses = [predictions[i] for i in indices]
            
            clinical_metrics = ClinicalMetrics(llm_evaluator)
            clin_results = clinical_metrics.evaluate_batch(
                sampled_questions,
                sampled_responses
            )
            results["clinical"] = clin_results
            
            logger.info("\nClinical Metrics (sampled):")
            logger.info(f"  overall_avg: {clin_results.get('overall_avg', 0):.4f}")
        
        return results
    
    def _calculate_improvements(
        self,
        systems: Dict[str, Dict]
    ) -> Dict[str, Dict[str, float]]:
        """计算性能提升"""
        improvements = {}
        
        bare_llm = systems.get("bare_llm", {})
        llm_rag = systems.get("llm_rag", {})
        full_system = systems.get("full_system", {})
        
        # RAG的提升（相对于裸LLM）
        improvements["rag_improvement"] = self._compute_relative_improvement(
            bare_llm, llm_rag, "RAG vs Bare LLM"
        )
        
        # 记忆系统的提升（相对于LLM+RAG）
        improvements["memory_improvement"] = self._compute_relative_improvement(
            llm_rag, full_system, "Memory vs LLM+RAG"
        )
        
        # 完整系统的提升（相对于裸LLM）
        improvements["full_system_improvement"] = self._compute_relative_improvement(
            bare_llm, full_system, "Full System vs Bare LLM"
        )
        
        return improvements
    
    def _compute_relative_improvement(
        self,
        baseline: Dict,
        target: Dict,
        comparison_name: str
    ) -> Dict[str, float]:
        """计算相对提升"""
        improvements = {}
        
        # 技术指标提升
        if "technical" in baseline and "technical" in target:
            base_tech = baseline["technical"]
            target_tech = target["technical"]
            
            for key in base_tech.keys():
                if key in target_tech:
                    base_val = base_tech[key]
                    target_val = target_tech[key]
                    
                    if base_val > 0:
                        improvement = ((target_val - base_val) / base_val) * 100
                        improvements[f"technical_{key}"] = improvement
        
        # 临床指标提升
        if "clinical" in baseline and "clinical" in target:
            base_clin = baseline["clinical"].get("overall_avg", 0)
            target_clin = target["clinical"].get("overall_avg", 0)
            
            if base_clin > 0:
                improvement = ((target_clin - base_clin) / base_clin) * 100
                improvements["clinical_overall"] = improvement
        
        logger.info(f"\n{comparison_name} Improvements:")
        for key, value in improvements.items():
            logger.info(f"  {key}: {value:+.2f}%")
        
        return improvements
    
    def _save_comparison_results(self, results: Dict):
        """保存对比结果"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 保存JSON结果
        results_file = self.output_dir / f"comparison_results_{timestamp}.json"
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        logger.info(f"\nResults saved to: {results_file}")
        
        # 生成对比报告
        self._generate_comparison_report(results, timestamp)
    
    def _generate_comparison_report(self, results: Dict, timestamp: str):
        """生成对比报告"""
        report_file = self.output_dir / f"comparison_report_{timestamp}.txt"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write(" SYSTEM COMPARISON REPORT \n")
            f.write("=" * 70 + "\n\n")
            f.write(f"Evaluation Time: {results['evaluation_time']}\n")
            f.write(f"Number of Samples: {results['num_samples']}\n\n")
            
            # 各系统性能
            systems = results.get("systems", {})
            
            f.write("SYSTEM PERFORMANCE\n")
            f.write("=" * 70 + "\n\n")
            
            for system_name, system_results in systems.items():
                f.write(f"{system_name.upper().replace('_', ' ')}:\n")
                f.write("-" * 50 + "\n")
                
                # 技术指标
                if "technical" in system_results:
                    f.write("Technical Metrics:\n")
                    for key, value in system_results["technical"].items():
                        f.write(f"  {key}: {value:.4f}\n")
                
                # 临床指标
                if "clinical" in system_results:
                    f.write("\nClinical Metrics:\n")
                    overall = system_results["clinical"].get("overall_avg", 0)
                    f.write(f"  overall_avg: {overall:.4f}\n")
                
                f.write("\n")
            
            # 性能提升
            f.write("\nPERFORMANCE IMPROVEMENTS\n")
            f.write("=" * 70 + "\n\n")
            
            improvements = results.get("improvements", {})
            
            for comparison_name, improvement_data in improvements.items():
                f.write(f"{comparison_name.upper().replace('_', ' ')}:\n")
                f.write("-" * 50 + "\n")
                for key, value in improvement_data.items():
                    f.write(f"  {key}: {value:+.2f}%\n")
                f.write("\n")
            
            f.write("=" * 70 + "\n")
        
        logger.info(f"Report saved to: {report_file}")
    
    def _print_comparison_summary(self, results: Dict):
        """打印对比总结"""
        logger.info("\n" + "=" * 70)
        logger.info(" COMPARISON SUMMARY ")
        logger.info("=" * 70)
        
        systems = results.get("systems", {})
        
        # BERT F1对比
        logger.info("\nBERT F1 Scores:")
        for system_name, system_results in systems.items():
            if "technical" in system_results:
                bert_f1 = system_results["technical"].get("bert_f1", 0)
                logger.info(f"  {system_name}: {bert_f1:.4f}")
        
        # 临床质量对比
        logger.info("\nClinical Quality (Overall Avg):")
        for system_name, system_results in systems.items():
            if "clinical" in system_results:
                clinical_avg = system_results["clinical"].get("overall_avg", 0)
                logger.info(f"  {system_name}: {clinical_avg:.4f}")
        
        # 关键提升
        improvements = results.get("improvements", {})
        
        logger.info("\nKey Improvements:")
        
        # RAG提升
        if "rag_improvement" in improvements:
            rag_imp = improvements["rag_improvement"]
            bert_imp = rag_imp.get("technical_bert_f1", 0)
            logger.info(f"  RAG Impact: {bert_imp:+.2f}% (BERT F1)")
        
        # 记忆系统提升
        if "memory_improvement" in improvements:
            mem_imp = improvements["memory_improvement"]
            bert_imp = mem_imp.get("technical_bert_f1", 0)
            logger.info(f"  Memory Impact: {bert_imp:+.2f}% (BERT F1)")
        
        # 总体提升
        if "full_system_improvement" in improvements:
            full_imp = improvements["full_system_improvement"]
            bert_imp = full_imp.get("technical_bert_f1", 0)
            logger.info(f"  Overall Improvement: {bert_imp:+.2f}% (BERT F1)")


def compare_system_configurations(
    questions: List[str],
    reference_answers: List[str],
    bare_llm_responses: List[str],
    llm_rag_responses: List[str],
    full_system_responses: List[str],
    llm_evaluator=None,
    output_dir: str = "./evaluation_results/comparisons"
) -> Dict[str, any]:
    """
    便捷函数：对比系统配置
    
    Args:
        questions: 问题列表
        reference_answers: 参考答案列表
        bare_llm_responses: 裸LLM回复
        llm_rag_responses: LLM+RAG回复
        full_system_responses: 完整系统回复
        llm_evaluator: LLM评估器
        output_dir: 输出目录
        
    Returns:
        对比结果
    """
    evaluator = ComparisonEvaluator(output_dir)
    return evaluator.compare_systems(
        questions,
        reference_answers,
        bare_llm_responses,
        llm_rag_responses,
        full_system_responses,
        llm_evaluator
    )
