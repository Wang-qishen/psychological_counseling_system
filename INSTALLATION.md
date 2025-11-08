# 安装和部署指南

## 项目已完成！🎉

你的心理咨询系统代码仓库已经完全构建完成。以下是完整的部署和使用指南。

## 📁 项目结构

```
psychological_counseling_system/
├── configs/
│   └── config.yaml                 # 配置文件
├── llm/                            # LLM抽象层
│   ├── __init__.py
│   ├── base.py                     # 基类
│   ├── openai_llm.py              # OpenAI实现
│   ├── local_llm.py               # 本地GGUF模型实现
│   └── factory.py                  # 工厂类
├── knowledge/                      # 知识库模块(RAG)
│   ├── __init__.py
│   ├── base.py                     # 基类
│   ├── chroma_kb.py               # ChromaDB实现
│   └── rag_manager.py             # RAG管理器
├── memory/                         # 记忆系统模块
│   ├── __init__.py
│   ├── models.py                   # 数据模型
│   ├── storage.py                  # 存储后端
│   └── manager.py                  # 记忆管理器
├── dialogue/                       # 对话管理模块
│   ├── __init__.py
│   └── manager.py                  # 对话管理器(整合所有组件)
├── utils/                          # 工具函数
│   ├── __init__.py
│   └── helpers.py
├── examples/                       # 示例代码
│   ├── basic_rag_chat.py          # 基础对话示例
│   └── multi_session_chat.py      # 多会话示例
├── tests/                          # 测试代码
│   └── test_system.py             # 系统测试
├── docs/                           # 文档
│   └── quickstart.md              # 快速入门
├── data/                           # 数据目录(自动创建)
├── logs/                           # 日志目录(自动创建)
├── requirements.txt                # 依赖列表
├── .env.template                   # 环境变量模板
└── README.md                       # 项目说明
```

## 🚀 快速开始

### 1. 上传到服务器

将整个 `psychological_counseling_system` 目录上传到你的服务器：

```bash
# 在你的本地机器
scp -r psychological_counseling_system root@your-server:/path/to/project/

# 或使用你喜欢的方式（如git, rsync等）
```

### 2. 安装依赖

在服务器上：

```bash
# 激活conda环境
conda activate psy_counsel  # 或创建新环境

# 进入项目目录
cd psychological_counseling_system

# 安装依赖
pip install -r requirements.txt
```

### 3. 配置系统

#### 方案A: 使用OpenAI API（推荐用于快速测试）

```bash
# 1. 复制环境变量模板
cp .env.template .env

# 2. 编辑.env文件，添加你的API密钥
nano .env
# 在文件中添加:
# OPENAI_API_KEY=sk-your-api-key-here

# 3. 编辑配置文件
nano configs/config.yaml
# 确保以下配置:
# llm:
#   backend: 'api'
#   api:
#     provider: 'openai'
#     model: 'gpt-4o-mini'
```

#### 方案B: 使用本地TinyLlama模型

```bash
# 1. 下载模型到项目内的models目录
cd psychological_counseling_system/models

# 方法1: 使用wget
wget https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf

# 方法2: 使用huggingface-cli（推荐，支持断点续传）
pip install huggingface-hub
huggingface-cli download TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF \
  tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf \
  --local-dir . \
  --local-dir-use-symlinks False

# 2. 返回项目根目录并编辑配置
cd ..
nano configs/config.yaml
# 修改:
# llm:
#   backend: 'local'
#   local:
#     model_path: './models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf'
#     n_gpu_layers: 35  # 利用你的A40 GPU
```

### 4. 运行测试

```bash
# 运行系统测试
python tests/test_system.py
```

如果看到所有测试都是 ✅ PASSED，说明系统运行正常！

### 5. 运行示例

```bash
# 基础对话示例
python examples/basic_rag_chat.py

# 多会话对话示例（展示记忆系统）
python examples/multi_session_chat.py
```

## 🎯 核心功能展示

### 功能1: RAG增强的对话

系统会自动从心理知识库检索相关信息：

```python
from dialogue import create_dialogue_manager_from_config
from utils import load_config

config = load_config()
dm = create_dialogue_manager_from_config(config)

# 添加心理知识
from knowledge import Document
dm.rag_manager.add_psychological_knowledge([
    Document(
        content="认知行为疗法(CBT)通过改变思维模式来改善情绪...",
        metadata={"source": "CBT基础"}
    )
])

# 用户问题会自动检索相关知识
response = dm.chat(user_id, session_id, "什么是CBT?")
```

### 功能2: 三层记忆系统

- **会话级记忆**：记住当前对话的所有内容
- **用户档案**：存储用户的基本信息和主要问题
- **长期趋势**：追踪情绪变化、话题演变

```python
# 第一次会话
session1_id = dm.start_session("user001")
dm.chat("user001", session1_id, "我最近压力很大")
dm.end_session("user001", session1_id)

# 第二次会话（几天后）
session2_id = dm.start_session("user001")
# 系统会记住第一次会话的内容！
dm.chat("user001", session2_id, "上次说的压力问题...")
```

### 功能3: 自动会话摘要

每次会话结束时，系统会自动：
1. 生成会话摘要
2. 提取主要话题
3. 记录情绪轨迹

## 🔧 自定义和扩展

### 添加新的LLM后端

```python
# 1. 创建新的LLM类
from llm.base import BaseLLM

class CustomLLM(BaseLLM):
    def generate(self, messages, **kwargs):
        # 你的实现
        pass
    
    def count_tokens(self, text):
        # 你的实现
        pass

# 2. 注册
from llm import LLMFactory
LLMFactory.register('custom', CustomLLM)

# 3. 在配置中使用
# config.yaml:
# llm:
#   backend: 'custom'
#   custom:
#     your_params: ...
```

### 添加新的知识库

```python
from knowledge.base import BaseKnowledgeBase

class MyKnowledgeBase(BaseKnowledgeBase):
    # 实现必需的方法
    pass

# 使用
my_kb = MyKnowledgeBase(config)
rag_manager = RAGManager(
    psychological_kb=my_kb,
    user_kb=user_kb,
    config=config
)
```

## 📊 性能优化

### 针对你的A40 GPU

```yaml
# configs/config.yaml
rag:
  embedding:
    device: 'cuda'  # 使用GPU

llm:
  local:
    n_gpu_layers: 35  # 全部层使用GPU
```

### 批量处理

如果需要处理多个用户：

```python
# 使用线程池或进程池
from concurrent.futures import ThreadPoolExecutor

def process_user(user_id, message):
    session_id = dm.start_session(user_id)
    response = dm.chat(user_id, session_id, message)
    dm.end_session(user_id, session_id)
    return response

with ThreadPoolExecutor(max_workers=4) as executor:
    results = executor.map(process_user, user_ids, messages)
```

## 🐛 常见问题

### Q1: CUDA out of memory

**解决方案**:
```yaml
# 减少GPU层数
llm:
  local:
    n_gpu_layers: 20  # 从35降到20
```

或使用CPU：
```yaml
rag:
  embedding:
    device: 'cpu'
```

### Q2: ChromaDB报错

**解决方案**:
```bash
# 删除旧的向量数据库
rm -rf data/vector_db
# 重新运行
```

### Q3: API调用超时

**解决方案**:
```python
# 增加超时时间
import openai
openai.api_timeout = 60  # 秒
```

## 📝 下一步开发计划

已完成：
- [x] Phase 1: 基础RAG框架
- [x] Phase 2: 记忆系统

即将开发：
- [ ] Phase 3: 多模态情感识别
  - 语音情感分析
  - 面部表情识别
  - 跨模态融合
- [ ] Phase 4: 强化学习优化

## 📞 技术支持

如果遇到问题：

1. **查看日志**: `logs/system.log`
2. **运行测试**: `python tests/test_system.py`
3. **查看文档**: `docs/quickstart.md`

## 🎓 论文写作建议

### 实验数据收集

系统已经内置了完整的日志和数据记录：

```python
# 记忆数据存储在
data/memory_db/user_xxx.json

# 可以用于分析:
# - 对话轮次
# - 会话摘要质量
# - 情绪变化趋势
# - RAG检索效果
```

### 评估指标

建议的评估维度：

1. **记忆准确性**: 系统能否正确引用历史信息
2. **RAG相关性**: 检索的知识是否相关
3. **用户满意度**: 主观评分
4. **对话连贯性**: 多轮对话的连贯性

### 对比实验

```python
# Baseline 1: 无记忆的RAG
config['dialogue']['generation']['enable_memory'] = False

# Baseline 2: 无RAG的对话
config['dialogue']['generation']['enable_rag'] = False

# 你的系统: 完整功能
# 对比三种配置的效果
```

## 🎉 恭喜！

你现在拥有一个：
- ✅ 高度模块化的代码库
- ✅ 支持增量开发
- ✅ 易于扩展和维护
- ✅ 完整的文档和示例
- ✅ Phase 1 & 2 功能完整实现

准备好开始你的实验了吗？祝你论文顺利！🚀
