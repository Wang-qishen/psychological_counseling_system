# Usage Examples

Practical code examples for using the Psychological Counseling System.

---

## Table of Contents

- [Basic Chat](#basic-chat)
- [RAG Usage](#rag-usage)
- [Memory System](#memory-system)
- [Configuration](#configuration)
- [Advanced Usage](#advanced-usage)

---

## Basic Chat

### Example 1: Simple Conversation

```python
from dialogue import create_dialogue_manager_from_config
import yaml

# Load config
with open('configs/config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Create manager
manager = create_dialogue_manager_from_config(config)

# Start session
user_id = "user001"
session_id = manager.start_session(user_id)

# Chat
response = manager.chat(
    user_id=user_id,
    session_id=session_id,
    user_message="I'm feeling very anxious about my job interview tomorrow."
)

print(response)

# End session
manager.end_session(user_id, session_id)
```

### Example 2: Multi-Turn Conversation

```python
messages = [
    "I've been feeling really stressed at work.",
    "My manager is very demanding and I can't keep up.",
    "I'm thinking about quitting but I need the money.",
    "What should I do?"
]

for msg in messages:
    response = manager.chat(
        user_id=user_id,
        session_id=session_id,
        user_message=msg
    )
    print(f"User: {msg}")
    print(f"Assistant: {response}\n")
```

### Example 3: Multiple Sessions

```python
# First session
session1 = manager.start_session(user_id)
manager.chat(user_id, session1, "I'm having trouble sleeping...")
manager.end_session(user_id, session1)

# Second session (next day)
session2 = manager.start_session(user_id)
manager.chat(user_id, session2, "I tried your suggestions from yesterday...")
# System will remember previous session!
manager.end_session(user_id, session2)
```

---

## RAG Usage

### Example 4: Adding Knowledge

```python
from knowledge import create_rag_manager_from_config

# Create RAG manager
rag_manager = create_rag_manager_from_config(config)

# Add professional knowledge
with open('data/cbt_techniques.txt', 'r') as f:
    content = f.read()

rag_manager.add_professional_knowledge(
    content=content,
    metadata={'source': 'CBT Manual', 'topic': 'anxiety'}
)

# Add user information
rag_manager.add_user_knowledge(
    user_id="user001",
    content="User is a 28-year-old software engineer with work-related stress.",
    metadata={'type': 'profile'}
)
```

### Example 5: Manual Retrieval

```python
# Retrieve professional knowledge
results = rag_manager.retrieve(
    query="How to manage anxiety?",
    user_id="user001"
)

print("Professional knowledge:")
print(results.professional_context)

print("\nUser-specific info:")
print(results.personal_context)
```

### Example 6: Comparing With/Without RAG

```python
# Without RAG
config_no_rag = config.copy()
config_no_rag['dialogue']['generation']['enable_rag'] = False
manager_no_rag = create_dialogue_manager_from_config(config_no_rag)

# With RAG
manager_rag = create_dialogue_manager_from_config(config)

query = "What is cognitive behavioral therapy?"

response_no_rag = manager_no_rag.chat(user_id, session_id, query)
response_rag = manager_rag.chat(user_id, session_id, query)

print("Without RAG:", response_no_rag)
print("\nWith RAG:", response_rag)
```

---

## Memory System

### Example 7: Accessing Memory

```python
from memory import create_memory_manager_from_config

memory_manager = create_memory_manager_from_config(config)

# Get user memory
user_memory = memory_manager.get_user_memory(user_id)

print("User profile:", user_memory.profile)
print("Number of sessions:", len(user_memory.sessions))
print("Total turns:", sum(len(s.turns) for s in user_memory.sessions))
```

### Example 8: Analyzing Memory

```python
# Get memory context
memory_context = memory_manager.retrieve_relevant_memory(
    user_id=user_id,
    current_context="feeling anxious today"
)

print("Profile:", memory_context['profile'])
print("Recent sessions:", memory_context['recent_sessions'])
print("Emotion trend:", memory_context['emotion_trend'])
```

### Example 9: Manual Memory Management

```python
# Manually add a turn
memory_manager.add_turn(
    user_id=user_id,
    session_id=session_id,
    user_message="I feel better today",
    assistant_message="That's great to hear!",
    emotion={'happiness': 0.8, 'anxiety': 0.2}
)

# Update user profile
memory_manager.update_user_profile(
    user_id=user_id,
    updates={
        'main_issues': ['work_stress', 'sleep_issues'],
        'occupation': 'software engineer'
    }
)

# Generate session summary
summary = memory_manager.summarize_session(user_id, session_id)
print("Session summary:", summary)
```

---

## Configuration

### Example 10: Programmatic Configuration

```python
# Create custom config
custom_config = {
    'llm': {
        'backend': 'api',
        'api': {
            'provider': 'openai',
            'model': 'gpt-4',
            'temperature': 0.8
        }
    },
    'rag': {
        'retrieval': {
            'top_k': 10,
            'score_threshold': 0.3
        }
    },
    'memory': {
        'layers': {
            'session': {'max_turns': 15}
        }
    }
}

manager = create_dialogue_manager_from_config(custom_config)
```

### Example 11: Environment-Based Config

```python
import os

# Load different config based on environment
env = os.getenv('ENV', 'dev')
config_file = f'configs/config_{env}.yaml'

with open(config_file, 'r') as f:
    config = yaml.safe_load(f)

manager = create_dialogue_manager_from_config(config)
```

### Example 12: Runtime Configuration Changes

```python
# Change LLM temperature mid-session
manager.llm.temperature = 0.9

# Toggle RAG
manager.enable_rag = False

# Toggle memory
manager.enable_memory = False
```

---

## Advanced Usage

### Example 13: Custom System Prompt

```python
custom_prompt = """
You are a specialized anxiety counselor. Focus on:
- Cognitive restructuring techniques
- Breathing exercises
- Exposure therapy principles

Be concise and actionable.
"""

config['dialogue']['system_prompt'] = custom_prompt
manager = create_dialogue_manager_from_config(config)
```

### Example 14: Streaming Responses

```python
# For OpenAI API backend
config['llm']['api']['stream'] = True

manager = create_dialogue_manager_from_config(config)

for chunk in manager.chat_stream(user_id, session_id, "Tell me about CBT"):
    print(chunk, end='', flush=True)
```

### Example 15: Batch Processing

```python
# Process multiple users
user_ids = ['user001', 'user002', 'user003']
messages = [
    "I feel anxious",
    "I can't sleep",
    "I'm stressed at work"
]

results = []
for user_id, message in zip(user_ids, messages):
    session_id = manager.start_session(user_id)
    response = manager.chat(user_id, session_id, message)
    results.append({'user_id': user_id, 'response': response})
    manager.end_session(user_id, session_id)

print(results)
```

### Example 16: Custom Evaluation

```python
from evaluation.metrics import ClinicalMetrics

metrics = ClinicalMetrics(manager.llm)

# Evaluate response
response = manager.chat(user_id, session_id, "I feel depressed")

scores = {
    'professionalism': metrics.evaluate_professionalism(response),
    'empathy': metrics.evaluate_empathy(response),
    'safety': metrics.check_safety(response)
}

print("Evaluation scores:", scores)
```

### Example 17: Export Conversation History

```python
# Export all conversations for a user
user_memory = memory_manager.get_user_memory(user_id)

# Convert to JSON
import json

history = {
    'user_id': user_id,
    'profile': user_memory.profile,
    'sessions': [
        {
            'session_id': s.session_id,
            'date': s.start_time.isoformat(),
            'turns': [
                {
                    'user': t.user_message,
                    'assistant': t.assistant_message
                }
                for t in s.turns
            ]
        }
        for s in user_memory.sessions
    ]
}

with open(f'exports/{user_id}_history.json', 'w') as f:
    json.dump(history, f, indent=2)
```

### Example 18: A/B Testing

```python
# Test two different configurations
configs = {
    'config_a': config_with_rag,
    'config_b': config_without_rag
}

results = {}
for name, cfg in configs.items():
    manager = create_dialogue_manager_from_config(cfg)
    session_id = manager.start_session(user_id)
    response = manager.chat(user_id, session_id, test_message)
    results[name] = response

# Compare
print("Config A:", results['config_a'])
print("Config B:", results['config_b'])
```

### Example 19: Error Handling

```python
from llm.base import LLMError
from knowledge.base import KnowledgeBaseError

try:
    response = manager.chat(user_id, session_id, message)
except LLMError as e:
    print(f"LLM error: {e}")
    # Fallback to simpler response
    response = "I'm having technical difficulties. Please try again."
except KnowledgeBaseError as e:
    print(f"RAG error: {e}")
    # Disable RAG and retry
    manager.enable_rag = False
    response = manager.chat(user_id, session_id, message)
except Exception as e:
    print(f"Unexpected error: {e}")
    response = "Something went wrong. Please contact support."
```

### Example 20: Integration with Web Framework

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

# Initialize system
with open('configs/config.yaml', 'r') as f:
    config = yaml.safe_load(f)
manager = create_dialogue_manager_from_config(config)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_id = data['user_id']
    session_id = data.get('session_id')
    message = data['message']
    
    if not session_id:
        session_id = manager.start_session(user_id)
    
    response = manager.chat(user_id, session_id, message)
    
    return jsonify({
        'session_id': session_id,
        'response': response
    })

@app.route('/end_session', methods=['POST'])
def end_session():
    data = request.json
    manager.end_session(data['user_id'], data['session_id'])
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)
```

---

## Example Scripts

All examples above are available as standalone scripts in `examples/`:

```bash
# Basic chat
python examples/basic_chat.py

# RAG demo
python examples/rag_demo.py

# Memory demo
python examples/memory_demo.py

# Comparison experiment
python examples/comparison_experiment.py

# Web server
python examples/web_server.py
```

---

## Interactive Examples

### Jupyter Notebook

See `examples/notebooks/` for interactive examples:

- `01_basic_usage.ipynb` - Basic system usage
- `02_rag_exploration.ipynb` - RAG deep dive
- `03_memory_analysis.ipynb` - Memory system analysis
- `04_evaluation.ipynb` - Evaluation examples

### CLI Tool

```bash
# Interactive chat
python -m dialogue.cli

# With specific config
python -m dialogue.cli --config configs/config_custom.yaml
```

---

## Testing Examples

### Unit Tests

```python
import pytest
from dialogue import DialogueManager

def test_chat():
    manager = create_test_manager()
    response = manager.chat("test_user", "test_session", "Hello")
    assert len(response) > 0
    assert "hello" in response.lower() or "hi" in response.lower()

def test_memory():
    manager = create_test_manager()
    session_id = manager.start_session("test_user")
    
    # First message
    manager.chat("test_user", session_id, "I'm anxious")
    
    # Second message should reference first
    response = manager.chat("test_user", session_id, "Still feeling the same")
    assert "anxious" in response.lower()
```

---

## Further Reading

- [Architecture](architecture.md) - System design
- [Configuration](configuration.md) - All configuration options
- [Evaluation](evaluation.md) - Evaluation guide

---

**Ready to code?** Start with Example 1 and work your way through!
