#!/usr/bin/env python3
"""
完整评估脚本 - 运行200样本的完整系统评估

用途：
1. 论文发表的标准评估
2. 所有21个指标的全面测试
3. 自动保存详细结果

使用方法：
    python evaluation/scripts/run_full_evaluation.py
    python evaluation/scripts/run_full_evaluation.py --samples 200 --config evaluation/configs/full_eval_config.yaml
"""

import sys
import os
import json
import yaml
import argparse
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from evaluation.framework import EvaluationFramework
from evaluation.datasets.mentalchat_loader import MentalChatLoader
from dialogue.manager import DialogueManager


class FullEvaluator:
    """完整评估管理器"""
    
    def __init__(self, system_config_path: str, eval_config_path: str):
        """
        初始化评估器
        
        Args:
            system_config_path: 系统配置文件路径
            eval_config_path: 评估配置文件路径
        """
        self.system_config_path = system_config_path
        self.eval_config_path = eval_config_path
        
        # 加载配置
        self.system_config = self._load_config(system_config_path)
        self.eval_config = self._load_config(eval_config_path)
        
        # 初始化组件
        self.dialogue_manager = None
        self.eval_framework = None
        self.results = {}
        
    def _load_config(self, config_path: str) -> Dict:
        """加载配置文件"""
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    # def initialize(self):
    #     """初始化评估系统"""
    #     print("\n" + "="*70)
    #     print(" "*20 + "完整评估 - 心理咨询系统")
    #     print("="*70)
        
    #     # 1. 初始化对话管理器
    #     print("\n" + "-"*70)
    #     print(" 1. 初始化对话管理器")
    #     print("-"*70)
        
    #     try:
    #         self.dialogue_manager = DialogueManager(self.system_config)
    #         print("✓ 对话管理器初始化成功")
    #     except Exception as e:
    #         print(f"✗ 对话管理器初始化失败: {e}")
    #         raise
        
    #     # 2. 创建评估框架
    #     print("\n" + "-"*70)
    #     print(" 2. 创建评估框架")
    #     print("-"*70)
        
    #     try:
    #         self.eval_framework = EvaluationFramework(
    #             dialogue_manager=self.dialogue_manager,
    #             config=self.eval_config
    #         )
    #         print("✓ 评估框架创建成功")
    #     except Exception as e:
    #         print(f"✗ 评估框架创建失败: {e}")
    #         raise
    
    def initialize(self):
        """初始化评估系统"""
        print("\n" + "="*70)
        print(" "*20 + "完整评估 - 心理咨询系统")
        print("="*70)
        
        # 1. 初始化对话管理器
        print("\n" + "-"*70)
        print(" 1. 初始化对话管理器")
        print("-"*70)
        
        try:
            # 创建LLM
            from llm.factory import create_llm_from_config
            llm = create_llm_from_config(self.system_config)

            # 创建RAG管理器
            from knowledge.rag_manager import RAGManager
            rag_config = self.system_config.get('rag', {})
            rag_manager = RAGManager(
                llm=llm,
                config=rag_config
            )

            # 创建记忆管理器
            from memory.manager import MemoryManager
            memory_config = self.system_config.get('memory', {})
            memory_manager = MemoryManager(config=memory_config)

            # 创建对话管理器
            self.dialogue_manager = DialogueManager(
                llm=llm,
                rag_manager=rag_manager,
                memory_manager=memory_manager,
                config=self.system_config.get('dialogue', {})
            )
            
            print("✓ 对话管理器初始化成功")
        except Exception as e:
            print(f"✗ 对话管理器初始化失败: {e}")
            raise
            

    def load_test_data(self, num_samples: int = None) -> List[Dict]:
        """
        加载测试数据
        
        Args:
            num_samples: 测试样本数量，None表示使用配置中的值
            
        Returns:
            测试问题列表
        """
        print("\n" + "-"*70)
        print(" 3. 加载测试数据")
        print("-"*70)
        
        if num_samples is None:
            num_samples = self.eval_config.get('num_test_samples', 200)
        
        try:
            # 从MentalChat16K加载测试数据
            loader = MentalChatLoader()
            test_questions = loader.get_test_questions(num_samples=num_samples)
            
            print(f"✓ 成功加载 {len(test_questions)} 个测试问题")
            print(f"  数据集: {dataset_name}")
            print(f"  样本数: {len(test_questions)}")
            
            return test_questions
            
        except Exception as e:
            print(f"✗ 加载测试数据失败: {e}")
            raise
    
    def run_evaluation(self, test_questions: List[Dict]) -> Dict:
        """
        运行完整评估
        
        Args:
            test_questions: 测试问题列表
            
        Returns:
            评估结果
        """
        print("\n" + "-"*70)
        print(" 4. 运行评估")
        print("-"*70)
        
        start_time = time.time()
        
        try:
            # 运行评估
            self.results = self.eval_framework.evaluate(test_questions)
            
            elapsed_time = time.time() - start_time
            
            print(f"\n✓ 评估完成！")
            print(f"  用时: {elapsed_time:.1f} 秒 ({elapsed_time/60:.1f} 分钟)")
            print(f"  平均每样本: {elapsed_time/len(test_questions):.2f} 秒")
            
            return self.results
            
        except Exception as e:
            print(f"\n✗ 评估失败: {e}")
            raise
    
    def print_results(self, results: Dict):
        """打印评估结果摘要"""
        print("\n" + "-"*70)
        print(" 5. 评估结果")
        print("-"*70)
        
        # 技术指标
        if 'technical_metrics' in results:
            print("\n📊 技术指标:")
            tech = results['technical_metrics']
            
            if 'bert_score' in tech:
                bert = tech['bert_score']
                print(f"  BERT Score F1:  {bert.get('f1', 0):.3f}")
                print(f"  BERT Precision: {bert.get('precision', 0):.3f}")
                print(f"  BERT Recall:    {bert.get('recall', 0):.3f}")
            
            if 'rouge' in tech:
                rouge = tech['rouge']
                print(f"  ROUGE-1:        {rouge.get('rouge1', 0):.3f}")
                print(f"  ROUGE-2:        {rouge.get('rouge2', 0):.3f}")
                print(f"  ROUGE-L:        {rouge.get('rougeL', 0):.3f}")
            
            if 'bleu' in tech:
                print(f"  BLEU:           {tech['bleu']:.3f}")
            
            if 'response_time' in tech:
                print(f"  平均响应时间:    {tech['response_time']:.2f} 秒")
            
            if 'response_length' in tech:
                print(f"  平均响应长度:    {tech['response_length']:.0f} 字符")
        
        # 临床指标
        if 'clinical_metrics' in results:
            print("\n📋 专业质量:")
            clinical = results['clinical_metrics']
            
            metrics_names = {
                'empathy': '共情',
                'support': '支持',
                'guidance': '指导',
                'relevance': '相关性',
                'communication': '沟通',
                'fluency': '流畅性',
                'safety': '安全性'
            }
            
            for key, name in metrics_names.items():
                if key in clinical:
                    score = clinical[key]
                    print(f"  {name:12s} {score:.2f}/5.0")
        
        # 记忆指标
        if 'memory_metrics' in results:
            print("\n🧠 记忆系统:")
            memory = results['memory_metrics']
            
            if 'short_term_recall' in memory:
                print(f"  短期记忆召回:    {memory['short_term_recall']*100:.2f}%")
            if 'working_memory_accuracy' in memory:
                print(f"  工作记忆准确率:  {memory['working_memory_accuracy']*100:.2f}%")
            if 'long_term_consistency' in memory:
                print(f"  长期记忆一致性:  {memory['long_term_consistency']*100:.2f}%")
            if 'overall_accuracy' in memory:
                print(f"  整体准确率:      {memory['overall_accuracy']*100:.2f}%")
        
        # RAG指标
        if 'rag_metrics' in results:
            print("\n🔍 RAG效果:")
            rag = results['rag_metrics']
            
            if 'recall' in rag:
                print(f"  检索召回率:      {rag['recall']*100:.2f}%")
            if 'precision' in rag:
                print(f"  检索精确率:      {rag['precision']*100:.2f}%")
            if 'f1' in rag:
                print(f"  F1 Score:       {rag['f1']:.3f}")
        
        # 安全性指标
        if 'safety_metrics' in results:
            print("\n🛡️ 安全性:")
            safety = results['safety_metrics']
            
            if 'harmful_content' in safety:
                print(f"  有害内容检测:    通过 {safety['harmful_content']*100:.1f}%")
            if 'privacy_protection' in safety:
                print(f"  隐私保护:        通过 {safety['privacy_protection']*100:.1f}%")
    
    def save_results(self, results: Dict, output_dir: str = None) -> str:
        """
        保存评估结果
        
        Args:
            results: 评估结果
            output_dir: 输出目录，None表示使用默认目录
            
        Returns:
            保存的文件路径
        """
        print("\n" + "-"*70)
        print(" 6. 保存结果")
        print("-"*70)
        
        # 确定输出目录
        if output_dir is None:
            output_dir = "evaluation/results/full_evaluation"
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # 生成文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result_file = output_path / f"full_evaluation_{timestamp}.json"
        
        # 添加元数据
        results_with_meta = {
            'metadata': {
                'timestamp': timestamp,
                'num_samples': len(results.get('individual_results', [])),
                'system_config': self.system_config_path,
                'eval_config': self.eval_config_path
            },
            'results': results
        }
        
        # 保存JSON
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(results_with_meta, f, indent=2, ensure_ascii=False)
        
        print(f"✓ 结果已保存: {result_file}")
        print(f"  文件大小: {result_file.stat().st_size / 1024:.1f} KB")
        
        return str(result_file)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='运行完整评估（200样本）')
    parser.add_argument('--samples', type=int, default=None,
                       help='测试样本数量（默认使用配置文件中的值）')
    parser.add_argument('--system-config', type=str, 
                       default='configs/config.yaml',
                       help='系统配置文件路径')
    parser.add_argument('--eval-config', type=str,
                       default='evaluation/configs/full_eval_config.yaml',
                       help='评估配置文件路径')
    parser.add_argument('--output-dir', type=str, default=None,
                       help='输出目录')
    parser.add_argument('--no-save', action='store_true',
                       help='不保存结果')
    
    args = parser.parse_args()
    
    try:
        # 创建评估器
        evaluator = FullEvaluator(args.system_config, args.eval_config)
        
        # 初始化
        evaluator.initialize()
        
        # 加载测试数据
        test_questions = evaluator.load_test_data(args.samples)
        
        # 运行评估
        results = evaluator.run_evaluation(test_questions)
        
        # 打印结果
        evaluator.print_results(results)
        
        # 保存结果
        if not args.no_save:
            result_file = evaluator.save_results(results, args.output_dir)
        
        # 完成
        print("\n" + "="*70)
        print(" "*25 + "评估完成！")
        print("="*70)
        
        if not args.no_save:
            print(f"\n✓ 结果文件: {result_file}")
        print(f"✓ 测试样本数: {len(test_questions)}")
        print(f"✓ 评估指标数: 21")
        
        print("\n📝 下一步:")
        print("  1. 查看详细结果: cat " + result_file if not args.no_save else "")
        print("  2. 运行对比实验: python evaluation/scripts/run_comparison.py")
        print("  3. 生成报告: python evaluation/scripts/generate_report.py")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  评估被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n✗ 评估失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
