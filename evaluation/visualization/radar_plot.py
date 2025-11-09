#!/usr/bin/env python3
"""
雷达图生成器 - 生成多维度性能对比雷达图

用途：
1. 可视化多个指标的性能对比
2. 论文中的重要图表
3. 直观展示系统优势

使用方法：
    from evaluation.visualization import create_radar_plot
    create_radar_plot(results, "output.png")
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, RegularPolygon
from matplotlib.path import Path
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D
from typing import Dict, List, Tuple
import json


def radar_factory(num_vars, frame='circle'):
    """
    创建雷达图坐标系
    
    Args:
        num_vars: 变量数量
        frame: 框架类型 ('circle', 'polygon')
    
    Returns:
        theta: 角度数组
        RadarAxes: 雷达图坐标类
    """
    theta = np.linspace(0, 2*np.pi, num_vars, endpoint=False)
    
    class RadarAxes(PolarAxes):
        name = 'radar'
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.set_theta_zero_location('N')
        
        def fill(self, *args, closed=True, **kwargs):
            return super().fill(closed=closed, *args, **kwargs)
        
        def plot(self, *args, **kwargs):
            lines = super().plot(*args, **kwargs)
            for line in lines:
                self._close_line(line)
        
        def _close_line(self, line):
            x, y = line.get_data()
            if x[0] != x[-1]:
                x = np.append(x, x[0])
                y = np.append(y, y[0])
                line.set_data(x, y)
        
        def set_varlabels(self, labels):
            self.set_thetagrids(np.degrees(theta), labels)
        
        def _gen_axes_patch(self):
            if frame == 'circle':
                return Circle((0.5, 0.5), 0.5)
            elif frame == 'polygon':
                return RegularPolygon((0.5, 0.5), num_vars,
                                     radius=.5, edgecolor="k")
            else:
                raise ValueError("Unknown value for 'frame': %s" % frame)
        
        def _gen_axes_spines(self):
            if frame == 'circle':
                return super()._gen_axes_spines()
            elif frame == 'polygon':
                spine = Spine(axes=self,
                            spine_type='circle',
                            path=Path.unit_regular_polygon(num_vars))
                spine.set_transform(Affine2D().scale(.5).translate(.5, .5)
                                  + self.transAxes)
                return {'polar': spine}
            else:
                raise ValueError("Unknown value for 'frame': %s" % frame)
    
    register_projection(RadarAxes)
    return theta, RadarAxes


def create_radar_plot(
    results: Dict,
    output_file: str,
    metrics: List[str] = None,
    title: str = "系统性能对比",
    figsize: Tuple[int, int] = (10, 8)
):
    """
    创建雷达图
    
    Args:
        results: 评估结果字典 (从comparison.json加载)
        output_file: 输出图片文件路径
        metrics: 要显示的指标列表，None表示使用默认指标
        title: 图表标题
        figsize: 图表大小
    """
    # 默认指标
    if metrics is None:
        metrics = [
            '共情', '支持', '指导', '相关性', 
            '沟通', '流畅性', '安全性'
        ]
    
    # 提取数据
    data_dict = {}
    
    # 映射英文指标名到中文
    metric_mapping = {
        '共情': 'empathy',
        '支持': 'support',
        '指导': 'guidance',
        '相关性': 'relevance',
        '沟通': 'communication',
        '流畅性': 'fluency',
        '安全性': 'safety'
    }
    
    configs = {
        '裸LLM': 'baseline',
        'LLM+RAG': 'rag_only',
        '完整系统': 'full_system'
    }
    
    for config_name, config_key in configs.items():
        if config_key in results.get('results', {}):
            clinical = results['results'][config_key]['results'].get('clinical_metrics', {})
            data_dict[config_name] = [
                clinical.get(metric_mapping[m], 0) for m in metrics
            ]
    
    # 创建雷达图
    num_vars = len(metrics)
    theta, RadarAxes = radar_factory(num_vars, frame='polygon')
    
    fig, ax = plt.subplots(figsize=figsize, subplot_kw=dict(projection='radar'))
    fig.subplots_adjust(top=0.85, bottom=0.05)
    
    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    
    # 颜色和样式
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
    linestyles = ['-', '--', '-.']
    markers = ['o', 's', '^']
    
    # 绘制数据
    for idx, (config_name, values) in enumerate(data_dict.items()):
        ax.plot(theta, values, 
               color=colors[idx],
               linestyle=linestyles[idx],
               marker=markers[idx],
               linewidth=2,
               markersize=8,
               label=config_name)
        ax.fill(theta, values, alpha=0.15, color=colors[idx])
    
    # 设置标签
    ax.set_varlabels(metrics)
    
    # 设置刻度范围
    ax.set_ylim(0, 5)
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_yticklabels(['1', '2', '3', '4', '5'])
    
    # 添加网格
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # 添加标题和图例
    plt.title(title, size=16, weight='bold', pad=20)
    plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0), fontsize=12)
    
    # 保存图片
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✓ 雷达图已保存: {output_file}")


def create_radar_plot_from_file(result_file: str, output_file: str, **kwargs):
    """
    从JSON文件创建雷达图
    
    Args:
        result_file: 评估结果JSON文件路径
        output_file: 输出图片文件路径
        **kwargs: 传递给create_radar_plot的其他参数
    """
    with open(result_file, 'r', encoding='utf-8') as f:
        results = json.load(f)
    
    create_radar_plot(results, output_file, **kwargs)


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 3:
        print("用法: python radar_plot.py <result.json> <output.png>")
        sys.exit(1)
    
    result_file = sys.argv[1]
    output_file = sys.argv[2]
    
    create_radar_plot_from_file(result_file, output_file)
    print(f"\n✓ 雷达图生成完成: {output_file}")
