#!/bin/bash

# 数据集集成一键运行脚本
# 用途: 下载、处理、导入中文心理咨询数据集到RAG系统

echo "========================================"
echo "  中文心理咨询数据集集成工具"
echo "========================================"
echo ""

# 设置颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 检查Python环境
echo -e "${YELLOW}[1/4] 检查Python环境...${NC}"
if ! command -v python &> /dev/null; then
    echo -e "${RED}✗ Python未安装${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python已安装${NC}"

# 检查依赖
echo ""
echo -e "${YELLOW}[2/4] 检查依赖包...${NC}"
python -c "import requests" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}安装requests...${NC}"
    pip install requests --break-system-packages
fi
echo -e "${GREEN}✓ 依赖检查完成${NC}"

# 步骤1: 下载数据集
echo ""
echo -e "${YELLOW}[3/4] 下载数据集...${NC}"
echo "这可能需要几分钟,请耐心等待..."
python data_integration/dataset_downloader.py --dataset all

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ 数据集下载完成${NC}"
else
    echo -e "${RED}✗ 数据集下载失败${NC}"
    echo "请查看 data/downloaded_datasets/数据集下载指南.md 了解手动下载方式"
fi

# 步骤2: 处理数据集
echo ""
echo -e "${YELLOW}[4/4] 处理数据集...${NC}"
python data_integration/process_datasets.py

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ 数据处理完成${NC}"
else
    echo -e "${RED}✗ 数据处理失败${NC}"
    exit 1
fi

# 步骤3: 导入到RAG
echo ""
echo -e "${YELLOW}导入到RAG知识库...${NC}"
echo "这可能需要较长时间,建议先喝杯咖啡 ☕"
python data_integration/import_to_rag.py --verify

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ 导入成功!${NC}"
else
    echo -e "${RED}✗ 导入失败${NC}"
    exit 1
fi

# 完成
echo ""
echo "========================================"
echo -e "${GREEN}  ✓ 全部完成!${NC}"
echo "========================================"
echo ""
echo "已完成以下工作:"
echo "  1. 下载了SmileChat等开源数据集"
echo "  2. 处理并转换为RAG可用格式"
echo "  3. 导入到ChromaDB知识库"
echo ""
echo "数据位置:"
echo "  - 原始数据: ./data/downloaded_datasets/"
echo "  - 处理后: ./data/processed_knowledge/"
echo "  - 向量库: ./data/vector_db/"
echo ""
echo "下一步:"
echo "  运行测试脚本验证集成效果"
echo "  python examples/test_new_knowledge.py"
echo ""
