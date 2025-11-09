# 📍 文件位置快速参考

> 第二、三阶段文件应该放在原仓库的什么位置

---

## 🎯 核心原则

**所有文件都是增量添加，不覆盖任何原有文件！**

---

## 📁 第二阶段文件（3个）

### evaluation/scripts/ 目录

```
原仓库/psychological_counseling_system/evaluation/scripts/
├── run_quick_test.py              # 已存在（第一阶段）
├── run_full_evaluation.py         # ⭐ 新增
├── run_comparison.py              # ⭐ 新增
└── generate_report.py             # ⭐ 新增
```

**复制命令**:
```bash
cp run_full_evaluation.py 原仓库路径/evaluation/scripts/
cp run_comparison.py 原仓库路径/evaluation/scripts/
cp generate_report.py 原仓库路径/evaluation/scripts/
```

---

## 📁 第三阶段文件（7个）

### evaluation/visualization/ 目录（新建）

```
原仓库/psychological_counseling_system/evaluation/visualization/
├── __init__.py                    # ⭐ 新增
├── radar_plot.py                  # ⭐ 新增
└── bar_plot.py                    # ⭐ 新增
```

**复制命令**:
```bash
mkdir -p 原仓库路径/evaluation/visualization
cp visualization__init__.py 原仓库路径/evaluation/visualization/__init__.py
cp radar_plot.py 原仓库路径/evaluation/visualization/
cp bar_plot.py 原仓库路径/evaluation/visualization/
```

### evaluation/reporting/ 目录（新建）

```
原仓库/psychological_counseling_system/evaluation/reporting/
├── __init__.py                    # ⭐ 新增
├── generate_latex_report.py       # ⭐ 新增
└── data_exporter.py               # ⭐ 新增
```

**复制命令**:
```bash
mkdir -p 原仓库路径/evaluation/reporting
cp reporting__init__.py 原仓库路径/evaluation/reporting/__init__.py
cp generate_latex_report.py 原仓库路径/evaluation/reporting/
cp data_exporter.py 原仓库路径/evaluation/reporting/
```

### evaluation/scripts/ 目录（追加）

```
原仓库/psychological_counseling_system/evaluation/scripts/
└── visualize_comparison.py        # ⭐ 新增
```

**复制命令**:
```bash
cp visualize_comparison.py 原仓库路径/evaluation/scripts/
```

---

## 📂 完整目录结构（新增后）

```
psychological_counseling_system/
└── evaluation/
    ├── README.md                   # 第一阶段
    ├── __init__.py                 # 原有
    ├── framework.py                # 原有
    │
    ├── configs/                    # 第一阶段
    │   ├── default_config.yaml
    │   ├── quick_test_config.yaml
    │   └── full_eval_config.yaml
    │
    ├── datasets/                   # 第一阶段
    │   ├── __init__.py
    │   ├── dataset_loader.py
    │   ├── mentalchat_loader.py
    │   ├── memory_test_generator.py
    │   └── download_datasets.py
    │
    ├── metrics/                    # 原有
    │   ├── __init__.py
    │   ├── technical_metrics.py
    │   ├── clinical_metrics.py
    │   ├── safety_metrics.py
    │   ├── memory_metrics.py
    │   └── rag_metrics.py
    │
    ├── evaluators/                 # 原有
    │   ├── __init__.py
    │   ├── system_evaluator.py
    │   └── comparison_evaluator.py
    │
    ├── scripts/                    # 第一阶段 + 第二、三阶段
    │   ├── run_quick_test.py               # 第一阶段
    │   ├── run_full_evaluation.py          # ⭐ 第二阶段
    │   ├── run_comparison.py               # ⭐ 第二阶段
    │   ├── generate_report.py              # ⭐ 第二阶段
    │   └── visualize_comparison.py         # ⭐ 第三阶段
    │
    ├── visualization/              # ⭐ 第三阶段（新目录）
    │   ├── __init__.py
    │   ├── radar_plot.py
    │   └── bar_plot.py
    │
    └── reporting/                  # ⭐ 第三阶段（新目录）
        ├── __init__.py
        ├── generate_latex_report.py
        └── data_exporter.py
```

---

## ✅ 快速验证

复制完成后，在原仓库根目录执行：

```bash
cd 原仓库路径/psychological_counseling_system

# 验证第二阶段文件
ls -l evaluation/scripts/run_full_evaluation.py
ls -l evaluation/scripts/run_comparison.py
ls -l evaluation/scripts/generate_report.py

# 验证第三阶段文件
ls -l evaluation/visualization/__init__.py
ls -l evaluation/visualization/radar_plot.py
ls -l evaluation/visualization/bar_plot.py
ls -l evaluation/reporting/__init__.py
ls -l evaluation/reporting/generate_latex_report.py
ls -l evaluation/reporting/data_exporter.py
ls -l evaluation/scripts/visualize_comparison.py
```

如果所有文件都存在，说明复制成功！✅

---

## 🔧 设置执行权限

```bash
cd 原仓库路径/psychological_counseling_system

chmod +x evaluation/scripts/run_full_evaluation.py
chmod +x evaluation/scripts/run_comparison.py
chmod +x evaluation/scripts/generate_report.py
chmod +x evaluation/scripts/visualize_comparison.py
chmod +x evaluation/visualization/radar_plot.py
chmod +x evaluation/visualization/bar_plot.py
chmod +x evaluation/reporting/generate_latex_report.py
chmod +x evaluation/reporting/data_exporter.py
```

---

## 📝 一键安装脚本

创建 `install_phase2_3.sh` 并执行：

```bash
#!/bin/bash
# 一键安装第二、三阶段文件

# 设置路径（请修改为你的实际路径）
SOURCE_DIR="下载的文件目录"
TARGET_DIR="原仓库路径/psychological_counseling_system"

echo "开始安装第二、三阶段文件..."

# 第二阶段 - scripts
echo "复制第二阶段文件..."
cp "$SOURCE_DIR/run_full_evaluation.py" "$TARGET_DIR/evaluation/scripts/"
cp "$SOURCE_DIR/run_comparison.py" "$TARGET_DIR/evaluation/scripts/"
cp "$SOURCE_DIR/generate_report.py" "$TARGET_DIR/evaluation/scripts/"

# 第三阶段 - visualization
echo "创建visualization目录..."
mkdir -p "$TARGET_DIR/evaluation/visualization"
cp "$SOURCE_DIR/visualization__init__.py" "$TARGET_DIR/evaluation/visualization/__init__.py"
cp "$SOURCE_DIR/radar_plot.py" "$TARGET_DIR/evaluation/visualization/"
cp "$SOURCE_DIR/bar_plot.py" "$TARGET_DIR/evaluation/visualization/"

# 第三阶段 - reporting
echo "创建reporting目录..."
mkdir -p "$TARGET_DIR/evaluation/reporting"
cp "$SOURCE_DIR/reporting__init__.py" "$TARGET_DIR/evaluation/reporting/__init__.py"
cp "$SOURCE_DIR/generate_latex_report.py" "$TARGET_DIR/evaluation/reporting/"
cp "$SOURCE_DIR/data_exporter.py" "$TARGET_DIR/evaluation/reporting/"

# 第三阶段 - visualize script
cp "$SOURCE_DIR/visualize_comparison.py" "$TARGET_DIR/evaluation/scripts/"

# 设置权限
echo "设置执行权限..."
chmod +x "$TARGET_DIR/evaluation/scripts/"*.py
chmod +x "$TARGET_DIR/evaluation/visualization/"*.py
chmod +x "$TARGET_DIR/evaluation/reporting/"*.py

echo ""
echo "===================="
echo "安装完成！"
echo "===================="
echo ""
echo "已安装文件："
echo "  第二阶段: 3个文件"
echo "  第三阶段: 7个文件"
echo "  总计: 10个文件"
echo ""
echo "下一步："
echo "  1. 安装依赖: pip install matplotlib numpy pandas openpyxl"
echo "  2. 验证安装: python -c 'from evaluation.visualization import create_radar_plot'"
echo "  3. 运行测试: python evaluation/scripts/run_comparison.py --samples 10"
```

---

## 🎯 关键要点

1. **不要覆盖任何原有文件** - 所有文件都是新增的
2. **创建新目录** - visualization/ 和 reporting/ 是新目录
3. **注意__init__.py** - 文件名是 `visualization__init__.py` 和 `reporting__init__.py`，复制时要改名为 `__init__.py`
4. **设置权限** - Python脚本需要执行权限

---

**完成后请阅读**:
- `README_PHASE2_3.md` - 功能说明
- `INSTALLATION_PHASE2_3.md` - 详细安装指南

**祝安装顺利！** 🚀
