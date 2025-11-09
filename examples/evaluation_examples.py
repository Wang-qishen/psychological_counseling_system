#!/usr/bin/env python3
"""
评估模块使用示例
位置: psychological_counseling_system/examples/evaluation_examples.py

展示评估模块的各种使用方法

目录:
1. 基础评估示例
2. 自定义配置评估
3. 对比实验示例
4. 单独指标评估
5. 批量评估示例
"""

import sys
from pathlib import Path
import yaml

# 添加项目路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from evaluation import EvaluationFramework
from dialogue import DialogueManager


def example_1_basic_evaluation():
    """
    示例1: 基础评估
    
    最简单的使用方式，使用默认配置
    """
    print("\n" + "="*70)
    print("示例1: 基础评估")
    print("="*70)
    
    # 1. 初始化系统
    dialogue_manager = DialogueManager()
    
    # 2. 创建评估框架
    evaluator = EvaluationFramework(
        dialogue_manager=dialogue_manager,
        data_dir="./data",
        output_dir="./evaluation/results"
    )
    
    # 3. 运行快速测试（10个样本）
    print("\n运行快速测试...")
    results = evaluator.quick_test(num_samples=10)
    
    # 4. 查看结果
    print("\n结果:")
    if 'technical' in results and 'bert_score' in results['technical']:
        bert = results['technical']['bert_score']
        print(f"  BERT Score F1: {bert['f1']:.3f}")
    
    if 'clinical' in results:
        print(f"  Clinical Average: {results['clinical'].get('overall', 0):.2f}/5")
    
    print("\n✓ 示例1完成")


def example_2_custom_config():
    """
    示例2: 自定义配置评估
    
    使用自定义配置进行评估
    """
    print("\n" + "="*70)
    print("示例2: 自定义配置评估")
    print("="*70)
    
    # 1. 加载自定义配置
    with open("configs/config.yaml") as f:
        config = yaml.safe_load(f)
    
    # 2. 初始化系统
    dialogue_manager = DialogueManager(config=config)
    
    # 3. 创建评估框架
    evaluator = EvaluationFramework(
        dialogue_manager=dialogue_manager
    )
    
    # 4. 运行完整评估（200个样本）
    print("\n运行完整评估...")
    results = evaluator.run_full_evaluation(
        dataset="mentalchat",
        num_test_samples=200,
        clinical_sample_size=50,
        generate_memory_tests=True
    )
    
    # 5. 查看详细结果
    print("\n详细结果:")
    print(f"  技术指标: {results.get('technical', {})}")
    print(f"  专业质量: {results.get('clinical', {})}")
    print(f"  记忆系统: {results.get('memory', {})}")
    print(f"  RAG效果: {results.get('rag', {})}")
    
    print("\n✓ 示例2完成")


def example_3_comparison_experiment():
    """
    示例3: 对比实验
    
    对比三种系统配置的效果
    """
    print("\n" + "="*70)
    print("示例3: 对比实验")
    print("="*70)
    
    # 1. 加载三种配置
    print("\n1. 加载配置...")
    
    # 裸LLM配置（无RAG、无记忆）
    bare_config = {
        'llm': {
            'model_type': 'openai_api',
            'model_name': 'gpt-3.5-turbo'
        },
        'rag': {
            'enabled': False
        },
        'memory': {
            'enabled': False
        }
    }
    
    # LLM+RAG配置（有RAG、无记忆）
    rag_config = {
        'llm': {
            'model_type': 'openai_api',
            'model_name': 'gpt-3.5-turbo'
        },
        'rag': {
            'enabled': True,
            'vector_db_type': 'chroma',
            'top_k': 3
        },
        'memory': {
            'enabled': False
        }
    }
    
    # 完整系统配置（RAG+记忆）
    full_config = {
        'llm': {
            'model_type': 'openai_api',
            'model_name': 'gpt-3.5-turbo'
        },
        'rag': {
            'enabled': True,
            'vector_db_type': 'chroma',
            'top_k': 3
        },
        'memory': {
            'enabled': True,
            'short_term_capacity': 5,
            'working_memory_capacity': 10,
            'long_term_capacity': 50
        }
    }
    
    # 2. 创建三个系统
    print("\n2. 初始化三个系统...")
    bare_llm = DialogueManager(config=bare_config)
    llm_rag = DialogueManager(config=rag_config)
    full_system = DialogueManager(config=full_config)
    
    # 3. 创建评估框架
    evaluator = EvaluationFramework()
    
    # 4. 运行对比评估
    print("\n3. 运行对比评估...")
    comparison_results = evaluator.run_comparison_evaluation(
        bare_llm_manager=bare_llm,
        llm_rag_manager=llm_rag,
        full_system_manager=full_system,
        dataset="mentalchat",
        num_test_samples=100
    )
    
    # 5. 显示对比结果
    print("\n4. 对比结果:")
    print("\n技术指标对比:")
    for system, scores in comparison_results.get('technical_scores', {}).items():
        print(f"\n  {system}:")
        print(f"    BERT Score: {scores.get('bert_score', 0):.3f}")
        print(f"    ROUGE-L:    {scores.get('rouge_l', 0):.3f}")
    
    print("\n专业质量对比:")
    for system, scores in comparison_results.get('clinical_scores', {}).items():
        print(f"  {system}: {scores.get('overall', 0):.2f}/5")
    
    print("\n✓ 示例3完成")


def example_4_individual_metrics():
    """
    示例4: 单独指标评估
    
    只评估特定的指标
    """
    print("\n" + "="*70)
    print("示例4: 单独指标评估")
    print("="*70)
    
    from evaluation.metrics import (
        TechnicalMetrics,
        ClinicalMetrics,
        MemoryMetrics
    )
    
    # 1. 准备测试数据
    predictions = [
        "我理解你现在的心情，让我们一起来分析这个问题...",
        "这是一个很常见的情况，我们可以尝试以下方法..."
    ]
    references = [
        "理解你的感受，我们可以一起探讨...",
        "这种情况确实比较常见，建议你可以..."
    ]
    
    # 2. 评估技术指标
    print("\n1. 技术指标:")
    tech_metrics = TechnicalMetrics(device="cpu")
    
    bert_scores = tech_metrics.compute_bert_score(predictions, references)
    print(f"  BERT Score F1: {bert_scores['f1']:.3f}")
    
    rouge_scores = tech_metrics.compute_rouge(predictions, references)
    print(f"  ROUGE-L: {rouge_scores['rougeL']:.3f}")
    
    # 3. 评估临床指标
    print("\n2. 临床指标:")
    clinical_metrics = ClinicalMetrics()
    
    # 注意: 需要LLM评分器
    # clinical_scores = clinical_metrics.evaluate_response(
    #     question="我最近感到很焦虑",
    #     response=predictions[0]
    # )
    # print(f"  Empathy: {clinical_scores['empathy']:.2f}/5")
    print("  (需要LLM评分器)")
    
    # 4. 评估记忆系统
    print("\n3. 记忆系统:")
    memory_metrics = MemoryMetrics()
    
    # 准备记忆测试数据
    conversation_history = [
        {"role": "user", "content": "我叫张三，是一名程序员"},
        {"role": "assistant", "content": "你好张三，很高兴认识你"},
        {"role": "user", "content": "你还记得我的名字吗？"},
    ]
    
    # 评估记忆召回
    # recall_score = memory_metrics.test_recall(conversation_history)
    # print(f"  记忆召回率: {recall_score:.2%}")
    print("  (需要完整系统)")
    
    print("\n✓ 示例4完成")


def example_5_batch_evaluation():
    """
    示例5: 批量评估
    
    对多个配置进行批量评估
    """
    print("\n" + "="*70)
    print("示例5: 批量评估")
    print("="*70)
    
    # 1. 定义多个配置
    configs = {
        "config_v1": {
            'llm': {'model_name': 'gpt-3.5-turbo'},
            'rag': {'top_k': 3}
        },
        "config_v2": {
            'llm': {'model_name': 'gpt-3.5-turbo'},
            'rag': {'top_k': 5}
        },
        "config_v3": {
            'llm': {'model_name': 'gpt-4'},
            'rag': {'top_k': 3}
        }
    }
    
    # 2. 批量评估
    results = {}
    
    for config_name, config in configs.items():
        print(f"\n评估配置: {config_name}")
        
        # 创建系统
        manager = DialogueManager(config=config)
        
        # 创建评估器
        evaluator = EvaluationFramework(
            dialogue_manager=manager,
            output_dir=f"./evaluation/results/{config_name}"
        )
        
        # 快速测试
        result = evaluator.quick_test(num_samples=10)
        results[config_name] = result
        
        # 显示结果
        if 'technical' in result:
            bert = result['technical'].get('bert_score', {})
            print(f"  BERT Score: {bert.get('f1', 0):.3f}")
    
    # 3. 对比所有配置
    print("\n" + "-"*70)
    print("批量评估总结:")
    print("-"*70)
    
    for config_name, result in results.items():
        bert_score = 0
        if 'technical' in result:
            bert_score = result['technical'].get('bert_score', {}).get('f1', 0)
        
        print(f"  {config_name:15s} BERT: {bert_score:.3f}")
    
    print("\n✓ 示例5完成")


def main():
    """运行所有示例"""
    print("\n" + "="*70)
    print(" "*15 + "评估模块使用示例")
    print("="*70)
    
    print("\n可用示例:")
    print("  1. 基础评估")
    print("  2. 自定义配置评估")
    print("  3. 对比实验")
    print("  4. 单独指标评估")
    print("  5. 批量评估")
    
    choice = input("\n请选择要运行的示例 (1-5, 或 'all'): ").strip().lower()
    
    if choice == '1':
        example_1_basic_evaluation()
    elif choice == '2':
        example_2_custom_config()
    elif choice == '3':
        example_3_comparison_experiment()
    elif choice == '4':
        example_4_individual_metrics()
    elif choice == '5':
        example_5_batch_evaluation()
    elif choice == 'all':
        print("\n运行所有示例...")
        example_1_basic_evaluation()
        example_2_custom_config()
        example_3_comparison_experiment()
        example_4_individual_metrics()
        example_5_batch_evaluation()
    else:
        print("\n无效选择")
        return
    
    print("\n" + "="*70)
    print(" "*20 + "所有示例运行完成！")
    print("="*70)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程序被用户中断")
    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()
