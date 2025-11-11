#!/usr/bin/env python3
"""
简化的对比实验脚本 - 易于使用的三系统对比
作者: 为期末作业设计
日期: 2025-11

功能:
- 对比裸LLM、LLM+RAG、完整系统三种配置
- 自动生成评估报告和可视化图表
- 支持自动评估和人工评估

使用方法:
    # 快速运行（使用默认30个问题）
    python evaluation/scripts/simple_comparison.py
    
    # 指定问题数量
    python evaluation/scripts/simple_comparison.py --num-questions 20
    
    # 跳过人工评估
    python evaluation/scripts/simple_comparison.py --skip-manual
"""

import sys
import os
import json
import yaml
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Tuple
import argparse

# 添加项目路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from utils.helpers import load_config, setup_directories


class SimpleComparisonExperiment:
    """简化的对比实验类"""
    
    def __init__(self, config_path: str = "configs/config.yaml"):
        """初始化实验"""
        print("\n" + "="*70)
        print(" "*20 + "🧪 三系统对比实验")
        print("="*70)
        
        # 加载配置
        print("\n📋 正在加载配置...")
        self.config = load_config(config_path)
        
        # 加载对比实验配置
        comparison_config_path = project_root / "evaluation/configs/comparison_config.yaml"
        with open(comparison_config_path, 'r', encoding='utf-8') as f:
            self.comparison_config = yaml.safe_load(f)['comparison']
        
        # 加载测试问题
        self.test_questions = self._load_test_questions()
        
        # 结果存储
        self.results = {
            'baseline': {},
            'rag_only': {},
            'full_system': {}
        }
        
        print(f"✓ 配置加载完成")
        print(f"✓ 测试问题数: {len(self.test_questions)}")
    
    def _load_test_questions(self) -> List[Dict]:
        """加载测试问题"""
        questions_file = project_root / self.comparison_config['test_questions']['custom_file']
        
        with open(questions_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return data['questions']
    
    def _create_dialogue_manager(self, config_name: str):
        """创建对话管理器"""
        from llm.factory import create_llm_from_config
        from knowledge.rag_manager import RAGManager
        from knowledge.chroma_kb import ChromaKnowledgeBase
        from memory.manager import MemoryManager
        from memory.storage import JSONMemoryStorage
        from dialogue.manager import DialogueManager
        
        # 根据配置名称调整配置
        config = self.config.copy()
        comp_config = self.comparison_config['configurations'][config_name]
        
        # 调整RAG开关
        if 'dialogue' not in config:
            config['dialogue'] = {}
        if 'generation' not in config['dialogue']:
            config['dialogue']['generation'] = {}
        
        config['dialogue']['generation']['enable_rag'] = comp_config['enable_rag']
        config['dialogue']['generation']['enable_memory'] = comp_config['enable_memory']
        
        # 创建LLM
        llm = create_llm_from_config(config)
        
        # 创建RAG管理器
        rag_config = config.get('rag', {})
        embedding_config = rag_config.get('embedding', {})
        persist_dir = rag_config.get('vector_store', {}).get('persist_directory', './data/vector_db')
        
        psych_kb_config = {
            'collection_name': 'psych_knowledge',
            'persist_directory': persist_dir,
            'embedding': embedding_config
        }
        
        user_kb_config = {
            'collection_name': 'user_info',
            'persist_directory': persist_dir,
            'embedding': embedding_config
        }
        
        psychological_kb = ChromaKnowledgeBase(psych_kb_config)
        user_kb = ChromaKnowledgeBase(user_kb_config)
        
        rag_manager = RAGManager(
            psychological_kb=psychological_kb,
            user_kb=user_kb,
            config=rag_config.get('retrieval', {})
        )
        
        # 创建记忆管理器
        memory_config = config.get('memory', {})
        storage_path = memory_config.get('storage', {}).get('path', './data/memory_db')
        storage = JSONMemoryStorage(storage_path)
        
        memory_manager = MemoryManager(
            storage=storage,
            summarizer=llm,
            config=memory_config
        )
        
        # 创建对话管理器
        dialogue_config = config.get('dialogue', {})
        dialogue_config['enable_rag'] = comp_config['enable_rag']
        dialogue_config['enable_memory'] = comp_config['enable_memory']
        
        dialogue_manager = DialogueManager(
            llm=llm,
            rag_manager=rag_manager,
            memory_manager=memory_manager,
            config=dialogue_config
        )
        
        return dialogue_manager
    
    def run_configuration(self, config_name: str, questions: List[Dict]) -> Dict:
        """运行单个配置的测试"""
        comp_config = self.comparison_config['configurations'][config_name]
        config_desc = comp_config['name']
        
        print(f"\n{'='*70}")
        print(f"  🔧 正在测试: {config_desc}")
        print(f"{'='*70}")
        print(f"  配置说明: {comp_config['description']}")
        print(f"  问题数量: {len(questions)}")
        
        # 创建对话管理器
        print(f"\n  ⚙️  初始化系统...")
        dialogue_manager = self._create_dialogue_manager(config_name)
        
        # 创建测试用户
        user_id = f"test_user_{config_name}"
        try:
            dialogue_manager.memory_manager.create_user(
                user_id=user_id,
                age=25,
                gender="未知",
                occupation="测试用户"
            )
        except:
            pass  # 用户可能已存在
        
        session_id = dialogue_manager.start_session(user_id)
        
        # 运行测试
        responses = []
        response_times = []
        
        print(f"\n  🚀 开始生成回复...")
        
        for i, q in enumerate(questions, 1):
            question = q['question']
            
            # 生成回复并计时
            start_time = time.time()
            try:
                response = dialogue_manager.chat(
                    user_id=user_id,
                    session_id=session_id,
                    user_message=question
                )
                elapsed = time.time() - start_time
                
                responses.append({
                    'question_id': q['id'],
                    'question': question,
                    'response': response,
                    'response_time': elapsed,
                    'category': q['category']
                })
                response_times.append(elapsed)
                
                # 进度显示
                if i % 5 == 0 or i == len(questions):
                    avg_time = sum(response_times) / len(response_times)
                    print(f"    进度: {i}/{len(questions)} | 平均响应时间: {avg_time:.2f}秒")
            
            except Exception as e:
                print(f"    ⚠️  问题 {i} 生成失败: {e}")
                responses.append({
                    'question_id': q['id'],
                    'question': question,
                    'response': "[生成失败]",
                    'response_time': 0,
                    'category': q['category'],
                    'error': str(e)
                })
        
        # 结束会话
        dialogue_manager.end_session(user_id, session_id)
        
        # 计算统计数据
        valid_times = [r['response_time'] for r in responses if r['response_time'] > 0]
        valid_responses = [r for r in responses if r['response_time'] > 0]
        
        results = {
            'config_name': config_name,
            'config_desc': config_desc,
            'responses': responses,
            'statistics': {
                'total_questions': len(questions),
                'successful_responses': len(valid_responses),
                'failed_responses': len(questions) - len(valid_responses),
                'avg_response_time': sum(valid_times) / len(valid_times) if valid_times else 0,
                'min_response_time': min(valid_times) if valid_times else 0,
                'max_response_time': max(valid_times) if valid_times else 0,
                'avg_response_length': sum(len(r['response']) for r in valid_responses) / len(valid_responses) if valid_responses else 0
            }
        }
        
        print(f"\n  ✓ {config_desc} 测试完成")
        print(f"    成功: {results['statistics']['successful_responses']}/{len(questions)}")
        print(f"    平均响应时间: {results['statistics']['avg_response_time']:.2f}秒")
        
        return results
    
    def run_all_configurations(self, num_questions: int = None):
        """运行所有配置的测试"""
        if num_questions is None:
            num_questions = self.comparison_config['num_test_samples']
        
        # 选择问题
        questions = self.test_questions[:num_questions]
        
        print(f"\n📝 将使用 {len(questions)} 个测试问题")
        print(f"   问题类别: {set(q['category'] for q in questions)}")
        
        # 依次测试三种配置
        for config_name in ['baseline', 'rag_only', 'full_system']:
            self.results[config_name] = self.run_configuration(config_name, questions)
            
            # 短暂休息
            time.sleep(1)
        
        print(f"\n{'='*70}")
        print(f"  ✅ 所有配置测试完成！")
        print(f"{'='*70}")
    
    def print_comparison(self):
        """打印对比结果"""
        print(f"\n{'='*70}")
        print(" "*20 + "📊 对比结果汇总")
        print(f"{'='*70}")
        
        # 自动评估指标对比
        print(f"\n{'指标':<20} {'裸LLM':<15} {'LLM+RAG':<15} {'完整系统':<15}")
        print("-"*70)
        
        # 响应时间
        times = [
            self.results['baseline']['statistics']['avg_response_time'],
            self.results['rag_only']['statistics']['avg_response_time'],
            self.results['full_system']['statistics']['avg_response_time']
        ]
        print(f"{'平均响应时间(秒)':<20} {times[0]:<15.2f} {times[1]:<15.2f} {times[2]:<15.2f}")
        
        # 回复长度
        lengths = [
            self.results['baseline']['statistics']['avg_response_length'],
            self.results['rag_only']['statistics']['avg_response_length'],
            self.results['full_system']['statistics']['avg_response_length']
        ]
        print(f"{'平均回复长度(字)':<20} {lengths[0]:<15.0f} {lengths[1]:<15.0f} {lengths[2]:<15.0f}")
        
        # 成功率
        success_rates = [
            self.results['baseline']['statistics']['successful_responses'] / self.results['baseline']['statistics']['total_questions'] * 100,
            self.results['rag_only']['statistics']['successful_responses'] / self.results['rag_only']['statistics']['total_questions'] * 100,
            self.results['full_system']['statistics']['successful_responses'] / self.results['full_system']['statistics']['total_questions'] * 100
        ]
        print(f"{'成功率(%)':<20} {success_rates[0]:<15.1f} {success_rates[1]:<15.1f} {success_rates[2]:<15.1f}")
    
    def save_results(self, output_dir: str = None) -> str:
        """保存结果"""
        if output_dir is None:
            output_dir = self.comparison_config['output']['results_dir']
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # 生成文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result_file = output_path / f"comparison_{timestamp}.json"
        
        # 准备保存数据
        save_data = {
            'metadata': {
                'timestamp': timestamp,
                'num_questions': len(self.test_questions),
                'configurations': self.comparison_config['configurations']
            },
            'results': self.results
        }
        
        # 保存
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ 结果已保存: {result_file}")
        
        return str(result_file)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='运行三系统对比实验（期末作业版）')
    parser.add_argument('--num-questions', type=int, default=30,
                       help='测试问题数量（默认30）')
    parser.add_argument('--config', type=str, default='configs/config.yaml',
                       help='系统配置文件')
    parser.add_argument('--skip-manual', action='store_true',
                       help='跳过人工评估')
    parser.add_argument('--output-dir', type=str, default=None,
                       help='输出目录')
    
    args = parser.parse_args()
    
    try:
        # 创建实验
        experiment = SimpleComparisonExperiment(args.config)
        
        # 运行所有配置
        experiment.run_all_configurations(args.num_questions)
        
        # 打印对比
        experiment.print_comparison()
        
        # 保存结果
        result_file = experiment.save_results(args.output_dir)
        
        # 完成提示
        print(f"\n{'='*70}")
        print(" "*25 + "✅ 实验完成！")
        print(f"{'='*70}")
        print(f"\n📁 结果文件: {result_file}")
        print(f"\n📝 下一步:")
        print(f"   1. 查看详细结果: cat {result_file}")
        print(f"   2. 生成可视化: python evaluation/scripts/visualize_comparison.py {result_file}")
        
        if not args.skip_manual:
            print(f"   3. 进行人工评估: python evaluation/scripts/manual_evaluation.py {result_file}")
        
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
