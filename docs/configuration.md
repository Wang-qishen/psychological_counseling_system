# Configuration Guide

This guide covers all configuration options for the Psychological Counseling System.

---

## Table of Contents

- [Configuration File Structure](#configuration-file-structure)
- [LLM Configuration](#llm-configuration)
- [RAG Configuration](#rag-configuration)
- [Memory Configuration](#memory-configuration)
- [Dialogue Configuration](#dialogue-configuration)
- [System Configuration](#system-configuration)
- [Configuration Examples](#configuration-examples)

---

## Configuration File Structure

The main configuration file is `configs/config.yaml`. It follows this structure:

```yaml
llm:           # Language model settings
  backend: ...
  api: ...
  local: ...

rag:           # Retrieval-Augmented Generation settings
  embedding: ...
  vector_store: ...
  retrieval: ...

knowledge:     # Knowledge base settings
  psychological_kb: ...
  user_kb: ...

memory:        # Memory system settings
  storage: ...
  layers: ...
  retrieval: ...
  update: ...

dialogue:      # Dialogue management settings
  system_prompt: ...
  max_context_length: ...
  generation: ...

logging:       # Logging settings
  level: ...
  log_file: ...

paths:         # System paths
  data_dir: ...
  logs_dir: ...
```

---

## LLM Configuration

### Backend Selection

```yaml
llm:
  backend: 'local'  # Options: 'local' or 'api'
```

### API Configuration (for OpenAI, Anthropic, etc.)

```yaml
llm:
  backend: 'api'
  api:
    provider: 'openai'          # Options: 'openai', 'anthropic', 'azure'
    model: 'gpt-4o-mini'        # Model name
    temperature: 0.7            # 0.0 - 2.0, higher = more creative
    max_tokens: 2000            # Maximum tokens in response
    api_key_env: 'OPENAI_API_KEY'  # Environment variable name
    
    # Optional advanced settings
    top_p: 0.95                # Nucleus sampling parameter
    frequency_penalty: 0.0     # -2.0 to 2.0
    presence_penalty: 0.0      # -2.0 to 2.0
    timeout: 60                # Request timeout in seconds
    max_retries: 3             # Retry failed requests
```

**Supported Providers:**

1. **OpenAI**:
   ```yaml
   provider: 'openai'
   model: 'gpt-4'              # or 'gpt-4o-mini', 'gpt-3.5-turbo'
   api_key_env: 'OPENAI_API_KEY'
   ```

2. **Anthropic**:
   ```yaml
   provider: 'anthropic'
   model: 'claude-3-opus'      # or 'claude-3-sonnet', 'claude-3-haiku'
   api_key_env: 'ANTHROPIC_API_KEY'
   ```

3. **Azure OpenAI**:
   ```yaml
   provider: 'azure'
   model: 'your-deployment-name'
   api_key_env: 'AZURE_OPENAI_KEY'
   azure_endpoint: 'https://your-resource.openai.azure.com/'
   api_version: '2023-12-01-preview'
   ```

### Local Model Configuration

```yaml
llm:
  backend: 'local'
  local:
    model_path: 'models/models/qwen2-7b-instruct-q4_k_m.gguf'
    n_ctx: 4096                # Context window size
    n_threads: 8               # CPU threads to use
    n_gpu_layers: 35           # Number of layers to offload to GPU
                               # Set to 0 for CPU-only
    temperature: 0.7           # 0.0 - 2.0
    max_tokens: 2000           # Maximum tokens in response
    
    # Advanced settings
    top_p: 0.95               # Nucleus sampling
    top_k: 40                 # Top-k sampling
    repeat_penalty: 1.1       # Penalty for repetition
    stop: ['User:', '\n\n']   # Stop sequences
```

**GPU Configuration:**

For **NVIDIA GPUs**:
```yaml
n_gpu_layers: 35  # Offload all layers
```

For **CPU only**:
```yaml
n_gpu_layers: 0
```

For **partial GPU offload** (when GPU memory is limited):
```yaml
n_gpu_layers: 20  # Offload only 20 layers
```

**Model Path:**
- Absolute path: `/home/user/models/model.gguf`
- Relative path: `models/models/model.gguf` (relative to project root)

---

## RAG Configuration

### Embedding Configuration

```yaml
rag:
  embedding:
    model_name: 'sentence-transformers/paraphrase-multilingual-mpnet-base-v2'
    device: 'cuda'             # 'cuda' or 'cpu'
    
    # Optional: Override default settings
    max_seq_length: 384        # Maximum sequence length
    normalize_embeddings: true # L2 normalize embeddings
```

**Supported Embedding Models:**

1. **Multilingual** (recommended for Chinese + English):
   ```yaml
   model_name: 'sentence-transformers/paraphrase-multilingual-mpnet-base-v2'
   ```

2. **English-only** (faster):
   ```yaml
   model_name: 'sentence-transformers/all-MiniLM-L6-v2'
   ```

3. **Large** (better quality):
   ```yaml
   model_name: 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'
   ```

### Vector Store Configuration

```yaml
rag:
  vector_store:
    type: 'chroma'                    # Options: 'chroma', 'faiss'
    persist_directory: './data/vector_db'
    
    # ChromaDB-specific settings
    chroma_settings:
      anonymized_telemetry: false     # Disable telemetry
      allow_reset: true               # Allow database reset
```

### Retrieval Configuration

```yaml
rag:
  retrieval:
    top_k: 5                    # Number of documents to retrieve
    score_threshold: 0.5        # Minimum similarity score (0.0 - 1.0)
    rerank: true                # Enable reranking
    
    # Advanced settings
    search_type: 'similarity'   # 'similarity' or 'mmr'
    mmr_lambda: 0.5            # MMR diversity parameter (if using MMR)
    fetch_k: 20                # Documents to fetch before reranking
```

**Retrieval Strategies:**

1. **Similarity Search** (default):
   ```yaml
   search_type: 'similarity'
   top_k: 5
   ```

2. **Maximum Marginal Relevance (MMR)** (diverse results):
   ```yaml
   search_type: 'mmr'
   top_k: 5
   mmr_lambda: 0.5  # 0 = diversity, 1 = relevance
   ```

---

## Knowledge Configuration

### Professional Knowledge Base

```yaml
knowledge:
  psychological_kb:
    path: './data/psychological_knowledge'
    collection_name: 'psych_knowledge'
    chunk_size: 500            # Characters per chunk
    chunk_overlap: 50          # Overlap between chunks
    
    # Optional: Metadata filtering
    metadata_filters:
      language: 'en'
      source: 'verified'
```

### User Knowledge Base

```yaml
knowledge:
  user_kb:
    path: './data/user_profiles'
    collection_name: 'user_info'
    chunk_size: 300
    chunk_overlap: 30
    
    # Privacy settings
    encryption: true           # Encrypt user data
    retention_days: 365        # Delete data after N days
```

---

## Memory Configuration

### Storage Configuration

```yaml
memory:
  storage:
    type: 'json'               # Options: 'json', 'sqlite', 'mongodb'
    path: './data/memory_db'
    
    # SQLite settings (if type: 'sqlite')
    sqlite:
      database: './data/memory.db'
      
    # MongoDB settings (if type: 'mongodb')
    mongodb:
      uri: 'mongodb://localhost:27017/'
      database: 'psychological_counseling'
```

### Memory Layers Configuration

```yaml
memory:
  layers:
    # Working Memory (intra-session)
    session:
      max_turns: 10            # Maximum turns to keep in working memory
      enabled: true
      
    # Short-term Memory (session-level)
    profile:
      auto_update: true        # Automatically update user profile
      fields:                  # Fields to extract and maintain
        - 'age'
        - 'gender'
        - 'occupation'
        - 'main_issues'
        - 'life_events'
      max_sessions: 20         # Keep summaries of last N sessions
      
    # Long-term Memory (persistent)
    trends:
      track_emotions: true     # Track emotion trends over time
      track_topics: true       # Track topic frequency
      track_interventions: true  # Track suggested interventions
      analysis_interval: 7     # Days between trend analysis
```

### Memory Retrieval Configuration

```yaml
memory:
  retrieval:
    time_decay_factor: 0.95    # Weight for recent memories
                               # 1.0 = no decay, 0.0 = complete decay
    max_history_sessions: 10   # Maximum past sessions to consider
    relevance_threshold: 0.3   # Minimum relevance score
```

### Memory Update Configuration

```yaml
memory:
  update:
    auto_summarize: true       # Auto-generate session summaries
    summarize_backend: 'local' # 'local' or 'api'
                               # 'local' uses smaller model to save cost
    summary_min_turns: 3       # Minimum turns before summarizing
    summary_prompt: |          # Custom summary prompt (optional)
      Summarize this counseling session...
```

---

## Dialogue Configuration

### System Prompt

```yaml
dialogue:
  system_prompt: |
    You are a professional, empathetic psychological counselor. Your tasks are:
    1. Listen to the user's concerns and feelings
    2. Provide professional psychological insights and advice
    3. Use CBT and other evidence-based techniques
    4. Maintain a warm, non-judgmental attitude
    5. Remember and relate to the user's historical information
```

### Context Management

```yaml
dialogue:
  max_context_length: 8000     # Maximum tokens in context
  
  # Priority order for truncation (when context too long)
  truncation_priority:
    - 'system_prompt'          # Always keep
    - 'user_profile'           # High priority
    - 'rag_results'            # High priority
    - 'current_message'        # Always keep
    - 'recent_history'         # Medium priority
    - 'older_history'          # Low priority (truncate first)
```

### Generation Configuration

```yaml
dialogue:
  generation:
    enable_rag: true           # Use RAG for knowledge retrieval
    enable_memory: true        # Use memory system
    
    # Knowledge source weights (when combining multiple sources)
    weights:
      psychological_knowledge: 0.6
      user_knowledge: 0.4
    
    # Response validation
    min_response_length: 50    # Minimum response length (chars)
    max_response_length: 1000  # Maximum response length (chars)
    
    # Safety checks
    check_harmful_content: true
    harmful_keywords: ['suicide', 'self-harm', 'kill']
```

---

## System Configuration

### Logging

```yaml
logging:
  level: 'INFO'               # DEBUG, INFO, WARNING, ERROR, CRITICAL
  log_file: './logs/system.log'
  log_to_console: true
  
  # Log format
  format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
  
  # Rotation
  max_bytes: 10485760         # 10MB
  backup_count: 5             # Keep 5 backup files
```

### Paths

```yaml
paths:
  data_dir: './data'
  logs_dir: './logs'
  cache_dir: './cache'
  models_dir: './models'
```

---

## Configuration Examples

### Example 1: Cost-Optimized Setup

For minimizing API costs:

```yaml
llm:
  backend: 'local'           # Use free local model
  
memory:
  update:
    auto_summarize: true
    summarize_backend: 'local'  # Use local model for summaries

rag:
  retrieval:
    top_k: 3                 # Retrieve fewer documents
```

### Example 2: Performance-Optimized Setup

For best response quality (costs more):

```yaml
llm:
  backend: 'api'
  api:
    provider: 'openai'
    model: 'gpt-4'           # Best quality

rag:
  retrieval:
    top_k: 10                # More context
    rerank: true
    
memory:
  layers:
    session:
      max_turns: 20          # More history
```

### Example 3: Privacy-Focused Setup

For maximum privacy:

```yaml
llm:
  backend: 'local'           # No data sent to API

memory:
  storage:
    type: 'json'             # Local storage only
    
knowledge:
  user_kb:
    encryption: true         # Encrypt user data
    retention_days: 90       # Auto-delete after 90 days
```

### Example 4: Development/Testing Setup

For rapid development:

```yaml
llm:
  backend: 'api'
  api:
    model: 'gpt-3.5-turbo'   # Faster, cheaper
    
logging:
  level: 'DEBUG'             # Verbose logging
  
memory:
  layers:
    session:
      max_turns: 5           # Smaller memory for faster testing
```

### Example 5: Research/Evaluation Setup

For research experiments:

```yaml
# Disable all enhancements for baseline
dialogue:
  generation:
    enable_rag: false
    enable_memory: false

# Or enable only RAG
dialogue:
  generation:
    enable_rag: true
    enable_memory: false

# Or enable only memory
dialogue:
  generation:
    enable_rag: false
    enable_memory: true
```

---

## Environment Variables

Some settings can be overridden by environment variables:

```bash
# LLM settings
export OPENAI_API_KEY='your-key'
export LLM_BACKEND='api'              # Override config
export LLM_MODEL='gpt-4'

# RAG settings
export RAG_TOP_K=5
export RAG_THRESHOLD=0.5

# Memory settings
export MEMORY_STORAGE_TYPE='json'
export MEMORY_STORAGE_PATH='./data/memory'

# Logging
export LOG_LEVEL='DEBUG'
```

**Priority**: Environment variable > Config file > Default value

---

## Configuration Validation

Validate your configuration before running:

```python
from utils.config_validator import validate_config
import yaml

with open('configs/config.yaml', 'r') as f:
    config = yaml.safe_load(f)

is_valid, errors = validate_config(config)

if not is_valid:
    for error in errors:
        print(f"❌ {error}")
else:
    print("✅ Configuration is valid")
```

---

## Best Practices

### 1. Use Version Control for Configs

```bash
# Create a custom config
cp configs/config.yaml configs/config_production.yaml

# Add to .gitignore if it contains sensitive info
echo "configs/config_production.yaml" >> .gitignore
```

### 2. Separate Dev and Prod Configs

```python
import os

env = os.getenv('ENV', 'dev')
config_file = f'configs/config_{env}.yaml'

with open(config_file, 'r') as f:
    config = yaml.safe_load(f)
```

### 3. Use Environment Variables for Secrets

```yaml
# Don't put API keys directly in config
api_key_env: 'OPENAI_API_KEY'  # ✅ Good

# Instead of
api_key: 'sk-abc123...'         # ❌ Bad
```

### 4. Document Custom Configs

```yaml
# configs/config_custom.yaml
# Author: John Doe
# Purpose: Optimized for GPT-4 + Local summarization
# Date: 2024-01-15

llm:
  backend: 'api'
  # ... rest of config
```

---

## Troubleshooting Configuration

### Config Not Loading

**Error**: `FileNotFoundError: config.yaml`

**Solution**: Ensure you're running from project root:
```bash
cd psychological_counseling_system
python your_script.py
```

### Invalid YAML Syntax

**Error**: `yaml.scanner.ScannerError`

**Solution**: Validate YAML syntax:
```bash
python -c "import yaml; yaml.safe_load(open('configs/config.yaml'))"
```

### Value Out of Range

**Error**: `ValueError: temperature must be between 0 and 2`

**Solution**: Check parameter ranges in this guide.

---

## Further Reading

- [Architecture Documentation](architecture.md) - Understanding the system
- [Quick Start Guide](quickstart.md) - Get started quickly
- [Evaluation Guide](evaluation.md) - Running experiments

---

**Questions?** Check the [FAQ](faq.md) or open an issue!
