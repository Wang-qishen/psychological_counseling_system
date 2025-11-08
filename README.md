# 🎁 新增文件包 - 增量开发

## 📦 这个文件夹包含什么？

这是为您的**心理咨询系统**增量开发的所有新文件，包括：

✅ **4个心理学专业知识文件** (11,000+字)  
✅ **2个详细用户档案**  
✅ **3个Python实验脚本**  
✅ **2个详细文档** (7,000+字)  
✅ **2个一键运行脚本**  

**总计：13个新文件**

---

## 🚀 快速开始（3步）

### 1️⃣ 查看文件放置位置

**请先阅读**：[文件放置位置.txt](文件放置位置.txt)  
了解每个文件应该放在原项目的哪个位置。

### 2️⃣ 复制文件到原项目

**详细步骤**：[安装说明.md](安装说明.md)  
包含完整的安装教程和验证方法。

### 3️⃣ 运行测试

```bash
cd 您的项目目录
python examples/add_knowledge.py
```

---

## 📂 文件清单

### 📚 知识库文件 (data/sample_knowledge/)

| 文件 | 内容 | 字数 |
|-----|------|------|
| cbt_therapy.txt | 认知行为疗法详解 | ~2000字 |
| anxiety_management.txt | 焦虑症管理技术 | ~2500字 |
| depression_treatment.txt | 抑郁症治疗方法 | ~3000字 |
| sleep_insomnia.txt | 失眠认知行为疗法 | ~3500字 |

**用途**：提供专业的心理学知识，用于RAG检索增强

---

### 👤 用户档案 (data/sample_user_info/)

| 文件 | 用户信息 |
|-----|---------|
| user_a_profile.txt | 28岁女性软件工程师，工作压力、失眠 |
| user_b_profile.txt | 35岁男性教师，抑郁、家庭问题 |

**用途**：示例用户档案，用于个性化咨询

---

### 🐍 实验脚本 (examples/)

| 文件 | 功能 |
|-----|------|
| add_knowledge.py | 将文本文件添加到知识库 |
| comparison_experiment.py | 对比裸LLM、LLM+RAG、完整系统 |
| visualize_results.py | 生成论文用的图表和分析 |

**用途**：**核心功能！** 用于实验和论文数据收集

---

### 📖 文档 (根目录)

| 文件 | 内容 |
|-----|------|
| EXPERIMENT_GUIDE.md | 详细使用教程 (4000+字) |
| UPDATE_SUMMARY.md | 完整更新说明 (3000+字) |

**用途**：完整的使用指南和功能说明

---

### 🚀 运行脚本 (根目录)

| 文件 | 平台 |
|-----|------|
| run_full_experiment.sh | Linux/Mac |
| run_full_experiment.bat | Windows |

**用途**：一键运行完整实验流程

---

## 💡 这些文件能做什么？

### 对于您的需求

✅ **添加本地知识库**
- 4个高质量心理学知识文件
- 2个详细用户档案
- 一键添加工具

✅ **对比实验和数据收集**
- 自动对比三种配置效果
- 生成论文所需的图表和数据
- 证明系统的有效性

### 实验会生成什么？

运行实验后，会在 `experiments/` 目录生成：

```
experiments/
├── comparison_report_*.json      # 完整实验数据
├── detailed_comparison.md        # 对比表格（可用于论文）
├── response_examples.md          # 响应案例（用于分析）
└── figures/
    ├── response_time_comparison.png    # 时间对比图
    ├── response_length_comparison.png  # 长度对比图
    └── scenario_comparison.png         # 场景对比图
```

**这些都是论文需要的！** 📝

---

## 📍 安装位置对照表

| 这个文件夹中的路径 | 应该放到原项目的位置 |
|------------------|-------------------|
| `data/sample_knowledge/*` | `原项目/data/sample_knowledge/` |
| `data/sample_user_info/*` | `原项目/data/sample_user_info/` |
| `examples/*.py` | `原项目/examples/` |
| `*.md` | `原项目/` (根目录) |
| `*.sh` | `原项目/` (根目录) |
| `*.bat` | `原项目/` (根目录) |

---

## ⚠️ 重要提示

1. **不会覆盖任何原有文件**
   - 所有文件都是新增的
   - 完全向后兼容

2. **需要额外依赖**
   ```bash
   pip install matplotlib numpy
   ```

3. **推荐使用顺序**
   - 先阅读 `文件放置位置.txt` (30秒)
   - 再看 `安装说明.md` (完整步骤)
   - 复制文件到原项目
   - 运行 `add_knowledge.py` 测试

---

## 🎯 下载后的第一步

### 最简单的方式

1. **打开** `文件放置位置.txt`
2. **复制**文件到对应位置
3. **运行**测试：
   ```bash
   cd 您的原项目目录
   python examples/add_knowledge.py
   ```

### 完整实验

```bash
cd 您的原项目目录
./run_full_experiment.sh          # Linux/Mac
# 或
run_full_experiment.bat           # Windows
```

3-5分钟后获得所有实验数据！

---

## 📚 推荐阅读顺序

1. **快速了解** → `文件放置位置.txt` (1分钟)
2. **详细安装** → `安装说明.md` (5分钟)
3. **功能说明** → `UPDATE_SUMMARY.md` (10分钟)
4. **使用教程** → `EXPERIMENT_GUIDE.md` (需要时查阅)

---

## ✅ 验证清单

安装后检查：
- [ ] `data/sample_knowledge/` 有4个txt文件
- [ ] `data/sample_user_info/` 有2个txt文件
- [ ] `examples/` 新增了3个py文件
- [ ] 根目录新增了4个文件（2个md + 2个脚本）

全部打勾？恭喜，安装成功！🎉

---

## 🎁 额外资源

本文件夹还包含：
- ✅ 完整的安装教程
- ✅ 详细的功能说明
- ✅ 快速参考卡片
- ✅ 常见问题解答

---

## 🚀 立即开始

**从这里开始**：
1. 打开 `文件放置位置.txt`
2. 按照说明复制文件
3. 运行第一个测试

**3分钟后**，您就可以运行实验并获取论文数据了！

---

## 📞 需要帮助？

- 安装问题 → 查看 `安装说明.md`
- 使用问题 → 查看 `EXPERIMENT_GUIDE.md`
- 功能说明 → 查看 `UPDATE_SUMMARY.md`

---

**祝您使用顺利！** 🎓📝✨
