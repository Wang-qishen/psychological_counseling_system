# 对比实验模块

## Comparison Experiment Module

本模块实现了心理咨询对话系统的三配置对比实验，用于评估RAG和记忆系统的效果。

---

## 📦 新增文件清单

### 配置文件
```
evaluation/configs/
└── comparison_config.yaml          # 对比实验配置文件
```

### 数据集
```
evaluation/datasets/
└── comparison_test_questions.json  # 30个精选测试问题
```

### 核心脚本
```
evaluation/scripts/
├── simple_comparison.py                    # 主实验脚本
├── visualize_comparison_simple.py         # 可视化脚本
└── generate_comparison_report.py          # 报告生成脚本
```

### 一键运行脚本
```
run_comparison_experiment.sh               # 一键运行所有步骤
```

### 文档
```
evaluation/
└── COMPARISON_GUIDE.md                    # 详细使用指南
```

---

## 🚀 快速开始

### 最简单的方式（推荐）

```bash
# 在项目根目录执行
./run_comparison_experiment.sh
```

这一个命令会自动完成：
1. 运行三种配置的实验
2. 生成5张可视化图表
3. 生成Markdown格式报告

**用时**: 10-30分钟

### 查看结果

```bash
# 查看生成的图表
open evaluation/results/comparison/figures/

# 查看评估报告
cat evaluation/results/comparison/reports/comparison_report_*.md
```

---

## 📊 实验内容

### 对比的三种配置

| 配置 | RAG | 记忆 | 用途 |
|------|-----|------|------|
| 裸LLM | ✗ | ✗ | 基线对照 |
| LLM+RAG | ✓ | ✗ | 验证RAG效果 |
| 完整系统 | ✓ | ✓ | 完整功能 |

### 评估维度

**自动指标**:
- ⏱️ 响应时间
- 📝 回复长度
- ✅ 成功率

**人工指标（可选）**:
- 相关性 (1-5分)
- 专业性 (1-5分)
- 共情能力 (1-5分)
- 有用性 (1-5分)
- 清晰度 (1-5分)

---

## 📁 输出文件

运行后会生成以下文件：

```
evaluation/results/comparison/
├── comparison_YYYYMMDD_HHMMSS.json     # 原始数据
├── figures/                             # 图表目录
│   ├── response_time_comparison.png    # 图1: 响应时间对比
│   ├── response_length_comparison.png  # 图2: 回复长度对比
│   ├── response_time_distribution.png  # 图3: 时间分布
│   ├── category_analysis.png           # 图4: 类别分析
│   └── summary_comparison.png          # 图5: 综合对比
└── reports/                             # 报告目录
    ├── comparison_report_XXX.md        # 详细报告
    └── SUMMARY.md                       # 简短总结
```

---

## 🎯 用途

### 期末作业/论文

本模块特别适合：
- ✅ 消融实验（Ablation Study）
- ✅ 系统性能评估
- ✅ 功能有效性验证
- ✅ 生成论文图表和数据

### 论文章节建议

```markdown
4. 实验与评估
  4.1 实验设计
    - 对比配置说明
    - 测试数据描述
    - 评估指标定义
  
  4.2 实验结果
    - 表4-1: 配置对比表
    - 图4-1: 响应时间对比
    - 图4-2: 回复长度对比
    
  4.3 案例分析
    - 选择3-5个典型案例
    - 对比三种配置的回复
    
  4.4 讨论与分析
    - RAG系统的作用
    - 记忆系统的价值
    - 系统局限性
```

---

## 💡 高级用法

### 自定义测试问题

编辑 `evaluation/datasets/comparison_test_questions.json`:

```json
{
  "questions": [
    {
      "id": 31,
      "category": "自定义类别",
      "question": "你的测试问题？",
      "difficulty": "medium"
    }
  ]
}
```

### 调整配置

编辑 `evaluation/configs/comparison_config.yaml`:

```yaml
comparison:
  num_test_samples: 20  # 改为20个问题
  
  evaluation_dimensions:
    manual:
      - relevance
      - custom_metric  # 添加自定义指标
```

### 分步运行

```bash
# 1. 只运行实验
python evaluation/scripts/simple_comparison.py --num-questions 10

# 2. 只生成图表
python evaluation/scripts/visualize_comparison_simple.py <结果文件>

# 3. 只生成报告
python evaluation/scripts/generate_comparison_report.py <结果文件>
```

---

## 📝 代码示例

### Python中使用

```python
from evaluation.scripts.simple_comparison import SimpleComparisonExperiment

# 创建实验
experiment = SimpleComparisonExperiment('configs/config.yaml')

# 运行实验
experiment.run_all_configurations(num_questions=20)

# 打印结果
experiment.print_comparison()

# 保存结果
result_file = experiment.save_results()
```

### 自定义评估

```python
# 添加自定义评估函数
def custom_evaluator(response_text):
    # 你的评估逻辑
    score = analyze_response(response_text)
    return score

# 在实验中使用
for response in experiment.results['baseline']['responses']:
    custom_score = custom_evaluator(response['response'])
    print(f"Custom score: {custom_score}")
```

---

## ⚙️ 依赖要求

本模块需要以下Python包：

```bash
# 核心依赖
matplotlib>=3.7.0
numpy>=1.24.0

# 已在项目中
pyyaml
```

安装方法：
```bash
pip install matplotlib numpy --break-system-packages
```

---

## 🐛 故障排除

### 问题1: 脚本没有执行权限

```bash
chmod +x run_comparison_experiment.sh
```

### 问题2: 图表中文乱码

安装中文字体：
```bash
# Ubuntu/Debian
sudo apt-get install fonts-wqy-microhei

# 或修改脚本使用英文
```

### 问题3: 实验运行失败

检查配置：
```bash
# 查看配置文件
cat configs/config.yaml

# 查看日志
cat evaluation/results/comparison/*.log
```

### 问题4: 找不到模型文件

确保模型已下载：
```bash
ls -lh models/
```

---

## 📚 相关文档

- [详细使用指南](COMPARISON_GUIDE.md) - 完整的使用说明
- [系统架构文档](../docs/architecture.md) - 了解系统设计
- [快速开始](../docs/quickstart.md) - 系统安装和配置

---

## 🎓 学术应用

### 论文图表建议

1. **图1**: 响应时间对比柱状图
   - 展示三种配置的性能差异
   - 突出效率对比

2. **图2**: 回复长度对比
   - 说明RAG对回复内容的影响
   - 展示信息丰富度

3. **图3**: 响应时间分布
   - 箱线图展示稳定性
   - 说明极端情况

4. **图4**: 类别分析
   - 展示不同问题类型的表现
   - 发现系统优势和不足

5. **图5**: 综合对比
   - 多维度总览
   - 一图看全局

### 数据引用示例

> 实验结果表明，完整系统（LLM+RAG+记忆）的平均响应时间为X.XX秒，
> 相比裸LLM基线提升了XX.X%，同时回复长度增加了XX.X%，
> 显示出RAG和记忆系统对系统性能的积极影响。

---

## 🔄 更新日志

### v1.0.0 (2025-11-11)
- ✅ 初始版本发布
- ✅ 实现三配置对比实验
- ✅ 30个精选测试问题
- ✅ 5种可视化图表
- ✅ Markdown报告生成
- ✅ 一键运行脚本
- ✅ 详细使用文档

---

## 📞 支持

如果遇到问题：

1. 查看 [COMPARISON_GUIDE.md](COMPARISON_GUIDE.md)
2. 检查配置文件是否正确
3. 查看生成的日志文件

---

## 📄 许可

本模块遵循项目主许可证。

---

**快速链接**:
- [返回项目主页](../README.md)
- [查看使用指南](COMPARISON_GUIDE.md)
- [查看系统架构](../docs/architecture.md)

---

*最后更新: 2025-11-11*
*版本: 1.0.0*
