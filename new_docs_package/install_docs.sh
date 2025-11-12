#!/bin/bash

# ================================================================
# 文档安装脚本
# 用途：将新文档复制到项目目录中
# ================================================================

echo "=========================================="
echo "安装新文档结构..."
echo "=========================================="

# 目标目录（你的项目根目录）
TARGET_DIR="/cephfs/shared/pengyang/deform_test_pengyang/src/benchmark_qishen/other/vla/base/sw/psychological_counseling_system"

# 检查目标目录是否存在
if [ ! -d "$TARGET_DIR" ]; then
    echo "❌ 错误: 目标目录不存在: $TARGET_DIR"
    echo "请修改脚本中的 TARGET_DIR 变量为你的项目路径"
    exit 1
fi

echo ""
echo "目标目录: $TARGET_DIR"
echo ""

# 当前脚本所在目录（新文档包目录）
SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "源目录: $SOURCE_DIR"
echo ""

# ==========================================
# 第一步：备份原有重要文档
# ==========================================
echo "[1/4] 备份原有重要文档..."

BACKUP_DIR="$TARGET_DIR/docs_backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

# 备份原有README和INSTALLATION
if [ -f "$TARGET_DIR/README.md" ]; then
    cp "$TARGET_DIR/README.md" "$BACKUP_DIR/"
    echo "✓ 已备份 README.md"
fi

if [ -f "$TARGET_DIR/INSTALLATION.md" ]; then
    cp "$TARGET_DIR/INSTALLATION.md" "$BACKUP_DIR/"
    echo "✓ 已备份 INSTALLATION.md"
fi

echo "✓ 备份完成: $BACKUP_DIR"

# ==========================================
# 第二步：安装根目录文档
# ==========================================
echo ""
echo "[2/4] 安装根目录文档..."

# 复制主要文档
cp "$SOURCE_DIR/README.md" "$TARGET_DIR/"
echo "✓ 已安装 README.md"

cp "$SOURCE_DIR/README_zh.md" "$TARGET_DIR/"
echo "✓ 已安装 README_zh.md"

cp "$SOURCE_DIR/INSTALLATION.md" "$TARGET_DIR/"
echo "✓ 已安装 INSTALLATION.md"

cp "$SOURCE_DIR/LICENSE" "$TARGET_DIR/"
echo "✓ 已安装 LICENSE"

# ==========================================
# 第三步：安装docs目录
# ==========================================
echo ""
echo "[3/4] 安装docs目录..."

# 创建docs目录（如果不存在）
mkdir -p "$TARGET_DIR/docs"

# 复制所有docs文档
cp "$SOURCE_DIR/docs/architecture.md" "$TARGET_DIR/docs/"
echo "✓ 已安装 docs/architecture.md"

cp "$SOURCE_DIR/docs/quickstart.md" "$TARGET_DIR/docs/"
echo "✓ 已安装 docs/quickstart.md"

cp "$SOURCE_DIR/docs/configuration.md" "$TARGET_DIR/docs/"
echo "✓ 已安装 docs/configuration.md"

cp "$SOURCE_DIR/docs/evaluation.md" "$TARGET_DIR/docs/"
echo "✓ 已安装 docs/evaluation.md"

cp "$SOURCE_DIR/docs/examples.md" "$TARGET_DIR/docs/"
echo "✓ 已安装 docs/examples.md"

# ==========================================
# 第四步：安装子模块README
# ==========================================
echo ""
echo "[4/4] 安装子模块README..."

# evaluation目录
if [ -d "$TARGET_DIR/evaluation" ]; then
    cp "$SOURCE_DIR/evaluation/README.md" "$TARGET_DIR/evaluation/"
    echo "✓ 已安装 evaluation/README.md"
fi

# models目录
if [ -d "$TARGET_DIR/models" ]; then
    cp "$SOURCE_DIR/models/README.md" "$TARGET_DIR/models/"
    echo "✓ 已安装 models/README.md"
fi

# ==========================================
# 完成
# ==========================================
echo ""
echo "=========================================="
echo "文档安装完成！"
echo "=========================================="
echo ""
echo "已安装的文档："
echo "  - README.md (主文档)"
echo "  - README_zh.md (中文版)"
echo "  - INSTALLATION.md (安装指南)"
echo "  - LICENSE (开源协议)"
echo "  - docs/ (5个详细文档)"
echo "  - evaluation/README.md"
echo "  - models/README.md"
echo ""
echo "备份位置: $BACKUP_DIR"
echo ""
echo "下一步："
echo "  1. 查看新的 README.md"
echo "  2. 运行清理脚本删除旧文档（可选）"
echo "  3. 测试系统是否正常工作"
echo ""

# 给出cleanup.sh的提示
if [ -f "$SOURCE_DIR/cleanup.sh" ]; then
    echo "要删除旧文档，请运行:"
    echo "  bash cleanup.sh"
    echo ""
fi

echo "完成!"
