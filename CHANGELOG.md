# 📋 更新日志

## ✨ 2025-11-08 更新

### 重要改进：模型管理优化

根据你的建议，我们将本地模型的存储位置从系统目录 `/home/models` 改为**项目内的 `models/` 目录**。

### 🎯 主要变更

#### 1. 新增内容
- ✅ `models/` 目录 - 存放本地模型
- ✅ `models/README.md` - 模型下载和管理说明
- ✅ `download_model.sh` - 一键下载脚本
- ✅ `.gitignore` - 排除大文件和临时文件
- ✅ `MODEL_GUIDE.md` - 完整的模型管理指南

#### 2. 配置更新
- ✅ `configs/config.yaml` - 模型路径改为 `./models/tinyllama-*.gguf`
- ✅ `INSTALLATION.md` - 更新安装说明
- ✅ `docs/quickstart.md` - 更新快速入门指南
- ✅ `DELIVERY_SUMMARY.md` - 更新示例路径

### 📦 新的项目结构

```
psychological_counseling_system/
├── models/                    # ✨ 新增：本地模型目录
│   ├── README.md             # 模型说明
│   └── *.gguf               # 模型文件（下载后）
├── download_model.sh         # ✨ 新增：一键下载脚本
├── .gitignore               # ✨ 新增：Git忽略配置
├── MODEL_GUIDE.md           # ✨ 新增：模型管理指南
└── ... (其他文件保持不变)
```

### 🚀 使用变化

#### 之前（已废弃）
```bash
# 下载到系统目录
mkdir -p /home/models
cd /home/models
wget https://...

# 配置
model_path: '/home/models/xxx.gguf'
```

#### 现在（推荐）
```bash
# 方法1: 使用一键脚本
cd psychological_counseling_system
./download_model.sh

# 方法2: 手动下载到项目内
cd psychological_counseling_system/models
wget https://...

# 配置（相对路径）
model_path: './models/xxx.gguf'
```

### ✅ 优点

1. **更好的项目管理**
   - 所有项目文件在一个目录
   - 便于查看和管理
   
2. **易于迁移**
   - 直接复制整个项目即可
   - 不依赖系统其他位置的文件

3. **不污染系统**
   - 不在系统目录存放大文件
   - 卸载时直接删除项目目录即可

4. **团队协作友好**
   - 每个开发者管理自己的模型
   - 模型文件自动被git忽略

5. **符合最佳实践**
   - 项目自包含
   - 依赖明确

### 📝 迁移说明

如果你之前已经下载了模型到 `/home/models`：

```bash
# 移动到项目内（可选）
mv /home/models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf \
   psychological_counseling_system/models/

# 或者创建软链接
ln -s /home/models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf \
      psychological_counseling_system/models/
```

### 🔍 验证

下载新版本后，检查：

```bash
cd psychological_counseling_system

# 1. 检查models目录
ls -la models/

# 2. 检查配置文件
grep "model_path" configs/config.yaml

# 3. 检查下载脚本
ls -l download_model.sh

# 应该看到：
# models/README.md
# model_path: './models/...'
# -rwxr-xr-x ... download_model.sh
```

### 📖 相关文档

- **模型管理完整指南**: [MODEL_GUIDE.md](./MODEL_GUIDE.md)
- **模型目录说明**: [models/README.md](./models/README.md)
- **安装指南**: [INSTALLATION.md](./INSTALLATION.md)

---

## 其他说明

### 项目状态
- ✅ Phase 1: 基础RAG框架 - 100%完成
- ✅ Phase 2: 记忆系统 - 100%完成
- ⏳ Phase 3: 多模态情感识别 - 待开发
- ⏳ Phase 4: 强化学习优化 - 待开发

### 文件大小
- 项目代码: ~144KB
- 压缩包: 38KB (tar.gz) / 58KB (zip)
- 模型文件: 需要单独下载 (~600MB)

### 兼容性
- Python 3.10+
- Linux / macOS / Windows
- CUDA 12.1+ (可选，用于GPU加速)

---

**更新时间**: 2025-11-08  
**更新原因**: 用户建议改进模型管理方式  
**影响范围**: 配置文件、文档、新增脚本  
**向后兼容**: 是（仍支持绝对路径配置）  
