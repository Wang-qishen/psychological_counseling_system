#!/usr/bin/env python3
"""
快速测试脚本
位置: psychological_counseling_system/evaluation/scripts/run_quick_test.py

快速验证系统功能，10个样本，5分钟完成

使用方法:
    python evaluation/scripts/run_quick_test.py
    
    # 指定样本数
    python evaluation/scripts/run_quick_test.py --samples 20
    
    # 指定配置文件
    python evaluation/scripts/run_quick_test.py --config evaluation/configs/quick_test_config.yaml
"""

import os
import sys
import argparse
import logging
import yaml
import json
from pathlib import Path
from datetime import datetime

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from evaluation import EvaluationFramework
from dialogue import create_dialogue_manager_from_config

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_config(config_file: str) -> dict:
    """加载配置文件"""
    with open(config_file, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def print_banner():
    """打印横幅"""
    print("\n" + "="*70)
    print(" "*20 + "快速测试 - 心理咨询系统评估")
    print("="*70)


def print_section(title: str):
    """打印章节标题"""
    print("\n" + "-"*70)
    print(f" {title}")
    print("-"*70)


def run_quick_test(
    config_file: str = None,
    num_samples: int = 10,
    save_results: bool = True
):
    """
    运行快速测试
    
    Args:
        config_file: 配置文件路径
        num_samples: 测试样本数
        save_results: 是否保存结果
    """
    print_banner()
    
    # 1. 加载配置
    print_section("1. 加载配置")
    
    if config_file is None:
        config_file = project_root / "configs" / "config.yaml"
    
    logger.info(f"配置文件: {config_file}")
    
    try:
        system_config = load_config(config_file)
        logger.info("✓ 系统配置加载成功")
    except Exception as e:
        logger.error(f"配置加载失败: {e}")
        return None
    
    # 加载评估配置
    eval_config_file = project_root / "evaluation" / "configs" / "quick_test_config.yaml"
    if eval_config_file.exists():
        eval_config = load_config(eval_config_file)
        logger.info("✓ 评估配置加载成功")
    else:
        eval_config = {}
        logger.warning("未找到评估配置，使用默认设置")
    
    # 2. 初始化系统
    print_section("2. 初始化系统")
    
    try:
        dialogue_manager = create_dialogue_manager_from_config(system_config)
        logger.info("✓ 对话管理器初始化成功")
    except Exception as e:
        logger.error(f"系统初始化失败: {e}")
        logger.error("请检查配置文件和依赖项")
        return None
    
    # 3. 创建评估框架
    print_section("3. 创建评估框架")
    
    data_dir = project_root / "data"
    output_dir = project_root / "evaluation" / "results" / "quick_test"
    
    evaluator = EvaluationFramework(
        dialogue_manager=dialogue_manager,
        data_dir=str(data_dir),
        output_dir=str(output_dir)
    )
    logger.info("✓ 评估框架创建成功")
    
    # 4. 准备测试数据
    print_section("4. 准备测试数据")
    
    logger.info(f"加载 MentalChat16K 数据集（{num_samples}个样本）...")
    
    try:
        eval_set = evaluator.load_mentalchat_dataset(num_test_samples=num_samples)
        logger.info(f"✓ 成功加载 {len(eval_set['questions'])} 个测试问题")
    except Exception as e:
        logger.error(f"数据加载失败: {e}")
        logger.error("\n可能的解决方案:")
        logger.error("1. 运行数据集下载脚本:")
        logger.error("   python evaluation/datasets/download_datasets.py --dataset mentalchat")
        logger.error("2. 检查网络连接")
        return None
    
    # 5. 运行评估
    print_section("5. 运行评估")
    
    logger.info("开始评估...")
    logger.info("这可能需要几分钟，请耐心等待...")
    
    start_time = datetime.now()
    
    try:
        results = evaluator.quick_test(num_samples=num_samples)
        
        end_time = datetime.now()
        elapsed_time = (end_time - start_time).total_seconds()
        
        logger.info(f"✓ 评估完成！用时: {elapsed_time:.1f} 秒")
        
    except Exception as e:
        logger.error(f"评估失败: {e}")
        import traceback
        traceback.print_exc()
        return None
    
    # 6. 显示结果
    print_section("6. 测试结果")
    
    print("\n📊 技术指标:")
    if 'technical' in results:
        tech = results['technical']
        if 'bert_score' in tech:
            bert = tech['bert_score']
            print(f"  BERT Score F1:  {bert.get('f1', 0):.3f}")
            print(f"  BERT Precision: {bert.get('precision', 0):.3f}")
            print(f"  BERT Recall:    {bert.get('recall', 0):.3f}")
        
        if 'rouge' in tech:
            rouge = tech['rouge']
            print(f"  ROUGE-1:        {rouge.get('rouge1', 0):.3f}")
            print(f"  ROUGE-L:        {rouge.get('rougeL', 0):.3f}")
        
        if 'response_stats' in tech:
            stats = tech['response_stats']
            print(f"  平均响应时间:    {stats.get('avg_time', 0):.2f} 秒")
            print(f"  平均响应长度:    {stats.get('avg_length', 0):.0f} 字符")
    
    print("\n📋 专业质量:")
    if 'clinical' in results:
        clinical = results['clinical']
        if isinstance(clinical, dict):
            for dimension, score in clinical.items():
                if isinstance(score, (int, float)):
                    print(f"  {dimension.capitalize():15s} {score:.2f}/5")
    
    print("\n🧠 记忆系统:")
    if 'memory' in results:
        memory = results['memory']
        if isinstance(memory, dict):
            if 'short_term_recall' in memory:
                print(f"  短期记忆召回:    {memory['short_term_recall']:.2%}")
            if 'accuracy' in memory:
                print(f"  整体准确率:      {memory['accuracy']:.2%}")
    
    print("\n🔍 RAG效果:")
    if 'rag' in results:
        rag = results['rag']
        if isinstance(rag, dict):
            if 'recall' in rag:
                print(f"  检索召回率:      {rag['recall']:.2%}")
            if 'precision' in rag:
                print(f"  检索精确率:      {rag['precision']:.2%}")
    
    # 7. 保存结果
    if save_results:
        print_section("7. 保存结果")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = output_dir / f"quick_test_{timestamp}.json"
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✓ 结果已保存: {output_file}")
    
    # 总结
    print("\n" + "="*70)
    print(" "*25 + "测试完成！")
    print("="*70)
    print(f"\n✓ 测试样本数: {num_samples}")
    print(f"✓ 用时: {elapsed_time:.1f} 秒")
    if save_results:
        print(f"✓ 结果文件: {output_file}")
    
    print("\n📝 下一步:")
    print("  1. 查看详细结果: cat", output_file)
    print("  2. 运行完整评估: python evaluation/scripts/run_full_evaluation.py")
    print("  3. 运行对比实验: python evaluation/scripts/run_comparison.py")
    
    return results


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="快速测试脚本 - 验证系统功能"
    )
    parser.add_argument(
        "--config",
        default=None,
        help="系统配置文件路径"
    )
    parser.add_argument(
        "--samples",
        type=int,
        default=10,
        help="测试样本数 (默认: 10)"
    )
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="不保存结果"
    )
    
    args = parser.parse_args()
    
    try:
        results = run_quick_test(
            config_file=args.config,
            num_samples=args.samples,
            save_results=not args.no_save
        )
        
        if results is None:
            sys.exit(1)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  测试被用户中断")
        sys.exit(1)
    except Exception as e:
        logger.error(f"测试失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
