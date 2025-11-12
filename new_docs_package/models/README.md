# Models Directory

This directory stores local language models for the system.

---

## Supported Models

### Qwen2-7B-Instruct (Recommended)

**Quantized versions** for efficient inference:

- **Q4_K_M** (Recommended): ~4GB, good balance
- **Q5_K_M**: ~5GB, better quality
- **Q8_0**: ~7GB, highest quality

---

## Download Methods

### Method 1: Automated Script (Recommended)

```bash
# From project root
bash download_model.sh
```

This downloads Qwen2-7B-Instruct Q4_K_M (~4GB) to `models/models/`.

### Method 2: Manual Download

```bash
# Create directory
mkdir -p models/models

# Download from Hugging Face
wget https://huggingface.co/Qwen/Qwen2-7B-Instruct-GGUF/resolve/main/qwen2-7b-instruct-q4_k_m.gguf \
     -O models/models/qwen2-7b-instruct-q4_k_m.gguf
```

### Method 3: Using huggingface-cli

```bash
pip install huggingface_hub

huggingface-cli download \
  Qwen/Qwen2-7B-Instruct-GGUF \
  qwen2-7b-instruct-q4_k_m.gguf \
  --local-dir models/models
```

---

## Directory Structure

```
models/
├── README.md              # This file
└── models/                # Model files
    └── qwen2-7b-instruct-q4_k_m.gguf  # Downloaded model
```

---

## Model Comparison

| Model | Size | Quality | Speed | Memory |
|-------|------|---------|-------|--------|
| Q4_K_M | 4GB | Good | Fast | 6GB RAM |
| Q5_K_M | 5GB | Better | Medium | 7GB RAM |
| Q8_0 | 7GB | Best | Slow | 9GB RAM |

### Which to Choose?

- **Limited RAM** (<8GB): Q4_K_M
- **Balanced** (8-16GB): Q5_K_M
- **Best Quality** (>16GB): Q8_0

---

## GPU Acceleration

### NVIDIA GPU (CUDA)

Set in `configs/config.yaml`:

```yaml
llm:
  local:
    n_gpu_layers: 35  # Offload all layers
```

**VRAM Requirements:**
- Q4_K_M: ~4GB VRAM
- Q5_K_M: ~5GB VRAM
- Q8_0: ~7GB VRAM

### CPU Only

```yaml
llm:
  local:
    n_gpu_layers: 0  # Use CPU only
```

---

## Alternative Models

### Other Qwen2 Variants

```bash
# Qwen2-1.5B (smaller, faster)
wget https://huggingface.co/Qwen/Qwen2-1.5B-Instruct-GGUF/resolve/main/qwen2-1_5b-instruct-q4_k_m.gguf

# Qwen2-14B (larger, better)
wget https://huggingface.co/Qwen/Qwen2-14B-Instruct-GGUF/resolve/main/qwen2-14b-instruct-q4_k_m.gguf
```

### Other Model Families

Compatible GGUF models:
- **Llama 3** (English-focused)
- **Mistral 7B** (Good general model)
- **Yi-6B** (Chinese-focused)

To use, update `configs/config.yaml`:

```yaml
llm:
  local:
    model_path: 'models/models/your-model.gguf'
```

---

## Verify Download

```bash
# Check file size
ls -lh models/models/

# Test loading
python -c "from llm import LocalLLM; llm = LocalLLM({'model_path': 'models/models/qwen2-7b-instruct-q4_k_m.gguf', 'n_ctx': 2048}); print('✓ Model loaded successfully')"
```

---

## Troubleshooting

### Issue: Download Failed

**Solution 1**: Try alternative mirror (China users)
```bash
export HF_ENDPOINT=https://hf-mirror.com
bash download_model.sh
```

**Solution 2**: Manual download from [Hugging Face](https://huggingface.co/Qwen/Qwen2-7B-Instruct-GGUF/tree/main)

### Issue: Model Not Found

**Error**: `FileNotFoundError: models/models/qwen2-7b-instruct-q4_k_m.gguf`

**Solution**: Check file exists
```bash
ls models/models/
```

### Issue: Out of Memory

**Error**: `RuntimeError: failed to allocate memory`

**Solution 1**: Reduce GPU layers
```yaml
n_gpu_layers: 20  # Instead of 35
```

**Solution 2**: Use smaller model
```bash
# Download Q4_K_M if you have Q5/Q8
```

---

## License

Models have their own licenses. Please check:
- Qwen2: Apache 2.0
- Check model card on Hugging Face for specific terms

---

## Further Reading

- [Installation Guide](../INSTALLATION.md) - Setup instructions
- [Configuration Guide](../docs/configuration.md) - Configure models
- [llama.cpp](https://github.com/ggerganov/llama.cpp) - Inference engine

---

**Questions?** See [Troubleshooting](../INSTALLATION.md#troubleshooting) or open an issue.
