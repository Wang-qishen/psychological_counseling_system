#!/usr/bin/env python3
"""
数据导出工具 - 将评估结果导出为各种格式

用途：
1. 导出Excel表格（方便数据分析）
2. 导出CSV文件（兼容性好）
3. 导出格式化的文本报告

使用方法：
    python evaluation/reporting/data_exporter.py --result comparison.json --format excel
"""

import json
import csv
import argparse
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime


class DataExporter:
    """数据导出器"""
    
    def __init__(self, result_file: str):
        """
        初始化导出器
        
        Args:
            result_file: 评估结果JSON文件路径
        """
        self.result_file = result_file
        
        with open(result_file, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
    
    def export_to_csv(self, output_file: str = None) -> str:
        """
        导出为CSV格式
        
        Args:
            output_file: 输出文件路径
            
        Returns:
            保存的文件路径
        """
        if output_file is None:
            result_path = Path(self.result_file)
            output_file = result_path.parent / f"{result_path.stem}.csv"
        
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        results = self.data.get('results', {})
        
        # 准备CSV数据
        rows = []
        
        # 表头
        headers = ['指标类型', '指标名称', '裸LLM', 'LLM+RAG', '完整系统', '改进幅度(%)']
        rows.append(headers)
        
        # 技术指标
        self._add_technical_metrics_to_rows(rows, results)
        
        # 临床指标
        self._add_clinical_metrics_to_rows(rows, results)
        
        # 记忆指标
        self._add_memory_metrics_to_rows(rows, results)
        
        # RAG指标
        self._add_rag_metrics_to_rows(rows, results)
        
        # 写入CSV
        with open(output_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(rows)
        
        print(f"✓ CSV文件已保存: {output_path}")
        return str(output_path)
    
    def export_to_excel(self, output_file: str = None) -> str:
        """
        导出为Excel格式（需要openpyxl或xlsxwriter）
        
        Args:
            output_file: 输出文件路径
            
        Returns:
            保存的文件路径
        """
        try:
            import pandas as pd
        except ImportError:
            print("⚠️  需要安装pandas: pip install pandas")
            print("尝试使用CSV格式...")
            return self.export_to_csv(output_file)
        
        if output_file is None:
            result_path = Path(self.result_file)
            output_file = result_path.parent / f"{result_path.stem}.xlsx"
        
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        results = self.data.get('results', {})
        
        # 创建Excel writer
        try:
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                # Sheet 1: 技术指标
                tech_df = self._create_technical_metrics_dataframe(results)
                tech_df.to_excel(writer, sheet_name='技术指标', index=False)
                
                # Sheet 2: 临床指标
                clinical_df = self._create_clinical_metrics_dataframe(results)
                clinical_df.to_excel(writer, sheet_name='临床指标', index=False)
                
                # Sheet 3: 记忆系统
                memory_df = self._create_memory_metrics_dataframe(results)
                memory_df.to_excel(writer, sheet_name='记忆系统', index=False)
                
                # Sheet 4: RAG效果
                rag_df = self._create_rag_metrics_dataframe(results)
                rag_df.to_excel(writer, sheet_name='RAG效果', index=False)
                
                # Sheet 5: 总结
                summary_df = self._create_summary_dataframe(results)
                summary_df.to_excel(writer, sheet_name='总结', index=False)
            
            print(f"✓ Excel文件已保存: {output_path}")
            return str(output_path)
        
        except ImportError:
            print("⚠️  需要安装openpyxl: pip install openpyxl")
            print("尝试使用CSV格式...")
            return self.export_to_csv(output_file.replace('.xlsx', '.csv'))
    
    def export_to_text(self, output_file: str = None) -> str:
        """
        导出为格式化的文本报告
        
        Args:
            output_file: 输出文件路径
            
        Returns:
            保存的文件路径
        """
        if output_file is None:
            result_path = Path(self.result_file)
            output_file = result_path.parent / f"{result_path.stem}.txt"
        
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        results = self.data.get('results', {})
        
        # 生成文本报告
        lines = []
        lines.append("="*70)
        lines.append(" "*20 + "心理咨询系统评估报告")
        lines.append("="*70)
        lines.append("")
        
        # 元数据
        metadata = self.data.get('metadata', {})
        lines.append(f"生成时间: {metadata.get('timestamp', 'N/A')}")
        lines.append(f"测试样本数: {metadata.get('num_samples', 'N/A')}")
        lines.append("")
        
        # 技术指标
        lines.append("-"*70)
        lines.append("技术指标对比")
        lines.append("-"*70)
        lines.append("")
        lines.append(f"{'指标':<20} {'裸LLM':<12} {'LLM+RAG':<12} {'完整系统':<12} {'改进幅度':<12}")
        lines.append("-"*70)
        
        self._add_technical_metrics_to_text(lines, results)
        
        # 临床指标
        lines.append("")
        lines.append("-"*70)
        lines.append("临床指标对比")
        lines.append("-"*70)
        lines.append("")
        lines.append(f"{'指标':<20} {'裸LLM':<12} {'LLM+RAG':<12} {'完整系统':<12} {'改进幅度':<12}")
        lines.append("-"*70)
        
        self._add_clinical_metrics_to_text(lines, results)
        
        # 记忆系统
        lines.append("")
        lines.append("-"*70)
        lines.append("记忆系统性能")
        lines.append("-"*70)
        
        self._add_memory_metrics_to_text(lines, results)
        
        # RAG效果
        lines.append("")
        lines.append("-"*70)
        lines.append("RAG检索效果")
        lines.append("-"*70)
        
        self._add_rag_metrics_to_text(lines, results)
        
        lines.append("")
        lines.append("="*70)
        lines.append(f"报告生成于: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("="*70)
        
        # 写入文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        print(f"✓ 文本报告已保存: {output_path}")
        return str(output_path)
    
    # ===== 辅助方法 =====
    
    def _add_technical_metrics_to_rows(self, rows: List, results: Dict):
        """添加技术指标到CSV行"""
        configs = ['baseline', 'rag_only', 'full_system']
        
        # BERT Score F1
        values = self._extract_values(results, configs, 'technical_metrics', 'bert_score', 'f1')
        improvement = self._calc_improvement(values[0], values[2])
        rows.append(['技术指标', 'BERT Score F1', f"{values[0]:.3f}", 
                    f"{values[1]:.3f}", f"{values[2]:.3f}", improvement])
        
        # ROUGE-L
        values = self._extract_values(results, configs, 'technical_metrics', 'rouge', 'rougeL')
        improvement = self._calc_improvement(values[0], values[2])
        rows.append(['技术指标', 'ROUGE-L', f"{values[0]:.3f}", 
                    f"{values[1]:.3f}", f"{values[2]:.3f}", improvement])
    
    def _add_clinical_metrics_to_rows(self, rows: List, results: Dict):
        """添加临床指标到CSV行"""
        configs = ['baseline', 'rag_only', 'full_system']
        
        metrics = ['empathy', 'support', 'guidance', 'relevance']
        names = ['共情', '支持', '指导', '相关性']
        
        for metric, name in zip(metrics, names):
            values = self._extract_values(results, configs, 'clinical_metrics', metric)
            improvement = self._calc_improvement(values[0], values[2])
            rows.append(['临床指标', name, f"{values[0]:.2f}", 
                        f"{values[1]:.2f}", f"{values[2]:.2f}", improvement])
    
    def _add_memory_metrics_to_rows(self, rows: List, results: Dict):
        """添加记忆指标到CSV行"""
        if 'full_system' in results:
            memory = results['full_system']['results'].get('memory_metrics', {})
            
            rows.append(['记忆系统', '短期记忆召回', '', '', 
                        f"{memory.get('short_term_recall', 0)*100:.2f}%", ''])
            rows.append(['记忆系统', '整体准确率', '', '', 
                        f"{memory.get('overall_accuracy', 0)*100:.2f}%", ''])
    
    def _add_rag_metrics_to_rows(self, rows: List, results: Dict):
        """添加RAG指标到CSV行"""
        for config in ['rag_only', 'full_system']:
            if config in results:
                name = 'LLM+RAG' if config == 'rag_only' else '完整系统'
                rag = results[config]['results'].get('rag_metrics', {})
                
                rows.append(['RAG效果', f'{name}-召回率', '', '', 
                            f"{rag.get('recall', 0)*100:.2f}%", ''])
                rows.append(['RAG效果', f'{name}-精确率', '', '', 
                            f"{rag.get('precision', 0)*100:.2f}%", ''])
    
    def _create_technical_metrics_dataframe(self, results: Dict):
        """创建技术指标DataFrame"""
        try:
            import pandas as pd
        except ImportError:
            return None
        
        configs = ['baseline', 'rag_only', 'full_system']
        data = []
        
        metrics_info = [
            ('BERT Score F1', 'technical_metrics', 'bert_score', 'f1'),
            ('ROUGE-L', 'technical_metrics', 'rouge', 'rougeL'),
            ('BLEU', 'technical_metrics', 'bleu')
        ]
        
        for metric_name, *keys in metrics_info:
            values = self._extract_values(results, configs, *keys)
            improvement = self._calc_improvement(values[0], values[2])
            
            data.append({
                '指标': metric_name,
                '裸LLM': f"{values[0]:.3f}",
                'LLM+RAG': f"{values[1]:.3f}",
                '完整系统': f"{values[2]:.3f}",
                '改进幅度': improvement
            })
        
        return pd.DataFrame(data)
    
    def _create_clinical_metrics_dataframe(self, results: Dict):
        """创建临床指标DataFrame"""
        try:
            import pandas as pd
        except ImportError:
            return None
        
        configs = ['baseline', 'rag_only', 'full_system']
        data = []
        
        metrics = {
            'empathy': '共情',
            'support': '支持',
            'guidance': '指导',
            'relevance': '相关性',
            'communication': '沟通',
            'fluency': '流畅性',
            'safety': '安全性'
        }
        
        for metric_key, metric_name in metrics.items():
            values = self._extract_values(results, configs, 'clinical_metrics', metric_key)
            improvement = self._calc_improvement(values[0], values[2])
            
            data.append({
                '指标': metric_name,
                '裸LLM': f"{values[0]:.2f}",
                'LLM+RAG': f"{values[1]:.2f}",
                '完整系统': f"{values[2]:.2f}",
                '改进幅度': improvement
            })
        
        return pd.DataFrame(data)
    
    def _create_memory_metrics_dataframe(self, results: Dict):
        """创建记忆指标DataFrame"""
        try:
            import pandas as pd
        except ImportError:
            return None
        
        data = []
        
        if 'full_system' in results:
            memory = results['full_system']['results'].get('memory_metrics', {})
            
            metrics = {
                'short_term_recall': '短期记忆召回',
                'working_memory_accuracy': '工作记忆准确率',
                'long_term_consistency': '长期记忆一致性',
                'overall_accuracy': '整体准确率'
            }
            
            for key, name in metrics.items():
                value = memory.get(key, 0) * 100
                data.append({
                    '指标': name,
                    '性能': f"{value:.2f}%"
                })
        
        return pd.DataFrame(data)
    
    def _create_rag_metrics_dataframe(self, results: Dict):
        """创建RAG指标DataFrame"""
        try:
            import pandas as pd
        except ImportError:
            return None
        
        data = []
        
        configs = {
            'rag_only': 'LLM+RAG',
            'full_system': '完整系统'
        }
        
        for config_key, config_name in configs.items():
            if config_key in results:
                rag = results[config_key]['results'].get('rag_metrics', {})
                
                data.append({
                    '配置': config_name,
                    '召回率': f"{rag.get('recall', 0)*100:.2f}%",
                    '精确率': f"{rag.get('precision', 0)*100:.2f}%",
                    'F1 Score': f"{rag.get('f1', 0):.3f}"
                })
        
        return pd.DataFrame(data)
    
    def _create_summary_dataframe(self, results: Dict):
        """创建总结DataFrame"""
        try:
            import pandas as pd
        except ImportError:
            return None
        
        improvements = self.data.get('improvements', {})
        
        data = []
        for metric, improvement in improvements.items():
            sign = '+' if improvement > 0 else ''
            data.append({
                '指标': metric,
                '改进幅度': f"{sign}{improvement:.2f}%"
            })
        
        return pd.DataFrame(data)
    
    def _add_technical_metrics_to_text(self, lines: List, results: Dict):
        """添加技术指标到文本"""
        configs = ['baseline', 'rag_only', 'full_system']
        
        # BERT Score F1
        values = self._extract_values(results, configs, 'technical_metrics', 'bert_score', 'f1')
        improvement = self._calc_improvement(values[0], values[2])
        lines.append(f"{'BERT Score F1':<20} {values[0]:<12.3f} {values[1]:<12.3f} {values[2]:<12.3f} {improvement:<12}")
    
    def _add_clinical_metrics_to_text(self, lines: List, results: Dict):
        """添加临床指标到文本"""
        configs = ['baseline', 'rag_only', 'full_system']
        
        metrics = {'empathy': '共情', 'support': '支持', 'relevance': '相关性'}
        
        for metric_key, metric_name in metrics.items():
            values = self._extract_values(results, configs, 'clinical_metrics', metric_key)
            improvement = self._calc_improvement(values[0], values[2])
            lines.append(f"{metric_name:<20} {values[0]:<12.2f} {values[1]:<12.2f} {values[2]:<12.2f} {improvement:<12}")
    
    def _add_memory_metrics_to_text(self, lines: List, results: Dict):
        """添加记忆指标到文本"""
        if 'full_system' in results:
            memory = results['full_system']['results'].get('memory_metrics', {})
            lines.append("")
            lines.append(f"短期记忆召回:    {memory.get('short_term_recall', 0)*100:.2f}%")
            lines.append(f"整体准确率:      {memory.get('overall_accuracy', 0)*100:.2f}%")
    
    def _add_rag_metrics_to_text(self, lines: List, results: Dict):
        """添加RAG指标到文本"""
        lines.append("")
        for config in ['rag_only', 'full_system']:
            if config in results:
                name = 'LLM+RAG' if config == 'rag_only' else '完整系统'
                rag = results[config]['results'].get('rag_metrics', {})
                lines.append(f"\n{name}:")
                lines.append(f"  召回率: {rag.get('recall', 0)*100:.2f}%")
                lines.append(f"  精确率: {rag.get('precision', 0)*100:.2f}%")
    
    def _extract_values(self, results: Dict, configs: List[str], *keys) -> List[float]:
        """提取指标值"""
        values = []
        for config in configs:
            if config in results:
                data = results[config]['results']
                for key in keys:
                    if isinstance(data, dict):
                        data = data.get(key, 0)
                    else:
                        data = 0
                        break
                values.append(data if isinstance(data, (int, float)) else 0)
            else:
                values.append(0)
        return values
    
    def _calc_improvement(self, baseline: float, improved: float) -> str:
        """计算改进幅度"""
        if baseline == 0:
            return "N/A"
        improvement = ((improved - baseline) / baseline) * 100
        sign = '+' if improvement > 0 else ''
        return f"{sign}{improvement:.2f}%"


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='导出评估结果')
    parser.add_argument('--result', type=str, required=True,
                       help='评估结果JSON文件路径')
    parser.add_argument('--format', type=str, choices=['csv', 'excel', 'txt', 'all'],
                       default='all', help='导出格式')
    parser.add_argument('--output', type=str, default=None,
                       help='输出文件路径')
    
    args = parser.parse_args()
    
    try:
        print("\n" + "="*70)
        print(" "*25 + "导出评估结果")
        print("="*70)
        
        exporter = DataExporter(args.result)
        
        if args.format == 'csv' or args.format == 'all':
            exporter.export_to_csv(args.output)
        
        if args.format == 'excel' or args.format == 'all':
            excel_file = args.output.replace('.csv', '.xlsx') if args.output else None
            exporter.export_to_excel(excel_file)
        
        if args.format == 'txt' or args.format == 'all':
            txt_file = args.output.replace('.csv', '.txt').replace('.xlsx', '.txt') if args.output else None
            exporter.export_to_text(txt_file)
        
        print("\n" + "="*70)
        print(" "*25 + "导出完成！")
        print("="*70)
        
    except Exception as e:
        print(f"\n✗ 导出失败: {e}")
        import traceback
        traceback.print_exc()
        import sys
        sys.exit(1)


if __name__ == '__main__':
    main()
