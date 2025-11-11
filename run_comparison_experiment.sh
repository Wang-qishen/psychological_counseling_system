#!/bin/bash
# 一键运行对比实验脚本
# 自动完成: 实验运行 -> 可视化 -> 报告生成

echo "========================================================================"
echo "                    🚀 对比实验一键运行脚本                             "
echo "========================================================================"
echo ""

# 配置参数
NUM_QUESTIONS=${1:-30}  # 默认30个问题
CONFIG_FILE=${2:-"configs/config.yaml"}

echo "📋 实验配置:"
echo "   - 测试问题数: $NUM_QUESTIONS"
echo "   - 配置文件: $CONFIG_FILE"
echo ""

# 步骤1: 运行对比实验
echo "========================================================================"
echo "  步骤 1/3: 运行对比实验"
echo "========================================================================"
echo ""

python evaluation/scripts/simple_comparison.py \
    --num-questions $NUM_QUESTIONS \
    --config $CONFIG_FILE \
    --skip-manual

if [ $? -ne 0 ]; then
    echo ""
    echo "✗ 实验运行失败！"
    exit 1
fi

# 获取最新的结果文件
RESULT_FILE=$(ls -t evaluation/results/comparison/comparison_*.json | head -1)

if [ -z "$RESULT_FILE" ]; then
    echo ""
    echo "✗ 找不到结果文件！"
    exit 1
fi

echo ""
echo "✓ 实验完成！结果文件: $RESULT_FILE"

# 步骤2: 生成可视化图表
echo ""
echo "========================================================================"
echo "  步骤 2/3: 生成可视化图表"
echo "========================================================================"
echo ""

python evaluation/scripts/visualize_comparison_simple.py "$RESULT_FILE"

if [ $? -ne 0 ]; then
    echo ""
    echo "⚠️  可视化生成失败，但实验结果已保存"
fi

# 步骤3: 生成评估报告
echo ""
echo "========================================================================"
echo "  步骤 3/3: 生成评估报告"
echo "========================================================================"
echo ""

python evaluation/scripts/generate_comparison_report.py "$RESULT_FILE"

if [ $? -ne 0 ]; then
    echo ""
    echo "⚠️  报告生成失败，但实验结果已保存"
fi

# 完成
echo ""
echo "========================================================================"
echo "                        ✅ 所有步骤完成！"
echo "========================================================================"
echo ""
echo "📁 输出文件位置:"
echo "   - 实验结果: $RESULT_FILE"
echo "   - 图表: evaluation/results/comparison/figures/"
echo "   - 报告: evaluation/results/comparison/reports/"
echo ""
echo "📝 下一步:"
echo "   1. 查看图表用于论文: open evaluation/results/comparison/figures/"
echo "   2. 查看详细报告: cat evaluation/results/comparison/reports/*.md"
echo "   3. 进行人工评估(可选): python evaluation/scripts/manual_evaluation.py"
echo ""
echo "🎓 期末作业提示:"
echo "   - 图表可直接插入论文"
echo "   - Markdown报告包含完整实验数据"
echo "   - 建议补充人工评估以增强说服力"
echo ""
