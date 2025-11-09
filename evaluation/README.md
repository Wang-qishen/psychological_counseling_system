# 📊 心理咨询系统评估模块

> 基于Mentalic Net论文和最新研究设计的全面评估框架

## 🎯 概述

本评估模块为心理咨询系统提供**6大类21个评估指标**，支持多种数据集和对比实验，专门设计用于学术研究和系统优化。

### 核心特点

- ✅ **21个专业指标** - 涵盖技术、临床、安全、用户体验等
- ✅ **多数据集支持** - MentalChat16K、Empathetic Dialogues等
- ✅ **记忆系统测评** - 专门评估三层记忆架构（核心创新）
- ✅ **RAG效果评估** - Precision、Recall、F1等
- ✅ **对比实验框架** - 裸LLM vs LLM+RAG vs 完整系统
- ✅ **自动化报告** - JSON/Markdown/图表自动生成

## 📁 模块结构

```
evaluation/
├── README.md                    # 本文档
├── __init__.py                  # 模块入口
├── framework.py                 # 评估框架主类
│
├── configs/                     # 配置文件（新增）
│   ├── default_config.yaml      # 默认配置
│   ├── quick_test_config.yaml   # 快速测试配置
│   └── full_eval_config.yaml    # 完整评估配置
│
├── datasets/                    # 数据集管理
│   ├── __init__.py
│   ├── dataset_loader.py        # 通用数据加载器
│   ├── mentalchat_loader.py     # MentalChat16K加载器
│   ├── memory_test_generator.py # 记忆测试生成器
│   └── download_datasets.py     # 数据集下载脚本（新增）
│
├── metrics/                     # 评估指标
│   ├── __init__.py
│   ├── technical_metrics.py     # 技术指标（BERT, ROUGE, BLEU）
│   ├── clinical_metrics.py      # 临床指标（7个专业指标）
│   ├── safety_metrics.py        # 安全性指标
│   ├── memory_metrics.py        # 记忆系统指标
│   └── rag_metrics.py           # RAG效果指标
│
├── evaluators/                  # 评估器
│   ├── __init__.py
│   ├── system_evaluator.py      # 系统评估器
│   └── comparison_evaluator.py  # 对比评估器
│
├── scripts/                     # 运行脚本（新增）
│   ├── run_full_evaluation.py   # 完整评估
│   ├── run_quick_test.py        # 快速测试
│   ├── run_comparison.py        # 对比实验
│   └── generate_report.py       # 生成报告
│
└── results/                     # 评估结果（自动创建）
    ├── technical/               # 技术指标结果
    ├── clinical/                # 临床指标结果
    ├── safety/                  # 安全性结果
    ├── comparison/              # 对比实验结果
    └── reports/                 # 最终报告
```

## 🎯 评估指标体系

### 1. 技术性能指标 (Technical Metrics)

| 指标 | 说明 | 目标值 | Mentalic Net |
|------|------|--------|--------------|
| **BERT Score** | 语义相似度 | ≥0.85 | 0.898 |
| **ROUGE-L** | 文本重叠度 | ≥0.30 | - |
| **BLEU** | 翻译质量 | ≥0.20 | - |
| **响应时间** | 平均响应延迟 | <2s | - |
| **响应长度** | 平均字符数 | 100-500 | - |

### 2. 专业质量指标 (Clinical Quality Metrics)

基于MentalChat16K的7个临床维度：

| 指标 | 说明 | 评分范围 |
|------|------|----------|
| **Empathy** | 共情能力 | 1-5 |
| **Support** | 情感支持 | 1-5 |
| **Guidance** | 专业指导 | 1-5 |
| **Relevance** | 内容相关性 | 1-5 |
| **Communication** | 沟通质量 | 1-5 |
| **Fluency** | 语言流畅性 | 1-5 |
| **Safety** | 回复安全性 | 1-5 |

### 3. 安全性指标 (Safety Metrics)

| 指标 | 说明 | 目标 |
|------|------|------|
| **有害内容检测** | 检测危险建议 | 0% |
| **隐私保护** | 敏感信息泄露 | 0% |
| **伦理合规** | 专业伦理遵守 | 100% |
| **边界案例** | 自杀/自伤处理 | 正确率100% |

### 4. 用户体验指标 (User Experience)

- 响应时间统计
- 对话完成率
- 用户满意度模拟
- 系统稳定性

### 5. 临床效果指标 (Clinical Effectiveness)

- 情绪改善度
- 问题解决效果
- 认知重构质量
- 行为改变建议

### 6. 系统特色指标 (System-Specific)

#### RAG效果评估
- **Recall**: 检索召回率（目标≥0.85）
- **Precision**: 检索精确率（目标≥0.70）
- **Relevance**: 知识相关性
- **Response Time**: 检索响应时间

#### 记忆系统评估 ⭐（核心创新）
- **短期记忆召回率**: 最近3轮对话
- **工作记忆准确率**: 关键信息保持
- **长期记忆稳定性**: 跨会话信息保持
- **记忆一致性**: 信息前后一致性
- **个性化提升度**: 相比无记忆系统的改进

## 🚀 快速开始

### 1. 环境准备

```bash
# 安装评估依赖
cd psychological_counseling_system
pip install -r requirements.txt

# 额外评估依赖
pip install bert-score rouge-score nltk matplotlib seaborn
```

### 2. 下载数据集

```bash
# 下载MentalChat16K数据集
python evaluation/datasets/download_datasets.py --dataset mentalchat

# 或下载全部数据集
python evaluation/datasets/download_datasets.py --all
```

### 3. 运行快速测试（10个样本）

```bash
python evaluation/scripts/run_quick_test.py
```

预期输出：
```
========================================
运行快速测试 (10 samples)
========================================
✓ 加载数据集...
✓ 技术指标评估...
  - BERT Score: 0.87
  - ROUGE-L: 0.32
✓ 临床指标评估...
  - Empathy: 4.2/5
  - Support: 4.1/5
✓ 测试完成！
结果保存: evaluation/results/quick_test_20241109.json
```

### 4. 运行完整评估（200个样本）

```bash
python evaluation/scripts/run_full_evaluation.py
```

### 5. 运行对比实验

```bash
python evaluation/scripts/run_comparison.py
```

## 📖 详细使用指南

### 方式1: 使用脚本（推荐）

最简单的方式是使用提供的脚本：

```bash
# 1. 快速测试（5分钟）
python evaluation/scripts/run_quick_test.py

# 2. 完整评估（30-60分钟）
python evaluation/scripts/run_full_evaluation.py --samples 200

# 3. 对比实验（60-120分钟）
python evaluation/scripts/run_comparison.py --samples 100

# 4. 生成报告
python evaluation/scripts/generate_report.py --result-dir evaluation/results/latest
```

### 方式2: 编程接口

使用Python代码进行更灵活的评估：

```python
from evaluation import EvaluationFramework
from dialogue import DialogueManager

# 1. 初始化系统
dialogue_manager = DialogueManager()
evaluator = EvaluationFramework(
    dialogue_manager=dialogue_manager,
    data_dir="./data",
    output_dir="./evaluation/results"
)

# 2. 运行完整评估
results = evaluator.run_full_evaluation(
    dataset="mentalchat",
    num_test_samples=200,
    clinical_sample_size=50,
    generate_memory_tests=True
)

# 3. 查看结果
print(f"BERT Score: {results['technical']['bert_score']['f1']:.3f}")
print(f"Empathy: {results['clinical']['empathy']:.2f}/5")
print(f"Memory Accuracy: {results['memory']['accuracy']:.2%}")
```

### 方式3: 对比实验

对比三种配置的效果：

```python
from evaluation import EvaluationFramework
from dialogue import DialogueManager
import yaml

# 加载不同配置
with open("configs/bare_llm.yaml") as f:
    bare_config = yaml.safe_load(f)
with open("configs/llm_rag.yaml") as f:
    rag_config = yaml.safe_load(f)
with open("configs/config.yaml") as f:
    full_config = yaml.safe_load(f)

# 创建三个系统
bare_llm = DialogueManager(bare_config)
llm_rag = DialogueManager(rag_config)
full_system = DialogueManager(full_config)

# 运行对比
evaluator = EvaluationFramework()
comparison = evaluator.run_comparison_evaluation(
    bare_llm_manager=bare_llm,
    llm_rag_manager=llm_rag,
    full_system_manager=full_system,
    num_test_samples=100
)

# 查看对比结果
print("\n对比结果:")
for system, scores in comparison['technical_scores'].items():
    print(f"{system}: BERT={scores['bert_score']:.3f}")
```

## 📊 数据集说明

### MentalChat16K ⭐（主要数据集）

- **来源**: https://huggingface.co/datasets/ShenLab/MentalChat16K
- **规模**: 16,113对话 + 200个测试问题
- **特点**: 
  - 7个临床评估维度
  - 专业心理咨询师标注
  - Mentalic Net论文使用的基准数据集
- **使用**: 技术指标、临床质量评估

### Empathetic Dialogues

- **来源**: https://github.com/facebookresearch/EmpatheticDialogues
- **规模**: 25k对话
- **特点**: 32种情绪场景
- **使用**: 共情能力专项评估

### Counsel Chat

- **来源**: Kaggle
- **规模**: 3k专业咨询对话
- **特点**: 真实咨询场景
- **使用**: 专业性评估

### 记忆测试集（自建）⭐

- **生成**: 自动生成200个测试场景
- **特点**: 
  - 多轮对话场景
  - 信息回顾要求
  - 一致性检查
- **使用**: 记忆系统评估（核心创新）

## 🔬 评估流程

### 标准评估流程

```
1. 数据准备
   ├── 下载数据集
   ├── 生成记忆测试
   └── 数据预处理

2. 技术指标评估
   ├── 生成系统回复（200个样本）
   ├── 计算BERT Score
   ├── 计算ROUGE/BLEU
   └── 统计响应时间和长度

3. 临床指标评估
   ├── 随机采样（50个）
   ├── LLM评分（7个维度）
   └── 统计分析

4. 安全性测试
   ├── 有害内容检测
   ├── 隐私保护测试
   ├── 伦理合规检查
   └── 边界案例测试

5. 记忆系统评估 ⭐
   ├── 短期记忆测试
   ├── 工作记忆测试
   ├── 长期记忆测试
   └── 一致性测试

6. RAG效果评估
   ├── 检索质量测试
   ├── 知识使用率
   └── 相关性评分

7. 结果汇总
   ├── 生成JSON报告
   ├── 生成Markdown报告
   └── 生成可视化图表
```

### 对比实验流程

```
1. 准备三个系统
   ├── 裸LLM（无RAG、无记忆）
   ├── LLM+RAG（有RAG、无记忆）
   └── 完整系统（RAG+记忆）

2. 生成回复
   ├── 每个系统处理相同测试集
   └── 记录所有指标

3. 对比分析
   ├── 技术指标对比
   ├── 临床质量对比
   ├── 响应时间对比
   └── 统计显著性检验

4. 可视化
   ├── 雷达图（多维对比）
   ├── 柱状图（指标对比）
   └── 箱线图（分布对比）
```

## 📈 结果输出

### 1. JSON报告

```json
{
  "metadata": {
    "timestamp": "2024-11-09T10:30:00",
    "dataset": "mentalchat",
    "num_samples": 200,
    "config": "full_system"
  },
  "technical_metrics": {
    "bert_score": {
      "precision": 0.895,
      "recall": 0.887,
      "f1": 0.891
    },
    "rouge": {
      "rouge1": 0.345,
      "rouge2": 0.156,
      "rougeL": 0.312
    },
    "response_stats": {
      "avg_time": 1.23,
      "avg_length": 256
    }
  },
  "clinical_metrics": {
    "empathy": 4.3,
    "support": 4.1,
    "guidance": 4.2,
    "relevance": 4.4,
    "communication": 4.3,
    "fluency": 4.5,
    "safety": 4.6,
    "overall": 4.34
  },
  "memory_metrics": {
    "short_term_recall": 0.92,
    "working_memory_accuracy": 0.88,
    "long_term_consistency": 0.85,
    "overall_accuracy": 0.88
  },
  "rag_metrics": {
    "recall": 0.87,
    "precision": 0.73,
    "f1": 0.79,
    "avg_relevance": 4.2
  },
  "safety_metrics": {
    "harmful_content": 0.0,
    "privacy_leakage": 0.0,
    "ethical_compliance": 1.0,
    "boundary_cases": 1.0
  }
}
```

### 2. Markdown报告

自动生成详细的Markdown报告，包含：
- 执行摘要
- 各项指标详细结果
- 与基准的对比
- 优势和改进建议
- 示例对话展示

### 3. 可视化图表

- 雷达图：多维度综合表现
- 柱状图：各指标对比
- 折线图：性能趋势
- 热力图：相关性分析

## 🎯 目标基准

基于Mentalic Net论文和最新研究：

| 指标类别 | 核心指标 | 目标值 | Mentalic Net | 说明 |
|---------|---------|--------|--------------|------|
| **技术** | BERT Score F1 | ≥0.85 | 0.898 | 达标即可 |
| **技术** | ROUGE-L | ≥0.30 | - | 新增指标 |
| **专业** | Clinical Average | ≥4.0/5 | 4.2/5 | 保持同水平 |
| **专业** | Empathy | ≥4.0/5 | - | 重点指标 |
| **RAG** | Recall | ≥0.85 | 0.86 | 保持 |
| **RAG** | Precision | ≥0.70 | 0.51 | **改进重点** |
| **记忆** | Overall Accuracy | ≥0.80 | N/A | **核心创新** ⭐ |
| **安全** | Compliance | 100% | - | 必须达标 |

### 核心优势点

我们的系统相比Mentalic Net的三大优势：

1. **三层记忆架构** ⭐⭐⭐⭐⭐
   - Mentalic Net完全没有记忆系统
   - 我们提供短期、工作、长期三层记忆
   - 显著提升个性化和连贯性

2. **更全面的评估** ⭐⭐⭐⭐
   - 21个指标 vs 9个指标
   - 增加安全性和记忆系统评估
   - 符合2025年最新标准

3. **系统化对比实验** ⭐⭐⭐
   - 证明每个组件的价值
   - 量化RAG和记忆的贡献
   - 提供消融实验数据

## 🛠️ 高级功能

### 1. 自定义评估指标

```python
from evaluation.metrics import BaseMetric

class CustomMetric(BaseMetric):
    """自定义评估指标"""
    
    def compute(self, predictions, references):
        # 实现你的评估逻辑
        return {"score": 0.85}

# 注册到框架
evaluator.register_metric("custom", CustomMetric())
```

### 2. 批量实验

```python
# 测试不同配置
configs = [
    "configs/config_v1.yaml",
    "configs/config_v2.yaml",
    "configs/config_v3.yaml"
]

results = []
for config_file in configs:
    manager = DialogueManager(config_file)
    result = evaluator.run_full_evaluation()
    results.append(result)

# 生成对比报告
generate_comparison_report(results)
```

### 3. 持续评估

```python
# 定期评估系统性能
from evaluation.scripts import continuous_evaluation

continuous_evaluation.start(
    interval_hours=24,
    num_samples=50,
    alert_threshold=0.80  # 低于此阈值发送警报
)
```

## 📚 相关资源

### 论文参考

1. **Mentalic Net** (2024)
   - MentalChat16K数据集
   - 7个临床评估维度
   - 我们的主要基准

2. **BERT Score** (2019)
   - 语义相似度评估标准
   - 广泛用于对话系统

3. **Empathetic Dialogues** (2019)
   - 共情对话数据集
   - Facebook AI Research

### 代码示例

- `examples/evaluation_examples.py` - 基础使用示例
- `evaluation/scripts/run_full_evaluation.py` - 完整评估脚本
- `evaluation/scripts/run_comparison.py` - 对比实验脚本

### 配置文件

- `evaluation/configs/default_config.yaml` - 默认配置
- `evaluation/configs/quick_test_config.yaml` - 快速测试
- `evaluation/configs/full_eval_config.yaml` - 完整评估

## ❓ 常见问题

### Q1: 评估需要多长时间？

- **快速测试**（10样本）: 5分钟
- **标准评估**（100样本）: 30分钟
- **完整评估**（200样本）: 60分钟
- **对比实验**（100样本×3系统）: 120分钟

### Q2: 需要多少GPU资源？

- BERT Score需要GPU加速（建议）
- 其他指标可以CPU运行
- 最低配置: GTX 1060 或更高
- 推荐配置: RTX 3060 或更高

### Q3: 如何解释评估结果？

参考`evaluation/docs/interpretation_guide.md`获取详细说明。

### Q4: 数据集下载失败怎么办？

```bash
# 使用镜像源
export HF_ENDPOINT=https://hf-mirror.com
python evaluation/datasets/download_datasets.py
```

### Q5: 如何提交评估结果？

评估结果保存在`evaluation/results/`目录，可以：
- 上传到GitHub作为实验数据
- 在论文中引用
- 与其他系统对比

## 🤝 贡献指南

欢迎贡献新的评估指标和数据集！

1. Fork本仓库
2. 创建特性分支
3. 提交代码和测试
4. 发起Pull Request

## 📝 更新日志

### v1.0.0 (2024-11-09)
- ✅ 初始版本
- ✅ 21个评估指标
- ✅ MentalChat16K数据集支持
- ✅ 记忆系统评估
- ✅ 对比实验框架
- ✅ 自动化报告生成

## 📄 许可证

MIT License

## 📧 联系方式

如有问题，请提交Issue或联系项目维护者。

---

**下一步**: 查看 [快速开始示例](../examples/evaluation_examples.py) 开始你的第一次评估！
