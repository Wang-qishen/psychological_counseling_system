#!/usr/bin/env python3
"""
柱状图生成器 - 生成指标对比柱状图

用途：
1. 对比不同系统配置的性能
2. 论文中的重要图表
3. 清晰展示改进幅度

使用方法：
    from evaluation.visualization import create_bar_plot
    create_bar_plot(results, "output.png")
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple
import json


def create_bar_plot(
    results: Dict,
    output_file: str,
    metric_type: str = 'clinical',
    title: str = None,
    figsize: Tuple[int, int] = (12, 6)
):
    """
    创建柱状图
    
    Args:
        results: 评估结果字典
        output_file: 输出图片文件路径
        metric_type: 指标类型 ('clinical', 'technical', 'all')
        title: 图表标题，None表示自动生成
        figsize: 图表大小
    """
    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    
    # 准备数据
    configs = {
        '裸LLM': 'baseline',
        'LLM+RAG': 'rag_only',
        '完整系统': 'full_system'
    }
    
    if metric_type == 'clinical':
        metrics = {
            '共情': 'empathy',
            '支持': 'support',
            '指导': 'guidance',
            '相关性': 'relevance',
            '沟通': 'communication',
            '流畅性': 'fluency',
            '安全性': 'safety'
        }
        default_title = "临床指标对比"
        y_label = "评分 (1-5)"
        y_max = 5.5
    elif metric_type == 'technical':
        metrics = {
            'BERT F1': ('bert_score', 'f1'),
            'ROUGE-L': ('rouge', 'rougeL'),
            'BLEU': 'bleu'
        }
        default_title = "技术指标对比"
        y_label = "分数"
        y_max = 1.0
    else:  # all
        # 组合所有指标
        metrics = {
            '共情': 'empathy',
            '支持': 'support',
            'BERT F1': ('bert_score', 'f1'),
            'ROUGE-L': ('rouge', 'rougeL')
        }
        default_title = "综合指标对比"
        y_label = "分数"
        y_max = 5.5
    
    if title is None:
        title = default_title
    
    # 提取数据
    data = {config_name: [] for config_name in configs.keys()}
    
    for metric_name, metric_key in metrics.items():
        for config_name, config_id in configs.items():
            if config_id in results.get('results', {}):
                if metric_type == 'clinical':
                    score = results['results'][config_id]['results'].get(
                        'clinical_metrics', {}
                    ).get(metric_key, 0)
                elif metric_type == 'technical':
                    tech_metrics = results['results'][config_id]['results'].get(
                        'technical_metrics', {}
                    )
                    if isinstance(metric_key, tuple):
                        score = tech_metrics.get(metric_key[0], {}).get(metric_key[1], 0)
                    else:
                        score = tech_metrics.get(metric_key, 0)
                else:  # all
                    if metric_name in ['共情', '支持']:
                        score = results['results'][config_id]['results'].get(
                            'clinical_metrics', {}
                        ).get(metric_key, 0)
                    else:
                        tech_metrics = results['results'][config_id]['results'].get(
                            'technical_metrics', {}
                        )
                        if isinstance(metric_key, tuple):
                            score = tech_metrics.get(metric_key[0], {}).get(metric_key[1], 0)
                        else:
                            score = tech_metrics.get(metric_key, 0)
                
                data[config_name].append(score)
            else:
                data[config_name].append(0)
    
    # 创建图表
    fig, ax = plt.subplots(figsize=figsize)
    
    # 设置位置
    x = np.arange(len(metrics))
    width = 0.25
    
    # 颜色
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
    
    # 绘制柱状图
    for idx, (config_name, values) in enumerate(data.items()):
        offset = width * (idx - 1)
        bars = ax.bar(x + offset, values, width, 
                     label=config_name, 
                     color=colors[idx],
                     alpha=0.8,
                     edgecolor='black',
                     linewidth=0.5)
        
        # 添加数值标签
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.2f}',
                   ha='center', va='bottom', fontsize=9)
    
    # 设置标签
    ax.set_xlabel('指标', fontsize=12, weight='bold')
    ax.set_ylabel(y_label, fontsize=12, weight='bold')
    ax.set_title(title, fontsize=14, weight='bold', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(metrics.keys(), fontsize=10)
    ax.legend(fontsize=11, loc='upper left')
    
    # 设置y轴范围
    ax.set_ylim(0, y_max)
    
    # 添加网格
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    ax.set_axisbelow(True)
    
    # 保存图片
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✓ 柱状图已保存: {output_file}")


def create_improvement_bar_plot(
    results: Dict,
    output_file: str,
    title: str = "完整系统相比裸LLM的改进幅度",
    figsize: Tuple[int, int] = (12, 6)
):
    """
    创建改进幅度柱状图
    
    Args:
        results: 评估结果字典
        output_file: 输出图片文件路径
        title: 图表标题
        figsize: 图表大小
    """
    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    
    # 从结果中获取改进数据
    improvements = results.get('improvements', {})
    
    if not improvements:
        print("⚠️  结果中没有改进数据")
        return
    
    # 准备数据
    metric_names_cn = {
        'bert_f1': 'BERT F1',
        'rouge_l': 'ROUGE-L',
        'bleu': 'BLEU',
        'empathy': '共情',
        'support': '支持',
        'guidance': '指导',
        'relevance': '相关性',
        'communication': '沟通',
        'fluency': '流畅性'
    }
    
    labels = []
    values = []
    colors_list = []
    
    for metric_key, improvement in improvements.items():
        if metric_key in metric_names_cn:
            labels.append(metric_names_cn[metric_key])
            values.append(improvement)
            # 正值用绿色，负值用红色
            colors_list.append('#2ca02c' if improvement > 0 else '#d62728')
    
    # 创建图表
    fig, ax = plt.subplots(figsize=figsize)
    
    # 绘制柱状图
    bars = ax.barh(range(len(labels)), values, 
                   color=colors_list, 
                   alpha=0.8,
                   edgecolor='black',
                   linewidth=0.5)
    
    # 添加数值标签
    for idx, (bar, value) in enumerate(zip(bars, values)):
        width = bar.get_width()
        label_x_pos = width + (0.5 if width > 0 else -0.5)
        ax.text(label_x_pos, bar.get_y() + bar.get_height()/2,
               f'{value:+.2f}%',
               ha='left' if width > 0 else 'right',
               va='center',
               fontsize=10,
               weight='bold')
    
    # 设置标签
    ax.set_yticks(range(len(labels)))
    ax.set_yticklabels(labels, fontsize=11)
    ax.set_xlabel('改进幅度 (%)', fontsize=12, weight='bold')
    ax.set_title(title, fontsize=14, weight='bold', pad=15)
    
    # 添加零线
    ax.axvline(x=0, color='black', linewidth=1, linestyle='-')
    
    # 添加网格
    ax.grid(axis='x', linestyle='--', alpha=0.3)
    ax.set_axisbelow(True)
    
    # 保存图片
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✓ 改进幅度柱状图已保存: {output_file}")


def create_bar_plot_from_file(
    result_file: str,
    output_file: str,
    metric_type: str = 'clinical',
    **kwargs
):
    """
    从JSON文件创建柱状图
    
    Args:
        result_file: 评估结果JSON文件路径
        output_file: 输出图片文件路径
        metric_type: 指标类型
        **kwargs: 传递给create_bar_plot的其他参数
    """
    with open(result_file, 'r', encoding='utf-8') as f:
        results = json.load(f)
    
    if metric_type == 'improvement':
        create_improvement_bar_plot(results, output_file, **kwargs)
    else:
        create_bar_plot(results, output_file, metric_type, **kwargs)


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 3:
        print("用法: python bar_plot.py <result.json> <output.png> [metric_type]")
        print("metric_type: clinical, technical, improvement")
        sys.exit(1)
    
    result_file = sys.argv[1]
    output_file = sys.argv[2]
    metric_type = sys.argv[3] if len(sys.argv) > 3 else 'clinical'
    
    create_bar_plot_from_file(result_file, output_file, metric_type)
    print(f"\n✓ 柱状图生成完成: {output_file}")
