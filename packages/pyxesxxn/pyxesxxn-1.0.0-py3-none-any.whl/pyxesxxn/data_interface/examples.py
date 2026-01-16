"""
数据接口模块示例

此文件包含数据接口各组件的使用示例和最佳实践
"""

from typing import Dict, Any, List
import pandas as pd
from datetime import datetime, timedelta

from .data_import import (
    ImportConfiguration, FileDataImporter, DatabaseDataImporter, APIDataImporter,
    create_file_importer, create_database_importer, create_api_importer
)
from .data_export import (
    ExportConfiguration, FileDataExporter, DatabaseDataExporter, APIDataExporter,
    create_file_exporter, create_database_exporter, create_api_exporter
)
from .data_validation import (
    ValidationManager, CompletenessValidator, TypeValidator, BusinessRuleValidator,
    create_validation_manager, quick_validate
)
from .data_mapping import (
    MappingManager, MappingRule, FieldMapping, MappingType,
    create_simple_mapping, create_dataframe_mapping
)


def example_file_import_export():
    """文件导入导出示例"""
    print("=== 文件导入导出示例 ===")
    
    # 创建导入配置
    import_config = ImportConfiguration(
        source_type="csv",
        file_path="example_data.csv",
        encoding="utf-8",
        delimiter=",",
        skip_rows=1,
        column_mapping={
            "timestamp": "datetime",
            "value": "float",
            "category": "string"
        }
    )
    
    # 创建导出配置
    export_config = ExportConfiguration(
        target_format="excel",
        file_path="output.xlsx",
        include_headers=True,
        compression="gzip"
    )
    
    # 创建导入导出器
    importer = create_file_importer(import_config)
    exporter = create_file_exporter(export_config)
    
    print(f"导入配置: {import_config}")
    print(f"导出配置: {export_config}")
    
    return importer, exporter


def example_database_import():
    """数据库导入示例"""
    print("=== 数据库导入示例 ===")
    
    # 数据库配置
    db_config = {
        "host": "localhost",
        "port": 5432,
        "database": "energy_data",
        "username": "user",
        "password": "password",
        "table": "renewable_energy",
        "query": "SELECT * FROM renewable_energy WHERE year >= 2020"
    }
    
    # 创建数据库导入器
    db_importer = DatabaseDataImporter(db_config)
    
    # 执行导入
    import_result = db_importer.import_data()
    
    print(f"导入结果: {import_result.records_imported} 条记录")
    print(f"导入状态: {import_result.status}")
    
    return db_importer, import_result


def example_api_import():
    """API导入示例"""
    print("=== API导入示例 ===")
    
    # API配置
    api_config = {
        "base_url": "https://api.energy.org/v1",
        "endpoint": "/renewable-capacity",
        "method": "GET",
        "headers": {
            "Authorization": "Bearer token123",
            "Content-Type": "application/json"
        },
        "params": {
            "country": "CN",
            "year_from": 2020,
            "year_to": 2023
        },
        "timeout": 30,
        "retry_attempts": 3
    }
    
    # 创建API导入器
    api_importer = APIDataImporter(api_config)
    
    # 执行导入
    import_result = api_importer.import_data()
    
    print(f"导入结果: {import_result.records_imported} 条记录")
    print(f"API响应状态: {import_result.metadata.get('status_code', 'N/A')}")
    
    return api_importer, import_result


def example_data_validation():
    """数据验证示例"""
    print("=== 数据验证示例 ===")
    
    # 创建测试数据
    test_data = pd.DataFrame({
        "timestamp": ["2023-01-01", "2023-01-02", "invalid_date", "2023-01-04"],
        "value": [100.5, 200.0, -50.0, 300.0],
        "category": ["solar", "wind", "solar", "hydro"]
    })
    
    # 快速验证
    quick_result = quick_validate(test_data)
    print(f"快速验证结果: {quick_result.is_valid}")
    print(f"验证错误数: {len(quick_result.errors)}")
    
    # 创建详细验证管理器
    validator = create_validation_manager([
        CompletenessValidator({"timestamp": "required", "value": "required"}),
        TypeValidator({"timestamp": "datetime", "value": "float", "category": "string"}),
        BusinessRuleValidator([
            ("value", lambda x: x >= 0, "数值必须非负"),
            ("category", lambda x: x in ["solar", "wind", "hydro"], "类别必须为有效值")
        ])
    ])
    
    # 执行详细验证
    detailed_result = validator.validate_data(test_data)
    
    print(f"详细验证结果: {detailed_result.overall_valid}")
    print(f"验证指标:")
    print(f"  完整性: {detailed_result.completeness_score:.2f}")
    print(f"  一致性: {detailed_result.consistency_score:.2f}")
    print(f"  准确性: {detailed_result.accuracy_score:.2f}")
    
    return validator, detailed_result


def example_data_mapping():
    """数据映射示例"""
    print("=== 数据映射示例 ===")
    
    # 创建映射管理器
    mapper = MappingManager()
    
    # 创建简单的字段映射规则
    simple_mapping = create_simple_mapping(
        rule_id="energy_data_mapping",
        source_format="csv",
        target_format="pypsa_network",
        mappings=[
            ("timestamp", "datetime"),
            ("solar_capacity", "solar_p_nom"),
            ("wind_capacity", "wind_p_nom"),
            ("load_demand", "load_p_set")
        ]
    )
    
    # 添加映射规则
    mapper.add_rule(simple_mapping)
    
    # 创建测试数据
    source_data = {
        "timestamp": "2023-01-01 00:00:00",
        "solar_capacity": 100.0,
        "wind_capacity": 200.0,
        "load_demand": 150.0
    }
    
    # 应用映射
    try:
        mapped_data = mapper.apply_mapping("energy_data_mapping", source_data)
        print(f"原始数据: {source_data}")
        print(f"映射结果: {mapped_data}")
    except Exception as e:
        print(f"映射失败: {e}")
    
    # DataFrame映射示例
    df_source = pd.DataFrame({
        "node_id": ["node1", "node2", "node3"],
        "gen_capacity": [100, 200, 150],
        "gen_type": ["solar", "wind", "hydro"]
    })
    
    df_mapping = create_dataframe_mapping(
        rule_id="network_mapping",
        source_columns=["node_id", "gen_capacity", "gen_type"],
        target_columns=["name", "p_nom", "carrier"]
    )
    
    mapper.add_rule(df_mapping)
    
    try:
        mapped_df = mapper.apply_mapping("network_mapping", df_source)
        print(f"DataFrame映射结果:")
        print(mapped_df)
    except Exception as e:
        print(f"DataFrame映射失败: {e}")
    
    return mapper


def example_comprehensive_workflow():
    """完整数据处理工作流示例"""
    print("=== 完整数据处理工作流 ===")
    
    # 1. 导入数据
    importer = create_file_importer(ImportConfiguration(
        source_type="csv",
        file_path="energy_data.csv",
        encoding="utf-8"
    ))
    
    # 2. 验证数据
    validator = create_validation_manager([
        CompletenessValidator(),
        TypeValidator()
    ])
    
    # 3. 数据映射
    mapper = MappingManager()
    mapping_rule = create_simple_mapping(
        rule_id="workflow_mapping",
        source_format="csv",
        target_format="network",
        mappings=[("capacity", "p_nom"), ("type", "carrier")]
    )
    mapper.add_rule(mapping_rule)
    
    # 4. 导出数据
    exporter = create_file_exporter(ExportConfiguration(
        target_format="json",
        file_path="processed_data.json"
    ))
    
    print("工作流组件已创建:")
    print(f"  数据导入器: {importer}")
    print(f"  数据验证器: {validator}")
    print(f"  数据映射器: {mapper}")
    print(f"  数据导出器: {exporter}")
    
    return {
        "importer": importer,
        "validator": validator,
        "mapper": mapper,
        "exporter": exporter
    }


def example_error_handling():
    """错误处理示例"""
    print("=== 错误处理示例 ===")
    
    # 创建带有错误处理的数据处理器
    try:
        # 尝试导入不存在的文件
        importer = create_file_importer(ImportConfiguration(
            source_type="csv",
            file_path="nonexistent_file.csv"
        ))
        
        result = importer.import_data()
        print(f"导入成功: {result.records_imported} 条记录")
        
    except FileNotFoundError as e:
        print(f"文件未找到: {e}")
    except Exception as e:
        print(f"导入失败: {e}")
    
    # 数据验证错误处理
    try:
        invalid_data = pd.DataFrame({
            "timestamp": ["invalid_date"],
            "value": ["not_a_number"]
        })
        
        result = quick_validate(invalid_data)
        if not result.is_valid:
            print(f"验证失败:")
            for error in result.errors:
                print(f"  - {error}")
    
    except Exception as e:
        print(f"验证过程出错: {e}")


# 配置文件示例
DEFAULT_IMPORT_CONFIGS = {
    "csv_energy": ImportConfiguration(
        source_type="csv",
        encoding="utf-8",
        delimiter=",",
        skip_rows=0,
        column_mapping={
            "datetime": "timestamp",
            "solar_mw": "solar_capacity",
            "wind_mw": "wind_capacity"
        }
    ),
    "api_renewable": ImportConfiguration(
        source_type="api",
        timeout=30,
        retry_attempts=3,
        headers={"Accept": "application/json"}
    ),
    "database_standard": ImportConfiguration(
        source_type="database",
        batch_size=1000,
        use_transactions=True
    )
}

DEFAULT_EXPORT_CONFIGS = {
    "json_network": ExportConfiguration(
        target_format="json",
        include_metadata=True,
        compression="gzip"
    ),
    "excel_report": ExportConfiguration(
        target_format="excel",
        include_headers=True,
        sheet_name="NetworkData"
    ),
    "csv_standard": ExportConfiguration(
        target_format="csv",
        encoding="utf-8",
        delimiter=","
    )
}

DEFAULT_VALIDATION_CONFIGS = {
    "energy_data": [
        CompletenessValidator({
            "timestamp": "required",
            "capacity": "required",
            "type": "required"
        }),
        TypeValidator({
            "timestamp": "datetime",
            "capacity": "float",
            "type": "string"
        }),
        BusinessRuleValidator([
            ("capacity", lambda x: x >= 0, "容量必须非负"),
            ("type", lambda x: x in ["solar", "wind", "hydro"], "类型必须为有效能源类型")
        ])
    ],
    "network_data": [
        CompletenessValidator(),
        TypeValidator(),
        BusinessRuleValidator([
            ("p_nom", lambda x: x > 0, "额定功率必须为正数"),
            ("v_nom", lambda x: 0.9 <= x <= 1.1, "额定电压应在合理范围内")
        ])
    ]
}

# 使用示例的便利函数
def get_example_importer(config_name: str = "csv_energy"):
    """获取示例导入器"""
    config = DEFAULT_IMPORT_CONFIGS.get(config_name)
    if config:
        return create_file_importer(config)
    return None

def get_example_exporter(config_name: str = "json_network"):
    """获取示例导出器"""
    config = DEFAULT_EXPORT_CONFIGS.get(config_name)
    if config:
        return create_file_exporter(config)
    return None

def get_example_validator(config_name: str = "energy_data"):
    """获取示例验证器"""
    rules = DEFAULT_VALIDATION_CONFIGS.get(config_name, [])
    return create_validation_manager(rules)


if __name__ == "__main__":
    print("数据接口模块示例")
    print("=================")
    
    # 运行各种示例
    example_file_import_export()
    print()
    
    example_database_import()
    print()
    
    example_api_import()
    print()
    
    example_data_validation()
    print()
    
    example_data_mapping()
    print()
    
    example_comprehensive_workflow()
    print()
    
    example_error_handling()
    print()
    
    print("所有示例执行完成！")