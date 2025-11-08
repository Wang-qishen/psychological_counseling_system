# 架构设计文档

## 设计理念

本系统采用**高度模块化、松耦合**的架构设计，核心设计理念包括：

1. **抽象与实现分离**: 每个模块都有清晰的抽象基类，便于扩展
2. **依赖注入**: 通过配置文件和工厂模式管理依赖
3. **单一职责**: 每个类只负责一个明确的功能
4. **开闭原则**: 对扩展开放，对修改关闭

## 系统层次结构

```
┌─────────────────────────────────────────────────────────┐
│                   应用层 (Application)                    │
│                                                           │
│  examples/          tests/           your_app.py         │
│  ├── basic_chat     └── test_system  └── custom_logic   │
│  └── multi_session                                        │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                   业务逻辑层 (Business)                    │
│                                                           │
│  dialogue/                                                │
│  └── DialogueManager  ← 整合所有组件的核心类              │
└─────────────────────────────────────────────────────────┘
                          ↓
┌──────────────┬─────────────────┬─────────────────────────┐
│  LLM模块      │   知识库模块     │   记忆模块              │
│              │                 │                         │
│  llm/        │   knowledge/    │   memory/               │
│  ├── Base    │   ├── Base      │   ├── Models            │
│  ├── OpenAI  │   ├── Chroma    │   ├── Storage           │
│  ├── Local   │   └── RAGMgr    │   └── Manager           │
│  └── Factory │                 │                         │
└──────────────┴─────────────────┴─────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                  基础设施层 (Infrastructure)               │
│                                                           │
│  - 文件系统 (JSON, SQLite)                                │
│  - 向量数据库 (ChromaDB, FAISS)                           │
│  - 外部API (OpenAI, Anthropic)                           │
│  - GPU/CPU计算资源                                         │
└─────────────────────────────────────────────────────────┘
```

## 核心模块详解

### 1. LLM模块 (llm/)

**职责**: 提供统一的大语言模型接口

**设计模式**: 策略模式 + 工厂模式

```
BaseLLM (抽象基类)
├── OpenAILLM (OpenAI API实现)
├── LocalLLM (本地GGUF模型实现)
└── [可扩展] AnthropicLLM, AzureLLM...

LLMFactory (工厂类)
└── 根据配置创建对应的LLM实例
```

**核心接口**:
```python
class BaseLLM:
    def generate(messages, temperature, max_tokens) -> LLMResponse
    def count_tokens(text) -> int
```

**扩展方式**:
```python
# 1. 继承BaseLLM
class NewLLM(BaseLLM):
    def generate(self, messages, **kwargs):
        # 实现你的逻辑
        pass

# 2. 注册到工厂
LLMFactory.register('new', NewLLM)
```

### 2. 知识库模块 (knowledge/)

**职责**: 管理心理知识库和用户知识库，提供RAG检索

**设计模式**: 策略模式 + 组合模式

```
BaseKnowledgeBase (抽象基类)
└── ChromaKnowledgeBase (基于ChromaDB的实现)
    └── [可扩展] FAISSKnowledgeBase, ElasticsearchKB...

RAGManager (组合多个知识库)
├── psychological_kb: BaseKnowledgeBase
├── user_kb: BaseKnowledgeBase
└── 提供统一的检索接口
```

**数据流**:
```
用户查询
  ↓
RAGManager.retrieve()
  ├→ psychological_kb.retrieve() (心理知识)
  ├→ user_kb.retrieve() (用户信息)
  ↓
重排序 (可选)
  ↓
构建组合上下文
  ↓
返回 RAGResult
```

**核心接口**:
```python
class BaseKnowledgeBase:
    def add_documents(documents)
    def retrieve(query, top_k, filter_dict) -> RetrievalResult
    def update_document(doc_id, document)
    def delete_document(doc_id)
```

### 3. 记忆系统模块 (memory/)

**职责**: 实现三层记忆架构，追踪用户状态

**设计模式**: 分层架构 + 存储库模式

```
记忆层次:
├── SessionMemory (会话级 - 短期)
│   └── 当前对话的所有轮次
├── UserProfile (用户档案 - 中期)
│   └── 基本信息、主要问题、生活事件
└── LongTermTrends (长期趋势 - 长期)
    ├── emotion_history (情绪历史)
    ├── topic_history (话题历史)
    └── intervention_history (干预历史)

存储后端:
BaseMemoryStorage (抽象基类)
├── JSONMemoryStorage (JSON文件实现)
└── [可扩展] SQLiteStorage, MongoDBStorage...

MemoryManager (管理记忆的CRUD)
└── 使用 BaseMemoryStorage 进行持久化
```

**核心接口**:
```python
class MemoryManager:
    def create_user(user_id, **profile) -> UserMemory
    def start_session(user_id) -> session_id
    def add_turn(user_id, session_id, user_msg, assistant_msg, emotion)
    def end_session(user_id, session_id)
    def retrieve_relevant_memory(user_id, context) -> Dict
```

**记忆检索策略**:
```
当前实现:
- 时间衰减: 最近的记忆权重更高
- 最大历史会话数: 限制检索范围

可扩展:
- 主题相似度匹配
- 情绪状态相关性
- 强化学习优化权重
```

### 4. 对话管理模块 (dialogue/)

**职责**: 整合所有组件，提供完整的对话功能

**设计模式**: 门面模式 + 模板方法模式

```
DialogueManager
├── llm: BaseLLM
├── rag_manager: RAGManager
├── memory_manager: MemoryManager
└── config: Dict

主要流程:
1. chat() ← 用户调用的主接口
   ├→ _build_context() ← 构建上下文
   │   ├→ memory_manager.retrieve_relevant_memory()
   │   └→ rag_manager.retrieve()
   ├→ _build_messages() ← 构建Prompt
   ├→ llm.generate() ← 生成回复
   └→ memory_manager.add_turn() ← 保存记忆
```

**Prompt构建策略**:
```
系统消息:
├── 基础系统提示词
├── 用户档案信息
├── 历史会话摘要
├── 情绪趋势
└── RAG检索的知识

对话历史:
└── 最近N轮对话

当前消息:
└── 用户输入
```

## 数据流图

### 完整对话流程

```
用户输入: "我最近压力很大"
    ↓
DialogueManager.chat(user_id, session_id, message, emotion)
    ↓
┌──────────────────────────────────────┐
│  步骤1: 构建上下文                     │
│  ┌────────────────────────────────┐  │
│  │ 1.1 记忆检索                    │  │
│  │ memory_manager.retrieve_relevant│  │
│  │ ├→ 获取用户档案                 │  │
│  │ ├→ 获取历史会话摘要             │  │
│  │ └→ 获取情绪趋势                 │  │
│  └────────────────────────────────┘  │
│  ┌────────────────────────────────┐  │
│  │ 1.2 RAG检索                     │  │
│  │ rag_manager.retrieve()         │  │
│  │ ├→ 从心理知识库检索             │  │
│  │ └→ 从用户知识库检索             │  │
│  └────────────────────────────────┘  │
└──────────────────────────────────────┘
    ↓
┌──────────────────────────────────────┐
│  步骤2: 构建Prompt                    │
│  _build_messages()                   │
│  ├→ 系统消息 (含记忆 + RAG)          │
│  ├→ 对话历史                          │
│  └→ 当前输入                          │
└──────────────────────────────────────┘
    ↓
┌──────────────────────────────────────┐
│  步骤3: LLM生成                       │
│  llm.generate(messages)              │
│  └→ 返回助手回复                      │
└──────────────────────────────────────┘
    ↓
┌──────────────────────────────────────┐
│  步骤4: 更新记忆                      │
│  memory_manager.add_turn()           │
│  ├→ 保存对话轮次                      │
│  ├→ 更新情绪轨迹                      │
│  └→ 更新长期趋势                      │
└──────────────────────────────────────┘
    ↓
返回: "我理解你的感受，压力大是很常见的..."
```

## 配置驱动架构

所有组件通过 `configs/config.yaml` 配置:

```yaml
系统配置结构:
├── llm: LLM配置
│   ├── backend: 'api' | 'local'
│   ├── api: API配置
│   └── local: 本地模型配置
├── rag: RAG配置
│   ├── embedding: Embedding模型
│   ├── vector_store: 向量数据库
│   └── retrieval: 检索参数
├── knowledge: 知识库配置
│   ├── psychological_kb: 心理知识库
│   └── user_kb: 用户知识库
├── memory: 记忆系统配置
│   ├── storage: 存储配置
│   ├── layers: 记忆层次配置
│   ├── retrieval: 检索策略
│   └── update: 更新策略
└── dialogue: 对话配置
    ├── system_prompt: 系统提示词
    ├── max_context_length: 上下文长度
    └── generation: 生成配置
```

**创建流程**:
```python
# 1. 加载配置
config = load_config('config.yaml')

# 2. 通过工厂方法创建各组件
llm = create_llm_from_config(config)
rag_manager = create_rag_manager_from_config(config)
memory_manager = create_memory_manager_from_config(config)

# 3. 组装对话管理器
dialogue_manager = DialogueManager(llm, rag_manager, memory_manager, config)
```

## 扩展点设计

### 1. 新增LLM后端

```python
# 步骤1: 实现接口
class CustomLLM(BaseLLM):
    def generate(self, messages, **kwargs):
        # 调用你的API或模型
        pass

# 步骤2: 注册
LLMFactory.register('custom', CustomLLM)

# 步骤3: 配置
# config.yaml:
# llm:
#   backend: 'custom'
#   custom:
#     your_param: value
```

### 2. 新增知识库后端

```python
# 步骤1: 实现接口
class ElasticsearchKB(BaseKnowledgeBase):
    def add_documents(self, documents):
        # Elasticsearch逻辑
        pass
    
    def retrieve(self, query, top_k, filter_dict):
        # 检索逻辑
        pass

# 步骤2: 在RAGManager中使用
rag_manager = RAGManager(
    psychological_kb=ElasticsearchKB(config),
    user_kb=ChromaKnowledgeBase(config),
    config=config
)
```

### 3. 新增记忆存储后端

```python
# 步骤1: 实现接口
class MongoDBMemoryStorage(BaseMemoryStorage):
    def save_user_memory(self, user_memory):
        # MongoDB逻辑
        pass
    
    def load_user_memory(self, user_id):
        # 加载逻辑
        pass

# 步骤2: 在storage.py中注册
def create_memory_storage(storage_type, config):
    if storage_type == 'mongodb':
        return MongoDBMemoryStorage(config)
    # ...
```

### 4. 自定义记忆检索策略

```python
# 继承MemoryManager并重写检索方法
class SmartMemoryManager(MemoryManager):
    def retrieve_relevant_memory(self, user_id, current_context):
        # 实现更智能的检索策略
        # 例如: 基于BERT的语义相似度
        pass
```

## 性能优化策略

### 1. 缓存机制

```python
# 添加LRU缓存
from functools import lru_cache

class CachedRAGManager(RAGManager):
    @lru_cache(maxsize=100)
    def retrieve(self, query, user_id=None, top_k=None):
        return super().retrieve(query, user_id, top_k)
```

### 2. 批量处理

```python
# Embedding批量计算
def batch_embed(texts, batch_size=32):
    embeddings = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        batch_embeddings = model.encode(batch)
        embeddings.extend(batch_embeddings)
    return embeddings
```

### 3. 异步处理

```python
import asyncio

async def async_chat(dialogue_manager, user_id, session_id, message):
    # 并行执行记忆检索和RAG检索
    memory_task = asyncio.create_task(
        get_memory_async(user_id)
    )
    rag_task = asyncio.create_task(
        get_rag_async(message, user_id)
    )
    
    memory, rag_result = await asyncio.gather(memory_task, rag_task)
    # 继续处理...
```

## 测试策略

### 单元测试

```python
# 每个模块独立测试
def test_llm():
    llm = OpenAILLM(config)
    response = llm.generate([Message(...)])
    assert response.content is not None

def test_knowledge_base():
    kb = ChromaKnowledgeBase(config)
    kb.add_documents([Document(...)])
    result = kb.retrieve("test query")
    assert len(result.documents) > 0
```

### 集成测试

```python
# 测试模块间协作
def test_dialogue_flow():
    dm = create_dialogue_manager_from_config(config)
    dm.memory_manager.create_user("test_user")
    session_id = dm.start_session("test_user")
    response = dm.chat("test_user", session_id, "test message")
    assert response is not None
```

### 性能测试

```python
import time

def benchmark_chat(n_turns=100):
    start = time.time()
    for i in range(n_turns):
        dm.chat(user_id, session_id, f"message {i}")
    elapsed = time.time() - start
    print(f"Average time per turn: {elapsed/n_turns:.2f}s")
```

## 安全性考虑

### 1. 数据隐私

```python
# 敏感数据加密
import hashlib

def hash_user_id(user_id):
    return hashlib.sha256(user_id.encode()).hexdigest()
```

### 2. 输入验证

```python
def validate_input(user_message):
    if len(user_message) > MAX_MESSAGE_LENGTH:
        raise ValueError("Message too long")
    
    # 检测注入攻击
    if contains_sql_injection(user_message):
        raise SecurityError("Invalid input")
```

### 3. Rate Limiting

```python
from functools import wraps
from time import time

def rate_limit(max_calls, time_window):
    calls = []
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time()
            calls[:] = [c for c in calls if c > now - time_window]
            if len(calls) >= max_calls:
                raise Exception("Rate limit exceeded")
            calls.append(now)
            return func(*args, **kwargs)
        return wrapper
    return decorator

@rate_limit(max_calls=10, time_window=60)
def chat(user_id, message):
    # ...
```

## 总结

这个架构的核心优势：

1. **高度模块化**: 每个模块职责单一，易于理解和维护
2. **易于扩展**: 通过抽象基类和工厂模式，新功能无需修改现有代码
3. **配置驱动**: 所有行为通过配置文件控制，无需改代码
4. **松耦合**: 模块间通过接口通信，降低依赖
5. **可测试性**: 每个模块可独立测试

适合：
- ✅ 增量开发
- ✅ 功能迭代
- ✅ 性能优化
- ✅ 学术研究
- ✅ 产品化
