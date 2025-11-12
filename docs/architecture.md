# System Architecture

This document describes the system architecture in detail, corresponding to Section 3 of our paper.

---

## Table of Contents

- [Overview](#overview)
- [Core Modules](#core-modules)
- [Dual Knowledge Base RAG](#dual-knowledge-base-rag)
- [Three-Layer Memory System](#three-layer-memory-system)
- [Data Flow](#data-flow)
- [Design Principles](#design-principles)

---

## Overview

The system follows a **modular layered architecture** with four core components:

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Interface                           │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Dialogue Manager                            │
│  • Orchestrates module interactions                             │
│  • Builds context from RAG + Memory                             │
│  • Prompt engineering                                           │
└──────┬───────────────────┬────────────────────┬─────────────────┘
       │                   │                    │
       ▼                   ▼                    ▼
┌─────────────┐   ┌──────────────────┐   ┌────────────────────┐
│  LLM Layer  │   │   RAG Layer       │   │   Memory Layer     │
│             │   │                   │   │                    │
│ ┌─────────┐ │   │ ┌──────────────┐ │   │ ┌────────────────┐ │
│ │ Local   │ │   │ │Professional  │ │   │ │Working Memory  │ │
│ │Qwen2-7B │ │◄──┤ │Knowledge Base│ │   │ │(Session)       │ │
│ └─────────┘ │   │ └──────────────┘ │   │ └────────────────┘ │
│     or      │   │                   │   │                    │
│ ┌─────────┐ │   │ ┌──────────────┐ │   │ ┌────────────────┐ │
│ │API Model│ │   │ │Personal      │ │   │ │Short-term      │ │
│ │(GPT-4)  │ │   │ │Knowledge Base│ │   │ │Memory (Summary)│ │
│ └─────────┘ │   │ └──────────────┘ │   │ └────────────────┘ │
│             │   │                   │   │                    │
│             │   │ ┌──────────────┐ │   │ ┌────────────────┐ │
│             │   │ │Hybrid        │ │   │ │Long-term Memory│ │
│             │   │ │Retrieval     │ │   │ │(Profile+Trends)│ │
│             │   │ └──────────────┘ │   │ └────────────────┘ │
└─────────────┘   └──────────────────┘   └────────────────────┘
       │                   │                    │
       └───────────────────┴────────────────────┘
                           │
                  ┌────────▼─────────┐
                  │  Vector Database  │
                  │  (ChromaDB)       │
                  └───────────────────┘
```

---

## Core Modules

### 1. Dialogue Manager (`dialogue/manager.py`)

**Responsibilities:**
- Coordinate interactions between LLM, RAG, and Memory layers
- Build complete context for LLM generation
- Manage conversation sessions
- Handle prompt engineering

**Key Methods:**
- `chat()`: Process user input and generate response
- `start_session()`: Initialize a new conversation session
- `end_session()`: Finalize session and trigger summarization
- `_build_context()`: Construct context from RAG and memory
- `_build_messages()`: Create LLM message list with proper formatting

**Context Construction Pipeline:**
```python
User Input 
  → Parallel Retrieval (RAG + Memory)
  → Context Fusion (Professional KB + Personal KB + Memory)
  → Prompt Engineering (System + Context + History + Current)
  → LLM Generation
  → Memory Update
  → Return Response
```

### 2. LLM Layer (`llm/`)

**Components:**
- `base.py`: Abstract base class defining LLM interface
- `local_llm.py`: Local model implementation using llama.cpp
- `openai_llm.py`: OpenAI API implementation
- `factory.py`: Factory pattern for creating LLM instances

**Features:**
- **Flexible Backend**: Switch between local and API models via configuration
- **Token Counting**: Accurate token estimation for context management
- **Error Handling**: Robust error handling and retry logic
- **Streaming Support**: Optional streaming for real-time responses

**Example:**
```python
# Local model
llm = LocalLLM(config={
    'model_path': 'models/qwen2-7b-instruct-q4_k_m.gguf',
    'n_ctx': 4096,
    'n_gpu_layers': 35
})

# API model
llm = OpenAILLM(config={
    'model': 'gpt-4o-mini',
    'temperature': 0.7
})

# Generate response
response = llm.generate(messages)
```

### 3. RAG Layer (`knowledge/`)

**Components:**
- `base.py`: Abstract knowledge base interface
- `chroma_kb.py`: ChromaDB vector store implementation
- `rag_manager.py`: Coordinates dual knowledge bases

**Dual Knowledge Base Architecture:**

#### Professional Knowledge Base
- **Content**: CBT techniques, anxiety management, depression treatment, etc.
- **Source**: SmileChat dataset + curated psychological literature
- **Collection**: `psych_knowledge`
- **Update**: Batch updates by maintainers

#### Personal Knowledge Base
- **Content**: User profiles, session history, preferences
- **Scope**: One collection per user (user ID isolation)
- **Collection**: `user_{user_id}_info`
- **Update**: Incremental after each session

**Retrieval Process:**
```python
Query → Embedding → Parallel Retrieval
  ├─ Professional KB: Semantic similarity search (top_k=5)
  └─ Personal KB: User-filtered semantic search (top_k=3)
       → Filtering (score > threshold)
       → Reranking (optional)
       → Context Fusion
```

### 4. Memory Layer (`memory/`)

**Components:**
- `models.py`: Data models (Turn, Session, UserMemory, etc.)
- `storage.py`: Storage backend (JSON, SQLite, MongoDB)
- `manager.py`: Memory management logic

**Three-Layer Memory Architecture:**

```
┌─────────────────────────────────────────────────────────────┐
│              Long-Term Memory (Persistent)                   │
│  • User Profile (age, occupation, issues)                   │
│  • Cross-session Trends (emotion, topics, interventions)    │
│  • Historical Summaries                                     │
│  • Storage: Persistent database                             │
│  • Capacity: Unlimited                                      │
└──────────────────────┬──────────────────────────────────────┘
                       │ Retrieval based on relevance
                       ▼
┌─────────────────────────────────────────────────────────────┐
│            Short-Term Memory (Session-level)                 │
│  • Session Summary (auto-generated after session)           │
│  • Key Information (important events, emotions)             │
│  • Intervention Record (techniques suggested)               │
│  • Storage: Recent 20 sessions                              │
│  • Capacity: ~20 sessions                                   │
└──────────────────────┬──────────────────────────────────────┘
                       │ Current session summary
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              Working Memory (Intra-session)                  │
│  • Current Session Turns (last 10 turns)                    │
│  • Real-time Emotion State                                  │
│  • Immediate Context                                        │
│  • Storage: In-memory (session scope)                       │
│  • Capacity: Last 10 turns                                  │
└─────────────────────────────────────────────────────────────┘
```

**Memory Operations:**

1. **Add Turn** (during conversation):
   ```python
   memory_manager.add_turn(
       user_id="user001",
       session_id="session123",
       user_message="I feel anxious",
       assistant_message="Let's explore that..."
   )
   ```

2. **Retrieve Relevant Memory** (before generation):
   ```python
   memory_context = memory_manager.retrieve_relevant_memory(
       user_id="user001",
       current_context="feeling anxious today"
   )
   # Returns: profile, recent sessions, emotion trends
   ```

3. **End Session** (trigger summarization):
   ```python
   memory_manager.end_session(
       user_id="user001",
       session_id="session123"
   )
   # Auto-generates summary and updates trends
   ```

---

## Dual Knowledge Base RAG

### Why Dual Knowledge Bases?

**Problem with Single Knowledge Base:**
- Professional knowledge (CBT techniques) and personal info (user profile) have different:
  - **Nature**: Generic vs. specific
  - **Update frequency**: Batch vs. real-time
  - **Retrieval strategy**: Similarity vs. user-filtered
  - **Privacy**: Public vs. private

**Solution: Separate Construction + Differentiated Retrieval**

### Professional Knowledge Base

**Content Sources:**
1. **SmileChat Dataset** (~16,000 counseling dialogues)
   - Extract high-quality counselor responses
   - Cover: anxiety, depression, relationships, work stress
   
2. **Curated Literature**
   - CBT techniques and practices
   - Mindfulness-based interventions
   - Crisis intervention protocols

**Preprocessing Pipeline:**
```python
Raw Text 
  → Cleaning (remove noise, normalize)
  → Chunking (chunk_size=500, overlap=50)
  → Embedding (sentence-transformers)
  → Store in ChromaDB (collection: psych_knowledge)
```

**Retrieval:**
```python
# Semantic similarity search
results = professional_kb.search(
    query="How to deal with anxiety?",
    top_k=5,
    score_threshold=0.5
)
```

### Personal Knowledge Base

**Content:**
- Basic info: age, gender, occupation, education
- Problem archive: main concerns, severity levels
- Intervention history: suggested techniques, user feedback
- Relationship context: family, social connections

**Structure:**
```json
{
  "user_id": "user001",
  "profile": {
    "age": 28,
    "gender": "female",
    "occupation": "software engineer",
    "main_issues": ["work_stress", "insomnia"]
  },
  "history": [
    {
      "date": "2024-01-15",
      "summary": "Discussed work-life balance...",
      "techniques": ["time_management", "breathing_exercise"]
    }
  ]
}
```

**Retrieval:**
```python
# User-filtered semantic search
results = personal_kb.search(
    query="recent work stress issues",
    user_id="user001",  # Filter by user
    top_k=3
)
```

### Context Fusion

Combine results from both knowledge bases:

```python
def _build_context(user_message, user_id):
    # Parallel retrieval
    prof_docs = professional_kb.retrieve(user_message, top_k=5)
    pers_docs = personal_kb.retrieve(user_message, user_id, top_k=3)
    
    # Format context
    context = f"""
    ### Relevant Professional Knowledge
    {format_docs(prof_docs)}
    
    ### User's Relevant Information
    {format_docs(pers_docs)}
    """
    
    return context
```

---

## Three-Layer Memory System

### Cognitive Psychology Inspiration

Based on:
- **Atkinson-Shiffrin Model**: Sensory → Short-term → Long-term
- **Baddeley's Working Memory Model**: Central executive + phonological loop + visuospatial sketchpad

### Layer 1: Working Memory

**Purpose**: Maintain conversation coherence within a session

**Implementation:**
```python
class WorkingMemory:
    def __init__(self, max_turns=10):
        self.max_turns = max_turns
        self.turns = []  # Recent turns only
    
    def add_turn(self, user_msg, assistant_msg):
        self.turns.append({'user': user_msg, 'assistant': assistant_msg})
        if len(self.turns) > self.max_turns:
            self.turns.pop(0)  # Sliding window
```

**Characteristics:**
- Capacity: Last 10 turns
- Lifetime: Single session
- Access: O(1) - direct access
- Update: Real-time after each turn

### Layer 2: Short-Term Memory

**Purpose**: Bridge between single session and long-term profile

**Implementation:**
```python
class ShortTermMemory:
    def __init__(self, max_sessions=20):
        self.max_sessions = max_sessions
        self.session_summaries = []
    
    def add_summary(self, session_id, summary):
        self.session_summaries.append({
            'session_id': session_id,
            'date': datetime.now(),
            'summary': summary,
            'key_points': extract_key_points(summary)
        })
        if len(self.session_summaries) > self.max_sessions:
            self.session_summaries.pop(0)
```

**Summary Generation:**
```python
def generate_session_summary(session_turns):
    prompt = f"""
    Summarize this counseling session in 2-3 sentences:
    
    {format_turns(session_turns)}
    
    Focus on:
    - User's main concerns
    - Key insights or breakthroughs
    - Techniques suggested
    """
    
    summary = llm.generate(prompt)
    return summary
```

**Characteristics:**
- Capacity: Last 20 sessions
- Lifetime: Recent weeks/months
- Access: Retrieved by relevance
- Update: After session ends

### Layer 3: Long-Term Memory

**Purpose**: Persistent user profile and trend analysis

**Components:**

1. **User Profile** (structured):
   ```python
   {
     "age": 28,
     "occupation": "software engineer",
     "main_issues": ["anxiety", "insomnia"],
     "start_date": "2024-01-01"
   }
   ```

2. **Emotion Trends** (time series):
   ```python
   {
     "emotion_history": [
       {"date": "2024-01-15", "anxiety": 7, "depression": 4},
       {"date": "2024-01-22", "anxiety": 6, "depression": 3}
     ],
     "average_emotions": {"anxiety": 6.5, "depression": 3.5}
   }
   ```

3. **Topic Evolution** (frequency analysis):
   ```python
   {
     "topics": {
       "work_stress": {"count": 15, "trend": "increasing"},
       "family_issues": {"count": 5, "trend": "stable"}
     }
   }
   ```

**Trend Analysis:**
```python
def analyze_emotion_trend(emotion_history, window=5):
    recent = emotion_history[-window:]
    avg_recent = mean([h['anxiety'] for h in recent])
    avg_overall = mean([h['anxiety'] for h in emotion_history])
    
    if avg_recent < avg_overall - 1:
        return "improving"
    elif avg_recent > avg_overall + 1:
        return "worsening"
    else:
        return "stable"
```

**Characteristics:**
- Capacity: Unlimited
- Lifetime: Persistent
- Access: Indexed queries
- Update: Periodic (after session, weekly analysis)

---

## Data Flow

### Complete Conversation Flow

```
1. User Input
   └─> "I'm feeling very anxious about work today"

2. Dialogue Manager receives input
   └─> Initiates parallel retrieval

3. Parallel Retrieval
   ├─> RAG Layer
   │   ├─> Professional KB search: "anxiety management techniques"
   │   └─> Personal KB search: user's work-related history
   │
   └─> Memory Layer
       ├─> Working Memory: last 10 turns of current session
       ├─> Short-term Memory: recent session summaries
       └─> Long-term Memory: user profile + emotion trends

4. Context Construction
   └─> Dialogue Manager combines all retrieved information:
       ├─> System prompt
       ├─> User profile (from long-term memory)
       ├─> Recent session summaries (from short-term memory)
       ├─> Professional knowledge (from RAG)
       ├─> Personal context (from RAG)
       └─> Conversation history (from working memory)

5. LLM Generation
   └─> LLM generates response based on enriched context

6. Memory Update
   ├─> Add turn to working memory
   ├─> Update emotion state (if needed)
   └─> If session ends: generate summary + update trends

7. Return Response
   └─> Response sent back to user
```

### Token Budget Management

To ensure context fits within model limits:

```python
def _truncate_context(messages, max_tokens=8000):
    # Priority: System > Current > Recent history > Older history
    
    current_tokens = count_tokens(messages)
    
    if current_tokens <= max_tokens:
        return messages
    
    # Keep system message and current user message
    system_msg = messages[0]
    user_msg = messages[-1]
    
    # Truncate middle (conversation history)
    history = messages[1:-1]
    truncated_history = []
    
    budget = max_tokens - count_tokens(system_msg) - count_tokens(user_msg)
    
    for msg in reversed(history):  # Keep most recent
        msg_tokens = count_tokens(msg)
        if budget - msg_tokens > 0:
            truncated_history.insert(0, msg)
            budget -= msg_tokens
        else:
            break
    
    return [system_msg] + truncated_history + [user_msg]
```

---

## Design Principles

### 1. Separation of Concerns

Each module has a single, well-defined responsibility:
- **LLM**: Text generation only
- **RAG**: Knowledge retrieval only
- **Memory**: State management only
- **Dialogue Manager**: Orchestration only

### 2. High Cohesion, Low Coupling

Modules interact through clean interfaces:
```python
# All LLMs implement the same interface
class BaseLLM(ABC):
    @abstractmethod
    def generate(self, messages: List[Message]) -> Response:
        pass
```

### 3. Configuration-Driven

All behavior controlled by YAML config:
```yaml
# Switch backends without code changes
llm:
  backend: 'local'  # Change to 'api'
```

### 4. Extensibility

Easy to add new components:
- New LLM backend: Implement `BaseLLM`
- New knowledge base: Implement `BaseKnowledgeBase`
- New memory storage: Implement `BaseStorage`

### 5. Privacy by Design

- User data isolation (separate collections)
- Local-first storage
- Minimal data retention
- Encryption support

---

## Performance Considerations

### Latency Optimization

1. **Parallel Retrieval**: RAG and memory retrieved simultaneously
2. **Async Updates**: Memory updates happen after response is returned
3. **Caching**: Embedding results cached
4. **Lazy Loading**: Models loaded on-demand

### Memory Optimization

1. **Sliding Windows**: Only keep recent data in memory
2. **Pagination**: Load long-term data in chunks
3. **Compression**: Summaries instead of full conversations

### Cost Optimization

1. **Local Summarization**: Use smaller local model for summaries
2. **Smart Retrieval**: Only retrieve when necessary
3. **Token Budgeting**: Strict context limits

---

## Security & Privacy

### Data Isolation

```python
# Each user has isolated storage
user_memory = get_user_memory(user_id)  # Only this user's data
user_kb = get_user_kb(user_id)  # Only this user's docs
```

### Access Control

```python
def retrieve_memory(user_id, session_id, requesting_user):
    if requesting_user != user_id:
        raise PermissionError("Cannot access other user's data")
    return memory_storage.get(user_id, session_id)
```

### Encryption (Optional)

```python
# Encrypt sensitive fields in storage
encrypted_profile = encrypt(user_profile, key=user_key)
storage.save(user_id, encrypted_profile)
```

---

## Further Reading

- [Configuration Guide](configuration.md) - Detailed configuration options
- [Evaluation Guide](evaluation.md) - System evaluation methodology
- [Examples](examples.md) - Code examples for each module

---

**Next**: [Quick Start Guide](quickstart.md) to see the system in action!
