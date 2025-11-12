# Quick Start Guide

Get started with the Psychological Counseling System in 5 minutes!

---

## Prerequisites

Before starting, ensure you have:
- Python 3.8 or higher
- pip installed
- (Optional) CUDA-capable GPU for local model

---

## Step 1: Installation (2 minutes)

```bash
# Clone the repository
git clone https://github.com/yourusername/psychological_counseling_system.git
cd psychological_counseling_system

# Install dependencies
pip install -r requirements.txt

# Download embedding model
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')"
```

---

## Step 2: Choose Your LLM Backend (1 minute)

### Option A: Use OpenAI API (Easiest, Recommended for First Try)

1. Get an OpenAI API key from https://platform.openai.com/api-keys

2. Set your API key:
   ```bash
   export OPENAI_API_KEY='your-api-key-here'
   ```

3. Edit `configs/config.yaml`:
   ```yaml
   llm:
     backend: 'api'
   ```

### Option B: Use Local Model (Free but Slower)

1. Download Qwen2-7B model:
   ```bash
   bash download_model.sh
   ```

2. Edit `configs/config.yaml`:
   ```yaml
   llm:
     backend: 'local'
   ```

---

## Step 3: Run Your First Conversation (1 minute)

Create a file `test_chat.py`:

```python
from dialogue import create_dialogue_manager_from_config
import yaml

# Load configuration
with open('configs/config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Create dialogue manager
manager = create_dialogue_manager_from_config(config)

# Start a new session
user_id = "demo_user"
session_id = manager.start_session(user_id)

# Have a conversation
messages = [
    "Hi, I've been feeling really stressed about work lately.",
    "I can't sleep well and I keep worrying about deadlines.",
    "What can I do to feel better?"
]

for msg in messages:
    print(f"\n👤 User: {msg}")
    response = manager.chat(
        user_id=user_id,
        session_id=session_id,
        user_message=msg
    )
    print(f"🤖 Assistant: {response}")

# End session
manager.end_session(user_id, session_id)
print("\n✅ Session ended")
```

Run it:
```bash
python test_chat.py
```

**Expected Output:**
```
👤 User: Hi, I've been feeling really stressed about work lately.
🤖 Assistant: I understand you're experiencing work-related stress. This is very common...

👤 User: I can't sleep well and I keep worrying about deadlines.
🤖 Assistant: Sleep difficulties and persistent worry about deadlines suggest anxiety...

👤 User: What can I do to feel better?
🤖 Assistant: Here are some evidence-based strategies you can try...

✅ Session ended
```

---

## Step 4: Explore Features (1 minute)

### Try with Memory

Run the conversation again with the same `user_id`. Notice how the system remembers previous conversations!

```python
# Continue from where we left off
session_id_2 = manager.start_session(user_id)

response = manager.chat(
    user_id=user_id,
    session_id=session_id_2,
    user_message="I tried the techniques you mentioned last time."
)

print(response)  # System will reference previous session!
```

### Try RAG Knowledge Retrieval

The system automatically retrieves relevant professional knowledge:

```python
response = manager.chat(
    user_id=user_id,
    session_id=session_id,
    user_message="What is cognitive behavioral therapy?"
)

# The response will include CBT techniques from the knowledge base
print(response)
```

---

## What Just Happened?

Behind the scenes, the system:

1. **Retrieved professional knowledge** about stress and anxiety from the psychological knowledge base
2. **Remembered your profile** (user_id, issues mentioned)
3. **Maintained conversation context** (working memory of last 10 turns)
4. **Generated a personalized response** using LLM + retrieved context
5. **Updated memory** after each turn
6. **Summarized the session** when you called `end_session()`

---

## Next Steps

### Explore Examples

Check out more examples in the `examples/` directory:

```bash
# Basic RAG chat
python examples/basic_rag_chat.py

# Multi-session chat (demonstrates memory)
python examples/multi_session_chat.py

# Add custom knowledge to the system
python examples/add_knowledge.py
```

### Run Evaluation Experiments

Reproduce the paper's experiments:

```bash
# Quick test (5 minutes)
python evaluation/scripts/run_quick_test.py

# Full comparison experiment
python examples/comparison_experiment.py
```

Results will be saved in `experiments/` and `evaluation/results/`.

### Customize the System

1. **Add your own knowledge**: Place `.txt` files in `data/psychological_knowledge/`
2. **Adjust parameters**: Edit `configs/config.yaml`
3. **Change system prompt**: Modify `dialogue.system_prompt` in config

See [Configuration Guide](configuration.md) for all options.

---

## Common Use Cases

### Use Case 1: Research on RAG Systems

```python
# Disable RAG to see baseline performance
manager = create_dialogue_manager_from_config(config)
manager.enable_rag = False

# Enable RAG
manager.enable_rag = True
```

### Use Case 2: Study Memory Systems

```python
# Disable memory
manager.enable_memory = False

# Enable only working memory
config['memory']['layers']['profile']['auto_update'] = False

# Enable full memory system
config['memory']['layers']['profile']['auto_update'] = True
```

### Use Case 3: Compare LLM Backends

```python
# Test with GPT-4
config['llm']['backend'] = 'api'
config['llm']['api']['model'] = 'gpt-4'

# Test with GPT-3.5
config['llm']['api']['model'] = 'gpt-3.5-turbo'

# Test with local Qwen2
config['llm']['backend'] = 'local'
```

---

## Troubleshooting Quick Start

### Issue: Import Error

**Error**: `ModuleNotFoundError: No module named 'dialogue'`

**Solution**: Make sure you're in the project root directory:
```bash
cd psychological_counseling_system
python test_chat.py
```

### Issue: OpenAI API Error

**Error**: `AuthenticationError`

**Solution**: Check your API key is set:
```bash
echo $OPENAI_API_KEY
```

### Issue: Model Download Failed

**Error**: `Cannot download model`

**Solution**: Try manual download:
```bash
wget https://huggingface.co/Qwen/Qwen2-7B-Instruct-GGUF/resolve/main/qwen2-7b-instruct-q4_k_m.gguf \
     -O models/models/qwen2-7b-instruct-q4_k_m.gguf
```

### Issue: Out of Memory

**Error**: `CUDA out of memory`

**Solution**: Reduce GPU layers in config:
```yaml
llm:
  local:
    n_gpu_layers: 10  # or 0 for CPU-only
```

---

## Configuration Cheat Sheet

Quick reference for common configurations:

```yaml
# Use GPT-4 API
llm:
  backend: 'api'
  api:
    model: 'gpt-4'

# Use local model with GPU
llm:
  backend: 'local'
  local:
    n_gpu_layers: 35

# Disable RAG
dialogue:
  generation:
    enable_rag: false

# Disable memory
dialogue:
  generation:
    enable_memory: false

# Increase working memory size
memory:
  layers:
    session:
      max_turns: 20

# More aggressive RAG retrieval
rag:
  retrieval:
    top_k: 10
    score_threshold: 0.3
```

---

## Interactive Quickstart Script

We provide an interactive script that guides you through setup:

```bash
python scripts/interactive_setup.py
```

This will:
1. Check your installation
2. Help you choose LLM backend
3. Test your configuration
4. Run a sample conversation

---

## Learning Path

**Beginner** (30 minutes):
1. ✅ This quickstart guide
2. Read [System Overview](../README.md)
3. Try `examples/basic_rag_chat.py`

**Intermediate** (2 hours):
1. Read [Architecture](architecture.md)
2. Try all examples in `examples/`
3. Run `comparison_experiment.py`

**Advanced** (1 day):
1. Read [Configuration Guide](configuration.md)
2. Read [Evaluation Guide](evaluation.md)
3. Modify and extend the system

---

## Getting Help

If you're stuck:

1. **Check documentation**: [docs/](.)
2. **Read examples**: [examples/](../examples/)
3. **Search issues**: [GitHub Issues](https://github.com/yourusername/psychological_counseling_system/issues)
4. **Ask questions**: Open a new issue

---

## What's Next?

Now that you have the system running, you can:

- 📖 **Learn more**: Read the [Architecture Documentation](architecture.md)
- 🔧 **Customize**: See the [Configuration Guide](configuration.md)
- 🔬 **Experiment**: Follow the [Evaluation Guide](evaluation.md)
- 💻 **Code**: Explore [Usage Examples](examples.md)
- 📊 **Analyze**: Review the [Paper Results](../experiments/)

---

**Congratulations!** 🎉 You've successfully set up and run your first psychological counseling conversation. Happy exploring!
