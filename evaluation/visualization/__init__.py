"""
可视化模块 - 生成论文用的图表

包含：
- radar_plot: 雷达图生成器
- bar_plot: 柱状图生成器

使用示例：
    from evaluation.visualization import create_radar_plot, create_bar_plot
    
    create_radar_plot(results, "radar.png")
    create_bar_plot(results, "bar.png")
"""

from .radar_plot import create_radar_plot, create_radar_plot_from_file
from .bar_plot import (
    create_bar_plot,
    create_improvement_bar_plot,
    create_bar_plot_from_file
)

__all__ = [
    'create_radar_plot',
    'create_radar_plot_from_file',
    'create_bar_plot',
    'create_improvement_bar_plot',
    'create_bar_plot_from_file'
]

__version__ = '1.0.0'
