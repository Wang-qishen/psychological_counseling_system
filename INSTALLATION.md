# Installation Guide

This guide covers the installation and setup of the Psychological Counseling System.

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation Steps](#installation-steps)
- [Configuration](#configuration)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

### System Requirements

- **Operating System**: Linux, macOS, or Windows
- **Python**: 3.8 or higher
- **Memory**: At least 8GB RAM (16GB recommended for local models)
- **Storage**: At least 10GB free space

### Optional: GPU Support

For faster inference with local models:
- **CUDA**: 11.8 or higher (NVIDIA GPUs)
- **GPU Memory**: At least 6GB VRAM for Qwen2-7B

---

## Installation Steps

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/psychological_counseling_system.git
cd psychological_counseling_system
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Using venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Or using conda
conda create -n psych_counsel python=3.8
conda activate psych_counsel
```

### Step 3: Install Dependencies

```bash
# Install core dependencies
pip install -r requirements.txt
```

**requirements.txt** includes:
```
transformers>=4.36.0
torch>=2.0.0
chromadb>=0.4.0
sentence-transformers>=2.2.0
pyyaml>=6.0
pydantic>=2.0.0
llama-cpp-python>=0.2.0
openai>=1.0.0
numpy>=1.24.0
pandas>=2.0.0
matplotlib>=3.7.0
pytest>=7.4.0
```

### Step 4: Install PyTorch with GPU Support (Optional)

If you have an NVIDIA GPU and want to use CUDA:

```bash
# For CUDA 11.8
pip install torch --index-url https://download.pytorch.org/whl/cu118

# For CUDA 12.1
pip install torch --index-url https://download.pytorch.org/whl/cu121
```

### Step 5: Download Models

#### A. Embedding Model (Required)

The embedding model will be downloaded automatically on first use, or you can download it manually:

```bash
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')"
```

#### B. Local LLM (Optional)

If you want to use a local model (Qwen2-7B):

1. Download the quantized model:
   ```bash
   # Create models directory
   mkdir -p models/models
   
   # Download Qwen2-7B-Instruct Q4_K_M quantized model
   wget https://huggingface.co/Qwen/Qwen2-7B-Instruct-GGUF/resolve/main/qwen2-7b-instruct-q4_k_m.gguf \
        -O models/models/qwen2-7b-instruct-q4_k_m.gguf
   ```

2. Or use the provided download script:
   ```bash
   bash download_model.sh
   ```

See [Model Guide](models/README.md) for alternative download methods.

---

## Configuration

### Step 1: Copy Configuration Template

```bash
# Configuration file is already in configs/
cp configs/config.yaml configs/config_custom.yaml  # Optional: create custom config
```

### Step 2: Configure LLM Backend

Edit `configs/config.yaml`:

#### Option A: Use Local Model (Free, Private)

```yaml
llm:
  backend: 'local'
  local:
    model_path: 'models/models/qwen2-7b-instruct-q4_k_m.gguf'
    n_ctx: 4096
    n_threads: 8
    n_gpu_layers: 35  # Set to 0 if no GPU
    temperature: 0.7
    max_tokens: 2000
```

#### Option B: Use OpenAI API (Faster, Costs Money)

```yaml
llm:
  backend: 'api'
  api:
    provider: 'openai'
    model: 'gpt-4o-mini'  # or 'gpt-4'
    temperature: 0.7
    max_tokens: 2000
    api_key_env: 'OPENAI_API_KEY'
```

Then set your API key:
```bash
export OPENAI_API_KEY='your-api-key-here'
```

### Step 3: Configure Other Settings

You can also adjust:
- RAG retrieval parameters (`rag.retrieval.top_k`, etc.)
- Memory system settings (`memory.layers`, etc.)
- Dialogue settings

See [Configuration Guide](docs/configuration.md) for all options.

---

## Verification

### Test 1: Import Check

```bash
python -c "from dialogue import create_dialogue_manager_from_config; print('✓ Import successful')"
```

### Test 2: Embedding Model Check

```bash
python -c "from sentence_transformers import SentenceTransformer; m = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2'); print('✓ Embedding model loaded')"
```

### Test 3: Quick System Test

```bash
python evaluation/scripts/run_quick_test.py
```

This runs a quick evaluation test (takes ~5 minutes). If it completes successfully, your installation is working!

### Test 4: Basic Chat Test

```python
# test_basic.py
from dialogue import create_dialogue_manager_from_config
import yaml

with open('configs/config.yaml', 'r') as f:
    config = yaml.safe_load(f)

manager = create_dialogue_manager_from_config(config)
user_id = "test_user"
session_id = manager.start_session(user_id)

response = manager.chat(
    user_id=user_id,
    session_id=session_id,
    user_message="Hello, I'm feeling anxious today."
)

print("System response:", response)
```

Run:
```bash
python test_basic.py
```

---

## Troubleshooting

### Issue 1: CUDA Out of Memory

**Symptom**: `RuntimeError: CUDA out of memory`

**Solutions**:
1. Reduce `n_gpu_layers` in config:
   ```yaml
   n_gpu_layers: 20  # or lower
   ```
2. Use a smaller model
3. Use CPU-only mode:
   ```yaml
   n_gpu_layers: 0
   ```

### Issue 2: llama-cpp-python Installation Failed

**Symptom**: Error during `pip install llama-cpp-python`

**Solutions**:

For CPU-only:
```bash
pip install llama-cpp-python --no-cache-dir
```

For CUDA support:
```bash
CMAKE_ARGS="-DLLAMA_CUBLAS=on" pip install llama-cpp-python --no-cache-dir
```

For Metal (macOS):
```bash
CMAKE_ARGS="-DLLAMA_METAL=on" pip install llama-cpp-python --no-cache-dir
```

### Issue 3: ChromaDB Installation Failed

**Symptom**: Error installing ChromaDB

**Solution**:
```bash
pip install chromadb==0.4.22  # Use specific version
```

### Issue 4: Embedding Model Download Slow

**Symptom**: Downloading embedding model is very slow

**Solutions**:
1. Use a mirror (China users):
   ```bash
   export HF_ENDPOINT=https://hf-mirror.com
   ```
2. Download manually from [Hugging Face](https://huggingface.co/sentence-transformers/paraphrase-multilingual-mpnet-base-v2)

### Issue 5: OpenAI API Key Not Working

**Symptom**: `AuthenticationError` when using OpenAI API

**Solutions**:
1. Check your API key is valid
2. Ensure environment variable is set:
   ```bash
   echo $OPENAI_API_KEY
   ```
3. Try setting it in Python:
   ```python
   import os
   os.environ['OPENAI_API_KEY'] = 'your-key'
   ```

### Issue 6: Import Error

**Symptom**: `ModuleNotFoundError` or `ImportError`

**Solutions**:
1. Ensure you're in the project root directory
2. Check virtual environment is activated
3. Reinstall dependencies:
   ```bash
   pip install -r requirements.txt --force-reinstall
   ```

---

## Directory Setup

After installation, your directory should look like this:

```
psychological_counseling_system/
├── configs/
│   └── config.yaml          ✓ Configuration file
├── models/
│   └── models/
│       └── qwen2-7b-instruct-q4_k_m.gguf  ✓ Downloaded model (if using local)
├── data/
│   ├── vector_db/           ✓ Created automatically on first run
│   └── memory_db/           ✓ Created automatically on first run
├── logs/                    ✓ Created automatically
└── cache/                   ✓ Created automatically
```

---

## Next Steps

Now that installation is complete:

1. **Read the Quick Start Guide**: [docs/quickstart.md](docs/quickstart.md)
2. **Explore Examples**: Check `examples/` directory
3. **Run Experiments**: Try `python examples/comparison_experiment.py`
4. **Read Documentation**: See [docs/](docs/) for detailed guides

---

## Getting Help

If you encounter issues not covered here:

1. Check [GitHub Issues](https://github.com/yourusername/psychological_counseling_system/issues)
2. Read the [FAQ](docs/faq.md)
3. Open a new issue with:
   - Your operating system
   - Python version
   - Error message
   - Steps to reproduce

---

## Optional: Development Setup

If you want to contribute or develop:

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run tests
pytest tests/
```

---

**Congratulations!** 🎉 You're all set up. Happy counseling!
