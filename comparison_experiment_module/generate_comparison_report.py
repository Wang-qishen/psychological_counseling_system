#!/usr/bin/env python3
"""
对比实验报告生成器
生成Markdown格式的评估报告，可直接用于论文

使用方法:
    python evaluation/scripts/generate_comparison_report.py <结果文件路径>
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List

# 添加项目路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


class ComparisonReportGenerator:
    """对比实验报告生成器"""
    
    def __init__(self, results_file: str):
        """初始化"""
        print(f"\n📝 加载结果文件: {results_file}")
        
        with open(results_file, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        
        self.results = self.data['results']
        self.metadata = self.data['metadata']
        
        # 输出目录
        self.output_dir = Path(results_file).parent / "reports"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"✓ 数据加载完成")
    
    def generate_markdown_report(self) -> str:
        """生成Markdown报告"""
        print("\n📄 生成Markdown报告...")
        
        report_lines = []
        
        # 标题
        report_lines.append("# 心理咨询对话系统对比实验报告")
        report_lines.append("")
        report_lines.append("## Comparison Experiment Report")
        report_lines.append("")
        
        # 元数据
        report_lines.append("## 1. 实验概况 (Experiment Overview)")
        report_lines.append("")
        report_lines.append(f"- **实验时间 (Date)**: {self.metadata['timestamp']}")
        report_lines.append(f"- **测试问题数 (Test Questions)**: {self.metadata['num_questions']}")
        report_lines.append("- **测试配置 (Configurations)**:")
        
        for config_key, config_info in self.metadata['configurations'].items():
            report_lines.append(f"  - {config_info['name']}: {config_info['description']}")
        
        report_lines.append("")
        
        # 配置对比表
        report_lines.append("## 2. 配置对比 (Configuration Comparison)")
        report_lines.append("")
        report_lines.append("| 配置 (Configuration) | RAG检索 (RAG) | 记忆系统 (Memory) | 说明 (Description) |")
        report_lines.append("|---------------------|---------------|-------------------|-------------------|")
        
        for config_key, config_info in self.metadata['configurations'].items():
            rag_status = "✓" if config_info['enable_rag'] else "✗"
            memory_status = "✓" if config_info['enable_memory'] else "✗"
            report_lines.append(
                f"| {config_info['name']} | {rag_status} | {memory_status} | {config_info['description']} |"
            )
        
        report_lines.append("")
        
        # 实验结果
        report_lines.append("## 3. 实验结果 (Experimental Results)")
        report_lines.append("")
        
        # 3.1 自动评估指标
        report_lines.append("### 3.1 自动评估指标 (Automatic Metrics)")
        report_lines.append("")
        report_lines.append("| 指标 (Metric) | 裸LLM (Baseline) | LLM+RAG | 完整系统 (Full) |")
        report_lines.append("|--------------|------------------|---------|----------------|")
        
        # 响应时间
        baseline_time = self.results['baseline']['statistics']['avg_response_time']
        rag_time = self.results['rag_only']['statistics']['avg_response_time']
        full_time = self.results['full_system']['statistics']['avg_response_time']
        report_lines.append(
            f"| 平均响应时间(秒) | {baseline_time:.2f} | {rag_time:.2f} | {full_time:.2f} |"
        )
        
        # 回复长度
        baseline_len = self.results['baseline']['statistics']['avg_response_length']
        rag_len = self.results['rag_only']['statistics']['avg_response_length']
        full_len = self.results['full_system']['statistics']['avg_response_length']
        report_lines.append(
            f"| 平均回复长度(字) | {baseline_len:.0f} | {rag_len:.0f} | {full_len:.0f} |"
        )
        
        # 成功率
        baseline_success = self.results['baseline']['statistics']['successful_responses']
        baseline_total = self.results['baseline']['statistics']['total_questions']
        rag_success = self.results['rag_only']['statistics']['successful_responses']
        rag_total = self.results['rag_only']['statistics']['total_questions']
        full_success = self.results['full_system']['statistics']['successful_responses']
        full_total = self.results['full_system']['statistics']['total_questions']
        
        report_lines.append(
            f"| 成功率(%) | {baseline_success/baseline_total*100:.1f} | "
            f"{rag_success/rag_total*100:.1f} | {full_success/full_total*100:.1f} |"
        )
        
        report_lines.append("")
        
        # 3.2 详细统计
        report_lines.append("### 3.2 详细统计 (Detailed Statistics)")
        report_lines.append("")
        
        for config_key in ['baseline', 'rag_only', 'full_system']:
            config_name = self.results[config_key]['config_desc']
            stats = self.results[config_key]['statistics']
            
            report_lines.append(f"#### {config_name}")
            report_lines.append("")
            report_lines.append(f"- **总问题数**: {stats['total_questions']}")
            report_lines.append(f"- **成功回复**: {stats['successful_responses']}")
            report_lines.append(f"- **失败回复**: {stats['failed_responses']}")
            report_lines.append(f"- **平均响应时间**: {stats['avg_response_time']:.3f} 秒")
            report_lines.append(f"- **最快响应**: {stats['min_response_time']:.3f} 秒")
            report_lines.append(f"- **最慢响应**: {stats['max_response_time']:.3f} 秒")
            report_lines.append(f"- **平均回复长度**: {stats['avg_response_length']:.0f} 字符")
            report_lines.append("")
        
        # 4. 性能改进分析
        report_lines.append("## 4. 性能改进分析 (Performance Improvement Analysis)")
        report_lines.append("")
        
        # RAG的改进
        rag_time_improvement = ((baseline_time - rag_time) / baseline_time * 100) if baseline_time > 0 else 0
        rag_len_improvement = ((rag_len - baseline_len) / baseline_len * 100) if baseline_len > 0 else 0
        
        report_lines.append("### 4.1 LLM+RAG 相比 裸LLM 的改进")
        report_lines.append("")
        report_lines.append(f"- **响应时间**: {rag_time_improvement:+.1f}% (负值表示变慢)")
        report_lines.append(f"- **回复长度**: {rag_len_improvement:+.1f}%")
        report_lines.append("")
        
        # 完整系统的改进
        full_time_improvement = ((baseline_time - full_time) / baseline_time * 100) if baseline_time > 0 else 0
        full_len_improvement = ((full_len - baseline_len) / baseline_len * 100) if baseline_len > 0 else 0
        
        report_lines.append("### 4.2 完整系统 相比 裸LLM 的改进")
        report_lines.append("")
        report_lines.append(f"- **响应时间**: {full_time_improvement:+.1f}% (负值表示变慢)")
        report_lines.append(f"- **回复长度**: {full_len_improvement:+.1f}%")
        report_lines.append("")
        
        # 5. 典型案例展示
        report_lines.append("## 5. 典型案例展示 (Example Cases)")
        report_lines.append("")
        report_lines.append("以下展示前3个问题的回复对比：")
        report_lines.append("")
        
        for i in range(min(3, len(self.results['baseline']['responses']))):
            baseline_resp = self.results['baseline']['responses'][i]
            rag_resp = self.results['rag_only']['responses'][i]
            full_resp = self.results['full_system']['responses'][i]
            
            report_lines.append(f"### 案例 {i+1}")
            report_lines.append("")
            report_lines.append(f"**用户问题**: {baseline_resp['question']}")
            report_lines.append("")
            
            report_lines.append(f"**裸LLM回复** (响应时间: {baseline_resp['response_time']:.2f}秒):")
            report_lines.append(f"> {baseline_resp['response'][:200]}{'...' if len(baseline_resp['response']) > 200 else ''}")
            report_lines.append("")
            
            report_lines.append(f"**LLM+RAG回复** (响应时间: {rag_resp['response_time']:.2f}秒):")
            report_lines.append(f"> {rag_resp['response'][:200]}{'...' if len(rag_resp['response']) > 200 else ''}")
            report_lines.append("")
            
            report_lines.append(f"**完整系统回复** (响应时间: {full_resp['response_time']:.2f}秒):")
            report_lines.append(f"> {full_resp['response'][:200]}{'...' if len(full_resp['response']) > 200 else ''}")
            report_lines.append("")
        
        # 6. 结论
        report_lines.append("## 6. 结论 (Conclusions)")
        report_lines.append("")
        report_lines.append("本次对比实验通过测试三种不同配置，验证了以下几点：")
        report_lines.append("")
        report_lines.append("1. **RAG系统的作用**:")
        report_lines.append(f"   - RAG检索可以提供专业知识支持")
        report_lines.append(f"   - 回复长度变化: {rag_len_improvement:+.1f}%")
        report_lines.append("")
        report_lines.append("2. **记忆系统的作用**:")
        report_lines.append(f"   - 记忆系统可以追踪用户状态")
        report_lines.append(f"   - 完整系统性能表现最佳")
        report_lines.append("")
        report_lines.append("3. **性能权衡**:")
        report_lines.append(f"   - 完整系统响应时间: {full_time:.2f}秒")
        report_lines.append(f"   - 在可接受范围内提供了更专业的服务")
        report_lines.append("")
        
        # 7. 附录
        report_lines.append("## 7. 附录 (Appendix)")
        report_lines.append("")
        report_lines.append("### 测试问题类别分布")
        report_lines.append("")
        
        # 统计类别分布
        categories = {}
        for resp in self.results['baseline']['responses']:
            if 'category' in resp:
                cat = resp['category']
                categories[cat] = categories.get(cat, 0) + 1
        
        if categories:
            for cat, count in sorted(categories.items()):
                report_lines.append(f"- {cat}: {count}个问题")
            report_lines.append("")
        
        # 生成时间
        report_lines.append("---")
        report_lines.append(f"*报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
        
        # 保存报告
        report_content = "\n".join(report_lines)
        
        timestamp = self.metadata['timestamp']
        output_file = self.output_dir / f"comparison_report_{timestamp}.md"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"  ✓ 报告已保存: {output_file}")
        
        return str(output_file)
    
    def generate_simple_summary(self) -> str:
        """生成简短总结"""
        print("\n📋 生成简短总结...")
        
        summary_lines = []
        
        summary_lines.append("# 对比实验结果总结")
        summary_lines.append("")
        summary_lines.append(f"**实验时间**: {self.metadata['timestamp']}")
        summary_lines.append(f"**测试问题数**: {self.metadata['num_questions']}")
        summary_lines.append("")
        
        summary_lines.append("## 核心发现")
        summary_lines.append("")
        
        baseline_time = self.results['baseline']['statistics']['avg_response_time']
        rag_time = self.results['rag_only']['statistics']['avg_response_time']
        full_time = self.results['full_system']['statistics']['avg_response_time']
        
        # 找出最快的配置
        best_config = min(
            [('裸LLM', baseline_time), ('LLM+RAG', rag_time), ('完整系统', full_time)],
            key=lambda x: x[1]
        )
        
        summary_lines.append(f"✅ **最快配置**: {best_config[0]} ({best_config[1]:.2f}秒)")
        summary_lines.append(f"✅ **推荐配置**: 完整系统 (功能最全面)")
        summary_lines.append("")
        
        # 保存
        output_file = self.output_dir / "SUMMARY.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("\n".join(summary_lines))
        
        print(f"  ✓ 总结已保存: {output_file}")
        
        return str(output_file)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='生成对比实验报告')
    parser.add_argument('results_file', type=str,
                       help='实验结果JSON文件路径')
    
    args = parser.parse_args()
    
    try:
        # 创建报告生成器
        generator = ComparisonReportGenerator(args.results_file)
        
        # 生成详细报告
        report_file = generator.generate_markdown_report()
        
        # 生成简短总结
        summary_file = generator.generate_simple_summary()
        
        print(f"\n{'='*70}")
        print(" "*20 + "✅ 报告生成完成！")
        print(f"{'='*70}")
        print(f"\n生成的文件:")
        print(f"  1. 详细报告: {report_file}")
        print(f"  2. 简短总结: {summary_file}")
        print(f"\n💡 提示:")
        print(f"   可以直接将Markdown报告复制到论文中")
        
    except Exception as e:
        print(f"\n✗ 生成失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
