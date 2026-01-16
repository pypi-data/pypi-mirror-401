#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化测试版本：验证RLMOGP程序是否正常工作
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from RLMOGP import EnergySystemEnvironment, TaskGenerator, MultiAgentTaskScheduler

def test_rlmogp():
    """测试RLMOGP程序的基本功能"""
    print("=== 开始RLMOGP简化测试 ===")
    
    # 1. 初始化能源系统环境（简化配置）
    env = EnergySystemEnvironment(generator_num=1, storage_num=2, load_num=3)
    print(f"✓ 能源系统环境初始化完成，共{env.node_count}个节点")
    
    # 2. 初始化任务生成器
    task_generator = TaskGenerator(task_types=["excavation", "transport"])
    print(f"✓ 任务生成器初始化完成，共{len(task_generator.task_types)}种任务类型")
    
    # 3. 初始化多智能体任务调度器
    scheduler = MultiAgentTaskScheduler(env=env, task_generator=task_generator)
    print(f"✓ 多智能体调度器初始化完成，共{len(scheduler.machine_agents)}个智能体")
    
    # 4. 运行简化仿真（只运行3个Episode，每个Episode5个任务）
    print("\n开始简化仿真测试...")
    scheduler.run_simulation(episodes=3, tasks_per_episode=5)
    
    # 5. 输出基本统计信息
    print("\n=== 测试结果摘要 ===")
    print(f"总任务数: {len(scheduler.task_history)}")
    
    if scheduler.task_history:
        avg_energy_cost = sum(task["energy_cost"] for task in scheduler.task_history) / len(scheduler.task_history)
        avg_reliability = sum(task["reliability"] for task in scheduler.task_history) / len(scheduler.task_history)
        total_carbon = sum(task["carbon_emission"] for task in scheduler.task_history)
        budget_exceed_rate = sum(task["budget_exceeded"] for task in scheduler.task_history) / len(scheduler.task_history)
        
        print(f"平均能源成本: {avg_energy_cost:.2f}元")
        print(f"平均可靠性: {avg_reliability:.4f}")
        print(f"总碳排放: {total_carbon:.2f}kg")
        print(f"预算超出率: {budget_exceed_rate:.2%}")
    
    print("\n✓ RLMOGP程序测试完成，基本功能正常！")
    return True

if __name__ == "__main__":
    try:
        test_rlmogp()
    except Exception as e:
        print(f"✗ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)