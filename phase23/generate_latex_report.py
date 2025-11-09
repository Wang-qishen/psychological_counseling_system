#!/usr/bin/env python3
"""
LaTeX报告生成器 - 生成论文用的LaTeX表格和报告

用途：
1. 生成论文中使用的LaTeX表格
2. 格式化的实验结果
3. 可直接复制到论文中

使用方法：
    python evaluation/reporting/generate_latex_report.py --result comparison.json
"""

import json
import argparse
from pathlib import Path
from typing import Dict, List
from datetime import datetime


class LaTeXReportGenerator:
    """LaTeX报告生成器"""
    
    def __init__(self, result_file: str):
        """
        初始化生成器
        
        Args:
            result_file: 评估结果JSON文件路径
        """
        self.result_file = result_file
        
        with open(result_file, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
    
    def generate_comparison_table(self) -> str:
        """生成对比表格"""
        latex_lines = [
            "\\begin{table}[htbp]",
            "\\centering",
            "\\caption{三种系统配置的性能对比}",
            "\\label{tab:system_comparison}",
            "\\begin{tabular}{lcccc}",
            "\\hline",
            "\\textbf{指标} & \\textbf{裸LLM} & \\textbf{LLM+RAG} & \\textbf{完整系统} & \\textbf{改进\\%} \\\\",
            "\\hline"
        ]
        
        results = self.data.get('results', {})
        
        # 技术指标
        latex_lines.append("\\multicolumn{5}{l}{\\textit{技术指标}} \\\\")
        
        # BERT Score F1
        bert_values = self._extract_metric_values(
            'technical_metrics', 'bert_score', 'f1'
        )
        improvement = self._calculate_improvement(bert_values[0], bert_values[2])
        latex_lines.append(
            f"BERT Score F1 & {bert_values[0]:.3f} & {bert_values[1]:.3f} & "
            f"{bert_values[2]:.3f} & {improvement} \\\\"
        )
        
        # ROUGE-L
        rouge_values = self._extract_metric_values(
            'technical_metrics', 'rouge', 'rougeL'
        )
        improvement = self._calculate_improvement(rouge_values[0], rouge_values[2])
        latex_lines.append(
            f"ROUGE-L & {rouge_values[0]:.3f} & {rouge_values[1]:.3f} & "
            f"{rouge_values[2]:.3f} & {improvement} \\\\"
        )
        
        # BLEU
        bleu_values = self._extract_metric_values('technical_metrics', 'bleu')
        improvement = self._calculate_improvement(bleu_values[0], bleu_values[2])
        latex_lines.append(
            f"BLEU & {bleu_values[0]:.3f} & {bleu_values[1]:.3f} & "
            f"{bleu_values[2]:.3f} & {improvement} \\\\"
        )
        
        latex_lines.append("\\hline")
        
        # 临床指标
        latex_lines.append("\\multicolumn{5}{l}{\\textit{临床指标}} \\\\")
        
        clinical_metrics = {
            'empathy': '共情',
            'support': '支持',
            'guidance': '指导',
            'relevance': '相关性'
        }
        
        for metric_key, metric_name in clinical_metrics.items():
            values = self._extract_metric_values('clinical_metrics', metric_key)
            improvement = self._calculate_improvement(values[0], values[2])
            latex_lines.append(
                f"{metric_name} & {values[0]:.2f} & {values[1]:.2f} & "
                f"{values[2]:.2f} & {improvement} \\\\"
            )
        
        latex_lines.extend([
            "\\hline",
            "\\end{tabular}",
            "\\end{table}"
        ])
        
        return '\n'.join(latex_lines)
    
    def generate_memory_table(self) -> str:
        """生成记忆系统性能表格"""
        latex_lines = [
            "\\begin{table}[htbp]",
            "\\centering",
            "\\caption{记忆系统性能评估}",
            "\\label{tab:memory_performance}",
            "\\begin{tabular}{lc}",
            "\\hline",
            "\\textbf{指标} & \\textbf{性能} \\\\",
            "\\hline"
        ]
        
        results = self.data.get('results', {})
        
        if 'full_system' in results:
            memory = results['full_system']['results'].get('memory_metrics', {})
            
            metrics = {
                'short_term_recall': '短期记忆召回',
                'working_memory_accuracy': '工作记忆准确率',
                'long_term_consistency': '长期记忆一致性',
                'overall_accuracy': '整体准确率'
            }
            
            for metric_key, metric_name in metrics.items():
                value = memory.get(metric_key, 0) * 100
                latex_lines.append(f"{metric_name} & {value:.2f}\\% \\\\")
        
        latex_lines.extend([
            "\\hline",
            "\\end{tabular}",
            "\\end{table}"
        ])
        
        return '\n'.join(latex_lines)
    
    def generate_rag_table(self) -> str:
        """生成RAG效果表格"""
        latex_lines = [
            "\\begin{table}[htbp]",
            "\\centering",
            "\\caption{RAG检索效果评估}",
            "\\label{tab:rag_performance}",
            "\\begin{tabular}{lccc}",
            "\\hline",
            "\\textbf{配置} & \\textbf{召回率} & \\textbf{精确率} & \\textbf{F1 Score} \\\\",
            "\\hline"
        ]
        
        results = self.data.get('results', {})
        
        configs = {
            'rag_only': 'LLM+RAG',
            'full_system': '完整系统'
        }
        
        for config_key, config_name in configs.items():
            if config_key in results:
                rag = results[config_key]['results'].get('rag_metrics', {})
                recall = rag.get('recall', 0) * 100
                precision = rag.get('precision', 0) * 100
                f1 = rag.get('f1', 0)
                
                latex_lines.append(
                    f"{config_name} & {recall:.2f}\\% & {precision:.2f}\\% & {f1:.3f} \\\\"
                )
        
        latex_lines.extend([
            "\\hline",
            "\\end{tabular}",
            "\\end{table}"
        ])
        
        return '\n'.join(latex_lines)
    
    def generate_full_report(self) -> str:
        """生成完整LaTeX报告"""
        latex_lines = [
            "% 心理咨询系统评估报告",
            "% 自动生成于 " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "",
            "\\section{实验结果}",
            "",
            "本节展示了三种系统配置的详细评估结果。",
            "",
            "\\subsection{系统对比}",
            "",
            self.generate_comparison_table(),
            "",
            "\\subsection{记忆系统性能}",
            "",
            "记忆系统是本系统的核心创新之一，表\\ref{tab:memory_performance}展示了其性能。",
            "",
            self.generate_memory_table(),
            "",
            "\\subsection{RAG检索效果}",
            "",
            "表\\ref{tab:rag_performance}展示了RAG系统的检索性能。",
            "",
            self.generate_rag_table(),
            ""
        ]
        
        return '\n'.join(latex_lines)
    
    def _extract_metric_values(self, metric_type: str, *keys) -> List[float]:
        """提取指标值"""
        results = self.data.get('results', {})
        configs = ['baseline', 'rag_only', 'full_system']
        values = []
        
        for config in configs:
            if config in results:
                metric_data = results[config]['results'].get(metric_type, {})
                
                # 支持嵌套的键
                for key in keys:
                    if isinstance(metric_data, dict):
                        metric_data = metric_data.get(key, 0)
                    else:
                        metric_data = 0
                        break
                
                values.append(metric_data if isinstance(metric_data, (int, float)) else 0)
            else:
                values.append(0)
        
        return values
    
    def _calculate_improvement(self, baseline: float, improved: float) -> str:
        """计算改进幅度"""
        if baseline == 0:
            return "--"
        
        improvement = ((improved - baseline) / baseline) * 100
        sign = '+' if improvement > 0 else ''
        return f"{sign}{improvement:.2f}\\%"
    
    def save(self, output_file: str = None) -> str:
        """保存LaTeX报告"""
        if output_file is None:
            result_path = Path(self.result_file)
            output_file = result_path.parent / f"{result_path.stem}_latex.tex"
        
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 生成报告
        report = self.generate_full_report()
        
        # 保存
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"✓ LaTeX报告已保存: {output_path}")
        print(f"  文件大小: {output_path.stat().st_size / 1024:.1f} KB")
        
        return str(output_path)
    
    def save_tables_separately(self, output_dir: str = None):
        """分别保存各个表格"""
        if output_dir is None:
            result_path = Path(self.result_file)
            output_dir = result_path.parent / "latex_tables"
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # 保存对比表格
        comparison_file = output_path / "comparison_table.tex"
        with open(comparison_file, 'w', encoding='utf-8') as f:
            f.write(self.generate_comparison_table())
        print(f"✓ 对比表格已保存: {comparison_file}")
        
        # 保存记忆表格
        memory_file = output_path / "memory_table.tex"
        with open(memory_file, 'w', encoding='utf-8') as f:
            f.write(self.generate_memory_table())
        print(f"✓ 记忆表格已保存: {memory_file}")
        
        # 保存RAG表格
        rag_file = output_path / "rag_table.tex"
        with open(rag_file, 'w', encoding='utf-8') as f:
            f.write(self.generate_rag_table())
        print(f"✓ RAG表格已保存: {rag_file}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='生成LaTeX报告')
    parser.add_argument('--result', type=str, required=True,
                       help='评估结果JSON文件路径')
    parser.add_argument('--output', type=str, default=None,
                       help='输出LaTeX文件路径')
    parser.add_argument('--separate', action='store_true',
                       help='分别保存各个表格')
    
    args = parser.parse_args()
    
    try:
        print("\n" + "="*70)
        print(" "*20 + "生成LaTeX报告")
        print("="*70)
        
        generator = LaTeXReportGenerator(args.result)
        
        if args.separate:
            # 分别保存
            generator.save_tables_separately()
        else:
            # 保存完整报告
            output_file = generator.save(args.output)
        
        print("\n" + "="*70)
        print(" "*20 + "LaTeX报告生成完成！")
        print("="*70)
        
        print("\n📝 使用方法:")
        print("  1. 将生成的.tex文件复制到论文中")
        print("  2. 确保论文中包含必要的LaTeX包")
        print("  3. 编译论文查看效果")
        
    except Exception as e:
        print(f"\n✗ LaTeX报告生成失败: {e}")
        import traceback
        traceback.print_exc()
        import sys
        sys.exit(1)


if __name__ == '__main__':
    main()
