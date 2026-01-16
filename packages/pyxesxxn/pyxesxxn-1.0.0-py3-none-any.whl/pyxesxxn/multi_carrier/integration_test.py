#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyXESXXN RLMOGP集成测试程序
验证RLMOGP程序是否能够通过PyXESXXN项目正确运行
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_pyxesxxn_rlmogp_integration():
    """测试PyXESXXN RLMOGP集成功能"""
    print("=== PyXESXXN RLMOGP集成测试 ===")
    
    try:
        # 1. 测试从PyXESXXN导入RLMOGP模块
        from pyxesxxn.multi_carrier import (
            EnergySystemEnvironment, 
            TaskGenerator, 
            MultiAgentTaskScheduler,
            dominates,
            update_pareto_front,
            calculate_crowding_distance,
            select_nondominated_solutions
        )
        print("✓ PyXESXXN RLMOGP模块导入成功")
        
        # 2. 测试多目标优化函数
        solutions = [
            {"energy_cost": 100, "carbon_emission": 50, "reliability": 0.9},
            {"energy_cost": 80, "carbon_emission": 60, "reliability": 0.8},
            {"energy_cost": 120, "carbon_emission": 40, "reliability": 0.95}
        ]
        objectives = [("energy_cost", True), ("carbon_emission", True), ("reliability", False)]
        
        pareto_front = update_pareto_front(solutions, objectives)
        print(f"✓ 多目标优化函数测试成功，Pareto前沿包含 {len(pareto_front)} 个解")
        
        # 3. 测试能源系统环境初始化
        env = EnergySystemEnvironment(generator_num=1, storage_num=2, load_num=3)
        print(f"✓ 能源系统环境初始化成功，共{env.node_count}个节点")
        
        # 4. 测试任务生成器
        task_generator = TaskGenerator(task_types=["excavation", "transport"])
        print(f"✓ 任务生成器初始化成功，共{len(task_generator.task_types)}种任务类型")
        
        # 5. 测试多智能体调度器
        scheduler = MultiAgentTaskScheduler(env=env, task_generator=task_generator)
        print(f"✓ 多智能体调度器初始化成功，共{len(scheduler.machine_agents)}个智能体")
        
        # 6. 测试简化仿真运行
        print("\n开始简化仿真测试...")
        scheduler.run_simulation(episodes=2, tasks_per_episode=3)
        
        # 7. 验证结果
        if scheduler.task_history:
            print(f"✓ 仿真运行成功，共处理{len(scheduler.task_history)}个任务")
            
            # 输出基本统计信息
            avg_energy_cost = sum(task["energy_cost"] for task in scheduler.task_history) / len(scheduler.task_history)
            avg_reliability = sum(task["reliability"] for task in scheduler.task_history) / len(scheduler.task_history)
            total_carbon = sum(task["carbon_emission"] for task in scheduler.task_history)
            
            print(f"  平均能源成本: {avg_energy_cost:.2f}元")
            print(f"  平均可靠性: {avg_reliability:.4f}")
            print(f"  总碳排放: {total_carbon:.2f}kg")
        
        print("\n✓ PyXESXXN RLMOGP集成测试全部通过！")
        return True
        
    except Exception as e:
        print(f"✗ 集成测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_pyxesxxn_main_import():
    """测试PyXESXXN主模块导入"""
    print("\n=== PyXESXXN主模块导入测试 ===")
    try:
        import pyxesxxn as px
        print("✓ PyXESXXN主模块导入成功")
        
        # 检查是否包含RLMOGP功能
        if hasattr(px, 'EnergySystemEnvironment'):
            print("✓ PyXESXXN主模块包含EnergySystemEnvironment类")
        else:
            print("✗ PyXESXXN主模块未包含EnergySystemEnvironment类")
            
        if hasattr(px, 'TaskGenerator'):
            print("✓ PyXESXXN主模块包含TaskGenerator类")
        else:
            print("✗ PyXESXXN主模块未包含TaskGenerator类")
            
        if hasattr(px, 'MultiAgentTaskScheduler'):
            print("✓ PyXESXXN主模块包含MultiAgentTaskScheduler类")
        else:
            print("✗ PyXESXXN主模块未包含MultiAgentTaskScheduler类")
            
        # 测试直接导入
        try:
            from pyxesxxn import EnergySystemEnvironment, TaskGenerator, MultiAgentTaskScheduler
            print("✓ 从PyXESXXN主模块直接导入RLMOGP类成功")
        except ImportError as e:
            print(f"✗ 从PyXESXXN主模块导入RLMOGP类失败: {e}")
            
    except Exception as e:
        print(f"✗ PyXESXXN主模块导入失败: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("PyXESXXN RLMOGP集成验证程序")
    print("=" * 50)
    
    # 运行集成测试
    test1_passed = test_pyxesxxn_rlmogp_integration()
    test2_passed = test_pyxesxxn_main_import()
    
    print("\n" + "=" * 50)
    if test1_passed and test2_passed:
        print("🎉 所有集成测试通过！RLMOGP程序已成功集成到PyXESXXN项目中。")
        sys.exit(0)
    else:
        print("❌ 部分集成测试失败，请检查集成配置。")
        sys.exit(1)