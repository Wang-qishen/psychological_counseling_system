#!/bin/bash
# 一键生成论文架构图脚本

echo "=================================="
echo "  论文架构图生成工具"
echo "=================================="
echo ""

# 检查conda是否可用
if ! command -v conda &> /dev/null; then
    echo "❌ 错误: 未找到conda命令"
    echo "请先安装Anaconda或Miniconda"
    exit 1
fi

# 检查环境是否存在
if conda env list | grep -q "paper-diagram"; then
    echo "✅ 环境已存在: paper-diagram"
else
    echo "📦 正在创建conda环境..."
    conda env create -f environment.yml
    if [ $? -ne 0 ]; then
        echo "❌ 环境创建失败"
        exit 1
    fi
    echo "✅ 环境创建成功"
fi

echo ""
echo "🚀 开始生成图片..."
echo ""

# 激活环境并运行脚本
eval "$(conda shell.bash hook)"
conda activate paper-diagram

python generate_architecture.py

if [ $? -eq 0 ]; then
    echo ""
    echo "=================================="
    echo "  ✅ 生成成功！"
    echo "=================================="
    echo ""
    echo "📁 生成的文件："
    ls -lh architecture_diagram.*
    echo ""
    echo "💡 提示："
    echo "   - architecture_diagram.png 适合Word文档"
    echo "   - architecture_diagram.pdf 适合LaTeX论文"
else
    echo ""
    echo "❌ 生成失败，请查看错误信息"
    exit 1
fi

conda deactivate
