# 📦 新文档包使用说明

这个包包含了整理后的标准化文档，用于替换你项目中混乱的旧文档。

---

## 📋 包含内容

### 脚本文件（2个）
- `cleanup.sh` - 删除旧文档脚本
- `install_docs.sh` - 安装新文档脚本

### 根目录文档（4个）
- `README.md` - 主README（英文，开源标准格式）
- `README_zh.md` - 中文版README
- `INSTALLATION.md` - 详细安装指南
- `LICENSE` - MIT开源协议

### docs/ 目录文档（5个）
- `architecture.md` - 系统架构（对应论文第3节）
- `quickstart.md` - 5分钟快速开始
- `configuration.md` - 完整配置说明
- `evaluation.md` - 评估和实验指南
- `examples.md` - 代码示例

### 子模块README（2个）
- `evaluation/README.md` - 评估模块说明
- `models/README.md` - 模型下载指南

**总计：13个文档 + 2个脚本**

---

## 🚀 使用步骤

### 第一步：解压文件包

```bash
cd /path/to/download
tar -xzf new_docs_package.tar.gz
cd new_docs_package
```

### 第二步：修改目标路径（重要！）

编辑两个脚本中的目标路径：

**1. 编辑 `cleanup.sh`**
```bash
nano cleanup.sh
# 或
vim cleanup.sh
```

找到这一行：
```bash
ROOT_DIR="/cephfs/shared/pengyang/deform_test_pengyang/src/benchmark_qishen/other/vla/base/sw/psychological_counseling_system"
```

修改为你的实际项目路径。

**2. 编辑 `install_docs.sh`**
```bash
nano install_docs.sh
# 或
vim install_docs.sh
```

找到这一行：
```bash
TARGET_DIR="/cephfs/shared/pengyang/deform_test_pengyang/src/benchmark_qishen/other/vla/base/sw/psychological_counseling_system"
```

修改为你的实际项目路径。

### 第三步：清理旧文档（可选但推荐）

```bash
# 赋予执行权限
chmod +x cleanup.sh

# 运行清理脚本
bash cleanup.sh
```

这将删除：
- 8个开发文档
- 6个冗余文档
- 4个无关目录
- 打包文件

### 第四步：安装新文档

```bash
# 赋予执行权限
chmod +x install_docs.sh

# 运行安装脚本
bash install_docs.sh
```

这将：
1. 备份原有重要文档
2. 安装所有新文档
3. 创建备份目录

---

## 📂 最终目录结构

完成后，你的项目将有以下文档结构：

```
psychological_counseling_system/
├── README.md                    ⭐ 新：主文档
├── README_zh.md                 ⭐ 新：中文版
├── INSTALLATION.md              ⭐ 新：安装指南
├── LICENSE                      ⭐ 新：开源协议
├── requirements.txt             保留
│
├── docs/                        ⭐ 新：详细文档
│   ├── architecture.md
│   ├── quickstart.md
│   ├── configuration.md
│   ├── evaluation.md
│   └── examples.md
│
├── evaluation/                  保留
│   └── README.md                ⭐ 新：简化版
│
├── models/                      保留
│   └── README.md                ⭐ 新：模型指南
│
├── dialogue/                    保留（代码）
├── llm/                         保留（代码）
├── knowledge/                   保留（代码）
├── memory/                      保留（代码）
├── examples/                    保留（代码）
├── configs/                     保留（配置）
└── ...                          其他代码目录保留
```

---

## ✅ 验证安装

运行安装后，检查：

```bash
# 进入你的项目目录
cd /your/project/path

# 检查新文档是否存在
ls -l README.md README_zh.md INSTALLATION.md LICENSE
ls -l docs/
ls -l evaluation/README.md
ls -l models/README.md

# 查看备份
ls -l docs_backup_*/
```

---

## 📝 后续修改

### 修改作者信息

在以下文件中更新你的信息：

**README.md**:
```markdown
- **Author**: [Your Name]  # 修改这里
- **Email**: your.email@example.com  # 修改这里
```

**LICENSE**:
```
Copyright (c) 2024 [Your Name]  # 修改这里
```

**BibTeX引用**:
```bibtex
@article{yourname2024psychological,  # 修改这里
  author={Your Name and Collaborators},  # 修改这里
  ...
}
```

### 添加论文链接

在README.md中找到：
```markdown
[Paper]()  # 添加你的论文链接
```

---

## 🔧 故障排查

### 问题1：权限错误

```bash
# 如果出现 "Permission denied"
chmod +x cleanup.sh install_docs.sh
```

### 问题2：路径不存在

检查脚本中的路径是否正确：
```bash
# 确认项目路径
ls /your/project/path/dialogue
ls /your/project/path/llm
```

### 问题3：备份失败

手动创建备份：
```bash
mkdir -p backup_$(date +%Y%m%d)
cp README.md backup_*/
cp INSTALLATION.md backup_*/
```

---

## 📊 对比：前 vs 后

### 之前（混乱）
- ❌ 40个Markdown文档
- ❌ 多个README、多个GUIDE
- ❌ 开发文档混在一起
- ❌ 无关目录（chatdatadoc等）
- ❌ 没有开源协议

### 之后（清晰）
- ✅ 13个核心文档
- ✅ 单一主README
- ✅ 专业的开源项目结构
- ✅ 清晰的文档层次
- ✅ MIT开源协议

---

## 🎯 使用新文档

安装完成后：

1. **查看主文档**
   ```bash
   cat README.md  # 或用编辑器打开
   ```

2. **快速开始**
   ```bash
   # 按照 docs/quickstart.md 的指导
   ```

3. **了解架构**
   ```bash
   # 阅读 docs/architecture.md
   ```

4. **运行实验**
   ```bash
   # 参考 docs/evaluation.md
   ```

---

## 💡 提示

1. **不要删除备份**：至少保留一周，确认新文档没问题后再删除
2. **逐步更新**：先安装文档，测试没问题后再清理旧文档
3. **版本控制**：如果使用git，记得commit新文档

---

## 📞 需要帮助？

如果遇到问题：

1. 检查脚本中的路径是否正确
2. 确认有写入权限
3. 查看备份目录中的原始文档

---

## ✨ 完成！

按照以上步骤，你的项目文档将从混乱变得清晰专业，可以直接开源发布！

**下一步：**
1. 修改README中的作者信息
2. 添加论文链接
3. 测试所有文档链接
4. 发布到GitHub！

---

**祝你开源顺利！** 🎉
