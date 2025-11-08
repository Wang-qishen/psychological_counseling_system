# 模型管理指南 📦

## ✅ 已更新：模型存放在项目内

所有本地模型现在存放在 **`models/`** 目录中，无需在系统其他位置下载。

## 📁 项目结构

```
psychological_counseling_system/
├── models/                          # ✨ 本地模型目录
│   ├── README.md                   # 模型说明
│   └── tinyllama-*.gguf           # 下载的模型文件
├── configs/
│   └── config.yaml                # 配置文件 (已更新路径)
├── download_model.sh              # ✨ 一键下载脚本
└── ...
```

## 🚀 快速下载模型

### 方法1: 使用一键脚本（最简单）

```bash
cd psychological_counseling_system
./download_model.sh
```

脚本会自动：
- ✅ 检查模型是否已存在
- ✅ 选择最佳下载工具（wget/curl）
- ✅ 显示下载进度
- ✅ 验证下载结果

### 方法2: 手动下载

```bash
cd psychological_counseling_system/models

# 使用wget
wget https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf

# 或使用curl
curl -L https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf -o tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf
```

### 方法3: 使用huggingface-cli（推荐，支持断点续传）

```bash
# 安装huggingface-hub
pip install huggingface-hub

# 下载模型
cd psychological_counseling_system/models
huggingface-cli download TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF \
  tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf \
  --local-dir . \
  --local-dir-use-symlinks False
```

## ⚙️ 配置说明

配置文件 `configs/config.yaml` 已更新：

```yaml
llm:
  backend: 'local'
  local:
    model_path: './models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf'  # ✅ 项目内路径
    n_gpu_layers: 35  # 使用GPU加速
```

## 📊 模型大小

- **TinyLlama-1.1B (Q4_K_M)**: ~600MB
- 预计下载时间: 1-5分钟（取决于网络速度）

## 🔄 切换模型

如果你想使用其他模型：

### 1. 下载到models目录

```bash
cd psychological_counseling_system/models

# 例如: 下载Mistral-7B
huggingface-cli download TheBloke/Mistral-7B-Instruct-v0.2-GGUF \
  mistral-7b-instruct-v0.2.Q4_K_M.gguf \
  --local-dir . \
  --local-dir-use-symlinks False
```

### 2. 更新配置

```yaml
llm:
  local:
    model_path: './models/mistral-7b-instruct-v0.2.Q4_K_M.gguf'
```

## 📝 推荐模型列表

### 适合你的A40 GPU

| 模型 | 大小 | VRAM需求 | 推荐用途 |
|------|------|----------|---------|
| TinyLlama-1.1B | 0.6GB | ~2GB | 快速测试 |
| Mistral-7B | 4.4GB | ~8GB | 平衡性能 |
| Llama-3-8B | 4.9GB | ~10GB | 更好质量 |
| Qwen2-7B | 4.5GB | ~9GB | 中文优化 |

### 下载命令参考

```bash
# Mistral-7B
huggingface-cli download TheBloke/Mistral-7B-Instruct-v0.2-GGUF \
  mistral-7b-instruct-v0.2.Q4_K_M.gguf --local-dir ./models --local-dir-use-symlinks False

# Llama-3-8B
huggingface-cli download QuantFactory/Meta-Llama-3-8B-Instruct-GGUF \
  Meta-Llama-3-8B-Instruct.Q4_K_M.gguf --local-dir ./models --local-dir-use-symlinks False

# Qwen2-7B (中文优化)
huggingface-cli download Qwen/Qwen2-7B-Instruct-GGUF \
  qwen2-7b-instruct-q4_k_m.gguf --local-dir ./models --local-dir-use-symlinks False
```

## 🗑️ 管理模型

### 查看已下载的模型

```bash
ls -lh models/*.gguf
```

### 删除不需要的模型

```bash
rm models/old_model.gguf
```

### 模型被.gitignore排除

所有 `*.gguf` 文件已自动排除在git追踪之外，不会被提交到仓库。

## ❓ 常见问题

### Q1: 下载速度慢怎么办？

**方案1**: 使用国内镜像
```bash
export HF_ENDPOINT=https://hf-mirror.com
huggingface-cli download ...
```

**方案2**: 使用代理
```bash
export https_proxy=http://your-proxy:port
wget ...
```

### Q2: 下载中断怎么办？

使用 `huggingface-cli` 支持断点续传：
```bash
huggingface-cli download ... --resume-download
```

或使用 `wget` 的 `-c` 参数：
```bash
wget -c https://...
```

### Q3: 如何验证模型完整性？

```bash
# 检查文件大小
ls -lh models/*.gguf

# TinyLlama应该约600MB
# 如果大小不对，重新下载
```

## 🎯 优点总结

✅ **便于管理**: 所有模型在项目内，清晰可见  
✅ **易于迁移**: 复制整个项目即可迁移  
✅ **不污染系统**: 不在系统其他位置存放大文件  
✅ **自动忽略**: git会自动忽略模型文件  
✅ **团队协作**: 每个开发者管理自己的模型  

---

**需要帮助?** 查看 `models/README.md` 获取更多信息。
