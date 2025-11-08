# 实验和论文数据收集指南

本指南帮助您完成以下任务：
1. 添加本地知识库文件
2. 运行对比实验
3. 生成论文用的数据和图表

## 📁 项目结构

```
psychological_counseling_system/
├── data/
│   ├── sample_knowledge/          # 心理学专业知识（已创建）
│   │   ├── cbt_therapy.txt
│   │   ├── anxiety_management.txt
│   │   ├── depression_treatment.txt
│   │   └── sleep_insomnia.txt
│   └── sample_user_info/          # 用户档案信息（已创建）
│       ├── user_a_profile.txt
│       └── user_b_profile.txt
├── examples/
│   ├── add_knowledge.py           # 知识库添加工具（新）
│   ├── comparison_experiment.py   # 对比实验脚本（新）
│   └── visualize_results.py       # 结果可视化（新）
└── experiments/                   # 实验结果输出目录
    ├── comparison_report_*.json   # 实验数据
    ├── detailed_comparison.md     # 详细对比
    ├── response_examples.md       # 响应示例
    └── figures/                   # 图表
        ├── response_time_comparison.png
        ├── response_length_comparison.png
        └── scenario_comparison.png
```

## 🚀 快速开始

### 步骤 1: 安装依赖

```bash
# 进入项目目录
cd psychological_counseling_system

# 安装基础依赖
pip install -r requirements.txt

# 安装可视化依赖
pip install matplotlib numpy
```

### 步骤 2: 配置环境

```bash
# 如果使用OpenAI API
export OPENAI_API_KEY="your-api-key-here"

# 或者编辑 configs/config.yaml 使用本地模型
```

### 步骤 3: 添加知识库

我已经为您创建了示例知识文件：

**心理学专业知识** (`data/sample_knowledge/`)：
- `cbt_therapy.txt` - 认知行为疗法
- `anxiety_management.txt` - 焦虑症管理
- `depression_treatment.txt` - 抑郁症治疗
- `sleep_insomnia.txt` - 睡眠障碍治疗

**用户档案信息** (`data/sample_user_info/`)：
- `user_a_profile.txt` - 用户A的详细档案
- `user_b_profile.txt` - 用户B的详细档案

运行以下命令将这些文件导入系统：

```bash
python examples/add_knowledge.py
```

**预期输出**：
```
============================================================
知识库添加工具
============================================================

[1/4] 加载配置...
[2/4] 创建必要的目录...
[3/4] 初始化系统...
[4/4] 添加知识文件...

============================================================
添加心理学专业知识到知识库...
============================================================
✓ 已加载: cbt_therapy.txt (xxxx 字符)
✓ 已加载: anxiety_management.txt (xxxx 字符)
...

成功添加 4 个心理学知识文档到知识库！

============================================================
添加用户个人信息到知识库...
============================================================
✓ 已加载: user_a_profile.txt (xxxx 字符)
✓ 已加载: user_b_profile.txt (xxxx 字符)

成功添加 2 个用户档案到知识库！

============================================================
知识库添加完成！
============================================================
```

### 步骤 4: 运行对比实验

这是**最重要的步骤**，将对比三种配置的效果：

```bash
python examples/comparison_experiment.py
```

**实验会测试**：
1. **裸LLM**（无RAG，无记忆）- 基线
2. **LLM + RAG**（有知识库，无记忆）- 显示RAG的价值
3. **完整系统**（有知识库，有记忆）- 显示记忆系统的价值

**预期输出**：
```
======================================================================
心理咨询系统对比实验
用于论文数据收集和系统评估
======================================================================

======================================================================
测试配置: 裸LLM（无RAG，无记忆）
======================================================================

  运行配置: 裸LLM（无RAG，无记忆）
  场景: 场景1: 首次咨询 - 工作压力和睡眠问题
    Turn 1: 1.23s, 256 字符
    Turn 2: 1.45s, 312 字符
    Turn 3: 1.18s, 289 字符
...

======================================================================
实验结果摘要
======================================================================

配置对比:
配置                            平均响应时间      平均响应长度
----------------------------------------------------------------------
裸LLM（无RAG，无记忆）            1.45秒            285字符
LLM + RAG（有知识库，无记忆）      1.67秒            412字符
完整系统（有知识库，有记忆）       1.89秒            456字符

======================================================================
```

### 步骤 5: 生成可视化图表

运行以下命令生成论文用的图表和分析文档：

```bash
python examples/visualize_results.py
```

**生成的文件**：
- `experiments/figures/response_time_comparison.png` - 响应时间对比柱状图
- `experiments/figures/response_length_comparison.png` - 响应长度对比柱状图
- `experiments/figures/scenario_comparison.png` - 不同场景的对比图
- `experiments/detailed_comparison.md` - 详细的数据对比表格
- `experiments/response_examples.md` - 具体的响应示例

## 📊 如何使用实验结果

### 1. 论文图表

生成的PNG图片可以直接插入到论文中：

```latex
\begin{figure}[h]
\centering
\includegraphics[width=0.8\textwidth]{response_time_comparison.png}
\caption{不同系统配置的响应时间对比}
\label{fig:response_time}
\end{figure}
```

### 2. 数据表格

`detailed_comparison.md` 包含完整的Markdown表格，可以转换为LaTeX：

```markdown
| 配置 | 平均响应时间 | 平均响应长度 |
|-----|------------|------------|
| 裸LLM | 1.45秒 | 285字符 |
| LLM+RAG | 1.67秒 | 412字符 |
| 完整系统 | 1.89秒 | 456字符 |
```

### 3. 案例分析

`response_examples.md` 提供了三种配置对同一问题的不同回答，可用于：
- 定性分析
- 说明RAG和记忆系统的实际效果
- 展示系统的专业性提升

### 4. 原始数据

`comparison_report_*.json` 包含所有原始数据，可以：
- 用Python进行进一步分析
- 计算更多统计指标
- 绘制自定义图表

## 🎯 实验分析要点

### 论文中可以强调的点：

1. **RAG的价值**：
   - 响应长度增加 → 提供了更多专业知识
   - 可以引用具体的治疗方法（如CBT技术）
   - 回答更加专业和详细

2. **记忆系统的价值**：
   - 能够记住用户的历史信息
   - 提供连贯的长期咨询
   - 第二次对话能引用第一次的内容
   - 实现真正的"记住"功能

3. **系统的实用性**：
   - 响应时间仍在可接受范围（<2秒）
   - 性能开销换来了质量提升
   - 适合实际部署

## 📝 添加自己的知识文件

### 添加心理学知识

1. 创建文本文件：`data/sample_knowledge/your_topic.txt`
2. 内容格式：纯文本，包含主题、原理、技术等
3. 重新运行：`python examples/add_knowledge.py`

**示例**：
```text
正念疗法基础

正念（Mindfulness）是一种心理状态，指有意识地、不加评判地
关注当下时刻的体验...

核心原理：
1. 活在当下
2. 不加评判的观察
3. 接纳现实
...
```

### 添加用户档案

1. 创建文件：`data/sample_user_info/user_c_profile.txt`
2. 包含：基本信息、主要问题、生活事件、治疗目标等
3. 重新运行：`python examples/add_knowledge.py`

## 🔧 自定义实验

### 修改测试场景

编辑 `examples/comparison_experiment.py` 中的 `TEST_SCENARIOS`：

```python
TEST_SCENARIOS = [
    {
        "name": "你的场景名称",
        "user_id": "test_user_003",
        "conversations": [
            {
                "turn": 1,
                "user": "用户输入...",
                "emotion": {"anxiety": 0.7}
            },
            # 添加更多轮次...
        ]
    },
    # 添加更多场景...
]
```

### 修改评估指标

在 `ExperimentRunner` 类中添加自定义指标：

```python
def calculate_custom_metrics(self, responses):
    # 计算专业术语使用频率
    # 计算情感词汇比例
    # 等等...
    pass
```

## ❓ 常见问题

### Q1: 知识库文件支持什么格式？
**A**: 目前支持 `.txt` 文件。内容会被自动分块并转换为向量。

### Q2: 如何验证知识库已成功添加？
**A**: 运行基础示例并观察回复是否引用了专业知识：
```bash
python examples/basic_rag_chat.py
```

### Q3: 实验需要运行多久？
**A**: 取决于LLM后端：
- OpenAI API: 约 2-5 分钟
- 本地模型: 约 5-10 分钟

### Q4: 如何添加更多测试场景？
**A**: 编辑 `comparison_experiment.py` 的 `TEST_SCENARIOS` 列表。

### Q5: 图表显示中文乱码怎么办？
**A**: 安装中文字体或修改 `visualize_results.py` 中的字体设置。

## 📖 下一步

完成实验后，您可以：

1. ✅ 将图表插入论文
2. ✅ 引用实验数据
3. ✅ 使用响应示例进行案例分析
4. ✅ 基于结果撰写讨论部分

**祝您实验顺利，论文写作成功！** 🎓

---

**需要帮助？**
- 查看详细文档：`docs/architecture.md`
- 运行测试：`python tests/test_system.py`
- 查看日志：`logs/system.log`
