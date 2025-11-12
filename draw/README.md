# 论文架构图生成工具

基于Python自动生成高质量学术论文配图的工具。

## 📋 目录
- [环境配置](#环境配置)
- [快速开始](#快速开始)
- [自定义配置](#自定义配置)
- [故障排除](#故障排除)

---

## 🚀 环境配置

### 第一步：创建conda虚拟环境

在你的Linux服务器上执行以下命令：

```bash
# 创建conda环境（使用提供的environment.yml）
conda env create -f environment.yml

# 激活环境
conda activate paper-diagram
```

### 第二步：验证安装

```bash
# 检查Python版本
python --version  # 应该显示 Python 3.10.x

# 检查matplotlib安装
python -c "import matplotlib; print(matplotlib.__version__)"
```

---

## ⚡ 快速开始

### 方式一：直接运行（推荐）

```bash
# 确保已激活conda环境
conda activate paper-diagram

# 运行脚本生成图片
python generate_architecture.py
```

执行后会生成两个文件：
- `architecture_diagram.png` - 300 DPI高分辨率PNG（推荐用于Word/LaTeX）
- `architecture_diagram.pdf` - 矢量PDF（推荐用于出版或需要缩放的场景）

### 方式二：在VSCode中运行

1. 确保VSCode已连接到你的Linux服务器
2. 打开 `generate_architecture.py`
3. 在VSCode终端中激活环境：
   ```bash
   conda activate paper-diagram
   ```
4. 点击右上角的运行按钮，或按 `F5`

---

## 🎨 自定义配置

### 修改输出分辨率

编辑 `generate_architecture.py` 的最后几行：

```python
# 生成更高分辨率的图片（用于打印）
create_architecture_diagram('architecture_diagram.png', dpi=600)

# 生成标准分辨率（用于电子版）
create_architecture_diagram('architecture_diagram.png', dpi=150)
```

### 修改配色方案

在脚本开头的 `COLORS` 字典中修改颜色：

```python
COLORS = {
    'primary': '#2E86AB',      # 主要颜色
    'secondary': '#A23B72',    # 次要颜色
    'accent': '#F18F01',       # 强调色
    # ... 其他颜色
}
```

### 调整图片尺寸

修改 `create_architecture_diagram` 函数中的 `figsize` 参数：

```python
fig, ax = plt.subplots(1, 1, figsize=(16, 20))  # (宽, 高) 单位：英寸
```

---

## 🔧 故障排除

### 问题1：中文显示为方块

**原因**：系统缺少中文字体

**解决方案**：

```bash
# Ubuntu/Debian系统
sudo apt-get update
sudo apt-get install fonts-wqy-microhei fonts-wqy-zenhei

# 清除matplotlib缓存
rm -rf ~/.cache/matplotlib
```

然后重新运行脚本。

### 问题2：ModuleNotFoundError

**原因**：依赖包未正确安装

**解决方案**：

```bash
# 重新安装依赖
conda activate paper-diagram
pip install matplotlib numpy pillow --upgrade
```

### 问题3：conda命令找不到

**原因**：conda未正确配置

**解决方案**：

```bash
# 初始化conda（根据你的shell类型选择）
conda init bash  # 如果使用bash
conda init zsh   # 如果使用zsh

# 重新加载配置
source ~/.bashrc  # 或 source ~/.zshrc
```

### 问题4：生成的图片为空或显示不正常

**解决方案**：

```bash
# 检查matplotlib后端
python -c "import matplotlib; print(matplotlib.get_backend())"

# 如果显示'agg'以外的内容，在脚本开头添加：
# import matplotlib
# matplotlib.use('Agg')
```

---

## 📊 输出文件说明

### PNG格式 (architecture_diagram.png)
- **用途**：Word文档、PowerPoint、网页展示
- **优点**：兼容性好，文件小
- **分辨率**：300 DPI（适合打印A4纸张）

### PDF格式 (architecture_diagram.pdf)
- **用途**：LaTeX论文、学术出版、需要缩放的场景
- **优点**：矢量图，无损缩放，印刷质量
- **推荐**：投稿SCI/EI期刊时使用

---

## 📝 使用建议

### 论文插图规范
1. **分辨率**：建议使用300-600 DPI
2. **格式**：
   - Word论文：使用PNG
   - LaTeX论文：使用PDF
3. **尺寸**：确保图片宽度不超过页面宽度（通常为14-16cm）

### 在LaTeX中使用

```latex
\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.95\textwidth]{architecture_diagram.pdf}
    \caption{基于双知识库RAG与三层记忆的智能心理咨询系统架构}
    \label{fig:architecture}
\end{figure}
```

### 在Word中使用

1. 插入图片：`插入 > 图片 > 此设备`
2. 选择 `architecture_diagram.png`
3. 右键图片 > 大小和位置 > 锁定纵横比
4. 调整宽度至页面宽度的90-95%

---

## 🆘 需要帮助？

如果遇到其他问题：
1. 检查错误日志信息
2. 确认Python和依赖版本
3. 尝试在纯Python环境中运行（不通过VSCode）

---

## 📜 许可证

本工具为学术研究使用，生成的图片版权归使用者所有。
