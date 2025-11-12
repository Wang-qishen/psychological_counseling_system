# 🚀 快速开始指南

## 最简单的方式（推荐）

在你的Linux服务器上执行以下命令：

```bash
# 1. 赋予脚本执行权限（如果还没有）
chmod +x run.sh

# 2. 运行一键脚本
./run.sh
```

这个脚本会自动：
- ✅ 创建conda环境（如果不存在）
- ✅ 安装所有依赖
- ✅ 生成高质量图片
- ✅ 显示生成结果

---

## 手动操作步骤

如果自动脚本出现问题，可以手动执行：

### 步骤1: 创建环境
```bash
conda env create -f environment.yml
conda activate paper-diagram
```

### 步骤2: 生成图片
```bash
python generate_architecture.py
```

### 步骤3: 查看结果
```bash
ls -lh architecture_diagram.*
```

---

## 📂 文件说明

| 文件名 | 用途 |
|--------|------|
| `environment.yml` | conda环境配置文件 |
| `generate_architecture.py` | 主程序脚本（2900+行） |
| `run.sh` | 一键运行脚本 |
| `README.md` | 详细使用文档 |
| `QUICKSTART.md` | 本文件（快速开始） |

---

## ⚠️ 常见问题

### Q: conda命令找不到？
**A:** 执行 `conda init bash` 然后 `source ~/.bashrc`

### Q: 中文显示为方块？
**A:** 安装中文字体：
```bash
sudo apt-get install fonts-wqy-microhei
rm -rf ~/.cache/matplotlib
```

### Q: 想修改图片样式？
**A:** 编辑 `generate_architecture.py` 中的 `COLORS` 字典

---

## 💡 使用建议

### 1. 论文投稿
- 使用 **PDF格式**（矢量图，无损缩放）
- 分辨率设置为 **300-600 DPI**

### 2. 毕业论文
- Word: 使用 **PNG格式**
- LaTeX: 使用 **PDF格式**

### 3. 演示文稿
- PowerPoint: 使用 **PNG格式** (300 DPI即可)

---

## 📞 需要更多帮助？

查看完整文档：`README.md`
