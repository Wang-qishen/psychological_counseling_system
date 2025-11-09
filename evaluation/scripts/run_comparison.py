#!/usr/bin/env python3
"""
对比实验脚本 - 三系统对比评估

对比三种配置：
1. 裸LLM（基线）
2. LLM + RAG
3. 完整系统（LLM + RAG + 记忆）

用途：
- 论文的消融实验
- 证明RAG和记忆系统的有效性
- 生成对比数据和图表

使用方法：
    python evaluation/scripts/run_comparison.py
    python evaluation/scripts/run_comparison.py --samples 50
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
from copy import deepcopy

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from evaluation.framework import EvaluationFramework
from evaluation.datasets.mentalchat_loader import MentalChatLoader
from dialogue.manager import DialogueManager


class ComparisonExperiment:
    """对比实验管理器"""
    
    def __init__(self, system_config_path: str, eval_config_path: str):
        """
        初始化对比实验
        
        Args:
            system_config_path: 系统配置文件路径
            eval_config_path: 评估配置文件路径
        """
        self.system_config_path = system_config_path
        self.eval_config_path = eval_config_path
        
        # 加载配置
        with open(system_config_path, 'r', encoding='utf-8') as f:
            self.base_config = yaml.safe_load(f)
        
        with open(eval_config_path, 'r', encoding='utf-8') as f:
            self.eval_config = yaml.safe_load(f)
        
        # 三种配置
        self.configs = {
            'baseline': self._create_baseline_config(),
            'rag_only': self._create_rag_only_config(),
            'full_system': self._create_full_system_config()
        }
        
        self.results = {}
    
    def _create_baseline_config(self) -> Dict:
        """创建裸LLM配置（禁用RAG和记忆）"""
        config = deepcopy(self.base_config)
        
        # 禁用RAG
        if 'rag' in config:
            config['rag']['enabled'] = False
        
        # 禁用记忆
        if 'memory' in config:
            config['memory']['enabled'] = False
        
        return config
    
    def _create_rag_only_config(self) -> Dict:
        """创建LLM+RAG配置（禁用记忆）"""
        config = deepcopy(self.base_config)
        
        # 启用RAG
        if 'rag' in config:
            config['rag']['enabled'] = True
        
        # 禁用记忆
        if 'memory' in config:
            config['memory']['enabled'] = False
        
        return config
    
    def _create_full_system_config(self) -> Dict:
        """创建完整系统配置（启用所有功能）"""
        config = deepcopy(self.base_config)
        
        # 启用RAG
        if 'rag' in config:
            config['rag']['enabled'] = True
        
        # 启用记忆
        if 'memory' in config:
            config['memory']['enabled'] = True
        
        return config
    
    def run_experiment(self, num_samples: int = None) -> Dict[str, Dict]:
        """
        运行对比实验
        
        Args:
            num_samples: 测试样本数量
            
        Returns:
            三种配置的评估结果
        """
        print("\n" + "="*70)
        print(" "*20 + "对比实验 - 三系统评估")
        print("="*70)
        
        # 加载测试数据
        print("\n" + "-"*70)
        print(" 1. 加载测试数据")
        print("-"*70)
        
        if num_samples is None:
            num_samples = self.eval_config.get('num_test_samples', 50)
        
        loader = MentalChatLoader()
        test_questions = loader.get_test_split(num_samples=num_samples)
        print(f"✓ 加载 {len(test_questions)} 个测试问题")
        
        # 依次运行三种配置
        config_names = {
            'baseline': '裸LLM（基线）',
            'rag_only': 'LLM + RAG',
            'full_system': '完整系统（LLM + RAG + 记忆）'
        }
        
        total_start_time = time.time()
        
        for config_name, config_desc in config_names.items():
            print("\n" + "="*70)
            print(f" 正在评估: {config_desc}")
            print("="*70)
            
            start_time = time.time()

            
                
            try:
                # 创建对话管理器
                print(f"\n初始化 {config_desc}...")
                
                # 创建LLM
                from llm.factory import create_llm_from_config
                llm = create_llm_from_config(self.configs[config_name])

                # 创建RAG管理器
                from knowledge.rag_manager import RAGManager
                from knowledge.chroma_kb import ChromaKnowledgeBase
                
                rag_config = self.configs[config_name].get('rag', {})
                
                # 为两个知识库准备配置
                psych_kb_config = {
                    'collection_name': 'psychological_knowledge',
                    'persist_directory': rag_config.get('persist_directory', './data/chroma_db'),
                    'embedding': rag_config.get('embedding', {})
                }
                
                user_kb_config = {
                    'collection_name': 'user_knowledge',
                    'persist_directory': rag_config.get('persist_directory', './data/chroma_db'),
                    'embedding': rag_config.get('embedding', {})
                }
                
                # 创建两个知识库
                psychological_kb = ChromaKnowledgeBase(psych_kb_config)
                user_kb = ChromaKnowledgeBase(user_kb_config)
                
                # 创建RAG管理器
                rag_manager = RAGManager(
                    psychological_kb=psychological_kb,
                    user_kb=user_kb,
                    config=rag_config
                )
                
                # 创建记忆管理器
                from memory.manager import MemoryManager
                from memory.storage import JSONMemoryStorage

                memory_config = self.configs[config_name].get('memory', {})
                storage_path = memory_config.get('storage', {}).get('path', './data/memory_db')
                storage = JSONMemoryStorage(storage_path)
                memory_manager = MemoryManager(
                    storage=storage,
                    summarizer=llm,
                    config=memory_config
                )

                # 创建对话管理器
                dialogue_manager = DialogueManager(
                    llm=llm,
                    rag_manager=rag_manager,
                    memory_manager=memory_manager,
                    config=self.configs[config_name].get('dialogue', {})
                )
                
                # 创建评估框架
                eval_framework = EvaluationFramework(
                    dialogue_manager=dialogue_manager,
                    llm_evaluator=llm,
                    data_dir=self.eval_config.get('data_dir', './data'),
                    output_dir=self.eval_config.get('output_dir', './evaluation_results')
                )
                
                # 运行评估
                print(f"开始评估...")
                results = eval_framework.run_full_evaluation(
                    dataset="mentalchat",
                    num_test_samples=len(test_questions),
                    generate_memory_tests=False
                )
                
                elapsed_time = time.time() - start_time
                
                # 保存结果
                self.results[config_name] = {
                    'config_desc': config_desc,
                    'results': results,
                    'elapsed_time': elapsed_time
                }
                
                print(f"\n✓ {config_desc} 评估完成")
                print(f"  用时: {elapsed_time:.1f} 秒")
                
            except Exception as e:
                print(f"\n✗ {config_desc} 评估失败: {e}")
                import traceback
                traceback.print_exc()
                continue
        
        total_elapsed = time.time() - total_start_time
        
        print("\n" + "="*70)
        print(" "*25 + "所有评估完成")
        print("="*70)
        print(f"总用时: {total_elapsed:.1f} 秒 ({total_elapsed/60:.1f} 分钟)")
        
        return self.results
    
    def print_comparison(self):
        """打印对比结果"""
        print("\n" + "="*70)
        print(" "*20 + "对比结果摘要")
        print("="*70)
        
        # 准备对比数据
        comparison_data = {}
        
        for config_name, data in self.results.items():
            results = data['results']
            comparison_data[config_name] = {
                'name': data['config_desc'],
                'tech': results.get('technical_metrics', {}),
                'clinical': results.get('clinical_metrics', {}),
                'memory': results.get('memory_metrics', {}),
                'rag': results.get('rag_metrics', {})
            }
        
        # 技术指标对比
        print("\n📊 技术指标对比:")
        print(f"{'指标':<20} {'裸LLM':<15} {'LLM+RAG':<15} {'完整系统':<15}")
        print("-"*70)
        
        tech_metrics = ['bert_f1', 'rouge_l', 'response_time']
        for metric in tech_metrics:
            values = []
            for config in ['baseline', 'rag_only', 'full_system']:
                if config in comparison_data:
                    tech = comparison_data[config]['tech']
                    if metric == 'bert_f1':
                        val = tech.get('bert_score', {}).get('f1', 0)
                    elif metric == 'rouge_l':
                        val = tech.get('rouge', {}).get('rougeL', 0)
                    elif metric == 'response_time':
                        val = tech.get('response_time', 0)
                    else:
                        val = 0
                    values.append(val)
                else:
                    values.append(0)
            
            metric_name = {
                'bert_f1': 'BERT Score F1',
                'rouge_l': 'ROUGE-L',
                'response_time': '响应时间(秒)'
            }[metric]
            
            print(f"{metric_name:<20} {values[0]:<15.3f} {values[1]:<15.3f} {values[2]:<15.3f}")
        
        # 临床指标对比
        print("\n📋 临床指标对比:")
        print(f"{'指标':<20} {'裸LLM':<15} {'LLM+RAG':<15} {'完整系统':<15}")
        print("-"*70)
        
        clinical_metrics = ['empathy', 'support', 'relevance']
        for metric in clinical_metrics:
            values = []
            for config in ['baseline', 'rag_only', 'full_system']:
                if config in comparison_data:
                    val = comparison_data[config]['clinical'].get(metric, 0)
                    values.append(val)
                else:
                    values.append(0)
            
            metric_name = {
                'empathy': '共情',
                'support': '支持',
                'relevance': '相关性'
            }[metric]
            
            print(f"{metric_name:<20} {values[0]:<15.2f} {values[1]:<15.2f} {values[2]:<15.2f}")
        
        # 记忆系统对比（只有完整系统有）
        print("\n🧠 记忆系统:")
        if 'full_system' in comparison_data:
            memory = comparison_data['full_system']['memory']
            print(f"  短期记忆召回: {memory.get('short_term_recall', 0)*100:.2f}%")
            print(f"  整体准确率:   {memory.get('overall_accuracy', 0)*100:.2f}%")
        else:
            print("  （未启用）")
        
        # RAG效果对比（rag_only和full_system有）
        print("\n🔍 RAG效果:")
        print(f"{'配置':<20} {'召回率':<15} {'精确率':<15}")
        print("-"*70)
        
        for config in ['rag_only', 'full_system']:
            if config in comparison_data:
                rag = comparison_data[config]['rag']
                name = comparison_data[config]['name']
                recall = rag.get('recall', 0) * 100
                precision = rag.get('precision', 0) * 100
                print(f"{name:<20} {recall:<15.2f} {precision:<15.2f}")
    
    def calculate_improvements(self) -> Dict:
        """计算改进幅度"""
        improvements = {}
        
        if 'baseline' not in self.results or 'full_system' not in self.results:
            return improvements
        
        baseline = self.results['baseline']['results']
        full = self.results['full_system']['results']
        
        # 技术指标改进
        baseline_tech = baseline.get('technical_metrics', {})
        full_tech = full.get('technical_metrics', {})
        
        # BERT Score F1
        baseline_bert = baseline_tech.get('bert_score', {}).get('f1', 0)
        full_bert = full_tech.get('bert_score', {}).get('f1', 0)
        if baseline_bert > 0:
            improvements['bert_f1'] = ((full_bert - baseline_bert) / baseline_bert) * 100
        
        # ROUGE-L
        baseline_rouge = baseline_tech.get('rouge', {}).get('rougeL', 0)
        full_rouge = full_tech.get('rouge', {}).get('rougeL', 0)
        if baseline_rouge > 0:
            improvements['rouge_l'] = ((full_rouge - baseline_rouge) / baseline_rouge) * 100
        
        # 临床指标改进
        baseline_clinical = baseline.get('clinical_metrics', {})
        full_clinical = full.get('clinical_metrics', {})
        
        for metric in ['empathy', 'support', 'relevance']:
            baseline_val = baseline_clinical.get(metric, 0)
            full_val = full_clinical.get(metric, 0)
            if baseline_val > 0:
                improvements[metric] = ((full_val - baseline_val) / baseline_val) * 100
        
        return improvements
    
    def print_improvements(self):
        """打印改进幅度"""
        improvements = self.calculate_improvements()
        
        if not improvements:
            print("\n⚠️  无法计算改进幅度（缺少基线或完整系统结果）")
            return
        
        print("\n" + "="*70)
        print(" "*20 + "完整系统相比裸LLM的改进")
        print("="*70)
        
        print("\n📈 改进幅度:")
        for metric, improvement in improvements.items():
            metric_name = {
                'bert_f1': 'BERT Score F1',
                'rouge_l': 'ROUGE-L',
                'empathy': '共情',
                'support': '支持',
                'relevance': '相关性'
            }.get(metric, metric)
            
            sign = '+' if improvement > 0 else ''
            print(f"  {metric_name:<20} {sign}{improvement:>6.2f}%")
    
    def save_results(self, output_dir: str = None) -> str:
        """保存对比实验结果"""
        if output_dir is None:
            output_dir = "evaluation/results/comparison"
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # 生成文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result_file = output_path / f"comparison_{timestamp}.json"
        
        # 准备保存数据
        save_data = {
            'metadata': {
                'timestamp': timestamp,
                'num_samples': self.eval_config.get('num_test_samples', 50),
                'system_config': self.system_config_path,
                'eval_config': self.eval_config_path
            },
            'results': self.results,
            'improvements': self.calculate_improvements()
        }
        
        # 保存JSON
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ 对比结果已保存: {result_file}")
        
        return str(result_file)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='运行三系统对比实验')
    parser.add_argument('--samples', type=int, default=50,
                       help='测试样本数量（默认50）')
    parser.add_argument('--system-config', type=str,
                       default='configs/config.yaml',
                       help='系统配置文件路径')
    parser.add_argument('--eval-config', type=str,
                       default='evaluation/configs/default_config.yaml',
                       help='评估配置文件路径')
    parser.add_argument('--output-dir', type=str, default=None,
                       help='输出目录')
    parser.add_argument('--no-save', action='store_true',
                       help='不保存结果')
    
    args = parser.parse_args()
    
    try:
        # 创建对比实验
        experiment = ComparisonExperiment(args.system_config, args.eval_config)
        
        # 运行实验
        results = experiment.run_experiment(args.samples)
        
        # 打印对比结果
        experiment.print_comparison()
        
        # 打印改进幅度
        experiment.print_improvements()
        
        # 保存结果
        if not args.no_save:
            result_file = experiment.save_results(args.output_dir)
        
        # 完成
        print("\n" + "="*70)
        print(" "*25 + "对比实验完成！")
        print("="*70)
        
        if not args.no_save:
            print(f"\n✓ 结果文件: {result_file}")
        print(f"✓ 测试样本数: {args.samples}")
        print(f"✓ 配置数量: 3")
        
        print("\n📝 下一步:")
        print("  1. 生成可视化图表: python evaluation/scripts/visualize_comparison.py")
        print("  2. 生成LaTeX报告: python evaluation/reporting/generate_latex_report.py")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  实验被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n✗ 实验失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
