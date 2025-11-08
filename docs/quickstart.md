# 快速入门指南

## 1. 环境配置

### 1.1 创建虚拟环境

```bash
conda create -n psy_counsel python=3.10
conda activate psy_counsel
```

### 1.2 安装依赖

```bash
cd psychological_counseling_system
pip install -r requirements.txt
```

### 1.3 配置API密钥（如果使用API后端）

```bash
# 复制环境变量模板
cp .env.template .env

# 编辑.env文件，填入你的API密钥
nano .env
```

### 1.4 下载本地模型（如果使用本地后端）

```bash
# 进入项目的models目录
cd psychological_counseling_system/models

# 方法1: 使用wget下载
wget https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf

# 方法2: 使用huggingface-cli下载（推荐）
pip install huggingface-hub
huggingface-cli download TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF \
  tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf \
  --local-dir . \
  --local-dir-use-symlinks False

# 返回项目根目录
cd ..
```

## 2. 配置系统

编辑 `configs/config.yaml`:

### 2.1 选择LLM后端

**使用API (推荐用于开发):**
```yaml
llm:
  backend: 'api'
  api:
    provider: 'openai'
    model: 'gpt-4o-mini'
```

**使用本地模型:**
```yaml
llm:
  backend: 'local'
  local:
    model_path: './models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf'
    n_gpu_layers: 35  # 使用GPU加速
```

### 2.2 配置embedding模型

默认使用多语言模型，适合中文：
```yaml
rag:
  embedding:
    model_name: 'sentence-transformers/paraphrase-multilingual-mpnet-base-v2'
    device: 'cuda'  # 使用GPU
```

## 3. 运行示例

### 3.1 基础RAG对话

```bash
python examples/basic_rag_chat.py
```

这个示例展示：
- ✅ 创建用户
- ✅ 添加心理知识
- ✅ 进行单次会话对话
- ✅ RAG检索功能
- ✅ 记忆存储

### 3.2 多会话对话（展示记忆系统）

```bash
python examples/multi_session_chat.py
```

这个示例展示：
- ✅ 跨会话记忆
- ✅ 自动会话摘要
- ✅ 情绪趋势追踪
- ✅ 用户档案管理

## 4. 核心使用方法

### 4.1 初始化系统

```python
from utils import load_config, setup_directories
from dialogue import create_dialogue_manager_from_config

# 加载配置
config = load_config()
setup_directories(config)

# 创建对话管理器
dialogue_manager = create_dialogue_manager_from_config(config)
```

### 4.2 创建用户

```python
# 创建新用户
user_id = "user_001"
dialogue_manager.memory_manager.create_user(
    user_id=user_id,
    age=28,
    gender="女",
    occupation="软件工程师"
)
```

### 4.3 添加知识

```python
from knowledge import Document

# 添加心理知识
knowledge = [
    Document(
        content="认知行为疗法(CBT)是...",
        metadata={"source": "CBT", "category": "therapy"}
    )
]
dialogue_manager.rag_manager.add_psychological_knowledge(knowledge)

# 添加用户个人信息
dialogue_manager.rag_manager.add_user_knowledge(
    user_id=user_id,
    content="用户曾经历过工作倦怠，目前正在恢复中。",
    metadata={"type": "history"}
)
```

### 4.4 进行对话

```python
# 开始会话
session_id = dialogue_manager.start_session(user_id)

# 对话
response = dialogue_manager.chat(
    user_id=user_id,
    session_id=session_id,
    user_message="我最近压力很大",
    emotion={"stress": 0.8, "anxiety": 0.6}  # 可选
)

print(response)

# 结束会话（会自动生成摘要）
dialogue_manager.end_session(user_id, session_id)
```

### 4.5 查看记忆

```python
# 获取用户记忆
user_memory = dialogue_manager.memory_manager.get_user_memory(user_id)

# 查看档案
print(user_memory.profile.to_dict())

# 查看最近会话
recent_sessions = user_memory.get_recent_sessions(n=5)
for session in recent_sessions:
    print(f"会话: {session.session_summary}")

# 查看情绪趋势
if user_memory.trends:
    for record in user_memory.trends.emotion_history:
        print(f"时间: {record.timestamp}, 情绪: {record.emotions}")
```

## 5. 系统架构说明

```
用户输入
  ↓
记忆检索 ← [会话记忆 + 用户档案 + 长期趋势]
  ↓
RAG检索 ← [心理知识库 + 用户知识库]
  ↓
构建Prompt (整合记忆 + RAG结果)
  ↓
LLM生成回复
  ↓
更新记忆 → [保存对话 + 更新情绪 + 生成摘要]
  ↓
返回回复
```

## 6. 扩展开发

### 6.1 添加新的LLM后端

```python
# 1. 在 llm/ 目录创建新文件，如 custom_llm.py
from llm.base import BaseLLM, Message, LLMResponse

class CustomLLM(BaseLLM):
    def generate(self, messages, **kwargs):
        # 实现你的逻辑
        pass
    
    def count_tokens(self, text):
        # 实现token计数
        pass

# 2. 注册到工厂
from llm import LLMFactory
LLMFactory.register('custom', CustomLLM)
```

### 6.2 添加新的存储后端

```python
# 在 memory/storage.py 中添加
class MongoDBMemoryStorage(BaseMemoryStorage):
    def save_user_memory(self, user_memory):
        # 实现MongoDB存储
        pass
    
    # ... 其他方法
```

### 6.3 自定义RAG检索策略

```python
# 继承RAGManager并重写方法
from knowledge import RAGManager

class CustomRAGManager(RAGManager):
    def _rerank(self, query, documents):
        # 实现自定义重排序逻辑
        pass
```

## 7. 故障排除

### 7.1 CUDA相关错误

如果看到CUDA错误，修改配置：
```yaml
rag:
  embedding:
    device: 'cpu'  # 改为CPU
```

### 7.2 API调用失败

检查：
1. `.env` 文件中API密钥是否正确
2. 网络连接是否正常
3. API额度是否用完

### 7.3 本地模型加载失败

检查：
1. 模型文件路径是否正确
2. 模型文件是否下载完整
3. GPU内存是否足够

## 8. 性能优化建议

### 8.1 生产环境

- 使用SQLite或MongoDB替代JSON存储
- 启用RAG缓存
- 批量处理embedding计算
- 使用更强大的LLM（如GPT-4）

### 8.2 开发环境

- 使用轻量级模型快速迭代
- 减少RAG检索的top_k值
- 禁用自动摘要功能

## 9. 下一步计划

Phase 3即将开发：
- [ ] 多模态情感识别
- [ ] 语音输入支持
- [ ] 面部表情分析
- [ ] 跨模态情感融合

敬请期待！
