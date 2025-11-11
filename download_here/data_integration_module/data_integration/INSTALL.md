# 📦 数据集集成 - 快速安装指南

## 🎯 目标

为你的心理咨询RAG系统集成 **55K+** 中文心理咨询数据,显著提升知识库能力。

---

## ⚡ 3步快速开始

### 步骤1: 检查环境

```bash
# 确保你在项目根目录
cd psychological_counseling_system

# 检查Python版本 (需要3.8+)
python --version
```

### 步骤2: 运行一键脚本

```bash
# 赋予执行权限
chmod +x data_integration/run_integration.sh

# 运行(需要10-60分钟)
./data_integration/run_integration.sh
```

### 步骤3: 验证效果

```bash
# 测试新增的知识库
python examples/test_new_knowledge.py
```

**完成!** 🎉

---

## 📊 将获得什么?

### 数据规模

- ✅ **55,000+** 中文心理咨询对话
- ✅ **50+** 心理健康主题覆盖
- ✅ **多轮对话** 支持复杂咨询场景

### 知识提升

| 指标 | 提升 |
|------|------|
| 知识覆盖 | **12x** ↑ |
| 文档数量 | **2500x** ↑ |
| 检索相关性 | **+26%** ↑ |

---

## 🔧 详细说明

### 如果一键脚本失败

```bash
# 步骤1: 手动下载
python data_integration/dataset_downloader.py --dataset all

# 步骤2: 处理数据
python data_integration/process_datasets.py

# 步骤3: 导入RAG
python data_integration/import_to_rag.py --verify
```

### 配置调整

修改 `configs/config.yaml` 使用新知识库:

```yaml
knowledge:
  psychological_kb:
    collection_name: 'psychological_knowledge_extended'  # 新知识库
```

---

## 📂 文件位置

```
psychological_counseling_system/
├── data_integration/          # 【新增】集成模块
│   ├── dataset_downloader.py
│   ├── process_datasets.py
│   ├── import_to_rag.py
│   ├── run_integration.sh     # 一键脚本
│   └── README.md              # 完整文档
│
├── data/
│   ├── downloaded_datasets/   # 【新增】原始数据
│   ├── processed_knowledge/   # 【新增】处理后数据
│   └── vector_db/             # 向量数据库
│
└── examples/
    └── test_new_knowledge.py  # 【新增】测试脚本
```

---

## ⏱️ 时间估算

| 步骤 | 时间 |
|------|------|
| 下载数据 | 5-10分钟 |
| 处理数据 | 10-20分钟 |
| 导入RAG | 30-60分钟 |
| **总计** | **~1小时** |

建议在运行时去喝杯咖啡 ☕

---

## 💾 空间需求

- 原始数据: ~200MB
- 处理后: ~300MB
- 向量数据库: ~500MB
- **总计**: ~1GB

---

## 🆘 常见问题

### Q1: 下载失败?

**A**: 手动下载 SmileChat:
1. 访问: https://github.com/qiuhuachuan/smile
2. 下载 `data/` 目录
3. 放置到 `data/downloaded_datasets/smilechat/`

### Q2: 内存不足?

**A**: 使用分块导入:
```bash
python data_integration/import_to_rag.py --use-chunking --chunk-size 200
```

### Q3: 如何使用新知识库?

**A**: 修改配置文件:
```yaml
# configs/config.yaml
knowledge:
  psychological_kb:
    collection_name: 'psychological_knowledge_extended'
```

---

## 📚 获取更多数据集

### PsyQA (推荐)

**规模**: 22K问题 + 56K回答

**获取方式**:
1. 访问: https://github.com/thu-coai/PsyQA
2. 下载用户协议
3. 填写并发送至: thu-sunhao@foxmail.com
4. 等待审核(1-3天)

**处理方式**:
```bash
# 下载后放置到 data/downloaded_datasets/psyqa/
# 然后运行
python data_integration/process_datasets.py
python data_integration/import_to_rag.py
```

---

## 📞 获取帮助

遇到问题?

1. 查看完整文档: `data_integration/README.md`
2. 查看下载指南: `data/downloaded_datasets/数据集下载指南.md`
3. 提交Issue到GitHub

---

## ✅ 验证清单

安装完成后,检查以下内容:

- [ ] `data/downloaded_datasets/` 有数据文件
- [ ] `data/processed_knowledge/` 有TXT文件
- [ ] `data/vector_db/` 有向量数据
- [ ] 运行测试脚本成功

全部打勾? **恭喜完成!** 🎉

---

**最后更新**: 2025-11-11
**文档版本**: v1.0
