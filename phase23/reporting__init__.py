"""
报告生成模块 - 生成论文用的报告和数据导出

包含：
- generate_latex_report: LaTeX报告生成器
- data_exporter: 数据导出工具（CSV, Excel, TXT）

使用示例：
    from evaluation.reporting import LaTeXReportGenerator, DataExporter
    
    # 生成LaTeX报告
    generator = LaTeXReportGenerator("result.json")
    generator.save("report.tex")
    
    # 导出数据
    exporter = DataExporter("result.json")
    exporter.export_to_excel("data.xlsx")
"""

from .generate_latex_report import LaTeXReportGenerator
from .data_exporter import DataExporter

__all__ = [
    'LaTeXReportGenerator',
    'DataExporter'
]

__version__ = '1.0.0'
