"""
数据映射模块

此模块提供数据源和目标格式之间的映射功能，支持：
- 数据字段映射
- 数据类型转换
- 格式标准化
- 映射规则管理
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Optional, Any, Callable, Union
from datetime import datetime
import json
import pandas as pd
import logging

# 配置日志
logger = logging.getLogger(__name__)


class MappingType(Enum):
    """映射类型枚举"""
    FIELD_TO_FIELD = auto()  # 字段到字段映射
    VALUE_TRANSFORMATION = auto()  # 值转换映射
    AGGREGATION = auto()  # 聚合映射
    FILTERING = auto()  # 过滤映射
    CALCULATION = auto()  # 计算映射


class MappingStatus(Enum):
    """映射状态枚举"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class FieldMapping:
    """字段映射配置"""
    source_field: str
    target_field: str
    transformation_type: MappingType = MappingType.FIELD_TO_FIELD
    transformation_function: Optional[Callable] = None
    default_value: Any = None
    validation_rules: List[Callable] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MappingRule:
    """映射规则"""
    rule_id: str
    name: str
    description: str
    source_format: str
    target_format: str
    field_mappings: List[FieldMapping]
    conditions: List[str] = field(default_factory=list)
    priority: int = 0
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class MappingResult:
    """映射结果"""
    rule_id: str
    source_records: int
    target_records: int
    mapped_records: int
    failed_records: int
    mapping_details: List[Dict[str, Any]]
    errors: List[str]
    warnings: List[str]
    status: MappingStatus
    execution_time: float
    created_at: datetime = field(default_factory=datetime.now)


class DataMapper:
    """数据映射器基类"""
    
    def __init__(self, rule: MappingRule):
        self.rule = rule
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    def apply_mapping(self, data: Any) -> Any:
        """应用映射规则"""
        raise NotImplementedError
    
    def validate_input(self, data: Any) -> bool:
        """验证输入数据"""
        raise NotImplementedError
    
    def transform_value(self, value: Any, mapping: FieldMapping) -> Any:
        """转换单个值"""
        if mapping.transformation_function:
            try:
                return mapping.transformation_function(value)
            except Exception as e:
                self.logger.warning(f"转换函数执行失败: {e}")
                return mapping.default_value if mapping.default_value is not None else value
        
        return value


class DictionaryDataMapper(DataMapper):
    """字典数据映射器"""
    
    def validate_input(self, data: Any) -> bool:
        return isinstance(data, dict)
    
    def apply_mapping(self, data: dict) -> dict:
        result = {}
        errors = []
        
        for mapping in self.rule.field_mappings:
            try:
                if mapping.source_field in data:
                    value = data[mapping.source_field]
                    transformed_value = self.transform_value(value, mapping)
                    result[mapping.target_field] = transformed_value
                elif mapping.default_value is not None:
                    result[mapping.target_field] = mapping.default_value
            except Exception as e:
                error_msg = f"字段 {mapping.source_field} 映射失败: {e}"
                errors.append(error_msg)
                self.logger.error(error_msg)
        
        if errors:
            raise ValueError(f"映射过程中发生错误: {errors}")
        
        return result


class DataFrameMapper(DataMapper):
    """DataFrame数据映射器"""
    
    def validate_input(self, data: Any) -> bool:
        return isinstance(data, pd.DataFrame)
    
    def apply_mapping(self, data: pd.DataFrame) -> pd.DataFrame:
        result_df = pd.DataFrame()
        errors = []
        
        for mapping in self.rule.field_mappings:
            try:
                if mapping.source_field in data.columns:
                    values = data[mapping.source_field]
                    if mapping.transformation_function:
                        transformed_values = values.apply(
                            lambda x: self.transform_value(x, mapping)
                        )
                    else:
                        transformed_values = values
                    
                    result_df[mapping.target_field] = transformed_values
                elif mapping.default_value is not None:
                    result_df[mapping.target_field] = mapping.default_value
            except Exception as e:
                error_msg = f"字段 {mapping.source_field} 映射失败: {e}"
                errors.append(error_msg)
                self.logger.error(error_msg)
        
        if errors:
            raise ValueError(f"映射过程中发生错误: {errors}")
        
        return result_df


class MappingManager:
    """映射管理器"""
    
    def __init__(self):
        self.rules: Dict[str, MappingRule] = {}
        self.mappers: Dict[str, DataMapper] = {}
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    def add_rule(self, rule: MappingRule) -> None:
        """添加映射规则"""
        self.rules[rule.rule_id] = rule
        
        # 根据源数据类型选择映射器
        if hasattr(rule, 'source_type'):
            mapper_class = rule.source_type
        else:
            mapper_class = DictionaryDataMapper  # 默认使用字典映射器
        
        self.mappers[rule.rule_id] = mapper_class(rule)
        self.logger.info(f"已添加映射规则: {rule.rule_id}")
    
    def remove_rule(self, rule_id: str) -> None:
        """移除映射规则"""
        if rule_id in self.rules:
            del self.rules[rule_id]
            if rule_id in self.mappers:
                del self.mappers[rule_id]
            self.logger.info(f"已移除映射规则: {rule_id}")
    
    def get_rule(self, rule_id: str) -> Optional[MappingRule]:
        """获取映射规则"""
        return self.rules.get(rule_id)
    
    def list_rules(self) -> List[MappingRule]:
        """列出所有映射规则"""
        return list(self.rules.values())
    
    def apply_mapping(self, rule_id: str, data: Any) -> Any:
        """应用映射规则"""
        if rule_id not in self.mappers:
            raise ValueError(f"映射规则 {rule_id} 不存在")
        
        mapper = self.mappers[rule_id]
        
        if not mapper.validate_input(data):
            raise ValueError(f"输入数据格式不正确")
        
        return mapper.apply_mapping(data)
    
    def create_field_mapping(self, source_field: str, target_field: str,
                           transformation_type: MappingType = MappingType.FIELD_TO_FIELD,
                           transformation_function: Optional[Callable] = None,
                           default_value: Any = None) -> FieldMapping:
        """创建字段映射"""
        return FieldMapping(
            source_field=source_field,
            target_field=target_field,
            transformation_type=transformation_type,
            transformation_function=transformation_function,
            default_value=default_value
        )
    
    def export_rules(self, file_path: str) -> None:
        """导出映射规则到文件"""
        rules_data = []
        for rule in self.rules.values():
            rule_dict = {
                'rule_id': rule.rule_id,
                'name': rule.name,
                'description': rule.description,
                'source_format': rule.source_format,
                'target_format': rule.target_format,
                'field_mappings': [
                    {
                        'source_field': m.source_field,
                        'target_field': m.target_field,
                        'transformation_type': m.transformation_type.name,
                        'default_value': m.default_value,
                        'metadata': m.metadata
                    }
                    for m in rule.field_mappings
                ],
                'conditions': rule.conditions,
                'priority': rule.priority,
                'is_active': rule.is_active
            }
            rules_data.append(rule_dict)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(rules_data, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"映射规则已导出到: {file_path}")
    
    def import_rules(self, file_path: str) -> None:
        """从文件导入映射规则"""
        with open(file_path, 'r', encoding='utf-8') as f:
            rules_data = json.load(f)
        
        for rule_dict in rules_data:
            # 重建字段映射
            field_mappings = []
            for m_dict in rule_dict['field_mappings']:
                mapping = FieldMapping(
                    source_field=m_dict['source_field'],
                    target_field=m_dict['target_field'],
                    transformation_type=MappingType[m_dict['transformation_type']],
                    default_value=m_dict['default_value'],
                    metadata=m_dict['metadata']
                )
                field_mappings.append(mapping)
            
            # 创建映射规则
            rule = MappingRule(
                rule_id=rule_dict['rule_id'],
                name=rule_dict['name'],
                description=rule_dict['description'],
                source_format=rule_dict['source_format'],
                target_format=rule_dict['target_format'],
                field_mappings=field_mappings,
                conditions=rule_dict.get('conditions', []),
                priority=rule_dict.get('priority', 0),
                is_active=rule_dict.get('is_active', True)
            )
            
            self.add_rule(rule)
        
        self.logger.info(f"已从 {file_path} 导入 {len(rules_data)} 个映射规则")


# 便捷函数
def create_simple_mapping(rule_id: str, source_format: str, target_format: str,
                        mappings: List[tuple]) -> MappingRule:
    """创建简单映射规则"""
    field_mappings = []
    for source_field, target_field in mappings:
        field_mappings.append(FieldMapping(
            source_field=source_field,
            target_field=target_field
        ))
    
    return MappingRule(
        rule_id=rule_id,
        name=f"{source_format} to {target_format} mapping",
        description=f"简单的字段映射规则",
        source_format=source_format,
        target_format=target_format,
        field_mappings=field_mappings
    )


def create_dataframe_mapping(rule_id: str, source_columns: List[str],
                           target_columns: List[str]) -> MappingRule:
    """创建DataFrame列映射"""
    if len(source_columns) != len(target_columns):
        raise ValueError("源列和目标列数量必须相同")
    
    field_mappings = []
    for source_col, target_col in zip(source_columns, target_columns):
        field_mappings.append(FieldMapping(
            source_field=source_col,
            target_field=target_col
        ))
    
    return MappingRule(
        rule_id=rule_id,
        name=f"DataFrame column mapping {rule_id}",
        description="DataFrame列映射规则",
        source_format="dataframe",
        target_format="dataframe",
        field_mappings=field_mappings
    )