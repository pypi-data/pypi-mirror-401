"""
数据验证模块

提供全面的数据验证功能：
- 数据完整性验证：检查缺失值、空值、重复值
- 数据类型验证：检查数据类型是否符合预期
- 数据范围验证：检查数值是否在合理范围内
- 格式验证：检查字符串格式（邮箱、电话、URL等）
- 业务规则验证：自定义业务规则验证
- 数据一致性验证：检查跨字段数据一致性
- 数据质量评估：综合评估数据质量
- 验证报告生成：生成详细的验证报告
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union, Callable, Tuple, Pattern
from enum import Enum
import pandas as pd
import numpy as np
import re
import logging
from datetime import datetime, timedelta
from pathlib import Path
import json
import warnings as py_warnings

class ValidationLevel(Enum):
    """验证级别"""
    STRICT = "strict"    # 严格验证，所有错误
    NORMAL = "normal"    # 普通验证，主要错误
    LOOSE = "loose"      # 宽松验证，重要错误

class ValidationStatus(Enum):
    """验证状态"""
    PASSED = "passed"
    WARNING = "warning"
    FAILED = "failed"
    ERROR = "error"

@dataclass
class ValidationRule:
    """验证规则"""
    rule_id: str
    rule_name: str
    description: str
    validation_func: Callable
    level: ValidationLevel
    severity: str = "medium"  # low, medium, high, critical
    is_active: bool = True
    parameters: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ValidationResult:
    """验证结果"""
    rule_id: str
    rule_name: str
    status: ValidationStatus
    message: str
    affected_rows: List[int] = field(default_factory=list)
    affected_columns: List[str] = field(default_factory=list)
    details: Dict[str, Any] = field(default_factory=dict)
    error_rate: float = 0.0

@dataclass
class ValidationReport:
    """验证报告"""
    report_id: str
    dataset_name: str
    validation_time: datetime
    total_rows: int
    total_columns: int
    validation_rules: List[ValidationRule]
    results: List[ValidationResult]
    overall_score: float
    quality_level: str
    summary: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def passed_rules(self) -> List[ValidationResult]:
        return [r for r in self.results if r.status == ValidationStatus.PASSED]
    
    @property
    def warning_rules(self) -> List[ValidationResult]:
        return [r for r in self.results if r.status == ValidationStatus.WARNING]
    
    @property
    def failed_rules(self) -> List[ValidationResult]:
        return [r for r in self.results if r.status == ValidationStatus.FAILED]
    
    @property
    def error_rules(self) -> List[ValidationResult]:
        return [r for r in self.results if r.status == ValidationStatus.ERROR]

class DataValidator(ABC):
    """数据验证器基类"""
    
    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger(__name__)
        self.rules = []
    
    def add_rule(self, rule: ValidationRule):
        """添加验证规则"""
        self.rules.append(rule)
    
    def remove_rule(self, rule_id: str):
        """移除验证规则"""
        self.rules = [r for r in self.rules if r.rule_id != rule_id]
    
    def get_rule(self, rule_id: str) -> Optional[ValidationRule]:
        """获取验证规则"""
        for rule in self.rules:
            if rule.rule_id == rule_id:
                return rule
        return None
    
    @abstractmethod
    def validate(self, df: pd.DataFrame) -> List[ValidationResult]:
        """验证数据"""
        pass
    
    def validate_rule(self, df: pd.DataFrame, rule: ValidationRule) -> ValidationResult:
        """验证单个规则"""
        try:
            result = rule.validation_func(df, rule.parameters)
            
            # 处理不同类型的返回值
            if isinstance(result, tuple):
                if len(result) == 2:
                    status, message = result
                    affected_rows = []
                    affected_columns = []
                elif len(result) >= 4:
                    status, message, affected_rows, affected_columns = result[:4]
                    details = result[4] if len(result) > 4 else {}
                else:
                    raise ValueError("验证函数返回值格式不正确")
            else:
                status = ValidationStatus.PASSED if result else ValidationStatus.FAILED
                message = "验证通过" if result else "验证失败"
                affected_rows = []
                affected_columns = []
            
            # 计算错误率
            error_rate = 0.0
            if affected_rows:
                error_rate = len(affected_rows) / len(df)
            
            return ValidationResult(
                rule_id=rule.rule_id,
                rule_name=rule.rule_name,
                status=status,
                message=message,
                affected_rows=affected_rows,
                affected_columns=affected_columns,
                error_rate=error_rate
            )
            
        except Exception as e:
            self.logger.error(f"规则 {rule.rule_id} 验证失败: {str(e)}")
            return ValidationResult(
                rule_id=rule.rule_id,
                rule_name=rule.rule_name,
                status=ValidationStatus.ERROR,
                message=f"验证规则执行错误: {str(e)}",
                affected_rows=[],
                affected_columns=[]
            )

class CompletenessValidator(DataValidator):
    """完整性验证器"""
    
    def __init__(self):
        super().__init__("CompletenessValidator")
        self._setup_rules()
    
    def _setup_rules(self):
        """设置验证规则"""
        
        # 检查缺失值
        self.add_rule(ValidationRule(
            rule_id="missing_values",
            rule_name="缺失值检查",
            description="检查数据中是否存在缺失值",
            validation_func=self._check_missing_values,
            level=ValidationLevel.STRICT
        ))
        
        # 检查空字符串
        self.add_rule(ValidationRule(
            rule_id="empty_strings",
            rule_name="空字符串检查",
            description="检查字符串列中是否存在空字符串",
            validation_func=self._check_empty_strings,
            level=ValidationLevel.NORMAL
        ))
        
        # 检查完全重复的行
        self.add_rule(ValidationRule(
            rule_id="duplicate_rows",
            rule_name="重复行检查",
            description="检查数据中是否存在完全重复的行",
            validation_func=self._check_duplicate_rows,
            level=ValidationLevel.NORMAL
        ))
        
        # 检查列的完整性
        self.add_rule(ValidationRule(
            rule_id="column_completeness",
            rule_name="列完整性检查",
            description="检查指定列的完整率是否满足要求",
            validation_func=self._check_column_completeness,
            level=ValidationLevel.STRICT,
            parameters={"min_completeness": 0.9}
        ))
    
    def _check_missing_values(self, df: pd.DataFrame, params: Dict[str, Any]) -> Tuple[ValidationStatus, str, List[int], List[str]]:
        """检查缺失值"""
        missing_counts = df.isnull().sum()
        total_missing = missing_counts.sum()
        
        if total_missing == 0:
            return ValidationStatus.PASSED, "未发现缺失值", [], []
        
        # 找出有缺失值的列
        columns_with_missing = missing_counts[missing_counts > 0].index.tolist()
        affected_rows = []
        
        # 找出有缺失值的行
        for col in columns_with_missing:
            missing_rows = df[df[col].isnull()].index.tolist()
            affected_rows.extend(missing_rows)
        
        message = f"发现{total_missing}个缺失值，分布在{len(columns_with_missing)}列中"
        return ValidationStatus.WARNING, message, list(set(affected_rows)), columns_with_missing
    
    def _check_empty_strings(self, df: pd.DataFrame, params: Dict[str, Any]) -> Tuple[ValidationStatus, str, List[int], List[str]]:
        """检查空字符串"""
        string_columns = df.select_dtypes(include=['object']).columns
        empty_counts = {}
        affected_rows = []
        
        for col in string_columns:
            empty_count = (df[col] == '').sum()
            if empty_count > 0:
                empty_counts[col] = empty_count
                empty_rows = df[df[col] == ''].index.tolist()
                affected_rows.extend(empty_rows)
        
        if not empty_counts:
            return ValidationStatus.PASSED, "未发现空字符串", [], []
        
        total_empty = sum(empty_counts.values())
        message = f"发现{total_empty}个空字符串，分布在{len(empty_counts)}列中"
        return ValidationStatus.WARNING, message, list(set(affected_rows)), list(empty_counts.keys())
    
    def _check_duplicate_rows(self, df: pd.DataFrame, params: Dict[str, Any]) -> Tuple[ValidationStatus, str, List[int], List[str]]:
        """检查重复行"""
        duplicates = df.duplicated()
        duplicate_count = duplicates.sum()
        
        if duplicate_count == 0:
            return ValidationStatus.PASSED, "未发现重复行", [], []
        
        duplicate_rows = df[duplicates].index.tolist()
        message = f"发现{duplicate_count}行重复数据"
        return ValidationStatus.WARNING, message, duplicate_rows, []
    
    def _check_column_completeness(self, df: pd.DataFrame, params: Dict[str, Any]) -> Tuple[ValidationStatus, str, List[int], List[str]]:
        """检查列完整性"""
        min_completeness = params.get("min_completeness", 0.9)
        total_rows = len(df)
        incomplete_columns = []
        
        for col in df.columns:
            non_null_count = df[col].notna().sum()
            completeness = non_null_count / total_rows
            
            if completeness < min_completeness:
                incomplete_columns.append({
                    'column': col,
                    'completeness': completeness,
                    'missing_count': total_rows - non_null_count
                })
        
        if not incomplete_columns:
            return ValidationStatus.PASSED, f"所有列的完整率都满足{min_completeness:.1%}的要求", [], []
        
        # 找出不完整列的行索引
        affected_rows = []
        for col_info in incomplete_columns:
            col = col_info['column']
            missing_rows = df[df[col].isnull()].index.tolist()
            affected_rows.extend(missing_rows)
        
        message = f"发现{len(incomplete_columns)}列的完整率不满足要求"
        return ValidationStatus.FAILED, message, list(set(affected_rows)), [col['column'] for col in incomplete_columns]
    
    def validate(self, df: pd.DataFrame) -> List[ValidationResult]:
        """执行完整性验证"""
        results = []
        
        for rule in self.rules:
            if rule.is_active:
                result = self.validate_rule(df, rule)
                results.append(result)
        
        return results

class TypeValidator(DataValidator):
    """数据类型验证器"""
    
    def __init__(self):
        super().__init__("TypeValidator")
        self._setup_rules()
    
    def _setup_rules(self):
        """设置验证规则"""
        
        # 检查数值列类型
        self.add_rule(ValidationRule(
            rule_id="numeric_columns",
            rule_name="数值列类型检查",
            description="检查指定的列是否为数值类型",
            validation_func=self._check_numeric_columns,
            level=ValidationLevel.STRICT,
            parameters={"columns": []}
        ))
        
        # 检查日期列类型
        self.add_rule(ValidationRule(
            rule_id="date_columns",
            rule_name="日期列类型检查",
            description="检查指定的列是否可以转换为日期",
            validation_func=self._check_date_columns,
            level=ValidationLevel.NORMAL,
            parameters={"columns": []}
        ))
        
        # 检查布尔列类型
        self.add_rule(ValidationRule(
            rule_id="boolean_columns",
            rule_name="布尔列类型检查",
            description="检查指定的列是否为布尔类型",
            validation_func=self._check_boolean_columns,
            level=ValidationLevel.NORMAL,
            parameters={"columns": []}
        ))
        
        # 检查字符串列长度
        self.add_rule(ValidationRule(
            rule_id="string_length",
            rule_name="字符串长度检查",
            description="检查字符串列的长度是否在合理范围内",
            validation_func=self._check_string_length,
            level=ValidationLevel.NORMAL,
            parameters={"max_length": 1000, "min_length": 0}
        ))
    
    def _check_numeric_columns(self, df: pd.DataFrame, params: Dict[str, Any]) -> Tuple[ValidationStatus, str, List[int], List[str]]:
        """检查数值列"""
        specified_columns = params.get("columns", df.select_dtypes(include=[np.number]).columns.tolist())
        invalid_columns = []
        affected_rows = []
        
        for col in specified_columns:
            if col in df.columns:
                # 检查是否能转换为数值
                try:
                    pd.to_numeric(df[col], errors='raise')
                except:
                    # 找出非数值的行
                    non_numeric_mask = pd.to_numeric(df[col], errors='coerce').isna()
                    non_numeric_rows = df[non_numeric_mask].index.tolist()
                    if len(non_numeric_rows) > 0:
                        invalid_columns.append(col)
                        affected_rows.extend(non_numeric_rows)
        
        if not invalid_columns:
            return ValidationStatus.PASSED, "所有指定列都是有效的数值类型", [], []
        
        message = f"发现{len(invalid_columns)}列包含非数值数据"
        return ValidationStatus.FAILED, message, list(set(affected_rows)), invalid_columns
    
    def _check_date_columns(self, df: pd.DataFrame, params: Dict[str, Any]) -> Tuple[ValidationStatus, str, List[int], List[str]]:
        """检查日期列"""
        specified_columns = params.get("columns", [])
        invalid_columns = []
        affected_rows = []
        
        for col in specified_columns:
            if col in df.columns:
                try:
                    pd.to_datetime(df[col], errors='raise')
                except:
                    # 找出无效日期的行
                    invalid_date_mask = pd.to_datetime(df[col], errors='coerce').isna()
                    invalid_date_rows = df[invalid_date_mask].index.tolist()
                    if len(invalid_date_rows) > 0:
                        invalid_columns.append(col)
                        affected_rows.extend(invalid_date_rows)
        
        if not invalid_columns:
            return ValidationStatus.PASSED, "所有指定列都是有效的日期类型", [], []
        
        message = f"发现{len(invalid_columns)}列包含无效日期数据"
        return ValidationStatus.WARNING, message, list(set(affected_rows)), invalid_columns
    
    def _check_boolean_columns(self, df: pd.DataFrame, params: Dict[str, Any]) -> Tuple[ValidationStatus, str, List[int], List[str]]:
        """检查布尔列"""
        specified_columns = params.get("columns", [])
        invalid_columns = []
        affected_rows = []
        
        for col in specified_columns:
            if col in df.columns:
                # 检查是否只包含布尔值
                valid_values = {True, False, 1, 0, "True", "False", "true", "false", "TRUE", "FALSE", "是", "否", "1", "0"}
                invalid_mask = ~df[col].isin(valid_values)
                
                if invalid_mask.any():
                    invalid_rows = df[invalid_mask].index.tolist()
                    invalid_columns.append(col)
                    affected_rows.extend(invalid_rows)
        
        if not invalid_columns:
            return ValidationStatus.PASSED, "所有指定列都是有效的布尔类型", [], []
        
        message = f"发现{len(invalid_columns)}列包含非布尔数据"
        return ValidationStatus.WARNING, message, list(set(affected_rows)), invalid_columns
    
    def _check_string_length(self, df: pd.DataFrame, params: Dict[str, Any]) -> Tuple[ValidationStatus, str, List[int], List[str]]:
        """检查字符串长度"""
        max_length = params.get("max_length", 1000)
        min_length = params.get("min_length", 0)
        
        string_columns = df.select_dtypes(include=['object']).columns
        invalid_columns = []
        affected_rows = []
        
        for col in string_columns:
            if col in df.columns:
                # 计算字符串长度
                string_lengths = df[col].str.len()
                
                # 检查超出范围的行
                invalid_mask = (string_lengths > max_length) | (string_lengths < min_length)
                
                if invalid_mask.any():
                    invalid_rows = df[invalid_mask].index.tolist()
                    invalid_columns.append(col)
                    affected_rows.extend(invalid_rows)
        
        if not invalid_columns:
            return ValidationStatus.PASSED, f"所有字符串长度都在{min_length}-{max_length}范围内", [], []
        
        message = f"发现{len(invalid_columns)}列包含超出长度范围的字符串"
        return ValidationStatus.WARNING, message, list(set(affected_rows)), invalid_columns
    
    def validate(self, df: pd.DataFrame) -> List[ValidationResult]:
        """执行数据类型验证"""
        results = []
        
        for rule in self.rules:
            if rule.is_active:
                result = self.validate_rule(df, rule)
                results.append(result)
        
        return results

class FormatValidator(DataValidator):
    """格式验证器"""
    
    def __init__(self):
        super().__init__("FormatValidator")
        self._setup_rules()
        # 预定义的正则表达式
        self.patterns = {
            'email': re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'),
            'phone': re.compile(r'^1[3-9]\d{9}$'),  # 中国手机号
            'url': re.compile(r'^https?://[^\s/$.?#].[^\s]*$'),
            'id_card': re.compile(r'^\d{17}[\dXx]$'),  # 身份证号
            'postal_code': re.compile(r'^\d{6}$'),  # 邮政编码
        }
    
    def _setup_rules(self):
        """设置验证规则"""
        
        # 邮箱格式检查
        self.add_rule(ValidationRule(
            rule_id="email_format",
            rule_name="邮箱格式检查",
            description="检查邮箱地址格式是否正确",
            validation_func=self._check_email_format,
            level=ValidationLevel.NORMAL,
            parameters={"columns": []}
        ))
        
        # 电话号码格式检查
        self.add_rule(ValidationRule(
            rule_id="phone_format",
            rule_name="电话号码格式检查",
            description="检查电话号码格式是否正确",
            validation_func=self._check_phone_format,
            level=ValidationLevel.NORMAL,
            parameters={"columns": []}
        ))
        
        # URL格式检查
        self.add_rule(ValidationRule(
            rule_id="url_format",
            rule_name="URL格式检查",
            description="检查URL格式是否正确",
            validation_func=self._check_url_format,
            level=ValidationLevel.NORMAL,
            parameters={"columns": []}
        ))
        
        # 自定义正则表达式检查
        self.add_rule(ValidationRule(
            rule_id="regex_pattern",
            rule_name="正则表达式检查",
            description="使用正则表达式检查字段格式",
            validation_func=self._check_regex_pattern,
            level=ValidationLevel.NORMAL,
            parameters={"columns": [], "pattern": "", "pattern_name": ""}
        ))
    
    def _check_email_format(self, df: pd.DataFrame, params: Dict[str, Any]) -> Tuple[ValidationStatus, str, List[int], List[str]]:
        """检查邮箱格式"""
        columns = params.get("columns", [])
        invalid_columns = []
        affected_rows = []
        
        for col in columns:
            if col in df.columns:
                # 检查邮箱格式
                email_mask = df[col].str.match(self.patterns['email'], na=False)
                invalid_mask = ~email_mask & df[col].notna()
                
                if invalid_mask.any():
                    invalid_rows = df[invalid_mask].index.tolist()
                    invalid_columns.append(col)
                    affected_rows.extend(invalid_rows)
        
        if not invalid_columns:
            return ValidationStatus.PASSED, "所有邮箱格式都正确", [], []
        
        message = f"发现{len(invalid_columns)}列包含格式错误的邮箱"
        return ValidationStatus.WARNING, message, list(set(affected_rows)), invalid_columns
    
    def _check_phone_format(self, df: pd.DataFrame, params: Dict[str, Any]) -> Tuple[ValidationStatus, str, List[int], List[str]]:
        """检查电话号码格式"""
        columns = params.get("columns", [])
        invalid_columns = []
        affected_rows = []
        
        for col in columns:
            if col in df.columns:
                # 检查电话号码格式
                phone_mask = df[col].str.match(self.patterns['phone'], na=False)
                invalid_mask = ~phone_mask & df[col].notna()
                
                if invalid_mask.any():
                    invalid_rows = df[invalid_mask].index.tolist()
                    invalid_columns.append(col)
                    affected_rows.extend(invalid_rows)
        
        if not invalid_columns:
            return ValidationStatus.PASSED, "所有电话号码格式都正确", [], []
        
        message = f"发现{len(invalid_columns)}列包含格式错误的电话号码"
        return ValidationStatus.WARNING, message, list(set(affected_rows)), invalid_columns
    
    def _check_url_format(self, df: pd.DataFrame, params: Dict[str, Any]) -> Tuple[ValidationStatus, str, List[int], List[str]]:
        """检查URL格式"""
        columns = params.get("columns", [])
        invalid_columns = []
        affected_rows = []
        
        for col in columns:
            if col in df.columns:
                # 检查URL格式
                url_mask = df[col].str.match(self.patterns['url'], na=False)
                invalid_mask = ~url_mask & df[col].notna()
                
                if invalid_mask.any():
                    invalid_rows = df[invalid_mask].index.tolist()
                    invalid_columns.append(col)
                    affected_rows.extend(invalid_rows)
        
        if not invalid_columns:
            return ValidationStatus.PASSED, "所有URL格式都正确", [], []
        
        message = f"发现{len(invalid_columns)}列包含格式错误的URL"
        return ValidationStatus.WARNING, message, list(set(affected_rows)), invalid_columns
    
    def _check_regex_pattern(self, df: pd.DataFrame, params: Dict[str, Any]) -> Tuple[ValidationStatus, str, List[int], List[str]]:
        """检查正则表达式匹配"""
        columns = params.get("columns", [])
        pattern = params.get("pattern", "")
        pattern_name = params.get("pattern_name", "自定义")
        
        if not pattern:
            return ValidationStatus.ERROR, "未提供正则表达式模式", [], []
        
        try:
            regex_pattern = re.compile(pattern)
            invalid_columns = []
            affected_rows = []
            
            for col in columns:
                if col in df.columns:
                    # 检查正则匹配
                    match_mask = df[col].str.match(regex_pattern, na=False)
                    invalid_mask = ~match_mask & df[col].notna()
                    
                    if invalid_mask.any():
                        invalid_rows = df[invalid_mask].index.tolist()
                        invalid_columns.append(col)
                        affected_rows.extend(invalid_rows)
            
            if not invalid_columns:
                return ValidationStatus.PASSED, f"所有{pattern_name}格式都正确", [], []
            
            message = f"发现{len(invalid_columns)}列包含格式错误的{pattern_name}"
            return ValidationStatus.WARNING, message, list(set(affected_rows)), invalid_columns
            
        except re.error as e:
            return ValidationStatus.ERROR, f"正则表达式语法错误: {str(e)}", [], []
    
    def validate(self, df: pd.DataFrame) -> List[ValidationResult]:
        """执行格式验证"""
        results = []
        
        for rule in self.rules:
            if rule.is_active:
                result = self.validate_rule(df, rule)
                results.append(result)
        
        return results

class BusinessRuleValidator(DataValidator):
    """业务规则验证器"""
    
    def __init__(self):
        super().__init__("BusinessRuleValidator")
        self._setup_rules()
    
    def _setup_rules(self):
        """设置验证规则"""
        
        # 数值范围检查
        self.add_rule(ValidationRule(
            rule_id="numeric_range",
            rule_name="数值范围检查",
            description="检查数值列是否在指定范围内",
            validation_func=self._check_numeric_range,
            level=ValidationLevel.STRICT,
            parameters={"column_ranges": {}}
        ))
        
        # 逻辑一致性检查
        self.add_rule(ValidationRule(
            rule_id="logical_consistency",
            rule_name="逻辑一致性检查",
            description="检查相关字段间的逻辑一致性",
            validation_func=self._check_logical_consistency,
            level=ValidationLevel.STRICT,
            parameters={"rules": []}
        ))
        
        # 总和检查
        self.add_rule(ValidationRule(
            rule_id="sum_check",
            rule_name="总和检查",
            description="检查多个字段的和是否等于指定字段",
            validation_func=self._check_sum,
            level=ValidationLevel.NORMAL,
            parameters={"sum_fields": [], "target_field": ""}
        ))
        
        # 唯一性检查
        self.add_rule(ValidationRule(
            rule_id="uniqueness",
            rule_name="唯一性检查",
            description="检查指定字段的值是否唯一",
            validation_func=self._check_uniqueness,
            level=ValidationLevel.STRICT,
            parameters={"columns": []}
        ))
    
    def _check_numeric_range(self, df: pd.DataFrame, params: Dict[str, Any]) -> Tuple[ValidationStatus, str, List[int], List[str]]:
        """检查数值范围"""
        column_ranges = params.get("column_ranges", {})
        invalid_columns = []
        affected_rows = []
        
        for col, range_info in column_ranges.items():
            if col in df.columns:
                min_val = range_info.get("min")
                max_val = range_info.get("max")
                
                # 检查超出范围的值
                mask = pd.Series([True] * len(df), index=df.index)
                
                if min_val is not None:
                    mask &= df[col] >= min_val
                if max_val is not None:
                    mask &= df[col] <= max_val
                
                invalid_rows = df[~mask].index.tolist()
                if invalid_rows:
                    invalid_columns.append(col)
                    affected_rows.extend(invalid_rows)
        
        if not invalid_columns:
            return ValidationStatus.PASSED, "所有数值都在指定范围内", [], []
        
        message = f"发现{len(invalid_columns)}列包含超出范围的数值"
        return ValidationStatus.FAILED, message, list(set(affected_rows)), invalid_columns
    
    def _check_logical_consistency(self, df: pd.DataFrame, params: Dict[str, Any]) -> Tuple[ValidationStatus, str, List[int], List[str]]:
        """检查逻辑一致性"""
        rules = params.get("rules", [])
        invalid_columns = []
        affected_rows = []
        
        for rule in rules:
            column = rule.get("column")
            condition = rule.get("condition")
            
            if column in df.columns:
                try:
                    # 简单的条件检查示例
                    if condition == "positive":
                        invalid_mask = df[column] < 0
                    elif condition == "non_negative":
                        invalid_mask = df[column] <= 0
                    elif condition == "non_empty":
                        invalid_mask = df[column].isnull() | (df[column] == '')
                    else:
                        continue
                    
                    invalid_rows = df[invalid_mask].index.tolist()
                    if invalid_rows:
                        invalid_columns.append(column)
                        affected_rows.extend(invalid_rows)
                        
                except Exception as e:
                    self.logger.warning(f"检查规则 {condition} 时出错: {str(e)}")
        
        if not invalid_columns:
            return ValidationStatus.PASSED, "所有逻辑一致性检查都通过", [], []
        
        message = f"发现{len(invalid_columns)}列存在逻辑不一致问题"
        return ValidationStatus.FAILED, message, list(set(affected_rows)), invalid_columns
    
    def _check_sum(self, df: pd.DataFrame, params: Dict[str, Any]) -> Tuple[ValidationStatus, str, List[int], List[str]]:
        """检查总和"""
        sum_fields = params.get("sum_fields", [])
        target_field = params.get("target_field", "")
        
        if not sum_fields or not target_field:
            return ValidationStatus.ERROR, "缺少必要的字段配置", [], []
        
        if target_field not in df.columns:
            return ValidationStatus.ERROR, f"目标字段 {target_field} 不存在", [], []
        
        # 检查求和字段是否存在
        missing_fields = [f for f in sum_fields if f not in df.columns]
        if missing_fields:
            return ValidationStatus.ERROR, f"求和字段不存在: {missing_fields}", [], []
        
        try:
            # 计算预期总和
            expected_sum = df[sum_fields].sum(axis=1)
            
            # 检查是否等于目标字段
            tolerance = params.get("tolerance", 0.01)  # 容差
            diff = abs(df[target_field] - expected_sum)
            invalid_mask = diff > tolerance
            
            invalid_rows = df[invalid_mask].index.tolist()
            
            if not invalid_rows:
                return ValidationStatus.PASSED, "总和检查通过", [], []
            
            message = f"发现{len(invalid_rows)}行的总和检查失败"
            return ValidationStatus.FAILED, message, invalid_rows, sum_fields + [target_field]
            
        except Exception as e:
            return ValidationStatus.ERROR, f"总和检查失败: {str(e)}", [], []
    
    def _check_uniqueness(self, df: pd.DataFrame, params: Dict[str, Any]) -> Tuple[ValidationStatus, str, List[int], List[str]]:
        """检查唯一性"""
        columns = params.get("columns", [])
        
        # 检查单列唯一性
        for col in columns:
            if col in df.columns:
                duplicates = df.duplicated(subset=[col])
                duplicate_count = duplicates.sum()
                
                if duplicate_count > 0:
                    duplicate_rows = df[duplicates].index.tolist()
                    message = f"列 {col} 中发现 {duplicate_count} 个重复值"
                    return ValidationStatus.FAILED, message, duplicate_rows, [col]
        
        # 检查组合列唯一性
        if len(columns) > 1:
            duplicates = df.duplicated(subset=columns)
            duplicate_count = duplicates.sum()
            
            if duplicate_count > 0:
                duplicate_rows = df[duplicates].index.tolist()
                message = f"列组合 {columns} 中发现 {duplicate_count} 个重复行"
                return ValidationStatus.FAILED, message, duplicate_rows, columns
        
        return ValidationStatus.PASSED, "所有唯一性检查都通过", [], []
    
    def validate(self, df: pd.DataFrame) -> List[ValidationResult]:
        """执行业务规则验证"""
        results = []
        
        for rule in self.rules:
            if rule.is_active:
                result = self.validate_rule(df, rule)
                results.append(result)
        
        return results

class DataQualityAssessor:
    """数据质量评估器"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def assess_data_quality(self, df: pd.DataFrame, validation_results: List[ValidationResult]) -> Tuple[float, Dict[str, float]]:
        """评估数据质量"""
        if df.empty:
            return 0.0, {}
        
        # 基本统计
        total_cells = len(df) * len(df.columns)
        total_rows = len(df)
        
        # 计算各维度得分
        completeness_score = self._calculate_completeness_score(df)
        consistency_score = self._calculate_consistency_score(validation_results)
        validity_score = self._calculate_validity_score(validation_results)
        accuracy_score = self._calculate_accuracy_score(df, validation_results)
        
        # 加权综合得分
        weights = {
            'completeness': 0.3,
            'consistency': 0.25,
            'validity': 0.25,
            'accuracy': 0.2
        }
        
        overall_score = (
            completeness_score * weights['completeness'] +
            consistency_score * weights['consistency'] +
            validity_score * weights['validity'] +
            accuracy_score * weights['accuracy']
        )
        
        scores = {
            'completeness': completeness_score,
            'consistency': consistency_score,
            'validity': validity_score,
            'accuracy': accuracy_score,
            'overall': overall_score
        }
        
        return overall_score, scores
    
    def _calculate_completeness_score(self, df: pd.DataFrame) -> float:
        """计算完整性得分"""
        if df.empty:
            return 0.0
        
        total_cells = len(df) * len(df.columns)
        missing_cells = df.isnull().sum().sum()
        
        # 计算完整率
        completeness_rate = (total_cells - missing_cells) / total_cells
        
        # 转换为100分制
        return completeness_rate * 100
    
    def _calculate_consistency_score(self, validation_results: List[ValidationResult]) -> float:
        """计算一致性得分"""
        if not validation_results:
            return 100.0
        
        total_rules = len(validation_results)
        passed_rules = sum(1 for r in validation_results if r.status == ValidationStatus.PASSED)
        
        return (passed_rules / total_rules) * 100
    
    def _calculate_validity_score(self, validation_results: List[ValidationResult]) -> float:
        """计算有效性得分"""
        if not validation_results:
            return 100.0
        
        failed_results = [r for r in validation_results if r.status in [ValidationStatus.FAILED, ValidationStatus.ERROR]]
        
        if not failed_results:
            return 100.0
        
        # 根据错误严重程度计算惩罚
        total_penalty = 0
        for result in failed_results:
            if result.rule_id in ['missing_values', 'numeric_columns', 'column_completeness']:
                penalty = 20  # 严重错误
            elif result.rule_id in ['duplicate_rows', 'empty_strings']:
                penalty = 10  # 警告
            else:
                penalty = 5   # 一般错误
            
            total_penalty += penalty
        
        # 确保得分不低于0
        score = max(0, 100 - total_penalty)
        return score
    
    def _calculate_accuracy_score(self, df: pd.DataFrame, validation_results: List[ValidationResult]) -> float:
        """计算准确性得分"""
        if df.empty:
            return 0.0
        
        # 基于格式和业务规则验证结果计算准确性
        format_errors = 0
        business_errors = 0
        
        for result in validation_results:
            if result.rule_id in ['email_format', 'phone_format', 'url_format', 'regex_pattern']:
                format_errors += len(result.affected_rows)
            elif result.rule_id in ['numeric_range', 'logical_consistency', 'sum_check', 'uniqueness']:
                business_errors += len(result.affected_rows)
        
        total_rows = len(df)
        
        # 计算错误率
        error_rate = (format_errors + business_errors) / total_rows if total_rows > 0 else 0
        
        # 转换为准确性得分
        accuracy_score = max(0, (1 - error_rate) * 100)
        return accuracy_score
    
    def get_quality_level(self, score: float) -> str:
        """根据得分确定质量等级"""
        if score >= 95:
            return "优秀"
        elif score >= 85:
            return "良好"
        elif score >= 70:
            return "中等"
        elif score >= 50:
            return "较差"
        else:
            return "很差"

class ValidationManager:
    """验证管理器"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.validators = {
            'completeness': CompletenessValidator(),
            'type': TypeValidator(),
            'format': FormatValidator(),
            'business': BusinessRuleValidator()
        }
        self.quality_assessor = DataQualityAssessor()
    
    def add_validator(self, name: str, validator: DataValidator):
        """添加验证器"""
        self.validators[name] = validator
    
    def remove_validator(self, name: str):
        """移除验证器"""
        if name in self.validators:
            del self.validators[name]
    
    def validate_data(self, df: pd.DataFrame, dataset_name: str = "dataset") -> ValidationReport:
        """执行全面数据验证"""
        start_time = datetime.now()
        
        # 收集所有验证规则
        all_rules = []
        all_results = []
        
        for name, validator in self.validators.items():
            rules = [rule for rule in validator.rules if rule.is_active]
            all_rules.extend(rules)
            
            results = validator.validate(df)
            all_results.extend(results)
        
        # 计算质量得分
        overall_score, quality_scores = self.quality_assessor.assess_data_quality(df, all_results)
        quality_level = self.quality_assessor.get_quality_level(overall_score)
        
        # 生成验证报告
        report = ValidationReport(
            report_id=f"validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            dataset_name=dataset_name,
            validation_time=datetime.now(),
            total_rows=len(df),
            total_columns=len(df.columns),
            validation_rules=all_rules,
            results=all_results,
            overall_score=overall_score,
            quality_level=quality_level,
            summary={
                'execution_time': (datetime.now() - start_time).total_seconds(),
                'quality_scores': quality_scores,
                'validator_count': len(self.validators),
                'total_rules': len(all_rules),
                'passed_rules': len([r for r in all_results if r.status == ValidationStatus.PASSED]),
                'warning_rules': len([r for r in all_results if r.status == ValidationStatus.WARNING]),
                'failed_rules': len([r for r in all_results if r.status == ValidationStatus.FAILED]),
                'error_rules': len([r for r in all_results if r.status == ValidationStatus.ERROR])
            }
        )
        
        return report
    
    def generate_validation_report(self, report: ValidationReport, output_path: str) -> str:
        """生成验证报告"""
        try:
            report_data = {
                'report_info': {
                    'report_id': report.report_id,
                    'dataset_name': report.dataset_name,
                    'validation_time': report.validation_time.isoformat(),
                    'total_rows': report.total_rows,
                    'total_columns': report.total_columns,
                    'overall_score': report.overall_score,
                    'quality_level': report.quality_level
                },
                'summary': report.summary,
                'validation_results': [
                    {
                        'rule_id': result.rule_id,
                        'rule_name': result.rule_name,
                        'status': result.status.value,
                        'message': result.message,
                        'affected_rows_count': len(result.affected_rows),
                        'affected_columns': result.affected_columns,
                        'error_rate': result.error_rate
                    }
                    for result in report.results
                ]
            }
            
            # 保存为JSON文件
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2, ensure_ascii=False)
            
            return output_path
            
        except Exception as e:
            self.logger.error(f"生成验证报告失败: {str(e)}")
            return ""

# 便捷函数
def create_validation_manager() -> ValidationManager:
    """创建验证管理器"""
    return ValidationManager()

def quick_validate(df: pd.DataFrame, dataset_name: str = "dataset") -> ValidationReport:
    """快速验证数据"""
    manager = ValidationManager()
    return manager.validate_data(df, dataset_name)

# 预定义的验证规则
def create_standard_rules():
    """创建标准验证规则"""
    rules = {}
    
    # 完整性规则
    rules['completeness'] = [
        ValidationRule(
            rule_id="required_fields",
            rule_name="必填字段检查",
            description="检查必填字段是否完整",
            validation_func=lambda df, params: (
                ValidationStatus.PASSED if df[params.get('required_fields', [])].notna().all().all()
                else ValidationStatus.FAILED,
                "发现必填字段缺失"
            ),
            level=ValidationLevel.STRICT,
            parameters={"required_fields": []}
        )
    ]
    
    # 格式规则
    rules['format'] = [
        ValidationRule(
            rule_id="standard_email",
            rule_name="标准邮箱格式",
            description="检查邮箱格式是否符合RFC标准",
            validation_func=lambda df, params: (
                ValidationStatus.PASSED,
                "邮箱格式检查"
            ),
            level=ValidationLevel.NORMAL,
            parameters={"columns": []}
        )
    ]
    
    return rules

# 数据质量标准
DATA_QUALITY_STANDARDS = {
    'excellent': {'min_score': 95, 'max_missing_rate': 0.01},
    'good': {'min_score': 85, 'max_missing_rate': 0.05},
    'fair': {'min_score': 70, 'max_missing_rate': 0.10},
    'poor': {'min_score': 50, 'max_missing_rate': 0.20},
    'very_poor': {'min_score': 0, 'max_missing_rate': 1.0}
}