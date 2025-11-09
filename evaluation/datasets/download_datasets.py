#!/usr/bin/env python3
"""
数据集下载和管理脚本
位置: psychological_counseling_system/evaluation/datasets/download_datasets.py

功能:
1. 下载MentalChat16K数据集
2. 下载Empathetic Dialogues数据集
3. 下载Counsel Chat数据集
4. 数据预处理和格式转换
5. 生成统计信息

使用方法:
    # 下载MentalChat16K
    python download_datasets.py --dataset mentalchat
    
    # 下载所有数据集
    python download_datasets.py --all
    
    # 指定输出目录
    python download_datasets.py --dataset mentalchat --output ./data
"""

import os
import argparse
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional
import sys

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DatasetDownloader:
    """数据集下载器"""
    
    def __init__(self, output_dir: str = "./data"):
        """
        初始化
        
        Args:
            output_dir: 输出目录
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 数据集配置
        self.datasets_config = {
            "mentalchat": {
                "name": "MentalChat16K",
                "source": "huggingface",
                "hf_name": "ShenLab/MentalChat16K",
                "size": "~200MB",
                "description": "16,113对话 + 200测试问题 + 7个临床维度"
            },
            "empathetic": {
                "name": "Empathetic Dialogues",
                "source": "huggingface",
                "hf_name": "empathetic_dialogues",
                "size": "~50MB",
                "description": "25k对话，32种情绪场景"
            },
            "counsel": {
                "name": "Counsel Chat",
                "source": "manual",
                "url": "https://www.kaggle.com/datasets/thedevastator/counsel-chat",
                "size": "~5MB",
                "description": "3k专业咨询对话（需手动下载）"
            }
        }
    
    def download_mentalchat(self) -> bool:
        """
        下载MentalChat16K数据集
        
        Returns:
            是否成功
        """
        logger.info("="*70)
        logger.info("下载 MentalChat16K 数据集")
        logger.info("="*70)
        
        try:
            from datasets import load_dataset
        except ImportError:
            logger.error("请安装 datasets 库: pip install datasets")
            return False
        
        output_path = self.output_dir / "mentalchat"
        output_path.mkdir(parents=True, exist_ok=True)
        
        try:
            logger.info("正在从 HuggingFace 下载...")
            logger.info("数据集: ShenLab/MentalChat16K")
            logger.info("这可能需要几分钟，请耐心等待...")
            
            # 下载数据集
            dataset = load_dataset("ShenLab/MentalChat16K")
            
            logger.info(f"✓ 下载完成！")
            logger.info(f"训练集大小: {len(dataset['train'])}")
            if 'test' in dataset:
                logger.info(f"测试集大小: {len(dataset['test'])}")
            
            # 保存为JSON格式
            logger.info("\n正在保存为JSON格式...")
            
            # 保存训练集
            train_file = output_path / "train.json"
            with open(train_file, 'w', encoding='utf-8') as f:
                json.dump(
                    [dict(item) for item in dataset['train']],
                    f,
                    ensure_ascii=False,
                    indent=2
                )
            logger.info(f"✓ 训练集保存至: {train_file}")
            
            # 保存测试集（如果存在）
            if 'test' in dataset:
                test_file = output_path / "test.json"
                with open(test_file, 'w', encoding='utf-8') as f:
                    json.dump(
                        [dict(item) for item in dataset['test']],
                        f,
                        ensure_ascii=False,
                        indent=2
                    )
                logger.info(f"✓ 测试集保存至: {test_file}")
            
            # 生成统计信息
            self._generate_stats(dataset, output_path / "stats.json")
            
            # 创建README
            self._create_readme(
                output_path,
                "MentalChat16K",
                "心理健康咨询对话数据集，包含16,113对话和200个测试问题"
            )
            
            logger.info("\n" + "="*70)
            logger.info("✓ MentalChat16K 数据集下载完成！")
            logger.info(f"保存位置: {output_path}")
            logger.info("="*70)
            
            return True
            
        except Exception as e:
            logger.error(f"下载失败: {e}")
            logger.error("\n可能的解决方案:")
            logger.error("1. 检查网络连接")
            logger.error("2. 使用镜像源: export HF_ENDPOINT=https://hf-mirror.com")
            logger.error("3. 手动下载后放入 data/mentalchat/ 目录")
            return False
    
    def download_empathetic_dialogues(self) -> bool:
        """
        下载Empathetic Dialogues数据集
        
        Returns:
            是否成功
        """
        logger.info("="*70)
        logger.info("下载 Empathetic Dialogues 数据集")
        logger.info("="*70)
        
        try:
            from datasets import load_dataset
        except ImportError:
            logger.error("请安装 datasets 库: pip install datasets")
            return False
        
        output_path = self.output_dir / "empathetic_dialogues"
        output_path.mkdir(parents=True, exist_ok=True)
        
        try:
            logger.info("正在从 HuggingFace 下载...")
            logger.info("数据集: empathetic_dialogues")
            
            dataset = load_dataset("empathetic_dialogues")
            
            logger.info(f"✓ 下载完成！")
            logger.info(f"训练集大小: {len(dataset['train'])}")
            logger.info(f"验证集大小: {len(dataset['validation'])}")
            logger.info(f"测试集大小: {len(dataset['test'])}")
            
            # 保存数据集
            for split in ['train', 'validation', 'test']:
                output_file = output_path / f"{split}.json"
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(
                        [dict(item) for item in dataset[split]],
                        f,
                        ensure_ascii=False,
                        indent=2
                    )
                logger.info(f"✓ {split} 保存至: {output_file}")
            
            # 生成统计信息
            self._generate_stats(dataset, output_path / "stats.json")
            
            # 创建README
            self._create_readme(
                output_path,
                "Empathetic Dialogues",
                "共情对话数据集，包含25k对话，涵盖32种情绪场景"
            )
            
            logger.info("\n" + "="*70)
            logger.info("✓ Empathetic Dialogues 数据集下载完成！")
            logger.info(f"保存位置: {output_path}")
            logger.info("="*70)
            
            return True
            
        except Exception as e:
            logger.error(f"下载失败: {e}")
            return False
    
    def download_counsel_chat(self) -> bool:
        """
        提供Counsel Chat数据集下载指导
        
        Returns:
            是否成功（仅检查指导信息是否生成）
        """
        logger.info("="*70)
        logger.info("Counsel Chat 数据集")
        logger.info("="*70)
        
        output_path = self.output_dir / "counsel_chat"
        output_path.mkdir(parents=True, exist_ok=True)
        
        # 创建下载指南
        guide = """# Counsel Chat 数据集下载指南

由于Counsel Chat数据集托管在Kaggle上，需要手动下载。

## 下载步骤

1. 访问 Kaggle 数据集页面:
   https://www.kaggle.com/datasets/thedevastator/counsel-chat

2. 点击 "Download" 按钮下载数据集

3. 解压下载的文件

4. 将 CSV 文件复制到以下目录:
   {}

5. 运行预处理脚本:
   python evaluation/datasets/preprocess_counsel_chat.py

## 数据集说明

- 规模: 约3000条专业咨询对话
- 格式: CSV
- 字段: question, answer, topic
- 用途: 专业性评估

## 注意事项

- 需要Kaggle账号
- 确保遵守数据集使用协议
- 仅用于研究和教育目的
""".format(output_path)
        
        guide_file = output_path / "DOWNLOAD_GUIDE.md"
        with open(guide_file, 'w', encoding='utf-8') as f:
            f.write(guide)
        
        logger.info(f"✓ 下载指南已创建: {guide_file}")
        logger.info("\n请按照指南手动下载 Counsel Chat 数据集")
        logger.info("数据集URL: https://www.kaggle.com/datasets/thedevastator/counsel-chat")
        
        return True
    
    def _generate_stats(self, dataset, output_file: Path):
        """生成数据集统计信息"""
        stats = {
            "splits": {},
            "total_examples": 0
        }
        
        for split in dataset.keys():
            split_size = len(dataset[split])
            stats["splits"][split] = split_size
            stats["total_examples"] += split_size
        
        if 'train' in dataset:
            sample = dataset['train'][0]
            stats["features"] = list(sample.keys())
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✓ 统计信息保存至: {output_file}")
    
    def _create_readme(self, output_dir: Path, name: str, description: str):
        """创建数据集README"""
        readme = f"""# {name}

{description}

## 数据集信息

- 下载时间: {Path(output_dir).stat().st_mtime}
- 存储位置: {output_dir}

## 文件说明

- `train.json`: 训练集
- `test.json`: 测试集（如果有）
- `stats.json`: 统计信息
- `README.md`: 本文档

## 使用方法

```python
import json

# 加载训练集
with open('train.json', 'r', encoding='utf-8') as f:
    train_data = json.load(f)

print(f"训练集大小: {{len(train_data)}}")
```

## 数据格式

查看 `train.json` 了解具体数据格式。

## 引用

如果使用本数据集，请引用原始论文和数据来源。
"""
        readme_file = output_dir / "README.md"
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme)
    
    def list_datasets(self):
        """列出所有可用数据集"""
        logger.info("\n" + "="*70)
        logger.info("可用数据集")
        logger.info("="*70)
        
        for key, config in self.datasets_config.items():
            logger.info(f"\n{config['name']} ({key})")
            logger.info(f"  来源: {config['source']}")
            logger.info(f"  大小: {config['size']}")
            logger.info(f"  说明: {config['description']}")
            
            # 检查是否已下载
            dataset_dir = self.output_dir / key.replace("_", "")
            if dataset_dir.exists():
                logger.info(f"  状态: ✓ 已下载")
                logger.info(f"  位置: {dataset_dir}")
            else:
                logger.info(f"  状态: ✗ 未下载")
    
    def download_all(self):
        """下载所有数据集"""
        logger.info("\n" + "="*70)
        logger.info("开始下载所有数据集")
        logger.info("="*70)
        
        results = {
            "mentalchat": self.download_mentalchat(),
            "empathetic": self.download_empathetic_dialogues(),
            "counsel": self.download_counsel_chat()
        }
        
        logger.info("\n" + "="*70)
        logger.info("下载总结")
        logger.info("="*70)
        
        for dataset, success in results.items():
            status = "✓ 成功" if success else "✗ 失败"
            logger.info(f"{dataset}: {status}")
        
        success_count = sum(results.values())
        logger.info(f"\n成功下载: {success_count}/{len(results)} 个数据集")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="下载和管理评估数据集"
    )
    parser.add_argument(
        "--dataset",
        choices=["mentalchat", "empathetic", "counsel"],
        help="要下载的数据集"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="下载所有数据集"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="列出所有可用数据集"
    )
    parser.add_argument(
        "--output",
        default="./data",
        help="输出目录 (默认: ./data)"
    )
    
    args = parser.parse_args()
    
    # 创建下载器
    downloader = DatasetDownloader(args.output)
    
    # 执行操作
    if args.list:
        downloader.list_datasets()
    elif args.all:
        downloader.download_all()
    elif args.dataset:
        if args.dataset == "mentalchat":
            downloader.download_mentalchat()
        elif args.dataset == "empathetic":
            downloader.download_empathetic_dialogues()
        elif args.dataset == "counsel":
            downloader.download_counsel_chat()
    else:
        parser.print_help()
        logger.info("\n示例:")
        logger.info("  python download_datasets.py --dataset mentalchat")
        logger.info("  python download_datasets.py --all")
        logger.info("  python download_datasets.py --list")


if __name__ == "__main__":
    main()
