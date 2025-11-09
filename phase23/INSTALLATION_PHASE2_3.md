# 📦 第二、三阶段安装指南

> 评估系统完整功能 - 论文发表必备

---

## 🎯 本次交付内容

### 第二阶段：核心评估功能（3个文件）

1. **run_full_evaluation.py** - 完整评估脚本
2. **run_comparison.py** - 对比实验脚本
3. **generate_report.py** - Markdown报告生成器

### 第三阶段：可视化与报告（7个文件）

1. **radar_plot.py** - 雷达图生成器
2. **bar_plot.py** - 柱状图生成器
3. **generate_latex_report.py** - LaTeX报告生成器
4. **data_exporter.py** - 数据导出工具
5. **visualize_comparison.py** - 可视化管理脚本
6. **visualization/__init__.py** - 可视化模块初始化
7. **reporting/__init__.py** - 报告模块初始化

**总计：10个新文件**

---

## 📁 文件放置位置

### 第二阶段文件

```bash
psychological_counseling_system/
└── evaluation/
    └── scripts/
        ├── run_full_evaluation.py      # 新增 ⭐
        ├── run_comparison.py           # 新增 ⭐
        └── generate_report.py          # 新增 ⭐
```

### 第三阶段文件

```bash
psychological_counseling_system/
└── evaluation/
    ├── visualization/                  # 新增目录 ⭐
    │   ├── __init__.py                # 新增 ⭐
    │   ├── radar_plot.py              # 新增 ⭐
    │   └── bar_plot.py                # 新增 ⭐
    │
    ├── reporting/                      # 新增目录 ⭐
    │   ├── __init__.py                # 新增 ⭐
    │   ├── generate_latex_report.py   # 新增 ⭐
    │   └── data_exporter.py           # 新增 ⭐
    │
    └── scripts/
        └── visualize_comparison.py     # 新增 ⭐
```

---

## 🚀 快速安装

### 方法1：手动复制（推荐）

```bash
# 进入你的项目根目录
cd psychological_counseling_system

# 1. 复制第二阶段文件到scripts目录
cp /path/to/run_full_evaluation.py evaluation/scripts/
cp /path/to/run_comparison.py evaluation/scripts/
cp /path/to/generate_report.py evaluation/scripts/

# 2. 创建并复制visualization目录
mkdir -p evaluation/visualization
cp /path/to/visualization__init__.py evaluation/visualization/__init__.py
cp /path/to/radar_plot.py evaluation/visualization/
cp /path/to/bar_plot.py evaluation/visualization/

# 3. 创建并复制reporting目录
mkdir -p evaluation/reporting
cp /path/to/reporting__init__.py evaluation/reporting/__init__.py
cp /path/to/generate_latex_report.py evaluation/reporting/
cp /path/to/data_exporter.py evaluation/reporting/

# 4. 复制可视化管理脚本
cp /path/to/visualize_comparison.py evaluation/scripts/

# 5. 设置执行权限
chmod +x evaluation/scripts/run_full_evaluation.py
chmod +x evaluation/scripts/run_comparison.py
chmod +x evaluation/scripts/generate_report.py
chmod +x evaluation/scripts/visualize_comparison.py
```

### 方法2：批量安装脚本

创建 `install_phase2_3.sh`:

```bash
#!/bin/bash
# 安装第二、三阶段文件

SOURCE_DIR="/path/to/downloaded/files"
TARGET_DIR="."

echo "安装第二、三阶段文件..."

# 第二阶段 - scripts
echo "复制第二阶段文件..."
cp "$SOURCE_DIR/run_full_evaluation.py" "$TARGET_DIR/evaluation/scripts/"
cp "$SOURCE_DIR/run_comparison.py" "$TARGET_DIR/evaluation/scripts/"
cp "$SOURCE_DIR/generate_report.py" "$TARGET_DIR/evaluation/scripts/"

# 第三阶段 - visualization
echo "复制可视化模块..."
mkdir -p "$TARGET_DIR/evaluation/visualization"
cp "$SOURCE_DIR/visualization__init__.py" "$TARGET_DIR/evaluation/visualization/__init__.py"
cp "$SOURCE_DIR/radar_plot.py" "$TARGET_DIR/evaluation/visualization/"
cp "$SOURCE_DIR/bar_plot.py" "$TARGET_DIR/evaluation/visualization/"

# 第三阶段 - reporting
echo "复制报告模块..."
mkdir -p "$TARGET_DIR/evaluation/reporting"
cp "$SOURCE_DIR/reporting__init__.py" "$TARGET_DIR/evaluation/reporting/__init__.py"
cp "$SOURCE_DIR/generate_latex_report.py" "$TARGET_DIR/evaluation/reporting/"
cp "$SOURCE_DIR/data_exporter.py" "$TARGET_DIR/evaluation/reporting/"

# 可视化管理脚本
cp "$SOURCE_DIR/visualize_comparison.py" "$TARGET_DIR/evaluation/scripts/"

# 设置权限
chmod +x "$TARGET_DIR/evaluation/scripts/"*.py

echo ""
echo "===================="
echo "安装完成！"
echo "===================="
```

---

## 📦 依赖安装

安装额外的Python包（用于可视化和数据导出）：

```bash
# 必需的可视化包
pip install matplotlib numpy

# 可选的数据导出包（推荐安装）
pip install pandas openpyxl

# 如果需要更好的中文字体支持
# macOS: 已有 Arial Unicode MS
# Linux: sudo apt-get install fonts-wqy-zenhei
# Windows: 系统自带 SimHei
```

---

## ✅ 验证安装

### 检查文件是否存在

```bash
cd psychological_counseling_system

# 检查第二阶段文件
ls -l evaluation/scripts/run_full_evaluation.py
ls -l evaluation/scripts/run_comparison.py
ls -l evaluation/scripts/generate_report.py

# 检查第三阶段文件
ls -l evaluation/visualization/__init__.py
ls -l evaluation/visualization/radar_plot.py
ls -l evaluation/visualization/bar_plot.py
ls -l evaluation/reporting/__init__.py
ls -l evaluation/reporting/generate_latex_report.py
ls -l evaluation/reporting/data_exporter.py
ls -l evaluation/scripts/visualize_comparison.py
```

### 测试导入

```bash
# 测试可视化模块
python -c "from evaluation.visualization import create_radar_plot; print('✓ 可视化模块导入成功')"

# 测试报告模块
python -c "from evaluation.reporting import LaTeXReportGenerator; print('✓ 报告模块导入成功')"
```

---

## 🎯 使用示例

### 1. 运行完整评估（200样本）

```bash
# 基础用法
python evaluation/scripts/run_full_evaluation.py

# 自定义样本数
python evaluation/scripts/run_full_evaluation.py --samples 100

# 指定配置文件
python evaluation/scripts/run_full_evaluation.py \
    --system-config configs/config.yaml \
    --eval-config evaluation/configs/full_eval_config.yaml
```

**预计用时**: 30-60分钟（200样本）  
**输出**: `evaluation/results/full_evaluation/full_evaluation_YYYYMMDD_HHMMSS.json`

---

### 2. 运行对比实验

```bash
# 基础用法（50样本）
python evaluation/scripts/run_comparison.py

# 自定义样本数
python evaluation/scripts/run_comparison.py --samples 100

# 不保存结果（仅查看）
python evaluation/scripts/run_comparison.py --no-save
```

**预计用时**: 15-30分钟（50样本）  
**输出**: `evaluation/results/comparison/comparison_YYYYMMDD_HHMMSS.json`

---

### 3. 生成Markdown报告

```bash
# 从对比实验结果生成报告
python evaluation/scripts/generate_report.py \
    --result evaluation/results/comparison/comparison_20241109_120000.json

# 指定输出文件
python evaluation/scripts/generate_report.py \
    --result comparison.json \
    --output report.md
```

**输出**: Markdown格式的详细报告

---

### 4. 生成可视化图表

```bash
# 一键生成所有图表
python evaluation/scripts/visualize_comparison.py \
    --result evaluation/results/comparison/comparison_20241109_120000.json

# 指定输出目录
python evaluation/scripts/visualize_comparison.py \
    --result comparison.json \
    --output-dir figures/
```

**输出**:
- `radar_comparison.png` - 雷达图
- `clinical_comparison.png` - 临床指标柱状图
- `technical_comparison.png` - 技术指标柱状图
- `improvement_comparison.png` - 改进幅度柱状图

---

### 5. 生成LaTeX报告

```bash
# 生成完整LaTeX报告
python evaluation/reporting/generate_latex_report.py \
    --result comparison.json

# 分别生成各个表格
python evaluation/reporting/generate_latex_report.py \
    --result comparison.json \
    --separate
```

**输出**: LaTeX表格，可直接复制到论文中

---

### 6. 导出数据

```bash
# 导出为Excel
python evaluation/reporting/data_exporter.py \
    --result comparison.json \
    --format excel

# 导出为CSV
python evaluation/reporting/data_exporter.py \
    --result comparison.json \
    --format csv

# 导出所有格式
python evaluation/reporting/data_exporter.py \
    --result comparison.json \
    --format all
```

**输出**: Excel, CSV, 或文本格式的数据文件

---

## 📊 完整工作流程（论文发表）

### 第1步：运行对比实验

```bash
# 运行50-100样本的对比实验
python evaluation/scripts/run_comparison.py --samples 100
```

**得到**: `comparison_YYYYMMDD_HHMMSS.json`

---

### 第2步：生成可视化图表

```bash
# 使用上一步的结果生成图表
python evaluation/scripts/visualize_comparison.py \
    --result evaluation/results/comparison/comparison_YYYYMMDD_HHMMSS.json
```

**得到**: 4张PNG图表（论文用）

---

### 第3步：生成LaTeX表格

```bash
# 生成LaTeX表格
python evaluation/reporting/generate_latex_report.py \
    --result evaluation/results/comparison/comparison_YYYYMMDD_HHMMSS.json \
    --separate
```

**得到**: LaTeX表格代码

---

### 第4步：导出数据

```bash
# 导出Excel用于数据分析
python evaluation/reporting/data_exporter.py \
    --result evaluation/results/comparison/comparison_YYYYMMDD_HHMMSS.json \
    --format excel
```

**得到**: Excel数据文件

---

### 第5步：整理论文素材

现在你有了：
- ✅ 4张高质量PNG图表
- ✅ LaTeX表格代码
- ✅ Excel数据文件
- ✅ JSON原始结果

**可以开始写论文了！** 📝

---

## 🎨 论文图表使用建议

### 雷达图使用场景

- **适合**: 多维度综合对比
- **论文位置**: 结果章节，展示整体性能
- **说明文字**: "图X展示了三种系统配置在7个临床指标上的性能对比"

### 柱状图使用场景

- **适合**: 单一指标详细对比
- **论文位置**: 
  - 临床指标图：展示专业质量
  - 技术指标图：展示技术性能
  - 改进幅度图：展示系统优势
- **说明文字**: "如图X所示，完整系统在各项指标上均优于基线"

### LaTeX表格使用

- **适合**: 详细数值展示
- **论文位置**: 结果章节，补充图表
- **使用方法**: 直接复制到.tex文件中

---

## ⚠️ 常见问题

### Q1: matplotlib中文显示乱码？

**解决方案**:
```bash
# macOS
# 已有 Arial Unicode MS，通常无需额外配置

# Linux
sudo apt-get install fonts-wqy-zenhei

# Windows
# 系统自带 SimHei，通常无需额外配置
```

### Q2: pandas/openpyxl未安装？

**解决方案**:
```bash
pip install pandas openpyxl
```

如果仍无法使用Excel导出，会自动降级到CSV格式。

### Q3: 图表生成失败？

**检查清单**:
1. ✅ 是否安装matplotlib和numpy
2. ✅ 结果JSON文件是否完整
3. ✅ 输出目录是否有写权限

---

## 📝 完整目录结构（新增后）

```
psychological_counseling_system/
└── evaluation/
    ├── scripts/
    │   ├── run_quick_test.py          # 第一阶段
    │   ├── run_full_evaluation.py     # 新增 ⭐
    │   ├── run_comparison.py          # 新增 ⭐
    │   ├── generate_report.py         # 新增 ⭐
    │   └── visualize_comparison.py    # 新增 ⭐
    │
    ├── visualization/                  # 新增目录 ⭐
    │   ├── __init__.py
    │   ├── radar_plot.py
    │   └── bar_plot.py
    │
    └── reporting/                      # 新增目录 ⭐
        ├── __init__.py
        ├── generate_latex_report.py
        └── data_exporter.py
```

---

## 🎉 安装完成检查清单

安装后，请确认：

- [ ] 第二阶段3个scripts文件已复制
- [ ] visualization目录已创建，包含3个文件
- [ ] reporting目录已创建，包含3个文件
- [ ] 所有Python脚本有执行权限
- [ ] matplotlib和numpy已安装
- [ ] pandas和openpyxl已安装（可选）
- [ ] 可以成功导入可视化和报告模块

全部打勾？**恭喜，安装成功！** 🎊

---

## 💡 使用技巧

### 技巧1：先小规模测试

```bash
# 先用10个样本快速测试
python evaluation/scripts/run_comparison.py --samples 10

# 确认无误后再运行完整评估
python evaluation/scripts/run_comparison.py --samples 100
```

### 技巧2：保存中间结果

所有评估结果都会自动保存JSON文件，可以：
- 重复生成图表而不重新评估
- 对比不同时间的实验结果
- 备份重要的评估数据

### 技巧3：批量生成图表

```bash
# 对多个结果文件批量生成图表
for file in evaluation/results/comparison/*.json; do
    python evaluation/scripts/visualize_comparison.py --result "$file"
done
```

---

## 📞 需要帮助？

如果遇到问题：

1. **查看错误信息** - 通常会提示具体问题
2. **检查依赖** - 确认所有包已安装
3. **验证结果文件** - 确认JSON文件完整且格式正确
4. **查看示例** - 参考本文档的使用示例

---

**祝使用顺利！论文发表成功！** 🎓📊🚀

---

**安装指南版本**: v2.0  
**适用阶段**: 第二、三阶段  
**最后更新**: 2024-11-09
