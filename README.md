# Psychological Counseling Dialogue System

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **A modular psychological counseling system with dual-knowledge-base RAG and three-layer memory**

[中文文档](README_zh.md) 

---

## 📝 Overview

This repository contains the implementation of our paper:

**"Intelligent Psychological Counseling Dialogue System Based on Dual-Knowledge-Base RAG and Three-Layer Memory"**

The system addresses key challenges in AI-powered mental health support:
- **Professional accuracy** through Retrieval-Augmented Generation (RAG)
- **Long-term personalization** with a three-layer memory system
- **Privacy protection** via local model deployment options

### Key Features

🔬 **Dual Knowledge Base Architecture**
- Separated professional psychology knowledge (CBT, anxiety management, etc.)
- Individual user profile knowledge base
- Differentiated retrieval strategies for balanced professionalism and personalization

🧠 **Three-Layer Memory System**
- **Working Memory**: Current session context (last 10 turns)
- **Short-term Memory**: Session-level summaries (last 20 sessions)
- **Long-term Memory**: Persistent user profiles and cross-session trends

🛠️ **Modular & Flexible Design**
- Support for both local models (Qwen2-7B) and API models (GPT-4)
- Easy configuration via YAML files
- Independent module testing and replacement

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/Wang-qishen/psychological_counseling_system.git
cd psychological_counseling_system

# Install dependencies
pip install -r requirements.txt

# Download embedding model (first time only)
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')"
```

### Basic Usage

```python
from dialogue import create_dialogue_manager_from_config
import yaml

# Load configuration
with open('configs/config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Create dialogue manager
manager = create_dialogue_manager_from_config(config)

# Start a conversation
user_id = "user001"
session_id = manager.start_session(user_id)

# Chat
response = manager.chat(
    user_id=user_id,
    session_id=session_id,
    user_message="I've been feeling very anxious lately..."
)

print(response)
```

### Run Evaluation Experiments

```bash
# Quick test (5 minutes)
python evaluation/scripts/run_quick_test.py

# Full comparison experiment (reproduces paper results)
python examples/comparison_experiment.py
```

See [Quick Start Guide](docs/quickstart.md) for more details.

---

## 📊 System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Interface                           │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Dialogue Manager                            │
│  Orchestrates modules · Context building · Prompt engineering    │
└──────┬───────────────────┬────────────────────┬─────────────────┘
       │                   │                    │
       ▼                   ▼                    ▼
┌─────────────┐   ┌──────────────────┐   ┌────────────────────┐
│  LLM Layer  │   │   RAG Layer       │   │   Memory Layer     │
│             │   │                   │   │                    │
│ • Qwen2-7B  │   │ • Professional KB │   │ • Working Memory   │
│ • GPT-4     │   │ • Personal KB     │   │ • Short-term Memory│
│             │   │                   │   │ • Long-term Memory │
└─────────────┘   └──────────────────┘   └────────────────────┘
```

See [Architecture Documentation](docs/architecture.md) for detailed design.

---

## 📂 Project Structure

```
psychological_counseling_system/
├── README.md                    # This file
├── INSTALLATION.md              # Detailed installation guide
├── requirements.txt             # Python dependencies
│
├── configs/                     # Configuration files
│   └── config.yaml              # Main configuration
│
├── dialogue/                    # Dialogue management module
│   └── manager.py               # Core dialogue manager
│
├── llm/                         # LLM layer (local + API)
│   ├── local_llm.py             # Local model (llama.cpp)
│   └── openai_llm.py            # OpenAI API
│
├── knowledge/                   # RAG layer
│   ├── chroma_kb.py             # ChromaDB knowledge base
│   └── rag_manager.py           # RAG manager
│
├── memory/                      # Memory system
│   ├── models.py                # Memory data models
│   ├── storage.py               # Storage backend
│   └── manager.py               # Memory manager
│
├── evaluation/                  # Evaluation framework
│   ├── configs/                 # Evaluation configs
│   ├── datasets/                # Dataset loaders
│   ├── metrics/                 # Evaluation metrics
│   └── scripts/                 # Evaluation scripts
│
├── examples/                    # Usage examples
│   ├── basic_rag_chat.py        # Basic RAG chat
│   ├── comparison_experiment.py # Comparison experiment
│   └── evaluation_examples.py   # Evaluation examples
│
├── experiments/                 # Experiment results
│   ├── detailed_comparison.md   # Comparison results
│   └── response_examples.md     # Response examples
│
├── docs/                        # Documentation
│   ├── architecture.md          # System architecture
│   ├── quickstart.md            # Quick start guide
│   ├── configuration.md         # Configuration guide
│   ├── evaluation.md            # Evaluation guide
│   └── examples.md              # Usage examples
│
└── models/                      # Model storage
    └── README.md                # Model download guide
```

---

## 📚 Documentation

- [Installation Guide](INSTALLATION.md) - Detailed setup instructions
- [Quick Start](docs/quickstart.md) - Get started in 5 minutes
- [Architecture](docs/architecture.md) - System design and components
- [Configuration](docs/configuration.md) - Configuration parameters
- [Evaluation Guide](docs/evaluation.md) - How to reproduce experiments
- [Usage Examples](docs/examples.md) - Code examples

---

## 🔬 Reproducing Paper Results

Our paper presents three main experiments:

### 1. Comparison Experiment

Compare three configurations: Bare LLM, LLM+RAG, and Full System

```bash
python examples/comparison_experiment.py
```

Results will be saved to `experiments/` directory.

### 2. Case Study

Run specific counseling scenarios:

```bash
python examples/case_study.py --scenario anxiety
```

### 3. User Experience Evaluation

See [Evaluation Guide](docs/evaluation.md) for details.

---

## 🛠️ Configuration

The system is highly configurable via `configs/config.yaml`:

```yaml
llm:
  backend: 'local'  # 'local' or 'api'
  local:
    model_path: 'models/qwen2-7b-instruct-q4_k_m.gguf'
  api:
    provider: 'openai'
    model: 'gpt-4o-mini'

rag:
  retrieval:
    top_k: 5
    score_threshold: 0.5

memory:
  layers:
    session:
      max_turns: 10
    profile:
      auto_update: true
```

See [Configuration Guide](docs/configuration.md) for all options.

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

