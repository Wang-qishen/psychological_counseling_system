"""
记忆系统测试数据生成器

生成用于测试三层记忆架构的测试数据：
- 多会话连续性测试
- 个性化信息记忆测试
- 跨会话信息召回测试
"""

import json
import random
import logging
from typing import List, Dict, Optional
from pathlib import Path
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class MemoryTestGenerator:
    """记忆测试数据生成器"""
    
    # 测试场景模板
    SCENARIO_TEMPLATES = [
        {
            "name": "personal_info_recall",
            "description": "个人信息记忆测试",
            "sessions": [
                {
                    "session_id": 1,
                    "user_input": "我叫{name}，今年{age}岁，是一名{job}。",
                    "expected_memory": ["name:{name}", "age:{age}", "job:{job}"]
                },
                {
                    "session_id": 2,
                    "user_input": "我最近工作压力很大。",
                    "query": "请问我叫什么名字？",
                    "expected_recall": "name:{name}"
                },
                {
                    "session_id": 3,
                    "user_input": "我还是很焦虑。",
                    "query": "你还记得我的职业吗？",
                    "expected_recall": "job:{job}"
                }
            ]
        },
        {
            "name": "emotional_state_tracking",
            "description": "情绪状态跟踪测试",
            "sessions": [
                {
                    "session_id": 1,
                    "user_input": "我最近感到{emotion1}，因为{reason1}。",
                    "expected_memory": ["emotion:{emotion1}", "reason:{reason1}"]
                },
                {
                    "session_id": 2,
                    "user_input": "现在我感觉{emotion2}了。",
                    "query": "我上次的情绪是什么？",
                    "expected_recall": "emotion:{emotion1}"
                }
            ]
        },
        {
            "name": "problem_solving_continuity",
            "description": "问题解决连续性测试",
            "sessions": [
                {
                    "session_id": 1,
                    "user_input": "我遇到了{problem}，想请你帮我。",
                    "expected_memory": ["problem:{problem}"]
                },
                {
                    "session_id": 2,
                    "user_input": "关于上次的问题，我试了你的建议。",
                    "query": "上次我提到的问题是什么？",
                    "expected_recall": "problem:{problem}"
                },
                {
                    "session_id": 3,
                    "user_input": "现在情况有所改善。",
                    "query": "我们之前讨论的问题解决了吗？",
                    "expected_context": "problem:{problem}"
                }
            ]
        }
    ]
    
    # 填充数据
    FILL_DATA = {
        "names": ["小明", "小红", "小李", "小张", "小王"],
        "ages": ["25", "30", "28", "35", "26"],
        "jobs": ["程序员", "教师", "医生", "设计师", "销售"],
        "emotion1": ["焦虑", "抑郁", "压力大", "失眠", "烦躁"],
        "emotion2": ["好多了", "轻松一些", "平静", "舒服"],
        "reason1": ["工作压力", "人际关系", "家庭问题", "学业困难"],
        "problems": ["失眠", "社交焦虑", "拖延症", "情绪管理", "人际冲突"]
    }
    
    def __init__(self, output_dir: str = "./data/memory_tests"):
        """
        初始化
        
        Args:
            output_dir: 输出目录
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_test_case(
        self,
        scenario_template: Dict,
        case_id: int
    ) -> Dict:
        """
        生成单个测试用例
        
        Args:
            scenario_template: 场景模板
            case_id: 用例ID
            
        Returns:
            测试用例字典
        """
        # 随机填充数据
        filled_data = {}
        for key, values in self.FILL_DATA.items():
            filled_data[key] = random.choice(values)
        
        # 填充模板
        sessions = []
        for session_template in scenario_template["sessions"]:
            session = {
                "session_id": session_template["session_id"],
                "user_id": f"test_user_{case_id}"
            }
            
            # 填充user_input
            if "user_input" in session_template:
                session["user_input"] = session_template["user_input"].format(**filled_data)
            
            # 填充expected_memory
            if "expected_memory" in session_template:
                session["expected_memory"] = [
                    mem.format(**filled_data) for mem in session_template["expected_memory"]
                ]
            
            # 填充query
            if "query" in session_template:
                session["query"] = session_template["query"].format(**filled_data)
            
            # 填充expected_recall
            if "expected_recall" in session_template:
                session["expected_recall"] = session_template["expected_recall"].format(**filled_data)
            
            # 填充expected_context
            if "expected_context" in session_template:
                session["expected_context"] = session_template["expected_context"].format(**filled_data)
            
            sessions.append(session)
        
        return {
            "case_id": case_id,
            "scenario": scenario_template["name"],
            "description": scenario_template["description"],
            "sessions": sessions,
            "metadata": filled_data
        }
    
    def generate_test_suite(
        self,
        num_cases_per_scenario: int = 20,
        output_filename: str = "memory_test_suite.json"
    ) -> List[Dict]:
        """
        生成完整测试套件
        
        Args:
            num_cases_per_scenario: 每个场景生成的用例数
            output_filename: 输出文件名
            
        Returns:
            测试套件列表
        """
        test_suite = []
        case_id = 1
        
        for template in self.SCENARIO_TEMPLATES:
            logger.info(f"Generating test cases for scenario: {template['name']}")
            
            for _ in range(num_cases_per_scenario):
                test_case = self.generate_test_case(template, case_id)
                test_suite.append(test_case)
                case_id += 1
        
        # 保存到文件
        output_path = self.output_dir / output_filename
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(test_suite, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Generated {len(test_suite)} test cases, saved to {output_path}")
        
        return test_suite
    
    def generate_recall_test_cases(
        self,
        num_cases: int = 50,
        output_filename: str = "memory_recall_tests.json"
    ) -> List[Dict]:
        """
        生成记忆召回测试用例
        
        Args:
            num_cases: 用例数量
            output_filename: 输出文件名
            
        Returns:
            测试用例列表
        """
        test_cases = []
        
        for i in range(num_cases):
            user_id = f"test_user_{i}"
            
            # 随机选择信息类型
            info_type = random.choice(["name", "age", "job", "emotion", "problem"])
            
            if info_type == "name":
                value = random.choice(self.FILL_DATA["names"])
                query = "请问我叫什么名字？"
                expected = f"name:{value}"
            elif info_type == "age":
                value = random.choice(self.FILL_DATA["ages"])
                query = "你还记得我多大吗？"
                expected = f"age:{value}"
            elif info_type == "job":
                value = random.choice(self.FILL_DATA["jobs"])
                query = "你还记得我的职业吗？"
                expected = f"job:{value}"
            elif info_type == "emotion":
                value = random.choice(self.FILL_DATA["emotion1"])
                query = "我上次的情绪状态是什么？"
                expected = f"emotion:{value}"
            else:  # problem
                value = random.choice(self.FILL_DATA["problems"])
                query = "我之前提到的问题是什么？"
                expected = f"problem:{value}"
            
            test_cases.append({
                "user_id": user_id,
                "query": query,
                "expected_info": expected,
                "memory_type": "all"
            })
        
        # 保存到文件
        output_path = self.output_dir / output_filename
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(test_cases, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Generated {len(test_cases)} recall test cases, saved to {output_path}")
        
        return test_cases
    
    def generate_consistency_test_cases(
        self,
        num_users: int = 10,
        output_filename: str = "memory_consistency_tests.json"
    ) -> List[Dict]:
        """
        生成记忆一致性测试用例
        
        Args:
            num_users: 用户数量
            output_filename: 输出文件名
            
        Returns:
            测试用例列表
        """
        test_cases = []
        
        for i in range(num_users):
            test_cases.append({
                "user_id": f"test_user_{i}",
                "session_count": 5
            })
        
        # 保存到文件
        output_path = self.output_dir / output_filename
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(test_cases, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Generated {len(test_cases)} consistency test cases, saved to {output_path}")
        
        return test_cases
    
    def generate_all_tests(
        self,
        num_cases_per_scenario: int = 20,
        num_recall_cases: int = 50,
        num_consistency_users: int = 10
    ) -> Dict[str, List[Dict]]:
        """
        生成所有记忆测试数据
        
        Args:
            num_cases_per_scenario: 每个场景的用例数
            num_recall_cases: 召回测试用例数
            num_consistency_users: 一致性测试用户数
            
        Returns:
            所有测试数据的字典
        """
        logger.info("Generating all memory test data...")
        
        return {
            "test_suite": self.generate_test_suite(num_cases_per_scenario),
            "recall_tests": self.generate_recall_test_cases(num_recall_cases),
            "consistency_tests": self.generate_consistency_test_cases(num_consistency_users)
        }


def generate_memory_tests(
    output_dir: str = "./data/memory_tests",
    num_cases_per_scenario: int = 20
) -> Dict[str, List[Dict]]:
    """
    便捷函数：生成记忆测试数据
    
    Args:
        output_dir: 输出目录
        num_cases_per_scenario: 每个场景的用例数
        
    Returns:
        所有测试数据
    """
    generator = MemoryTestGenerator(output_dir)
    return generator.generate_all_tests(num_cases_per_scenario)
