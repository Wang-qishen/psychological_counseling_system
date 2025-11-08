# 项目更新总结 - 知识库和实验功能

## 🎉 新增功能

本次更新为您的心理咨询系统添加了以下关键功能，**专门用于论文实验和数据收集**：

### 1. 示例知识库文件 ✅

#### 心理学专业知识 (`data/sample_knowledge/`)
已创建4个高质量的专业知识文件：

- **`cbt_therapy.txt`** (2000+字)
  - 认知行为疗法基础
  - 核心原理和技术
  - 适用范围和治疗过程

- **`anxiety_management.txt`** (2500+字)
  - 焦虑症类型识别
  - 身体症状和管理技术
  - 呼吸练习、渐进性放松等方法

- **`depression_treatment.txt`** (3000+字)
  - 抑郁症诊断标准
  - CBT治疗方法
  - 行为激活技术

- **`sleep_insomnia.txt`** (3500+字)
  - 失眠认知行为疗法(CBT-I)
  - 睡眠限制、刺激控制
  - 认知重构和放松技术

#### 用户档案信息 (`data/sample_user_info/`)
已创建2个详细的用户档案：

- **`user_a_profile.txt`** - 张晓敏
  - 28岁女性软件工程师
  - 工作压力、睡眠障碍、社交困难
  - 完整的生活事件时间线
  - 治疗目标和风险评估

- **`user_b_profile.txt`** - 李明
  - 35岁男性中学教师
  - 抑郁情绪、家庭关系压力、工作倦怠
  - 丧亲之痛的处理
  - 详细的背景和治疗计划

### 2. 知识库添加工具 ✅

**文件**: `examples/add_knowledge.py`

功能：
- 自动读取 `.txt` 文件
- 转换为向量并存储到ChromaDB
- 支持心理学知识和用户档案两种类型
- 自动提取元数据（分类、来源等）

使用方法：
```bash
python examples/add_knowledge.py
```

### 3. 对比实验脚本 ✅ （最重要！）

**文件**: `examples/comparison_experiment.py`

这是**论文实验的核心**，对比三种配置：

| 配置 | RAG | 记忆系统 | 用途 |
|-----|-----|---------|------|
| 裸LLM | ❌ | ❌ | 基线对比 |
| LLM+RAG | ✅ | ❌ | 证明RAG的价值 |
| 完整系统 | ✅ | ✅ | 证明记忆系统的价值 |

**测试场景**：
- 场景1：首次咨询（工作压力和睡眠）
- 场景2：第二次咨询（测试记忆功能）
- 场景3：焦虑情绪管理

**收集的指标**：
- 响应时间
- 响应长度
- 完整的对话记录
- 各场景的详细数据

**输出**：
- JSON格式的完整实验数据
- 可直接用于论文的统计分析

使用方法：
```bash
python examples/comparison_experiment.py
```

### 4. 结果可视化工具 ✅

**文件**: `examples/visualize_results.py`

自动生成论文需要的图表和文档：

**生成的图表**：
1. `response_time_comparison.png` - 响应时间对比柱状图
2. `response_length_comparison.png` - 响应长度对比柱状图
3. `scenario_comparison.png` - 不同场景的性能对比

**生成的文档**：
1. `detailed_comparison.md` - 详细数据对比表格（可转LaTeX）
2. `response_examples.md` - 三种配置的响应示例（用于案例分析）

使用方法：
```bash
python examples/visualize_results.py
```

### 5. 完整文档 ✅

**文件**: `EXPERIMENT_GUIDE.md`

包含：
- 完整的使用教程
- 每一步的详细说明
- 常见问题解答
- 如何将结果用于论文
- 自定义实验的方法

### 6. 一键运行脚本 ✅

**文件**: 
- `run_full_experiment.sh` (Linux/Mac)
- `run_full_experiment.bat` (Windows)

一个命令完成所有操作：
```bash
# Linux/Mac
./run_full_experiment.sh

# Windows
run_full_experiment.bat
```

自动执行：
1. 添加知识库
2. 运行对比实验
3. 生成可视化
4. 输出结果位置

## 📊 实验流程

```
开始
  ↓
[1] 添加知识库
  ├─ 心理学知识 (4个文件)
  └─ 用户档案 (2个文件)
  ↓
[2] 运行对比实验
  ├─ 测试：裸LLM
  ├─ 测试：LLM + RAG
  └─ 测试：完整系统
  ↓
[3] 生成结果
  ├─ JSON数据报告
  ├─ 可视化图表
  └─ 对比分析文档
  ↓
完成！→ 用于论文
```

## 🎯 论文写作要点

### 可以引用的数据

1. **定量数据**：
   - 三种配置的响应时间对比
   - 响应长度的差异
   - 不同场景下的性能表现

2. **定性分析**：
   - 裸LLM vs RAG：专业知识的引用
   - RAG vs 完整系统：记忆连贯性
   - 具体的对话案例

3. **可视化图表**：
   - 直接插入到论文中
   - 清晰展示系统优势

### 论文章节建议

**实验设计**：
```
3.1 实验配置
  - 基线系统（裸LLM）
  - RAG增强系统
  - 完整系统（RAG + 记忆）

3.2 测试场景
  - 场景1：首次咨询
  - 场景2：多次咨询（测试记忆）
  - 场景3：专业知识应用

3.3 评估指标
  - 响应时间
  - 响应质量（长度、专业性）
  - 记忆连贯性
```

**实验结果**：
```
4.1 性能对比
  - 插入图表：response_time_comparison.png
  - 插入表格：来自 detailed_comparison.md

4.2 质量分析
  - 响应长度增加 → 更多专业内容
  - 引用案例：来自 response_examples.md

4.3 记忆效果
  - 跨会话的信息保持
  - 用户历史的准确引用
```

## 📁 完整文件清单

### 新增文件

```
psychological_counseling_system/
├── data/
│   ├── sample_knowledge/              [新增]
│   │   ├── cbt_therapy.txt           [新增] 2000+字
│   │   ├── anxiety_management.txt    [新增] 2500+字
│   │   ├── depression_treatment.txt  [新增] 3000+字
│   │   └── sleep_insomnia.txt        [新增] 3500+字
│   └── sample_user_info/             [新增]
│       ├── user_a_profile.txt        [新增] 详细档案
│       └── user_b_profile.txt        [新增] 详细档案
├── examples/
│   ├── add_knowledge.py              [新增] 知识库工具
│   ├── comparison_experiment.py      [新增] 对比实验
│   └── visualize_results.py          [新增] 结果可视化
├── EXPERIMENT_GUIDE.md               [新增] 完整指南
├── run_full_experiment.sh            [新增] 一键运行(Linux)
└── run_full_experiment.bat           [新增] 一键运行(Windows)
```

### 运行后生成

```
experiments/                          [自动创建]
├── comparison_report_*.json         [实验数据]
├── detailed_comparison.md           [对比表格]
├── response_examples.md             [响应示例]
└── figures/                         [图表目录]
    ├── response_time_comparison.png
    ├── response_length_comparison.png
    └── scenario_comparison.png
```

## 🚀 快速开始

### 最简单的方式（推荐）

```bash
# 1. 进入项目目录
cd psychological_counseling_system

# 2. 运行一键脚本
./run_full_experiment.sh          # Linux/Mac
# 或
run_full_experiment.bat           # Windows

# 3. 查看结果
ls experiments/
```

### 分步执行

```bash
# 步骤1：添加知识库
python examples/add_knowledge.py

# 步骤2：运行实验
python examples/comparison_experiment.py

# 步骤3：生成图表
python examples/visualize_results.py
```

## 💡 使用技巧

### 添加自己的知识

1. 在 `data/sample_knowledge/` 创建 `.txt` 文件
2. 写入心理学相关内容
3. 重新运行 `add_knowledge.py`

### 自定义测试场景

编辑 `comparison_experiment.py` 中的 `TEST_SCENARIOS`：

```python
TEST_SCENARIOS = [
    {
        "name": "你的场景",
        "user_id": "test_user_003",
        "conversations": [
            {
                "turn": 1,
                "user": "用户输入...",
                "emotion": {"anxiety": 0.7}
            }
        ]
    }
]
```

### 修改图表样式

编辑 `visualize_results.py` 中的绘图函数，调整：
- 颜色
- 字体
- 图表大小
- 标签文字

## ⚠️ 注意事项

1. **API成本**：
   - 对比实验会调用多次LLM
   - 建议使用 `gpt-4o-mini` 降低成本
   - 或使用本地模型（修改 `config.yaml`）

2. **实验时间**：
   - OpenAI API: 约2-5分钟
   - 本地模型: 约5-10分钟

3. **数据保存**：
   - 所有结果自动保存
   - 可多次运行对比不同配置

## 📈 后续扩展

### 可以进一步做的

1. **添加更多测试场景**：
   - 不同心理问题
   - 不同用户类型
   - 更长的对话序列

2. **更多评估指标**：
   - 专业术语使用频率
   - 情感词汇分析
   - 用户满意度评分

3. **对比更多配置**：
   - 不同的embedding模型
   - 不同的检索策略
   - 不同的记忆管理方式

## 🎓 论文撰写建议

### 标题建议
- "基于RAG和长期记忆的智能心理咨询对话系统"
- "知识增强的心理健康对话系统：RAG与记忆机制的应用"

### 创新点
1. 三层记忆架构（会话/档案/趋势）
2. 双知识库RAG（专业+个人）
3. 完整的实验验证

### 实验部分结构
```
第3章 系统设计与实现
  3.1 系统架构
  3.2 RAG模块设计
  3.3 记忆系统设计

第4章 实验与评估
  4.1 实验设置
  4.2 对比实验设计
  4.3 评估指标
  4.4 实验结果
    4.4.1 性能对比
    4.4.2 质量分析  
    4.4.3 案例分析
  4.5 讨论

第5章 总结与展望
```

## ✅ 验证清单

运行实验前确认：

- [ ] 已安装所有依赖 (`pip install -r requirements.txt`)
- [ ] 已安装可视化依赖 (`pip install matplotlib numpy`)
- [ ] 已配置API密钥（如使用API模式）
- [ ] `data/sample_knowledge/` 目录存在且有文件
- [ ] `data/sample_user_info/` 目录存在且有文件

运行实验后确认：

- [ ] `experiments/` 目录已创建
- [ ] JSON报告文件已生成
- [ ] 三张PNG图表已生成
- [ ] Markdown文档已生成
- [ ] 图表中文显示正常

## 🎉 总结

本次更新完全解决了您的两个核心需求：

✅ **需求1**: 添加本地知识库
- 提供了完整的示例知识文件
- 创建了易用的添加工具
- 支持心理学知识和用户档案

✅ **需求2**: 对比不同配置的效果
- 实现了三种配置的自动对比
- 生成了论文所需的数据和图表
- 提供了案例分析的素材

**现在您可以**：
1. 一键运行完整实验
2. 获得论文需要的所有数据
3. 使用图表和分析证明系统有效性
4. 不仅说"系统能跑"，还能证明"系统有效"

**祝您实验顺利，论文成功！** 🎓📝

---

**需要帮助？**
- 查看 `EXPERIMENT_GUIDE.md` 获取详细教程
- 查看 `docs/architecture.md` 了解系统架构
- 运行 `python tests/test_system.py` 测试系统
