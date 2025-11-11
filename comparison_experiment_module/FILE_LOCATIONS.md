# 对比实验模块 - 文件放置说明

## 📂 新增文件位置对照表

本次开发为你的心理咨询系统新增了对比实验功能。以下是所有新增文件的位置说明。

---

## 🆕 新增文件清单

### 1. 配置文件

| 文件 | 位置 | 说明 |
|------|------|------|
| `comparison_config.yaml` | `evaluation/configs/` | 对比实验配置文件 |

### 2. 数据集

| 文件 | 位置 | 说明 |
|------|------|------|
| `comparison_test_questions.json` | `evaluation/datasets/` | 30个精选测试问题 |

### 3. 核心脚本

| 文件 | 位置 | 说明 |
|------|------|------|
| `simple_comparison.py` | `evaluation/scripts/` | 主实验脚本 |
| `visualize_comparison_simple.py` | `evaluation/scripts/` | 可视化生成脚本 |
| `generate_comparison_report.py` | `evaluation/scripts/` | 报告生成脚本 |

### 4. 一键运行脚本

| 文件 | 位置 | 说明 |
|------|------|------|
| `run_comparison_experiment.sh` | 项目根目录 | 一键运行所有步骤 |

### 5. 文档

| 文件 | 位置 | 说明 |
|------|------|------|
| `COMPARISON_GUIDE.md` | `evaluation/` | 详细使用指南 |
| `COMPARISON_README.md` | `evaluation/` | 模块说明文档 |
| `FILE_LOCATIONS.md` | `evaluation/` | 本文件（放置说明）|

---

## 📋 完整的文件树结构

新增文件在原仓库中的位置：

```
psychological_counseling_system/              # 项目根目录
│
├── run_comparison_experiment.sh             # ⭐ 新增：一键运行脚本
│
├── configs/
│   └── config.yaml                           # 已有：系统配置
│
├── evaluation/
│   │
│   ├── COMPARISON_GUIDE.md                   # ⭐ 新增：使用指南
│   ├── COMPARISON_README.md                  # ⭐ 新增：模块说明
│   ├── FILE_LOCATIONS.md                     # ⭐ 新增：本文件
│   │
│   ├── configs/
│   │   ├── default_config.yaml               # 已有
│   │   └── comparison_config.yaml            # ⭐ 新增：对比实验配置
│   │
│   ├── datasets/
│   │   ├── __init__.py                       # 已有
│   │   ├── mentalchat_loader.py             # 已有
│   │   └── comparison_test_questions.json    # ⭐ 新增：测试问题集
│   │
│   ├── scripts/
│   │   ├── run_comparison.py                 # 已有（但可能需要更新）
│   │   ├── simple_comparison.py              # ⭐ 新增：简化实验脚本
│   │   ├── visualize_comparison_simple.py    # ⭐ 新增：可视化脚本
│   │   └── generate_comparison_report.py     # ⭐ 新增：报告生成脚本
│   │
│   └── results/
│       └── comparison/                        # 自动创建：实验结果目录
│           ├── *.json                         # 实验数据
│           ├── figures/                       # 图表
│           └── reports/                       # 报告
│
└── [其他目录保持不变]
```

---

## ✅ 文件集成检查清单

安装后请检查以下项目：

- [ ] `run_comparison_experiment.sh` 在项目根目录
- [ ] `comparison_config.yaml` 在 `evaluation/configs/`
- [ ] `comparison_test_questions.json` 在 `evaluation/datasets/`
- [ ] `simple_comparison.py` 在 `evaluation/scripts/`
- [ ] `visualize_comparison_simple.py` 在 `evaluation/scripts/`
- [ ] `generate_comparison_report.py` 在 `evaluation/scripts/`
- [ ] `COMPARISON_GUIDE.md` 在 `evaluation/`
- [ ] `COMPARISON_README.md` 在 `evaluation/`
- [ ] `run_comparison_experiment.sh` 有执行权限

---

## 🚀 快速验证

安装完成后，运行以下命令验证：

```bash
# 1. 检查文件是否存在
ls evaluation/configs/comparison_config.yaml
ls evaluation/datasets/comparison_test_questions.json
ls evaluation/scripts/simple_comparison.py
ls run_comparison_experiment.sh

# 2. 检查脚本权限
ls -l run_comparison_experiment.sh

# 3. 测试运行（干运行）
python evaluation/scripts/simple_comparison.py --help

# 4. 查看使用指南
cat evaluation/COMPARISON_GUIDE.md
```

---

## 📦 依赖检查

确保已安装必要的依赖：

```bash
# 检查matplotlib
python -c "import matplotlib; print(matplotlib.__version__)"

# 检查numpy
python -c "import numpy; print(numpy.__version__)"

# 如果缺失，安装
pip install matplotlib numpy --break-system-packages
```

---

## 🔧 与现有代码的兼容性

### 不会修改的现有文件

本次新增**完全不会修改**现有文件，包括：
- ✅ `configs/config.yaml` - 系统配置保持不变
- ✅ `dialogue/manager.py` - 对话管理器代码不变
- ✅ `knowledge/rag_manager.py` - RAG管理器不变
- ✅ `memory/manager.py` - 记忆管理器不变
- ✅ 其他所有已有文件

### 可能的文件冲突

如果以下文件已存在，请注意：

1. **`evaluation/scripts/visualize_comparison.py`**
   - 已有的旧版本已被备份为 `visualize_comparison_old.py`
   - 新版本命名为 `visualize_comparison_simple.py`
   - **无冲突**

2. **`evaluation/scripts/run_comparison.py`**
   - 这是你原有的对比脚本
   - 新脚本名为 `simple_comparison.py`
   - **无冲突**，两个可以共存

---

## 💡 使用建议

### 第一次运行

1. **先小规模测试**（5-10个问题）:
```bash
./run_comparison_experiment.sh 10
```

2. **检查输出**:
```bash
ls -R evaluation/results/comparison/
```

3. **查看图表**:
```bash
open evaluation/results/comparison/figures/
```

4. **查看报告**:
```bash
cat evaluation/results/comparison/reports/*.md
```

### 正式实验

确认测试成功后，运行完整实验：
```bash
./run_comparison_experiment.sh 30
```

---

## 🎓 用于期末作业的建议

### 最小工作量（1-2天）

1. 运行对比实验（30个问题）
2. 使用生成的5张图表
3. 参考Markdown报告写实验部分
4. 选择3-5个案例进行详细分析

### 完整方案（3-5天）

1. 运行对比实验（30个问题）
2. 使用所有生成的图表和报告
3. 进行人工评估（可选但推荐）
4. 详细的案例分析（10个案例）
5. 深入的结果讨论

---

## 📝 集成到论文

### 可以直接使用的内容

1. **图表** (5张)：
   - 全部是300 DPI高质量PNG
   - 可直接插入Word/LaTeX

2. **表格** (Markdown报告中)：
   - 配置对比表
   - 性能指标表
   - 可直接复制到Word

3. **数据** (JSON文件)：
   - 原始实验数据
   - 可用于进一步分析

### 论文写作建议

参考 `COMPARISON_GUIDE.md` 中的"论文写作建议"章节。

---

## ❓ 常见问题

### Q: 这些新文件会覆盖我的现有代码吗？

**A**: 不会。所有新文件都是独立的，不会修改任何现有文件。

### Q: 如果我的evaluation目录结构不同怎么办？

**A**: 按照文件树结构创建对应的目录即可。例如：
```bash
mkdir -p evaluation/configs
mkdir -p evaluation/datasets  
mkdir -p evaluation/scripts
```

### Q: 我可以只使用部分功能吗？

**A**: 可以！三个脚本可以独立运行：
- 只运行实验: `simple_comparison.py`
- 只生成图表: `visualize_comparison_simple.py`
- 只生成报告: `generate_comparison_report.py`

---

## 🔍 故障排除

### 错误: "找不到模块"

```bash
# 解决方案：确保在项目根目录运行
cd /path/to/psychological_counseling_system
python evaluation/scripts/simple_comparison.py
```

### 错误: "permission denied"

```bash
# 解决方案：添加执行权限
chmod +x run_comparison_experiment.sh
```

### 错误: "找不到配置文件"

```bash
# 解决方案：检查文件是否在正确位置
ls evaluation/configs/comparison_config.yaml
```

---

## 📞 需要帮助？

1. 查看 `COMPARISON_GUIDE.md` 获取详细使用说明
2. 查看 `COMPARISON_README.md` 了解模块功能
3. 检查 `evaluation/results/comparison/*.log` 日志文件

---

## ✨ 总结

本次新增了对比实验功能，包括：

- ✅ **7个新文件**（3个脚本、2个配置、2个文档）
- ✅ **完全独立**，不修改现有代码
- ✅ **开箱即用**，一键运行
- ✅ **论文友好**，自动生成图表和报告

**下一步**：
```bash
# 1. 验证安装
./run_comparison_experiment.sh 10

# 2. 查看结果
ls -R evaluation/results/comparison/

# 3. 阅读使用指南
cat evaluation/COMPARISON_GUIDE.md
```

---

**祝你的期末作业顺利完成！🎓✨**

---

*创建日期: 2025-11-11*
*版本: 1.0*
