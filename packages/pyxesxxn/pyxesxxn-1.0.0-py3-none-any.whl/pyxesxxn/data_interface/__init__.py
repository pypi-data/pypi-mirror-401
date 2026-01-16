"""
数据接口模块

提供统一的数据接口，支持多种数据格式和源的数据导入、导出、验证、转换功能：

主要功能：
- 数据导入：从各种数据源（文件、数据库、API）导入数据
- 数据导出：支持多种格式的数据导出（CSV、Excel、JSON、数据库等）
- 格式转换：不同数据格式间的转换（CSV、Excel、JSON、XML等）
- 数据验证：数据完整性、准确性、格式验证
- 数据映射：组件属性映射和数据标准化
- 实时数据：实时数据获取和更新接口
- 云存储：云端数据存储和同步
"""

from .data_import import DataImporter, FileDataImporter, DatabaseDataImporter, APIDataImporter
from .data_export import DataExporter, FileDataExporter, DatabaseDataExporter, APIExporter
from .format_converters import FormatConverter, CSVConverter, ExcelConverter, JSONConverter, XMLConverter
from .data_validators import DataValidator, SchemaValidator, BusinessRuleValidator, DataQualityValidator
from .data_mappers import DataMapper, ComponentMapper, AttributeMapper, StandardizedMapper

__all__ = [
    # 导入器
    'DataImporter',
    'FileDataImporter', 
    'DatabaseDataImporter',
    'APIDataImporter',
    
    # 导出器
    'DataExporter',
    'FileDataExporter',
    'DatabaseDataExporter', 
    'APIExporter',
    
    # 转换器
    'FormatConverter',
    'CSVConverter',
    'ExcelConverter',
    'JSONConverter',
    'XMLConverter',
    
    # 验证器
    'DataValidator',
    'SchemaValidator',
    'BusinessRuleValidator',
    'DataQualityValidator',
    
    # 映射器
    'DataMapper',
    'ComponentMapper',
    'AttributeMapper',
    'StandardizedMapper'
]

# 默认配置
DEFAULT_IMPORT_CONFIG = {
    'file_encoding': 'utf-8',
    'max_file_size_mb': 100,
    'batch_size': 10000,
    'timeout_seconds': 300,
    'retry_attempts': 3,
    'validate_on_import': True,
    'cache_parsed_data': True
}

DEFAULT_EXPORT_CONFIG = {
    'file_format': 'csv',
    'compression': False,
    'include_metadata': True,
    'encoding': 'utf-8',
    'batch_export': True,
    'backup_original': False
}

DEFAULT_VALIDATION_CONFIG = {
    'strict_mode': False,
    'skip_external_refs': True,
    'validate_schema': True,
    'validate_business_rules': True,
    'report_warnings': True
}

DEFAULT_MAPPING_CONFIG = {
    'auto_detect_columns': True,
    'case_sensitive': False,
    'fuzzy_matching': True,
    'default_values': {},
    'transformation_rules': {}
}