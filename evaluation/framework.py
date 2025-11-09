"""
评估框架主入口

提供统一的评估接口，整合所有评估功能
"""

import logging
from typing import Dict, List, Optional
from pathlib import Path

from .evaluators import SystemEvaluator, ComparisonEvaluator
from .datasets import (
    MentalChatLoader,
    MemoryTestGenerator,
    create_dataset_loader
)

logger = logging.getLogger(__name__)


class EvaluationFramework:
    """评估框架"""
    
    def __init__(
        self,
        dialogue_manager=None,
        llm_evaluator=None,
        data_dir: str = "./data",
        output_dir: str = "./evaluation_results"
    ):
        """
        初始化
        
        Args:
            dialogue_manager: 对话管理器
            llm_evaluator: LLM评估器
            data_dir: 数据目录
            output_dir: 输出目录
        """
        self.dialogue_manager = dialogue_manager
        self.llm_evaluator = llm_evaluator
        self.data_dir = Path(data_dir)
        self.output_dir = Path(output_dir)
        
        # 创建目录
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 初始化评估器
        if dialogue_manager:
            self.system_evaluator = SystemEvaluator(
                dialogue_manager, llm_evaluator, output_dir
            )
        else:
            self.system_evaluator = None
        
        self.comparison_evaluator = ComparisonEvaluator(
            str(self.output_dir / "comparisons")
        )
    
    def load_mentalchat_dataset(
        self,
        num_test_samples: int = 200
    ) -> Dict[str, List]:
        """
        加载MentalChat16K数据集
        
        Args:
            num_test_samples: 测试样本数量
            
        Returns:
            数据集字典
        """
        logger.info("Loading MentalChat16K dataset...")
        
        loader = MentalChatLoader(
            data_dir=str(self.data_dir / "mentalchat")
        )
        
        evaluation_set = loader.create_evaluation_set(num_test_samples)
        
        logger.info(f"Loaded {len(evaluation_set['questions'])} test samples")
        
        return evaluation_set
    
    def generate_memory_tests(
        self,
        num_cases_per_scenario: int = 20
    ) -> Dict[str, List]:
        """
        生成记忆测试数据
        
        Args:
            num_cases_per_scenario: 每个场景的用例数
            
        Returns:
            记忆测试数据
        """
        logger.info("Generating memory test data...")
        
        generator = MemoryTestGenerator(
            str(self.data_dir / "memory_tests")
        )
        
        test_data = generator.generate_all_tests(num_cases_per_scenario)
        
        logger.info(f"Generated {len(test_data['test_suite'])} memory test cases")
        
        return test_data
    
    def run_full_evaluation(
        self,
        dataset: str = "mentalchat",
        num_test_samples: int = 200,
        clinical_sample_size: int = 50,
        generate_memory_tests: bool = True
    ) -> Dict[str, any]:
        """
        运行完整评估
        
        Args:
            dataset: 数据集名称（"mentalchat"）
            num_test_samples: 测试样本数量
            clinical_sample_size: 临床评估采样大小
            generate_memory_tests: 是否生成记忆测试
            
        Returns:
            评估结果
        """
        if self.system_evaluator is None:
            raise ValueError("No dialogue manager provided")
        
        logger.info("=" * 70)
        logger.info(" PREPARING EVALUATION ")
        logger.info("=" * 70)
        
        # 准备测试数据
        test_data = {}
        
        # 1. 加载主数据集
        if dataset == "mentalchat":
            eval_set = self.load_mentalchat_dataset(num_test_samples)
            test_data["questions"] = eval_set["questions"]
            test_data["reference_answers"] = eval_set["reference_answers"]
        else:
            raise ValueError(f"Unknown dataset: {dataset}")
        
        # 2. 生成记忆测试数据
        if generate_memory_tests:
            memory_tests = self.generate_memory_tests()
            test_data["memory_test_suite"] = {
                "recall_tests": memory_tests["recall_tests"],
                "consistency_tests": memory_tests["consistency_tests"]
            }
        
        # 3. 运行评估
        logger.info("\n" + "=" * 70)
        logger.info(" STARTING EVALUATION ")
        logger.info("=" * 70)
        
        results = self.system_evaluator.run_full_evaluation(
            test_data,
            clinical_sample_size
        )
        
        return results
    
    def run_comparison_evaluation(
        self,
        bare_llm_manager,
        llm_rag_manager,
        full_system_manager,
        dataset: str = "mentalchat",
        num_test_samples: int = 200
    ) -> Dict[str, any]:
        """
        运行对比评估
        
        Args:
            bare_llm_manager: 裸LLM管理器
            llm_rag_manager: LLM+RAG管理器
            full_system_manager: 完整系统管理器
            dataset: 数据集名称
            num_test_samples: 测试样本数量
            
        Returns:
            对比结果
        """
        logger.info("=" * 70)
        logger.info(" PREPARING COMPARISON EVALUATION ")
        logger.info("=" * 70)
        
        # 1. 加载测试数据
        if dataset == "mentalchat":
            eval_set = self.load_mentalchat_dataset(num_test_samples)
            questions = eval_set["questions"]
            references = eval_set["reference_answers"]
        else:
            raise ValueError(f"Unknown dataset: {dataset}")
        
        # 2. 生成各系统的回复
        logger.info("\n" + "=" * 70)
        logger.info(" GENERATING RESPONSES ")
        logger.info("=" * 70)
        
        logger.info("\n1. Generating Bare LLM responses...")
        bare_llm_responses = self._generate_responses(bare_llm_manager, questions)
        
        logger.info("\n2. Generating LLM+RAG responses...")
        llm_rag_responses = self._generate_responses(llm_rag_manager, questions)
        
        logger.info("\n3. Generating Full System responses...")
        full_system_responses = self._generate_responses(full_system_manager, questions)
        
        # 3. 运行对比评估
        logger.info("\n" + "=" * 70)
        logger.info(" STARTING COMPARISON ")
        logger.info("=" * 70)
        
        results = self.comparison_evaluator.compare_systems(
            questions,
            references,
            bare_llm_responses,
            llm_rag_responses,
            full_system_responses,
            self.llm_evaluator
        )
        
        return results
    
    def _generate_responses(
        self,
        manager,
        questions: List[str]
    ) -> List[str]:
        """生成回复"""
        responses = []
        
        for i, question in enumerate(questions):
            if i % 10 == 0:
                logger.info(f"  Processing {i}/{len(questions)}...")
            
            try:
                response = manager.chat(
                    user_id="eval_user",
                    message=question
                )
                responses.append(response)
            except Exception as e:
                logger.error(f"Error generating response: {e}")
                responses.append("")
        
        logger.info(f"  Generated {len(responses)} responses")
        return responses
    
    def quick_test(
        self,
        num_samples: int = 10
    ) -> Dict[str, any]:
        """
        快速测试（用于调试）
        
        Args:
            num_samples: 测试样本数
            
        Returns:
            测试结果
        """
        logger.info("Running quick test...")
        
        return self.run_full_evaluation(
            num_test_samples=num_samples,
            clinical_sample_size=min(5, num_samples),
            generate_memory_tests=False
        )
