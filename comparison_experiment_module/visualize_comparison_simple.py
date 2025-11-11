#!/usr/bin/env python3
"""
对比实验可视化脚本 - 期末作业版
生成各种对比图表，用于论文

使用方法:
    python evaluation/scripts/visualize_comparison_simple.py <结果文件路径>
    
示例:
    python evaluation/scripts/visualize_comparison_simple.py evaluation/results/comparison/comparison_20251111_120000.json
"""

import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

# 设置中文字体
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False

# 添加项目路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


class ComparisonVisualizer:
    """对比实验可视化器"""
    
    def __init__(self, results_file: str):
        """初始化"""
        print(f"\n📊 加载结果文件: {results_file}")
        
        with open(results_file, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        
        self.results = self.data['results']
        self.metadata = self.data['metadata']
        
        # 输出目录
        self.output_dir = Path(results_file).parent / "figures"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"✓ 数据加载完成")
        print(f"✓ 图表将保存至: {self.output_dir}")
    
    def plot_response_time_comparison(self):
        """绘制响应时间对比柱状图"""
        print("\n📈 生成响应时间对比图...")
        
        configs = ['baseline', 'rag_only', 'full_system']
        config_names = [
            self.results[c]['config_desc'] 
            for c in configs
        ]
        
        avg_times = [
            self.results[c]['statistics']['avg_response_time']
            for c in configs
        ]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        bars = ax.bar(config_names, avg_times, 
                     color=['#ff9999', '#66b3ff', '#99ff99'],
                     alpha=0.8, edgecolor='black', linewidth=1.5)
        
        # 添加数值标签
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.2f}s',
                   ha='center', va='bottom', fontsize=12, fontweight='bold')
        
        ax.set_ylabel('Average Response Time (seconds)', fontsize=12, fontweight='bold')
        ax.set_title('Response Time Comparison Across Three Configurations', fontsize=14, fontweight='bold', pad=20)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        
        plt.tight_layout()
        output_file = self.output_dir / "response_time_comparison.png"
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"  ✓ Saved: {output_file}")
        return str(output_file)
    
    def plot_response_length_comparison(self):
        """绘制回复长度对比柱状图"""
        print("\n📈 生成回复长度对比图...")
        
        configs = ['baseline', 'rag_only', 'full_system']
        config_names = [
            self.results[c]['config_desc'] 
            for c in configs
        ]
        
        avg_lengths = [
            self.results[c]['statistics']['avg_response_length']
            for c in configs
        ]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        bars = ax.bar(config_names, avg_lengths,
                     color=['#ffcc99', '#99ccff', '#ccff99'],
                     alpha=0.8, edgecolor='black', linewidth=1.5)
        
        # 添加数值标签
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', fontsize=12, fontweight='bold')
        
        ax.set_ylabel('Average Response Length (characters)', fontsize=12, fontweight='bold')
        ax.set_title('Response Length Comparison Across Three Configurations', fontsize=14, fontweight='bold', pad=20)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        
        plt.tight_layout()
        output_file = self.output_dir / "response_length_comparison.png"
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"  ✓ Saved: {output_file}")
        return str(output_file)
    
    def plot_response_time_distribution(self):
        """绘制响应时间分布箱线图"""
        print("\n📈 生成响应时间分布图...")
        
        configs = ['baseline', 'rag_only', 'full_system']
        config_names = [
            self.results[c]['config_desc'] 
            for c in configs
        ]
        
        # 提取每个配置的所有响应时间
        time_distributions = []
        for c in configs:
            times = [
                r['response_time'] 
                for r in self.results[c]['responses']
                if r['response_time'] > 0
            ]
            time_distributions.append(times)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        bp = ax.boxplot(time_distributions, labels=config_names,
                       patch_artist=True,
                       boxprops=dict(facecolor='lightblue', alpha=0.7),
                       medianprops=dict(color='red', linewidth=2),
                       whiskerprops=dict(linewidth=1.5),
                       capprops=dict(linewidth=1.5))
        
        # 为每个箱子设置不同颜色
        colors = ['#ff9999', '#66b3ff', '#99ff99']
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
        
        ax.set_ylabel('Response Time (seconds)', fontsize=12, fontweight='bold')
        ax.set_title('Response Time Distribution', fontsize=14, fontweight='bold', pad=20)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        
        plt.tight_layout()
        output_file = self.output_dir / "response_time_distribution.png"
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"  ✓ Saved: {output_file}")
        return str(output_file)
    
    def plot_category_analysis(self):
        """按问题类别分析响应情况"""
        print("\n📈 生成类别分析图...")
        
        # 收集各类别的数据
        categories = set()
        for config in ['baseline', 'rag_only', 'full_system']:
            for response in self.results[config]['responses']:
                if 'category' in response:
                    categories.add(response['category'])
        
        if not categories:
            print("  ⚠️  No category information found, skipping...")
            return None
        
        categories = sorted(list(categories))
        
        # 计算每个类别在每个配置下的平均响应时间
        category_times = {cat: [] for cat in categories}
        
        for config in ['baseline', 'rag_only', 'full_system']:
            for cat in categories:
                cat_responses = [
                    r['response_time'] 
                    for r in self.results[config]['responses']
                    if r.get('category') == cat and r['response_time'] > 0
                ]
                avg_time = sum(cat_responses) / len(cat_responses) if cat_responses else 0
                category_times[cat].append(avg_time)
        
        # 绘图
        fig, ax = plt.subplots(figsize=(14, 6))
        
        x = np.arange(len(categories))
        width = 0.25
        
        config_names = ['Baseline LLM', 'LLM+RAG', 'Full System']
        colors = ['#ff9999', '#66b3ff', '#99ff99']
        
        for i, config_name in enumerate(config_names):
            values = [category_times[cat][i] for cat in categories]
            ax.bar(x + i*width, values, width, 
                  label=config_name, color=colors[i], alpha=0.8)
        
        ax.set_xlabel('Question Category', fontsize=12, fontweight='bold')
        ax.set_ylabel('Average Response Time (seconds)', fontsize=12, fontweight='bold')
        ax.set_title('Response Time by Question Category', fontsize=14, fontweight='bold', pad=20)
        ax.set_xticks(x + width)
        ax.set_xticklabels(categories, rotation=45, ha='right')
        ax.legend()
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        
        plt.tight_layout()
        output_file = self.output_dir / "category_analysis.png"
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"  ✓ Saved: {output_file}")
        return str(output_file)
    
    def plot_summary_comparison(self):
        """绘制综合对比图"""
        print("\n📈 生成综合对比图...")
        
        configs = ['baseline', 'rag_only', 'full_system']
        config_names = [self.results[c]['config_desc'] for c in configs]
        
        # 准备数据
        metrics = {
            'Avg Time (s)': [self.results[c]['statistics']['avg_response_time'] for c in configs],
            'Avg Length': [self.results[c]['statistics']['avg_response_length'] / 100 for c in configs],  # 归一化
            'Success Rate (%)': [
                self.results[c]['statistics']['successful_responses'] / 
                self.results[c]['statistics']['total_questions'] * 100 
                for c in configs
            ]
        }
        
        # 创建子图
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        colors = ['#ff9999', '#66b3ff', '#99ff99']
        
        for idx, (metric_name, values) in enumerate(metrics.items()):
            ax = axes[idx]
            bars = ax.bar(config_names, values, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
            
            # 添加数值标签
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.2f}',
                       ha='center', va='bottom', fontsize=10, fontweight='bold')
            
            ax.set_title(metric_name, fontsize=12, fontweight='bold')
            ax.grid(axis='y', alpha=0.3, linestyle='--')
            ax.set_xticklabels(config_names, rotation=15, ha='right')
        
        plt.suptitle('Comprehensive Comparison', fontsize=14, fontweight='bold', y=1.02)
        plt.tight_layout()
        
        output_file = self.output_dir / "summary_comparison.png"
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"  ✓ Saved: {output_file}")
        return str(output_file)
    
    def generate_all_figures(self):
        """生成所有图表"""
        print(f"\n{'='*70}")
        print(" "*20 + "🎨 Generating Visualizations")
        print(f"{'='*70}")
        
        generated_files = []
        
        file1 = self.plot_response_time_comparison()
        if file1: generated_files.append(file1)
        
        file2 = self.plot_response_length_comparison()
        if file2: generated_files.append(file2)
        
        file3 = self.plot_response_time_distribution()
        if file3: generated_files.append(file3)
        
        file4 = self.plot_category_analysis()
        if file4: generated_files.append(file4)
        
        file5 = self.plot_summary_comparison()
        if file5: generated_files.append(file5)
        
        print(f"\n{'='*70}")
        print(" "*20 + "✅ All Figures Generated!")
        print(f"{'='*70}")
        print(f"\n📁 Output Directory: {self.output_dir}")
        print(f"\nGenerated {len(generated_files)} figures:")
        for i, file in enumerate(generated_files, 1):
            print(f"  {i}. {Path(file).name}")
        
        return generated_files


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='Generate comparison visualizations')
    parser.add_argument('results_file', type=str,
                       help='Path to experiment results JSON file')
    
    args = parser.parse_args()
    
    try:
        # 创建可视化器
        visualizer = ComparisonVisualizer(args.results_file)
        
        # 生成所有图表
        files = visualizer.generate_all_figures()
        
        print(f"\n💡 Tip:")
        print(f"   These figures are ready for your paper/report")
        print(f"   Format: PNG, Resolution: 300 DPI")
        
    except Exception as e:
        print(f"\n✗ Generation failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
