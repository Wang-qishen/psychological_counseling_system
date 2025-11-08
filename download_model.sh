#!/bin/bash
# 自动下载本地模型脚本

set -e

echo "======================================"
echo "下载本地模型 (TinyLlama)"
echo "======================================"
echo ""

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# 创建models目录
mkdir -p models
cd models

MODEL_FILE="tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
MODEL_URL="https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/$MODEL_FILE"

# 检查是否已存在
if [ -f "$MODEL_FILE" ]; then
    echo "✅ 模型已存在: $MODEL_FILE"
    echo "文件大小: $(du -h $MODEL_FILE | cut -f1)"
    echo ""
    read -p "是否重新下载? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "跳过下载"
        exit 0
    fi
    rm -f "$MODEL_FILE"
fi

echo "开始下载模型..."
echo "URL: $MODEL_URL"
echo "目标: ./models/$MODEL_FILE"
echo ""

# 检查wget或curl
if command -v wget &> /dev/null; then
    echo "使用 wget 下载..."
    wget --progress=bar:force:noscroll "$MODEL_URL" -O "$MODEL_FILE"
elif command -v curl &> /dev/null; then
    echo "使用 curl 下载..."
    curl -L --progress-bar "$MODEL_URL" -o "$MODEL_FILE"
else
    echo "❌ 错误: 需要 wget 或 curl"
    echo ""
    echo "请安装其中一个:"
    echo "  sudo apt install wget"
    echo "  或"
    echo "  sudo apt install curl"
    exit 1
fi

# 检查下载是否成功
if [ -f "$MODEL_FILE" ]; then
    FILE_SIZE=$(du -h "$MODEL_FILE" | cut -f1)
    echo ""
    echo "======================================"
    echo "✅ 下载完成!"
    echo "======================================"
    echo "模型文件: $MODEL_FILE"
    echo "文件大小: $FILE_SIZE"
    echo "位置: $(pwd)/$MODEL_FILE"
    echo ""
    echo "下一步:"
    echo "1. 编辑 configs/config.yaml"
    echo "2. 设置: llm.backend = 'local'"
    echo "3. 运行测试: python tests/test_system.py"
else
    echo ""
    echo "❌ 下载失败"
    exit 1
fi
