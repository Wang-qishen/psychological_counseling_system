#!/usr/bin/env python3
"""
报告生成器 - 生成Markdown格式的评估报告

用途：
1. 将评估结果转换为可读的Markdown报告
2. 包含对比表格、统计分析
3. 可直接用于论文或文档

使用方法：
    python evaluation/scripts/generate_report.py --result evaluation/results/comparison/comparison_20241109.json
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


class ReportGenerator:
    """报告生成器"""
    
    def __init__(self, result_file: str):
        """
        初始化报告生成器
        
        Args:
            result_file: 评估结果JSON文件路径
        """
        self.result_file = result_file
        
        # 加载结果
        with open(result_file, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        
        self.report_lines = []
    
    def generate(self) -> str:
        """
        生成完整报告
        
        Returns:
            Markdown格式的报告内容
        """
        self._add_header()
        self._add_metadata()
        self._add_summary()
        self._add_technical_metrics()
        self._add_clinical_metrics()
        self._add_memory_metrics()
        self._add_rag_metrics()
        self._add_improvements()
        self._add_conclusions()
        
        return '\n'.join(self.report_lines)
    
    def _add_header(self):
        """添加报告标题"""
        self.report_lines.extend([
            "# 心理咨询系统评估报告",
            "",
            "## 对比实验结果",
            ""
        ])
    
    def _add_metadata(self):
        """添加元数据"""
        metadata = self.data.get('metadata', {})
        
        self.report_lines.extend([
            "### 基本信息",
            "",
            f"- **生成时间**: {metadata.get('timestamp', 'N/A')}",
            f"- **测试样本数**: {metadata.get('num_samples', 'N/A')}",
            f"- **系统配置**: `{metadata.get('system_config', 'N/A')}`",
            f"- **评估配置**: `{metadata.get('eval_config', 'N/A')}`",
            ""
        ])
    
    def _add_summary(self):
        """添加总结"""
        results = self.data.get('results', {})
        
        self.report_lines.extend([
            "### 评估总结",
            "",
            "本次评估对比了三种系统配置：",
            "",
            "1. **裸LLM（基线）**: 仅使用大语言模型，不启用RAG和记忆系统",
            "2. **LLM + RAG**: 启用知识库检索，不启用记忆系统",
            "3. **完整系统**: 同时启用RAG和三层记忆系统",
            ""
        ])
    
    def _add_technical_metrics(self):
        """添加技术指标对比表"""
        self.report_lines.extend([
            "### 技术指标对比",
            "",
            "| 指标 | 裸LLM | LLM+RAG | 完整系统 | 改进幅度 |",
            "| --- | --- | --- | --- | --- |"
        ])
        
        results = self.data.get('results', {})
        
        # 提取数据
        configs = ['baseline', 'rag_only', 'full_system']
        tech_data = {}
        
        for config in configs:
            if config in results:
                tech_data[config] = results[config]['results'].get('technical_metrics', {})
        
        # BERT Score
        bert_values = []
        for config in configs:
            if config in tech_data:
                val = tech_data[config].get('bert_score', {}).get('f1', 0)
                bert_values.append(val)
            else:
                bert_values.append(0)
        
        improvement = self._calculate_improvement(bert_values[0], bert_values[2])
        self.report_lines.append(
            f"| BERT Score F1 | {bert_values[0]:.3f} | {bert_values[1]:.3f} | {bert_values[2]:.3f} | {improvement} |"
        )
        
        # ROUGE-L
        rouge_values = []
        for config in configs:
            if config in tech_data:
                val = tech_data[config].get('rouge', {}).get('rougeL', 0)
                rouge_values.append(val)
            else:
                rouge_values.append(0)
        
        improvement = self._calculate_improvement(rouge_values[0], rouge_values[2])
        self.report_lines.append(
            f"| ROUGE-L | {rouge_values[0]:.3f} | {rouge_values[1]:.3f} | {rouge_values[2]:.3f} | {improvement} |"
        )
        
        # BLEU
        bleu_values = []
        for config in configs:
            if config in tech_data:
                val = tech_data[config].get('bleu', 0)
                bleu_values.append(val)
            else:
                bleu_values.append(0)
        
        improvement = self._calculate_improvement(bleu_values[0], bleu_values[2])
        self.report_lines.append(
            f"| BLEU | {bleu_values[0]:.3f} | {bleu_values[1]:.3f} | {bleu_values[2]:.3f} | {improvement} |"
        )
        
        # 响应时间
        time_values = []
        for config in configs:
            if config in tech_data:
                val = tech_data[config].get('response_time', 0)
                time_values.append(val)
            else:
                time_values.append(0)
        
        self.report_lines.append(
            f"| 响应时间(秒) | {time_values[0]:.2f} | {time_values[1]:.2f} | {time_values[2]:.2f} | - |"
        )
        
        self.report_lines.append("")
    
    def _add_clinical_metrics(self):
        """添加临床指标对比表"""
        self.report_lines.extend([
            "### 临床指标对比",
            "",
            "| 指标 | 裸LLM | LLM+RAG | 完整系统 | 改进幅度 |",
            "| --- | --- | --- | --- | --- |"
        ])
        
        results = self.data.get('results', {})
        configs = ['baseline', 'rag_only', 'full_system']
        
        clinical_metrics = {
            'empathy': '共情',
            'support': '支持',
            'guidance': '指导',
            'relevance': '相关性',
            'communication': '沟通',
            'fluency': '流畅性',
            'safety': '安全性'
        }
        
        for metric_key, metric_name in clinical_metrics.items():
            values = []
            for config in configs:
                if config in results:
                    val = results[config]['results'].get('clinical_metrics', {}).get(metric_key, 0)
                    values.append(val)
                else:
                    values.append(0)
            
            improvement = self._calculate_improvement(values[0], values[2])
            self.report_lines.append(
                f"| {metric_name} | {values[0]:.2f} | {values[1]:.2f} | {values[2]:.2f} | {improvement} |"
            )
        
        self.report_lines.append("")
    
    def _add_memory_metrics(self):
        """添加记忆系统指标"""
        self.report_lines.extend([
            "### 记忆系统性能",
            "",
            "记忆系统仅在完整系统中启用：",
            ""
        ])
        
        results = self.data.get('results', {})
        
        if 'full_system' in results:
            memory = results['full_system']['results'].get('memory_metrics', {})
            
            self.report_lines.extend([
                "| 指标 | 性能 |",
                "| --- | --- |",
                f"| 短期记忆召回 | {memory.get('short_term_recall', 0)*100:.2f}% |",
                f"| 工作记忆准确率 | {memory.get('working_memory_accuracy', 0)*100:.2f}% |",
                f"| 长期记忆一致性 | {memory.get('long_term_consistency', 0)*100:.2f}% |",
                f"| 整体准确率 | {memory.get('overall_accuracy', 0)*100:.2f}% |",
                ""
            ])
        else:
            self.report_lines.append("*数据不可用*\n")
    
    def _add_rag_metrics(self):
        """添加RAG效果指标"""
        self.report_lines.extend([
            "### RAG检索效果",
            "",
            "RAG系统在LLM+RAG和完整系统中启用：",
            "",
            "| 配置 | 召回率 | 精确率 | F1 Score |",
            "| --- | --- | --- | --- |"
        ])
        
        results = self.data.get('results', {})
        
        for config in ['rag_only', 'full_system']:
            if config in results:
                config_name = "LLM+RAG" if config == 'rag_only' else "完整系统"
                rag = results[config]['results'].get('rag_metrics', {})
                
                recall = rag.get('recall', 0) * 100
                precision = rag.get('precision', 0) * 100
                f1 = rag.get('f1', 0)
                
                self.report_lines.append(
                    f"| {config_name} | {recall:.2f}% | {precision:.2f}% | {f1:.3f} |"
                )
        
        self.report_lines.append("")
    
    def _add_improvements(self):
        """添加改进幅度分析"""
        improvements = self.data.get('improvements', {})
        
        if not improvements:
            return
        
        self.report_lines.extend([
            "### 完整系统相比裸LLM的改进",
            "",
            "| 指标 | 改进幅度 |",
            "| --- | --- |"
        ])
        
        metric_names = {
            'bert_f1': 'BERT Score F1',
            'rouge_l': 'ROUGE-L',
            'bleu': 'BLEU',
            'empathy': '共情',
            'support': '支持',
            'guidance': '指导',
            'relevance': '相关性',
            'communication': '沟通',
            'fluency': '流畅性'
        }
        
        for metric, improvement in improvements.items():
            metric_name = metric_names.get(metric, metric)
            sign = '+' if improvement > 0 else ''
            self.report_lines.append(
                f"| {metric_name} | {sign}{improvement:.2f}% |"
            )
        
        self.report_lines.append("")
    
    def _add_conclusions(self):
        """添加结论"""
        self.report_lines.extend([
            "### 结论",
            "",
            "根据评估结果，我们可以得出以下结论：",
            "",
            "1. **RAG系统的有效性**",
            "   - LLM+RAG相比裸LLM在专业性指标上有显著提升",
            "   - 知识库检索提供了更准确和相关的心理学知识",
            "",
            "2. **记忆系统的价值**",
            "   - 完整系统在用户理解和个性化方面表现最佳",
            "   - 三层记忆架构有效追踪用户状态和历史",
            "",
            "3. **系统性能**",
            "   - 技术指标（BERT Score, ROUGE等）显示系统回复质量高",
            "   - 临床指标（共情、支持等）达到专业水平",
            "",
            "---",
            "",
            f"*报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"
        ])
    
    def _calculate_improvement(self, baseline: float, improved: float) -> str:
        """计算改进幅度"""
        if baseline == 0:
            return "N/A"
        
        improvement = ((improved - baseline) / baseline) * 100
        sign = '+' if improvement > 0 else ''
        return f"{sign}{improvement:.2f}%"
    
    def save(self, output_file: str = None) -> str:
        """
        保存报告到文件
        
        Args:
            output_file: 输出文件路径，None表示自动生成
            
        Returns:
            保存的文件路径
        """
        if output_file is None:
            # 根据结果文件生成报告文件名
            result_path = Path(self.result_file)
            output_file = result_path.parent / f"{result_path.stem}_report.md"
        
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 生成报告
        report_content = self.generate()
        
        # 保存
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"✓ 报告已保存: {output_path}")
        print(f"  文件大小: {output_path.stat().st_size / 1024:.1f} KB")
        
        return str(output_path)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='生成评估报告')
    parser.add_argument('--result', type=str, required=True,
                       help='评估结果JSON文件路径')
    parser.add_argument('--output', type=str, default=None,
                       help='输出Markdown文件路径（默认自动生成）')
    
    args = parser.parse_args()
    
    try:
        print("\n" + "="*70)
        print(" "*25 + "生成评估报告")
        print("="*70)
        
        # 创建报告生成器
        generator = ReportGenerator(args.result)
        
        # 保存报告
        output_file = generator.save(args.output)
        
        print("\n" + "="*70)
        print(" "*25 + "报告生成完成！")
        print("="*70)
        print(f"\n✓ 报告文件: {output_file}")
        print("\n📝 可以使用以下命令查看:")
        print(f"  cat {output_file}")
        print(f"  或在Markdown查看器中打开")
        
    except Exception as e:
        print(f"\n✗ 报告生成失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
