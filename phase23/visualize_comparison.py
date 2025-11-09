#!/usr/bin/env python3
"""
可视化管理脚本 - 一键生成所有论文需要的图表

用途：
1. 自动生成雷达图、柱状图
2. 批量处理评估结果
3. 论文图表一站式生成

使用方法：
    python evaluation/scripts/visualize_comparison.py --result comparison.json
"""

import sys
import argparse
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# 导入可视化模块
from evaluation.visualization.radar_plot import create_radar_plot_from_file
from evaluation.visualization.bar_plot import create_bar_plot_from_file


def visualize_all(result_file: str, output_dir: str = None):
    """
    生成所有可视化图表
    
    Args:
        result_file: 评估结果JSON文件路径
        output_dir: 输出目录，None表示使用默认目录
    """
    print("\n" + "="*70)
    print(" "*20 + "生成可视化图表")
    print("="*70)
    
    # 确定输出目录
    if output_dir is None:
        result_path = Path(result_file)
        output_dir = result_path.parent / "figures"
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    print(f"\n输出目录: {output_path}")
    print()
    
    # 1. 雷达图
    print("1. 生成雷达图...")
    radar_file = output_path / "radar_comparison.png"
    try:
        create_radar_plot_from_file(
            result_file,
            str(radar_file),
            title="三种系统配置性能对比"
        )
    except Exception as e:
        print(f"   ✗ 雷达图生成失败: {e}")
    
    # 2. 临床指标柱状图
    print("\n2. 生成临床指标柱状图...")
    clinical_bar_file = output_path / "clinical_comparison.png"
    try:
        create_bar_plot_from_file(
            result_file,
            str(clinical_bar_file),
            metric_type='clinical'
        )
    except Exception as e:
        print(f"   ✗ 临床指标柱状图生成失败: {e}")
    
    # 3. 技术指标柱状图
    print("\n3. 生成技术指标柱状图...")
    tech_bar_file = output_path / "technical_comparison.png"
    try:
        create_bar_plot_from_file(
            result_file,
            str(tech_bar_file),
            metric_type='technical'
        )
    except Exception as e:
        print(f"   ✗ 技术指标柱状图生成失败: {e}")
    
    # 4. 改进幅度柱状图
    print("\n4. 生成改进幅度柱状图...")
    improvement_file = output_path / "improvement_comparison.png"
    try:
        create_bar_plot_from_file(
            result_file,
            str(improvement_file),
            metric_type='improvement'
        )
    except Exception as e:
        print(f"   ✗ 改进幅度柱状图生成失败: {e}")
    
    # 完成
    print("\n" + "="*70)
    print(" "*20 + "可视化生成完成！")
    print("="*70)
    
    print(f"\n✓ 图表已保存到: {output_path}")
    print("\n生成的图表:")
    print(f"  1. {radar_file.name} - 雷达图")
    print(f"  2. {clinical_bar_file.name} - 临床指标柱状图")
    print(f"  3. {tech_bar_file.name} - 技术指标柱状图")
    print(f"  4. {improvement_file.name} - 改进幅度柱状图")
    
    print("\n📝 下一步:")
    print("  1. 查看生成的图表")
    print("  2. 将图表插入论文")
    print("  3. 生成LaTeX报告: python evaluation/reporting/generate_latex_report.py")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='生成所有可视化图表')
    parser.add_argument('--result', type=str, required=True,
                       help='评估结果JSON文件路径')
    parser.add_argument('--output-dir', type=str, default=None,
                       help='输出目录（默认为结果文件同目录下的figures文件夹）')
    
    args = parser.parse_args()
    
    try:
        visualize_all(args.result, args.output_dir)
    except Exception as e:
        print(f"\n✗ 可视化生成失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
