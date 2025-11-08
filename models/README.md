# Local Models Directory

This directory stores locally downloaded models.

## Download TinyLlama Model

```bash
cd models
wget https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf
```

Or use huggingface-cli:

```bash
pip install huggingface-hub
cd models
huggingface-cli download TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf --local-dir . --local-dir-use-symlinks False
```

## Model Files

After download, you should have:
- tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf (约 600MB)

## Other Recommended Models

### Larger Models (if you have enough VRAM)
- Mistral-7B: `TheBloke/Mistral-7B-Instruct-v0.2-GGUF`
- Llama-3-8B: `TheBloke/Meta-Llama-3-8B-Instruct-GGUF`

### Chinese Models
- Qwen2-7B: `Qwen/Qwen2-7B-Instruct-GGUF`
- ChatGLM3-6B: `THUDM/chatglm3-6b-GGUF`

## Note

Models are automatically gitignored (see .gitignore)

