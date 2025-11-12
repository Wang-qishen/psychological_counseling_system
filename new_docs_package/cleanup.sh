#!/bin/bash

# ================================================================
# 文档清理脚本
# 用途：删除开发过程中的临时文档，保留核心文档
# ================================================================

echo "=========================================="
echo "开始清理文档..."
echo "=========================================="

# 当前目录（根目录）
ROOT_DIR="/cephfs/shared/pengyang/deform_test_pengyang/src/benchmark_qishen/other/vla/base/sw/psychological_counseling_system"

cd "$ROOT_DIR" || exit 1

# ==========================================
# 第一步：删除开发文档（8个）
# ==========================================
echo ""
echo "[1/4] 删除开发文档..."

rm -f 00-START_HERE.md
rm -f DELIVERY_FINAL.md
rm -f DELIVERY_SUMMARY.md
rm -f PHASE1_SUMMARY.md
rm -f README_PHASE1.md
rm -f UPDATE_SUMMARY.md
rm -f FILE_CHECKLIST.md
rm -f CHANGELOG.md

echo "✓ 已删除开发文档"

# ==========================================
# 第二步：删除冗余/重复文档（6个）
# ==========================================
echo ""
echo "[2/4] 删除冗余文档..."

rm -f DATA_INTEGRATION_GUIDE.md
rm -f EXPERIMENT_GUIDE.md
rm -f MODEL_GUIDE.md
rm -f 安装说明.md
rm -f DIRECTORY_STRUCTURE.txt
rm -f FILES_TO_COPY.txt

echo "✓ 已删除冗余文档"

# ==========================================
# 第三步：删除整个目录（4个）
# ==========================================
echo ""
echo "[3/4] 删除无关目录..."

rm -rf chatdatadoc/
rm -rf comparison_experiment_module/
rm -rf data_integration/
rm -rf phase23/

echo "✓ 已删除无关目录"

# ==========================================
# 第四步：删除evaluation中的冗余文档
# ==========================================
echo ""
echo "[4/4] 清理evaluation目录..."

rm -f evaluation/COMPARISON_GUIDE.md
rm -f evaluation/COMPARISON_README.md

echo "✓ 已清理evaluation目录"

# ==========================================
# 第五步：删除打包文件和临时文件
# ==========================================
echo ""
echo "[额外] 删除打包文件和临时文件..."

rm -f comparison_experiment_module.tar.gz
rm -f evaluation_phase1_delivery.tar.gz
rm -f new_files_package.zip
rm -rf new_files_to_add/
rm -rf download_here/

echo "✓ 已删除打包文件"

# ==========================================
# 完成
# ==========================================
echo ""
echo "=========================================="
echo "清理完成！"
echo "=========================================="
echo ""
echo "已删除的内容："
echo "  - 8个开发文档"
echo "  - 6个冗余文档"
echo "  - 4个无关目录（chatdatadoc, comparison_experiment_module, data_integration, phase23）"
echo "  - evaluation中的2个冗余文档"
echo "  - 打包文件和临时目录"
echo ""
echo "现在请运行新文档安装脚本来创建标准文档结构"
echo ""
