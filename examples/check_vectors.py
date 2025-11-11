"""检查向量库状态"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from dialogue.manager import create_dialogue_manager_from_config
import yaml

print("="*60)
print("  向量库诊断")
print("="*60)

with open("configs/config.yaml", 'r') as f:
    config = yaml.safe_load(f)

dm = create_dialogue_manager_from_config(config)

# 1. 检查文档数
stats = dm.rag_manager.get_stats()
doc_count = stats.get('psychological_kb', {}).get('document_count', 0)
print(f"\n1. 文档数量: {doc_count:,}")

# 2. 检查向量库
try:
    collection = dm.rag_manager.psychological_kb.collection
    print(f"2. Collection名称: {collection.name}")
    print(f"3. Collection文档数: {collection.count():,}")
    
    # 3. 尝试直接查询
    try:
        results = collection.query(
            query_texts=["测试"],
            n_results=1
        )
        if results and results.get('documents'):
            print(f"4. 直接查询: ✅ 成功")
            print(f"   返回文档数: {len(results['documents'][0])}")
        else:
            print(f"4. 直接查询: ❌ 返回空")
    except Exception as e:
        print(f"4. 直接查询: ❌ 失败 - {e}")
    
    # 4. 检查是否有embeddings
    try:
        sample = collection.peek(1)
        if sample and sample.get('embeddings'):
            print(f"5. Embeddings: ✅ 存在")
            print(f"   维度: {len(sample['embeddings'][0]) if sample['embeddings'] else 'N/A'}")
        else:
            print(f"5. Embeddings: ❌ 不存在")
    except Exception as e:
        print(f"5. Embeddings检查: ❌ {e}")
        
except Exception as e:
    print(f"\n错误: {e}")

print("\n" + "="*60)
