"""
对比实验脚本
对比三种配置的效果差异：
1. 裸LLM（无RAG，无记忆）
2. LLM + RAG（有知识库，无记忆）
3. 完整系统（有知识库，有记忆）

用于论文实验数据收集
"""

import sys
import os
import json
import time
from datetime import datetime
from typing import List, Dict, Any

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import load_config, setup_directories
from dialogue import create_dialogue_manager_from_config
from memory import MemoryManager


# 测试对话场景
TEST_SCENARIOS = [
    {
        "name": "场景1: 首次咨询 - 工作压力和睡眠问题",
        "user_id": "test_user_001",
        "conversations": [
            {
                "turn": 1,
                "user": "你好，我最近工作压力很大，每天都要加班到很晚。",
                "emotion": {"stress": 0.8, "anxiety": 0.6}
            },
            {
                "turn": 2,
                "user": "是的，而且我晚上经常失眠，躺在床上一两个小时都睡不着。",
                "emotion": {"stress": 0.7, "anxiety": 0.7}
            },
            {
                "turn": 3,
                "user": "我试过数羊，但是没什么用。你有什么建议吗？",
                "emotion": {"stress": 0.6, "anxiety": 0.6}
            }
        ]
    },
    {
        "name": "场景2: 第二次咨询 - 继续讨论睡眠（测试记忆）",
        "user_id": "test_user_001",
        "conversations": [
            {
                "turn": 1,
                "user": "我上次说的失眠问题，这几天情况怎么样？你还记得我的情况吗？",
                "emotion": {"anxiety": 0.5}
            },
            {
                "turn": 2,
                "user": "我试了一些方法，但还是很难入睡。我的工作压力也没有减轻。",
                "emotion": {"stress": 0.7, "anxiety": 0.6}
            },
            {
                "turn": 3,
                "user": "认知行为疗法？这个具体怎么做呢？",
                "emotion": {"curiosity": 0.7, "anxiety": 0.5}
            }
        ]
    },
    {
        "name": "场景3: 焦虑情绪管理",
        "user_id": "test_user_002",
        "conversations": [
            {
                "turn": 1,
                "user": "我最近总是感到很焦虑，尤其是在面对社交场合的时候。",
                "emotion": {"anxiety": 0.8, "fear": 0.6}
            },
            {
                "turn": 2,
                "user": "我会心跳加速，出汗，甚至有时候感觉呼吸困难。",
                "emotion": {"anxiety": 0.9, "fear": 0.7}
            },
            {
                "turn": 3,
                "user": "有什么方法可以帮我缓解这种焦虑吗？",
                "emotion": {"anxiety": 0.7, "hope": 0.5}
            }
        ]
    }
]


class ExperimentRunner:
    """实验运行器"""
    
    def __init__(self):
        self.results = {
            "bare_llm": [],      # 裸LLM
            "llm_rag": [],       # LLM + RAG
            "full_system": []    # 完整系统
        }
        self.base_config = load_config()
    
    def create_config_variant(self, enable_rag: bool, enable_memory: bool) -> Dict[str, Any]:
        """
        创建配置变体
        
        Args:
            enable_rag: 是否启用RAG
            enable_memory: 是否启用记忆
            
        Returns:
            配置字典
        """
        config = self.base_config.copy()
        config['dialogue']['generation']['enable_rag'] = enable_rag
        config['dialogue']['generation']['enable_memory'] = enable_memory
        return config
    
    def run_scenario(self, scenario: Dict[str, Any], config_name: str, 
                    enable_rag: bool, enable_memory: bool) -> Dict[str, Any]:
        """
        运行单个场景
        
        Args:
            scenario: 场景数据
            config_name: 配置名称
            enable_rag: 是否启用RAG
            enable_memory: 是否启用记忆
            
        Returns:
            场景结果
        """
        print(f"\n  运行配置: {config_name}")
        print(f"  场景: {scenario['name']}")
        
        # 创建配置
        config = self.create_config_variant(enable_rag, enable_memory)
        
        # 创建对话管理器
        dialogue_manager = create_dialogue_manager_from_config(config)
        
        # 创建或获取用户
        user_id = scenario['user_id']
        user_memory = dialogue_manager.memory_manager.get_user_memory(user_id)
        
        if not user_memory:
            dialogue_manager.memory_manager.create_user(
                user_id=user_id,
                age=28,
                gender="女" if "001" in user_id else "男",
                occupation="软件工程师" if "001" in user_id else "教师"
            )
        
        # 开始会话
        session_id = dialogue_manager.start_session(user_id)
        
        # 记录结果
        scenario_result = {
            "scenario_name": scenario['name'],
            "user_id": user_id,
            "config": config_name,
            "enable_rag": enable_rag,
            "enable_memory": enable_memory,
            "turns": []
        }
        
        # 运行对话
        for conv in scenario['conversations']:
            turn_start = time.time()
            
            # 生成回复
            response = dialogue_manager.chat(
                user_id=user_id,
                session_id=session_id,
                user_message=conv['user'],
                emotion=conv.get('emotion')
            )
            
            turn_time = time.time() - turn_start
            
            # 记录结果
            turn_result = {
                "turn": conv['turn'],
                "user_message": conv['user'],
                "assistant_response": response,
                "response_time": turn_time,
                "response_length": len(response)
            }
            
            scenario_result['turns'].append(turn_result)
            
            print(f"    Turn {conv['turn']}: {turn_time:.2f}s, {len(response)} 字符")
        
        # 结束会话
        dialogue_manager.end_session(user_id, session_id)
        
        # 计算统计
        scenario_result['avg_response_time'] = sum(
            t['response_time'] for t in scenario_result['turns']
        ) / len(scenario_result['turns'])
        
        scenario_result['avg_response_length'] = sum(
            t['response_length'] for t in scenario_result['turns']
        ) / len(scenario_result['turns'])
        
        return scenario_result
    
    def run_all_experiments(self):
        """运行所有实验"""
        print("="*70)
        print("开始对比实验")
        print("="*70)
        
        configs = [
            ("bare_llm", "裸LLM（无RAG，无记忆）", False, False),
            ("llm_rag", "LLM + RAG（有知识库，无记忆）", True, False),
            ("full_system", "完整系统（有知识库，有记忆）", True, True)
        ]
        
        for config_key, config_name, enable_rag, enable_memory in configs:
            print(f"\n{'='*70}")
            print(f"测试配置: {config_name}")
            print(f"{'='*70}")
            
            for scenario in TEST_SCENARIOS:
                result = self.run_scenario(
                    scenario, config_name, enable_rag, enable_memory
                )
                self.results[config_key].append(result)
            
            # 清理内存，避免跨配置的记忆污染
            import shutil
            memory_path = "./data/memory_db"
            if os.path.exists(memory_path):
                shutil.rmtree(memory_path)
                os.makedirs(memory_path, exist_ok=True)
    
    def generate_report(self):
        """生成实验报告"""
        print("\n" + "="*70)
        print("生成实验报告")
        print("="*70)
        
        report = {
            "experiment_time": datetime.now().isoformat(),
            "configurations": {
                "bare_llm": "裸LLM（无RAG，无记忆）",
                "llm_rag": "LLM + RAG（有知识库，无记忆）",
                "full_system": "完整系统（有知识库，有记忆）"
            },
            "results": self.results,
            "summary": {}
        }
        
        # 计算每个配置的总体统计
        for config_key, config_name in report['configurations'].items():
            scenarios_data = self.results[config_key]
            
            if scenarios_data:
                report['summary'][config_key] = {
                    "config_name": config_name,
                    "total_scenarios": len(scenarios_data),
                    "avg_response_time": sum(
                        s['avg_response_time'] for s in scenarios_data
                    ) / len(scenarios_data),
                    "avg_response_length": sum(
                        s['avg_response_length'] for s in scenarios_data
                    ) / len(scenarios_data)
                }
        
        # 保存报告
        os.makedirs("./experiments", exist_ok=True)
        report_file = f"./experiments/comparison_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n✓ 实验报告已保存到: {report_file}")
        
        return report
    
    def print_summary(self, report: Dict[str, Any]):
        """打印实验摘要"""
        print("\n" + "="*70)
        print("实验结果摘要")
        print("="*70)
        
        summary = report['summary']
        
        print("\n配置对比:")
        print(f"{'配置':<30} {'平均响应时间':<15} {'平均响应长度':<15}")
        print("-" * 70)
        
        for config_key, stats in summary.items():
            print(f"{stats['config_name']:<30} "
                  f"{stats['avg_response_time']:.2f}秒{'':<10} "
                  f"{stats['avg_response_length']:.0f}字符")
        
        print("\n" + "="*70)
        print("详细结果请查看生成的JSON报告文件")
        print("="*70)


def main():
    """主函数"""
    print("="*70)
    print("心理咨询系统对比实验")
    print("用于论文数据收集和系统评估")
    print("="*70)
    
    # 创建实验运行器
    runner = ExperimentRunner()
    
    # 运行所有实验
    runner.run_all_experiments()
    
    # 生成报告
    report = runner.generate_report()
    
    # 打印摘要
    runner.print_summary(report)
    
    print("\n提示:")
    print("- 实验数据已保存，可用于论文写作")
    print("- 运行 python examples/visualize_results.py 可生成可视化图表")
    print("- 查看 experiments/ 目录获取详细数据")


if __name__ == "__main__":
    main()
