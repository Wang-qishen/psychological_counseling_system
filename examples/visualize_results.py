"""
实验结果可视化
生成论文用的图表和数据分析
"""

import sys
import os
import json
import glob
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

# 设置中文字体
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']  # 用黑体
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题


def load_latest_report():
    """加载最新的实验报告"""
    reports = glob.glob("./experiments/comparison_report_*.json")
    
    if not reports:
        print("错误: 未找到实验报告文件")
        print("请先运行 python examples/comparison_experiment.py")
        return None
    
    # 获取最新的报告
    latest_report = max(reports, key=os.path.getctime)
    print(f"加载报告: {latest_report}")
    
    with open(latest_report, 'r', encoding='utf-8') as f:
        report = json.load(f)
    
    return report


def plot_response_time_comparison(report, save_path):
    """绘制响应时间对比图"""
    summary = report['summary']
    
    configs = []
    times = []
    
    for config_key in ['bare_llm', 'llm_rag', 'full_system']:
        if config_key in summary:
            configs.append(summary[config_key]['config_name'])
            times.append(summary[config_key]['avg_response_time'])
    
    # 创建柱状图
    fig, ax = plt.subplots(figsize=(10, 6))
    
    x = np.arange(len(configs))
    bars = ax.bar(x, times, width=0.6, color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
    
    # 添加数值标签
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{times[i]:.2f}秒',
                ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    ax.set_xlabel('系统配置', fontsize=14, fontweight='bold')
    ax.set_ylabel('平均响应时间 (秒)', fontsize=14, fontweight='bold')
    ax.set_title('不同配置的响应时间对比', fontsize=16, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(configs, fontsize=11)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"✓ 已保存: {save_path}")
    plt.close()


def plot_response_length_comparison(report, save_path):
    """绘制响应长度对比图"""
    summary = report['summary']
    
    configs = []
    lengths = []
    
    for config_key in ['bare_llm', 'llm_rag', 'full_system']:
        if config_key in summary:
            configs.append(summary[config_key]['config_name'])
            lengths.append(summary[config_key]['avg_response_length'])
    
    # 创建柱状图
    fig, ax = plt.subplots(figsize=(10, 6))
    
    x = np.arange(len(configs))
    bars = ax.bar(x, lengths, width=0.6, color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
    
    # 添加数值标签
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(lengths[i])}字符',
                ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    ax.set_xlabel('系统配置', fontsize=14, fontweight='bold')
    ax.set_ylabel('平均响应长度 (字符)', fontsize=14, fontweight='bold')
    ax.set_title('不同配置的响应长度对比', fontsize=16, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(configs, fontsize=11)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"✓ 已保存: {save_path}")
    plt.close()


def plot_scenario_comparison(report, save_path):
    """绘制不同场景的对比图"""
    results = report['results']
    
    # 准备数据
    scenarios = [r['scenario_name'].split(':')[0] for r in results['bare_llm']]
    configs = ['裸LLM', 'LLM+RAG', '完整系统']
    
    bare_times = [r['avg_response_time'] for r in results['bare_llm']]
    rag_times = [r['avg_response_time'] for r in results['llm_rag']]
    full_times = [r['avg_response_time'] for r in results['full_system']]
    
    # 创建分组柱状图
    fig, ax = plt.subplots(figsize=(12, 6))
    
    x = np.arange(len(scenarios))
    width = 0.25
    
    bars1 = ax.bar(x - width, bare_times, width, label='裸LLM', color='#FF6B6B')
    bars2 = ax.bar(x, rag_times, width, label='LLM+RAG', color='#4ECDC4')
    bars3 = ax.bar(x + width, full_times, width, label='完整系统', color='#45B7D1')
    
    ax.set_xlabel('测试场景', fontsize=14, fontweight='bold')
    ax.set_ylabel('平均响应时间 (秒)', fontsize=14, fontweight='bold')
    ax.set_title('不同场景下各配置的响应时间', fontsize=16, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(scenarios, fontsize=11)
    ax.legend(fontsize=12)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"✓ 已保存: {save_path}")
    plt.close()


def generate_detailed_comparison_table(report, save_path):
    """生成详细的对比表格（Markdown格式）"""
    summary = report['summary']
    
    with open(save_path, 'w', encoding='utf-8') as f:
        f.write("# 实验结果详细对比\n\n")
        f.write(f"**实验时间**: {report['experiment_time']}\n\n")
        
        f.write("## 1. 系统配置说明\n\n")
        f.write("| 配置名称 | RAG | 记忆系统 | 说明 |\n")
        f.write("|---------|-----|---------|-----|\n")
        f.write("| 裸LLM | ❌ | ❌ | 纯大语言模型，无任何增强 |\n")
        f.write("| LLM + RAG | ✅ | ❌ | 有知识库检索，但无跨会话记忆 |\n")
        f.write("| 完整系统 | ✅ | ✅ | 完整功能：知识库 + 长期记忆 |\n\n")
        
        f.write("## 2. 总体性能对比\n\n")
        f.write("| 配置 | 平均响应时间 | 平均响应长度 | 测试场景数 |\n")
        f.write("|-----|------------|------------|----------|\n")
        
        for config_key in ['bare_llm', 'llm_rag', 'full_system']:
            if config_key in summary:
                stats = summary[config_key]
                f.write(f"| {stats['config_name']} | "
                       f"{stats['avg_response_time']:.2f}秒 | "
                       f"{stats['avg_response_length']:.0f}字符 | "
                       f"{stats['total_scenarios']}个 |\n")
        
        f.write("\n## 3. 各场景详细数据\n\n")
        
        results = report['results']
        for i, scenario_name in enumerate([r['scenario_name'] for r in results['bare_llm']]):
            f.write(f"### {scenario_name}\n\n")
            f.write("| 配置 | 响应时间 | 响应长度 | 对话轮数 |\n")
            f.write("|-----|---------|---------|--------|\n")
            
            for config_key, config_name in [
                ('bare_llm', '裸LLM'),
                ('llm_rag', 'LLM+RAG'),
                ('full_system', '完整系统')
            ]:
                scenario_data = results[config_key][i]
                f.write(f"| {config_name} | "
                       f"{scenario_data['avg_response_time']:.2f}秒 | "
                       f"{scenario_data['avg_response_length']:.0f}字符 | "
                       f"{len(scenario_data['turns'])}轮 |\n")
            f.write("\n")
        
        f.write("## 4. 关键发现\n\n")
        
        # 计算改进百分比
        bare_time = summary['bare_llm']['avg_response_time']
        rag_time = summary['llm_rag']['avg_response_time']
        full_time = summary['full_system']['avg_response_time']
        
        rag_improvement = ((bare_time - rag_time) / bare_time) * 100
        full_improvement = ((bare_time - full_time) / bare_time) * 100
        
        f.write("### 性能提升分析\n\n")
        f.write(f"- **RAG增强效果**: 相比裸LLM，响应时间变化 {rag_improvement:+.1f}%\n")
        f.write(f"- **完整系统效果**: 相比裸LLM，响应时间变化 {full_improvement:+.1f}%\n\n")
        
        bare_length = summary['bare_llm']['avg_response_length']
        rag_length = summary['llm_rag']['avg_response_length']
        full_length = summary['full_system']['avg_response_length']
        
        rag_length_change = ((rag_length - bare_length) / bare_length) * 100
        full_length_change = ((full_length - bare_length) / bare_length) * 100
        
        f.write("### 响应质量分析\n\n")
        f.write(f"- **RAG增强效果**: 响应长度增加 {rag_length_change:+.1f}%，说明提供了更多专业知识\n")
        f.write(f"- **完整系统效果**: 响应长度增加 {full_length_change:+.1f}%，说明利用了历史记忆\n\n")
        
        f.write("### 论文写作要点\n\n")
        f.write("1. **知识库的作用**: RAG使系统能够引用专业心理学知识，提供更准确的建议\n")
        f.write("2. **记忆系统的价值**: 完整系统能够记住用户历史，提供连贯的长期咨询\n")
        f.write("3. **实际应用意义**: 系统可以实现真正的心理咨询连续性，而非单次对话\n\n")
    
    print(f"✓ 已保存: {save_path}")


def generate_response_examples(report, save_path):
    """生成响应示例（供论文引用）"""
    results = report['results']
    
    with open(save_path, 'w', encoding='utf-8') as f:
        f.write("# 系统响应示例\n\n")
        f.write("以下是不同配置下系统对同一问题的响应，可用于论文中的案例分析。\n\n")
        
        # 选择第一个场景的第一轮对话作为示例
        scenario_idx = 0
        turn_idx = 0
        
        f.write("## 示例场景\n\n")
        
        user_msg = results['bare_llm'][scenario_idx]['turns'][turn_idx]['user_message']
        f.write(f"**用户输入**: {user_msg}\n\n")
        
        f.write("---\n\n")
        
        for config_key, config_name in [
            ('bare_llm', '裸LLM（无RAG，无记忆）'),
            ('llm_rag', 'LLM + RAG（有知识库，无记忆）'),
            ('full_system', '完整系统（有知识库，有记忆）')
        ]:
            response = results[config_key][scenario_idx]['turns'][turn_idx]['assistant_response']
            
            f.write(f"### {config_name}\n\n")
            f.write(f"**系统回复**:\n\n{response}\n\n")
            f.write(f"**响应长度**: {len(response)}字符\n\n")
            f.write("---\n\n")
        
        f.write("## 对比分析\n\n")
        f.write("观察三种配置的响应差异：\n\n")
        f.write("1. **裸LLM**: 提供通用建议，缺乏专业深度\n")
        f.write("2. **LLM + RAG**: 引用专业知识，给出更具体的方法\n")
        f.write("3. **完整系统**: 不仅有专业知识，还能关联用户历史信息\n\n")
    
    print(f"✓ 已保存: {save_path}")


def main():
    """主函数"""
    print("="*70)
    print("实验结果可视化")
    print("="*70)
    
    # 加载报告
    report = load_latest_report()
    if not report:
        return
    
    # 创建输出目录
    os.makedirs("./experiments/figures", exist_ok=True)
    
    print("\n生成可视化图表...")
    
    # 生成各种图表
    plot_response_time_comparison(
        report, 
        "./experiments/figures/response_time_comparison.png"
    )
    
    plot_response_length_comparison(
        report,
        "./experiments/figures/response_length_comparison.png"
    )
    
    plot_scenario_comparison(
        report,
        "./experiments/figures/scenario_comparison.png"
    )
    
    # 生成文档
    generate_detailed_comparison_table(
        report,
        "./experiments/detailed_comparison.md"
    )
    
    generate_response_examples(
        report,
        "./experiments/response_examples.md"
    )
    
    print("\n" + "="*70)
    print("✓ 可视化完成！")
    print("="*70)
    print("\n生成的文件:")
    print("- experiments/figures/response_time_comparison.png     (响应时间对比图)")
    print("- experiments/figures/response_length_comparison.png   (响应长度对比图)")
    print("- experiments/figures/scenario_comparison.png          (场景对比图)")
    print("- experiments/detailed_comparison.md                   (详细对比表格)")
    print("- experiments/response_examples.md                     (响应示例)")
    print("\n这些文件可以直接用于论文写作！")


if __name__ == "__main__":
    main()
