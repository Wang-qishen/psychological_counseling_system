# 对比实验使用指南

## Comparison Experiment Guide

本指南说明如何使用对比实验系统评估心理咨询对话系统的三种配置。

---

## 📋 目录

1. [快速开始](#快速开始)
2. [实验说明](#实验说明)
3. [使用方法](#使用方法)
4. [输出文件](#输出文件)
5. [人工评估](#人工评估)
6. [常见问题](#常见问题)

---

## 🚀 快速开始

### 一键运行（推荐）

```bash
# 在项目根目录执行
./run_comparison_experiment.sh

# 或指定问题数量（默认30个）
./run_comparison_experiment.sh 20
```

这个脚本会自动完成：
1. ✅ 运行三种配置的对比实验
2. ✅ 生成可视化图表（5张）
3. ✅ 生成评估报告（Markdown格式）

**预计用时**: 10-30分钟（取决于问题数量和模型速度）

### 分步运行

如果你想更细致地控制每个步骤：

```bash
# 步骤1: 运行实验
python evaluation/scripts/simple_comparison.py --num-questions 30

# 步骤2: 生成图表（使用最新的结果文件）
python evaluation/scripts/visualize_comparison_simple.py evaluation/results/comparison/comparison_XXXXXX.json

# 步骤3: 生成报告
python evaluation/scripts/generate_comparison_report.py evaluation/results/comparison/comparison_XXXXXX.json
```

---

## 🔬 实验说明

### 对比的三种配置

| 配置 | RAG检索 | 记忆系统 | 说明 |
|------|---------|----------|------|
| **裸LLM（基线）** | ✗ | ✗ | 仅使用LLM生成回复，作为基准对照 |
| **LLM + RAG** | ✓ | ✗ | 使用RAG检索知识库，但不使用记忆 |
| **完整系统** | ✓ | ✓ | 使用RAG和记忆系统的完整配置 |

### 测试问题

系统预设了30个精心设计的测试问题，覆盖以下类别：
- 焦虑情绪（5个）
- 抑郁症状（5个）
- 工作压力（4个）
- 睡眠问题（4个）
- 人际关系（4个）
- 自我认知（4个）
- 情感问题（2个）
- 家庭关系（2个）

### 评估指标

#### 自动评估指标
- **响应时间**: 平均回复生成时间（秒）
- **回复长度**: 平均回复字符数
- **成功率**: 成功生成回复的比例

#### 人工评估指标（可选）
- **相关性**: 回复与问题的相关程度（1-5分）
- **专业性**: 回复的专业水平（1-5分）
- **共情能力**: 回复的同理心表现（1-5分）
- **有用性**: 回复的实际帮助程度（1-5分）
- **清晰度**: 回复的表达清晰度（1-5分）

---

## 📖 使用方法

### 方法1: 一键运行（最简单）

```bash
# 使用默认配置（30个问题）
./run_comparison_experiment.sh

# 自定义问题数量
./run_comparison_experiment.sh 20

# 使用自定义配置文件
./run_comparison_experiment.sh 30 configs/custom_config.yaml
```

### 方法2: Python脚本运行

#### 运行实验

```bash
python evaluation/scripts/simple_comparison.py \
    --num-questions 30 \
    --config configs/config.yaml \
    --skip-manual
```

参数说明：
- `--num-questions`: 测试问题数量（默认30）
- `--config`: 系统配置文件路径
- `--skip-manual`: 跳过人工评估
- `--output-dir`: 自定义输出目录

#### 生成图表

```bash
python evaluation/scripts/visualize_comparison_simple.py \
    evaluation/results/comparison/comparison_20251111_120000.json
```

#### 生成报告

```bash
python evaluation/scripts/generate_comparison_report.py \
    evaluation/results/comparison/comparison_20251111_120000.json
```

---

## 📁 输出文件

实验完成后，会在以下目录生成文件：

```
evaluation/results/comparison/
├── comparison_YYYYMMDD_HHMMSS.json    # 实验原始数据
├── figures/                            # 可视化图表
│   ├── response_time_comparison.png   # 响应时间对比
│   ├── response_length_comparison.png # 回复长度对比
│   ├── response_time_distribution.png # 响应时间分布
│   ├── category_analysis.png          # 类别分析
│   └── summary_comparison.png         # 综合对比
└── reports/                            # 评估报告
    ├── comparison_report_XXX.md       # 详细报告
    └── SUMMARY.md                      # 简短总结
```

### 文件说明

1. **comparison_*.json**: 
   - 包含所有实验数据
   - 可用于后续分析
   - JSON格式，易于处理

2. **figures/*.png**: 
   - 高分辨率图表（300 DPI）
   - 可直接用于论文
   - PNG格式，兼容性好

3. **reports/*.md**: 
   - Markdown格式报告
   - 包含完整实验结果
   - 可直接复制到论文

---

## 👤 人工评估（可选但推荐）

人工评估可以大大增强实验的可信度！

### 为什么需要人工评估？

- ✅ 评估回复的**质量**而非仅速度
- ✅ 发现自动指标无法捕捉的**细微差异**
- ✅ 增加实验的**学术价值**
- ✅ 为论文提供**主观评价数据**

### 如何进行人工评估？

#### 方法1: 邀请同学/朋友（推荐）

1. 导出测试问题和回复：
```bash
python evaluation/scripts/export_for_manual_eval.py \
    evaluation/results/comparison/comparison_XXX.json
```

2. 将生成的Excel文件分发给评估者

3. 评估者对每个回复进行1-5分打分

4. 收集评分结果并导入：
```bash
python evaluation/scripts/import_manual_scores.py \
    manual_scores.xlsx \
    evaluation/results/comparison/comparison_XXX.json
```

#### 方法2: 自己评估

```bash
python evaluation/scripts/manual_evaluation.py \
    evaluation/results/comparison/comparison_XXX.json
```

按照提示对每个回复进行打分即可。

### 评估建议

- **评估人数**: 至少3-5人（可以取平均分）
- **时间**: 每人约30-60分钟
- **盲测**: 不告诉评估者哪个是哪种配置
- **随机顺序**: 打乱配置顺序避免偏见

---

## ❓ 常见问题

### Q1: 实验运行很慢怎么办？

**A**: 可以减少测试问题数量：
```bash
./run_comparison_experiment.sh 10  # 只测试10个问题
```

### Q2: 某个配置运行失败怎么办？

**A**: 检查以下几点：
1. 配置文件是否正确（`configs/config.yaml`）
2. 知识库是否已准备好（`data/vector_db/`）
3. 模型文件是否存在（`models/`）

### Q3: 如何自定义测试问题？

**A**: 编辑文件：
```bash
vi evaluation/datasets/comparison_test_questions.json
```

添加或修改问题，格式如下：
```json
{
  "id": 31,
  "category": "新类别",
  "question": "你的问题？",
  "difficulty": "medium"
}
```

### Q4: 图表中文显示乱码怎么办？

**A**: 安装中文字体：
```bash
# Ubuntu/Debian
sudo apt-get install fonts-wqy-microhei

# macOS
# 系统自带中文字体，无需安装

# 或修改可视化脚本使用英文
```

### Q5: 如何在论文中引用实验结果？

**A**: 参考生成的Markdown报告中的表格和数据，例如：

> 本研究对比了三种系统配置（裸LLM、LLM+RAG、完整系统），使用30个测试问题进行评估。
> 结果显示，完整系统的平均响应时间为X.XX秒，回复长度为XXX字符，
> 相比裸LLM基线配置提升了XX.X%。

### Q6: 评估结果不理想怎么办？

**A**: 这也是有价值的发现！可以：
1. 分析失败案例，找出原因
2. 在论文中讨论系统的局限性
3. 提出改进建议作为"未来工作"

---

## 📝 论文写作建议

### 实验部分结构

```markdown
4. 实验与评估
  4.1 实验设计
    4.1.1 对比配置
    4.1.2 测试数据
    4.1.3 评估指标
  
  4.2 实验结果
    4.2.1 自动评估结果
    4.2.2 人工评估结果（如果有）
    4.2.3 性能分析
  
  4.3 案例分析
    4.3.1 典型成功案例
    4.3.2 失败案例分析
  
  4.4 讨论
    4.4.1 RAG的作用
    4.4.2 记忆系统的作用
    4.4.3 系统局限性
```

### 可以使用的图表

1. **图4-1**: 响应时间对比柱状图
2. **图4-2**: 回复长度对比柱状图  
3. **图4-3**: 响应时间分布箱线图
4. **图4-4**: 问题类别分析图
5. **图4-5**: 综合对比图

### 可以使用的表格

1. **表4-1**: 配置对比表
2. **表4-2**: 自动评估指标对比表
3. **表4-3**: 人工评估得分表（如果有）
4. **表4-4**: 详细统计数据表

---

## 🎓 期末作业提示

### 最小可行方案（1-2天）

1. ✅ 运行对比实验（30个问题）
2. ✅ 生成图表和报告
3. ✅ 选择3-5个典型案例进行详细分析
4. ✅ 撰写实验部分（2000字左右）

### 完整方案（3-5天）

1. ✅ 运行对比实验（30个问题）
2. ✅ 生成图表和报告
3. ✅ 进行人工评估（邀请5-10人）
4. ✅ 详细案例分析（10个案例）
5. ✅ 撰写完整实验章节（3000-4000字）

### 加分项

- 📊 更多可视化图表
- 👥 人工评估数据
- 📝 深入的失败案例分析
- 💡 系统改进建议
- 📈 统计显著性检验

---

## 📞 需要帮助？

如果遇到问题，可以：

1. 查看日志文件：`evaluation/results/comparison/*.log`
2. 检查配置文件：`evaluation/configs/comparison_config.yaml`
3. 查看示例输出：`evaluation/results/comparison/example/`

---

**祝实验顺利！Good luck with your project! 🎓✨**

---

*最后更新: 2025-11-11*
