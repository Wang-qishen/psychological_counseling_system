"""
数据集下载器 - 支持多个中文心理咨询数据集 (修复版)
"""

import os
import json
import subprocess
from typing import List, Dict, Optional
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatasetDownloader:
    """统一的数据集下载器"""
    
    def __init__(self, output_dir: str = "./data/downloaded_datasets"):
        """
        初始化下载器
        
        Args:
            output_dir: 下载数据集的输出目录
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def download_smilechat(self) -> str:
        """
        下载SmileChat数据集 (提供多种方法)
        
        Returns:
            数据集保存路径
        """
        logger.info("开始准备SmileChat数据集...")
        
        dataset_dir = self.output_dir / "smilechat"
        dataset_dir.mkdir(exist_ok=True)
        
        # 尝试Git克隆方法
        try:
            logger.info("尝试使用Git克隆...")
            if self._clone_smile_repo(dataset_dir):
                logger.info("✓ Git克隆成功!")
                self._create_smilechat_readme(dataset_dir, success=True)
                logger.info(f"\n✓ SmileChat数据集准备完成!")
                logger.info(f"保存位置: {dataset_dir}")
                return str(dataset_dir)
        except Exception as e:
            logger.warning(f"Git克隆失败: {e}")
        
        # 如果自动下载失败，提供详细的手动说明
        logger.warning("\n自动下载失败,已生成详细的手动下载指南")
        self._create_smilechat_readme(dataset_dir, success=False)
        
        logger.info(f"\n✓ SmileChat下载指南已生成!")
        logger.info(f"保存位置: {dataset_dir}")
        logger.info(f"请查看: {dataset_dir}/README.md 了解手动下载方法\n")
        
        return str(dataset_dir)
    
    def _clone_smile_repo(self, dataset_dir: Path) -> bool:
        """
        克隆SmileChat的GitHub仓库
        
        Args:
            dataset_dir: 数据集保存目录
            
        Returns:
            是否成功
        """
        try:
            # 检查git是否可用
            subprocess.run(["git", "--version"], capture_output=True, check=True)
            
            temp_dir = dataset_dir / "temp_repo"
            
            # 清理旧的临时目录
            if temp_dir.exists():
                import shutil
                shutil.rmtree(temp_dir)
            
            # 克隆仓库
            logger.info("正在克隆GitHub仓库...")
            result = subprocess.run(
                ["git", "clone", "--depth=1", "https://github.com/qiuhuachuan/smile.git", str(temp_dir)],
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode != 0:
                logger.warning(f"克隆失败: {result.stderr}")
                return False
            
            # 复制data目录下的文件
            import shutil
            data_source = temp_dir / "data"
            
            if data_source.exists():
                files_copied = 0
                for file in data_source.glob("*"):
                    if file.is_file():
                        dest = dataset_dir / file.name
                        shutil.copy(file, dest)
                        logger.info(f"✓ 复制: {file.name}")
                        files_copied += 1
                
                # 清理临时目录
                shutil.rmtree(temp_dir)
                
                return files_copied > 0
            
            return False
            
        except Exception as e:
            logger.debug(f"Git克隆失败: {e}")
            return False
    
    def _create_smilechat_readme(self, dataset_dir: Path, success: bool = False):
        """
        创建SmileChat的README文件
        
        Args:
            dataset_dir: 数据集目录
            success: 是否成功下载
        """
        readme_path = dataset_dir / "README.md"
        
        if success:
            content = """# SmileChat数据集

## ✓ 下载成功

数据集已成功下载到本目录。

## 数据来源
- 论文: SMILE: Single-turn to Multi-turn Inclusive Language Expansion via ChatGPT for Mental Health Support
- GitHub: https://github.com/qiuhuachuan/smile
- 作者: 西湖大学 + 浙江大学

## 数据规模
- 约55K多轮对话数据
- 涵盖多种心理健康主题

## 数据格式
查看本目录下的文件了解具体格式。

## 下一步
运行数据处理脚本:
```bash
python data_integration/process_datasets.py
```

## 引用
```bibtex
@inproceedings{qiu-etal-2024-smile,
    title = "SMILE: Single-turn to Multi-turn Inclusive Language Expansion via ChatGPT for Mental Health Support",
    author = "Qiu, Huachuan and He, Hongliang and Zhang, Shuai and Li, Anqi and Lan, Zhenzhong",
    booktitle = "Findings of EMNLP 2024",
    year = "2024"
}
```
"""
        else:
            content = """# SmileChat数据集 - 手动下载指南

## ⚠️ 自动下载失败

请使用以下任一方法手动获取数据。

---

## 🌟 方法1: Git克隆 (最简单,推荐)

```bash
# 在项目根目录执行
cd /path/to/psychological_counseling_system

# 克隆SmileChat仓库
git clone --depth=1 https://github.com/qiuhuachuan/smile.git temp_smile

# 复制data目录的内容
cp -r temp_smile/data/* data/downloaded_datasets/smilechat/

# 删除临时目录
rm -rf temp_smile

# 查看下载的文件
ls -lh data/downloaded_datasets/smilechat/
```

---

## 方法2: 手动下载

1. 访问: https://github.com/qiuhuachuan/smile
2. 点击绿色的"Code"按钮
3. 选择"Download ZIP"
4. 解压后,将`data/`目录中的所有文件复制到:
   ```
   data/downloaded_datasets/smilechat/
   ```

---

## 方法3: 使用备用数据集

如果SmileChat下载困难,可以使用其他优质数据集:

### PsyQA (强烈推荐)
- 22K问题 + 56K专业回答
- 清华大学出品,质量更高
- 获取方式: 查看 `../psyqa/如何获取PsyQA数据集.md`

### CPsyCoun
- 中科院提供
- 真实心理咨询对话
- 可能可通过HuggingFace获取

---

## 下一步操作

### 如果已经获取到数据文件:

1. 确认文件在正确位置:
   ```
   data/downloaded_datasets/smilechat/
   ├── (SmileChat的数据文件)
   ```

2. 运行处理脚本:
   ```bash
   python data_integration/process_datasets.py
   ```

3. 导入到RAG:
   ```bash
   python data_integration/import_to_rag.py
   ```

### 如果没有获取到数据:

**选项A**: 使用PsyQA (推荐)
- 数据质量更高
- 包含专业策略标注
- 适合学术研究

**选项B**: 使用现有数据
- 先用 `data/sample_knowledge/` 测试系统
- 后续再补充大规模数据

**选项C**: 跳过SmileChat
- 直接处理其他已有数据集
- 系统仍然可以正常运行

---

## 📊 数据集对比

| 数据集 | 规模 | 获取难度 | 质量 | 推荐度 |
|--------|------|----------|------|--------|
| SmileChat | 55K | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| PsyQA | 22K+56K | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| CPsyCoun | 多轮对话 | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

---

## 💡 建议

1. **优先使用PsyQA**: 
   - 申请简单(邮件申请,1-3天)
   - 数据质量最高
   - 有策略标注

2. **SmileChat作为补充**:
   - 如果需要大规模多轮对话
   - 可以通过Git克隆获取

3. **组合使用**:
   - 同时使用多个数据集
   - 效果最好

---

## 🆘 需要帮助?

1. 查看完整文档: `../../DATA_INTEGRATION_GUIDE.md`
2. 查看数据集总指南: `../数据集下载指南.md`
3. SmileChat GitHub: https://github.com/qiuhuachuan/smile/issues

---

**更新时间**: 2025-11-11
**状态**: 等待手动下载
"""
        
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def download_psyqa_info(self) -> str:
        """
        生成PsyQA数据集的获取说明
        
        Returns:
            说明文件路径
        """
        logger.info("生成PsyQA数据集获取说明...")
        
        dataset_dir = self.output_dir / "psyqa"
        dataset_dir.mkdir(exist_ok=True)
        
        info_path = dataset_dir / "如何获取PsyQA数据集.md"
        with open(info_path, 'w', encoding='utf-8') as f:
            f.write("""# PsyQA数据集获取指南

## 📊 数据集信息

- **名称**: PsyQA (Psychological QA Dataset)
- **来源**: 清华大学
- **论文**: ACL 2021 Findings
- **规模**: 22,346个问题 + 56,063个专业回答
- **特点**: 包含6种助人策略标注

## 🌟 为什么推荐PsyQA?

相比SmileChat,PsyQA具有以下优势:

1. ✅ **质量更高**: 专业心理咨询师回答
2. ✅ **有策略标注**: 6种心理咨询策略
3. ✅ **学术认可**: 高引用量,权威性强
4. ✅ **获取简单**: 免费申请,1-3天即可

## 📝 获取步骤

### 步骤1: 下载用户协议

访问GitHub仓库:
https://github.com/thu-coai/PsyQA

下载【PsyQA数据集使用用户协议】PDF文件

### 步骤2: 填写协议

在协议中填写:
- 您的姓名
- 单位/学校
- 邮箱
- 使用目的(研究)
- 授权时间
- 电子签名

### 步骤3: 发送邮件

将填写好的PDF发送至:
```
thu-sunhao@foxmail.com
```

邮件主题建议:
```
PsyQA数据集申请 - [您的姓名/单位]
```

### 步骤4: 等待审核

- 审核时间: 通常1-3个工作日
- 审核通过后,会收到数据集下载链接
- 下载数据集

### 步骤5: 放置数据

将下载的数据文件放置到:
```
psychological_counseling_system/data/downloaded_datasets/psyqa/
```

### 步骤6: 处理数据

```bash
# 处理PsyQA数据
python data_integration/process_datasets.py

# 导入到RAG
python data_integration/import_to_rag.py
```

---

## 📋 数据格式

PsyQA数据包含:

```json
{
  "question": "用户问题",
  "description": "问题详细描述",
  "answer": "专业回答",
  "strategy": ["策略1", "策略2"],
  "keywords": ["关键词1", "关键词2"]
}
```

### 6种助人策略

1. **Restatement**: 复述
2. **Information**: 提供信息
3. **Interpretation**: 解释
4. **Direct Guidance**: 直接指导
5. **Self-disclosure**: 自我披露
6. **Approval & Reassurance**: 认可与安慰

---

## ⚠️ 使用注意事项

1. **仅限研究用途**: 不可商用
2. **引用论文**: 使用时必须引用
3. **保密协议**: 遵守用户协议
4. **数据安全**: 妥善保管数据

### 引用格式

```bibtex
@inproceedings{sun-etal-2021-psyqa,
    title = "PsyQA: A Chinese Dataset for Generating Long Counseling Text for Mental Health Support",
    author = "Sun, Hao and Lin, Zhenru and Zheng, Chujie and Liu, Siyang and Huang, Minlie",
    booktitle = "Findings of ACL-IJCNLP 2021",
    year = "2021",
    pages = "1489--1503"
}
```

---

## 💡 使用建议

### 优先级设置

1. **首选PsyQA**: 质量最高,最适合学术研究
2. **SmileChat作为补充**: 增加数据量和多轮对话
3. **组合使用**: 效果最佳

### 数据处理顺序

```bash
# 1. 处理PsyQA(质量高)
python data_integration/process_datasets.py

# 2. 如果有SmileChat,一起处理
# 会自动识别多个数据集

# 3. 导入RAG
python data_integration/import_to_rag.py --verify
```

---

## 🆘 常见问题

### Q1: 多久能收到回复?

A: 通常1-3个工作日,最快当天,最慢一周

### Q2: 申请被拒怎么办?

A: 
- 检查协议是否完整填写
- 确认使用目的为研究
- 重新申请或联系作者说明

### Q3: 数据集大小?

A: 压缩后约100MB,解压后约200MB

### Q4: 可以分享给他人吗?

A: 不可以,每个使用者需要单独申请

### Q5: 没有回复怎么办?

A: 
- 检查垃圾邮件
- 重新发送邮件
- 访问GitHub Issues询问

---

## 📞 联系方式

- **GitHub**: https://github.com/thu-coai/PsyQA
- **邮箱**: thu-sunhao@foxmail.com
- **论文**: https://aclanthology.org/2021.findings-acl.130/

---

**建议**: 现在就申请PsyQA,数据质量最好! 💪

**更新时间**: 2025-11-11
"""

)
        
        logger.info(f"✓ PsyQA获取说明已生成: {info_path}")
        return str(info_path)
    
    def create_manual_download_guide(self) -> str:
        """
        创建手动下载总指南
        
        Returns:
            指南文件路径
        """
        guide_path = self.output_dir / "数据集下载指南.md"
        
        with open(guide_path, 'w', encoding='utf-8') as f:
            f.write("""# 中文心理咨询数据集下载总指南

本指南帮助您获取适合心理咨询RAG系统的中文数据集。

---

## 📊 推荐数据集清单

### 1. PsyQA ⭐⭐⭐⭐⭐ (最推荐)

**规模**: 22K问题 + 56K回答

**优势**:
- ✅ **质量最高**: 专业心理咨询师回答  
- ✅ **有策略标注**: 6种助人策略
- ✅ **学术认可**: ACL 2021,高引用
- ✅ **获取简单**: 邮件申请,免费

**获取方式**:
1. 访问: https://github.com/thu-coai/PsyQA
2. 下载用户协议并填写
3. 发送至: thu-sunhao@foxmail.com
4. 等待1-3天审核

**详细说明**: 查看 `psyqa/如何获取PsyQA数据集.md`

---

### 2. SmileChat ⭐⭐⭐⭐

**规模**: 55K+ 多轮对话

**优势**:
- ✅ 完全开源
- ✅ 多轮对话丰富
- ✅ 数据量大

**获取方式**:

#### 方法A: Git克隆(推荐)
```bash
git clone --depth=1 https://github.com/qiuhuachuan/smile.git temp
cp -r temp/data/* data/downloaded_datasets/smilechat/
rm -rf temp
```

#### 方法B: 手动下载
1. 访问 https://github.com/qiuhuachuan/smile
2. 点击"Code" → "Download ZIP"
3. 解压并复制data目录

**详细说明**: 查看 `smilechat/README.md`

---

### 3. CPsyCoun ⭐⭐⭐⭐

**规模**: 多轮心理咨询对话

**来源**: 中科院

**获取方式**:
- HuggingFace: https://huggingface.co/datasets/CAS-SIAT-XinHai/CPsyCoun
- 使用datasets库下载

---

## 🚀 快速开始

### 最简单的方式

```bash
cd psychological_counseling_system

# 1. 运行下载脚本(会生成指南)
python data_integration/dataset_downloader.py --dataset all

# 2. 按照生成的README手动下载数据

# 3. 处理数据
python data_integration/process_datasets.py

# 4. 导入RAG
python data_integration/import_to_rag.py --verify
```

---

## 💡 推荐策略

### 🥇 最佳方案: PsyQA为主

```
1. 申请PsyQA(1-3天)
2. 等待期间可以先测试其他功能
3. 获取后处理导入
4. 可选: 补充SmileChat增加数据量
```

**优势**: 质量最高,最适合论文

### 🥈 备选方案: SmileChat为主

```
1. Git克隆SmileChat(5分钟)
2. 立即处理导入
3. 可选: 后续申请PsyQA补充
```

**优势**: 立即可用,数据量大

### 🥉 保守方案: 使用现有数据

```
1. 先用data/sample_knowledge/测试
2. 同时申请PsyQA
3. 获取后再扩展
```

**优势**: 风险最小,稳妥

---

## 📂 数据存放结构

```
psychological_counseling_system/
└── data/
    └── downloaded_datasets/
        ├── smilechat/              # SmileChat数据
        │   ├── README.md
        │   └── (数据文件)
        │
        ├── psyqa/                  # PsyQA数据
        │   ├── 如何获取PsyQA数据集.md
        │   └── (申请后的数据文件)
        │
        ├── cpyscoun/               # CPsyCoun数据
        │   └── (如果下载)
        │
        └── 数据集下载指南.md       # 本文件
```

---

## 🎯 使用流程

### 完整流程

```
下载原始数据
    ↓
运行 process_datasets.py (转换格式)
    ↓  
运行 import_to_rag.py (导入向量库)
    ↓
运行 test_new_knowledge.py (验证效果)
    ↓
在对话系统中使用
```

### 命令示例

```bash
# 步骤1: 下载/准备数据
python data_integration/dataset_downloader.py --dataset all

# 步骤2: 手动获取数据(如果需要)
# - SmileChat: git clone方式
# - PsyQA: 邮件申请

# 步骤3: 处理数据
python data_integration/process_datasets.py

# 步骤4: 导入RAG
python data_integration/import_to_rag.py --verify

# 步骤5: 测试效果
python examples/test_new_knowledge.py
```

---

## ⚠️ 注意事项

### 数据使用规范

- ✅ **学术研究**: 可以使用
- ✅ **论文撰写**: 需正确引用
- ❌ **商业用途**: 需要授权
- ❌ **二次分发**: 不允许

### 存储空间

- SmileChat: ~200MB
- PsyQA: ~200MB  
- 处理后: ~500MB
- 向量库: ~500MB
- **总计**: 至少2GB空间

### 时间估算

- 下载: 取决于方法(5分钟-3天)
- 处理: 10-20分钟
- 导入: 30-60分钟

---

## 🆘 故障排除

### Q1: Git克隆失败?

```bash
# 尝试浅克隆
git clone --depth=1 https://github.com/qiuhuachuan/smile.git

# 或者直接下载ZIP
# 访问GitHub页面手动下载
```

### Q2: PsyQA申请无回复?

- 检查垃圾邮件
- 重新发送申请
- 在GitHub提Issue

### Q3: 处理脚本出错?

```bash
# 查看错误信息
python data_integration/process_datasets.py

# 检查数据文件是否在正确位置
ls -R data/downloaded_datasets/
```

### Q4: 内存不足?

```bash
# 使用分块处理
python data_integration/process_datasets.py --chunk-size 50

# 使用CPU模式
# 修改 configs/config.yaml
# rag.embedding.device: 'cpu'
```

---

## 📚 参考资源

### 论文链接

- **SmileChat**: https://arxiv.org/abs/2305.00450
- **PsyQA**: https://aclanthology.org/2021.findings-acl.130/

### GitHub仓库

- **SmileChat**: https://github.com/qiuhuachuan/smile
- **PsyQA**: https://github.com/thu-coai/PsyQA
- **CPsyCoun**: https://huggingface.co/datasets/CAS-SIAT-XinHai/CPsyCoun

### 项目文档

- 完整说明: `../../DATA_INTEGRATION_GUIDE.md`
- 快速安装: `../../data_integration/INSTALL.md`

---

## ✅ 检查清单

下载和设置完成后,检查:

- [ ] 数据文件已下载到正确位置
- [ ] 已运行process_datasets.py
- [ ] 已运行import_to_rag.py
- [ ] 测试脚本运行成功
- [ ] data/processed_knowledge/有处理后的文件
- [ ] data/vector_db/有向量数据

---

**更新时间**: 2025-11-11
**维护**: 心理咨询系统开发团队

**祝您使用顺利!** 🚀
"""

)
        
        logger.info(f"✓ 下载指南已生成: {guide_path}")
        return str(guide_path)


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="下载中文心理咨询数据集")
    parser.add_argument(
        "--dataset",
        type=str,
        choices=['smilechat', 'psyqa', 'all'],
        default='all',
        help="选择要下载的数据集"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="./data/downloaded_datasets",
        help="输出目录"
    )
    
    args = parser.parse_args()
    
    downloader = DatasetDownloader(output_dir=args.output_dir)
    
    print("\n" + "="*60)
    print("  中文心理咨询数据集下载工具")
    print("="*60 + "\n")
    
    if args.dataset == 'smilechat' or args.dataset == 'all':
        try:
            downloader.download_smilechat()
        except Exception as e:
            logger.error(f"SmileChat处理失败: {e}")
    
    if args.dataset == 'psyqa' or args.dataset == 'all':
        downloader.download_psyqa_info()
    
    # 总是生成下载指南
    downloader.create_manual_download_guide()
    
    print("\n" + "="*60)
    print("  ✓ 完成!")
    print("="*60)
    print(f"\n数据保存在: {args.output_dir}")
    print(f"\n📖 请查看以下文档:")
    print(f"  - 总指南: {args.output_dir}/数据集下载指南.md")
    print(f"  - SmileChat: {args.output_dir}/smilechat/README.md")
    print(f"  - PsyQA: {args.output_dir}/psyqa/如何获取PsyQA数据集.md\n")
    
    print("💡 建议:")
    print("  1. 优先申请PsyQA(质量最高)")
    print("  2. 使用Git克隆SmileChat(立即可用)")
    print("  3. 查看详细文档了解更多方法\n")


if __name__ == "__main__":
    main()
