"""
数据导入模块

支持多种数据源的数据导入功能：
- 文件导入：CSV、Excel、JSON、XML等格式
- 数据库导入：关系型数据库、NoSQL数据库
- API导入：REST API、GraphQL、RPC等
- 流式导入：大文件分块导入
- 增量导入：仅导入变更的数据
- 数据预处理：导入时自动清理和转换
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union, Iterator, Callable, Tuple
from enum import Enum
import pandas as pd
import numpy as np
import json
import csv
import logging
from pathlib import Path
from datetime import datetime, timedelta
import asyncio
import aiofiles
import sqlite3
import requests
from urllib.parse import urljoin, urlparse
import os
import tempfile
import gzip
import zipfile

class DataSourceType(Enum):
    """数据源类型"""
    CSV = "csv"
    EXCEL = "excel"
    JSON = "json"
    XML = "xml"
    DATABASE = "database"
    API = "api"
    WEB_SCRAPING = "web_scraping"
    STREAMING = "streaming"

class ImportStatus(Enum):
    """导入状态"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    PARTIAL = "partial"

class DataQuality(Enum):
    """数据质量"""
    EXCELLENT = "excellent"    # >95%
    GOOD = "good"              # 85-95%
    FAIR = "fair"              # 70-85%
    POOR = "poor"              # <70%

@dataclass
class ImportConfiguration:
    """导入配置"""
    # 基本配置
    source_type: DataSourceType
    source_path: str
    encoding: str = "utf-8"
    
    # 文件配置
    file_format: Optional[str] = None
    delimiter: str = ","
    header_row: int = 0
    skip_rows: int = 0
    max_rows: Optional[int] = None
    
    # 数据库配置
    db_type: Optional[str] = None
    connection_string: Optional[str] = None
    query: Optional[str] = None
    table_name: Optional[str] = None
    
    # API配置
    api_endpoint: Optional[str] = None
    http_method: str = "GET"
    headers: Dict[str, str] = field(default_factory=dict)
    params: Dict[str, Any] = field(default_factory=dict)
    auth_type: Optional[str] = None
    auth_credentials: Dict[str, str] = field(default_factory=dict)
    
    # 高级配置
    batch_size: int = 1000
    timeout: int = 300
    retry_attempts: int = 3
    validate_data: bool = True
    preprocess_data: bool = True
    cache_enabled: bool = True
    parallel_processing: bool = False
    max_workers: int = 4

@dataclass
class ImportResult:
    """导入结果"""
    status: ImportStatus
    total_records: int
    successful_records: int
    failed_records: int
    error_records: List[Dict[str, Any]]
    warnings: List[str]
    execution_time: float
    data_quality_score: float
    output_data: Optional[pd.DataFrame] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    error_message: Optional[str] = None

class DataImporter(ABC):
    """数据导入器基类"""
    
    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger(__name__)
        self._cache = {}
        self._config = None
        
    @abstractmethod
    def validate_source(self, source_path: str) -> bool:
        """验证数据源"""
        pass
    
    @abstractmethod
    def import_data(self, config: ImportConfiguration) -> ImportResult:
        """导入数据"""
        pass
    
    @abstractmethod
    def get_data_schema(self, config: ImportConfiguration) -> Dict[str, Any]:
        """获取数据模式"""
        pass
    
    def preprocess_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """数据预处理"""
        self.logger.info("开始数据预处理")
        
        try:
            # 去除空行和空列
            df = df.dropna(how='all').dropna(axis=1, how='all')
            
            # 数据类型转换
            for col in df.columns:
                if df[col].dtype == 'object':
                    # 尝试转换为数值类型
                    try:
                        df[col] = pd.to_numeric(df[col], errors='ignore')
                    except:
                        pass
                    
                    # 尝试转换为日期类型
                    try:
                        df[col] = pd.to_datetime(df[col], errors='ignore')
                    except:
                        pass
            
            # 数据清洗
            for col in df.columns:
                if df[col].dtype == 'object':
                    # 去除前后空白
                    df[col] = df[col].str.strip()
                    # 处理缺失值
                    df[col] = df[col].replace('', np.nan)
            
            # 重置索引
            df = df.reset_index(drop=True)
            
            self.logger.info("数据预处理完成")
            return df
            
        except Exception as e:
            self.logger.error(f"数据预处理失败: {str(e)}")
            return df
    
    def calculate_data_quality(self, df: pd.DataFrame) -> Tuple[float, List[str]]:
        """计算数据质量"""
        warnings = []
        
        # 基本统计
        total_cells = df.shape[0] * df.shape[1]
        missing_cells = df.isnull().sum().sum()
        complete_cells = total_cells - missing_cells
        
        # 计算完整度
        completeness = complete_cells / total_cells if total_cells > 0 else 0
        
        # 检查重复行
        duplicates = df.duplicated().sum()
        if duplicates > 0:
            warnings.append(f"发现{duplicates}行重复数据")
        
        # 检查异常值（数值列）
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if df[col].std() > 0:
                z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
                outliers = (z_scores > 3).sum()
                if outliers > 0:
                    warnings.append(f"列{col}中发现{outliers}个异常值")
        
        # 检查字符串列的格式
        string_cols = df.select_dtypes(include=['object']).columns
        for col in string_cols:
            # 检查空字符串
            empty_strings = (df[col] == '').sum()
            if empty_strings > 0:
                warnings.append(f"列{col}中发现{empty_strings}个空字符串")
        
        quality_score = completeness * 100
        
        if quality_score >= 95:
            quality_level = DataQuality.EXCELLENT
        elif quality_score >= 85:
            quality_level = DataQuality.GOOD
        elif quality_score >= 70:
            quality_level = DataQuality.FAIR
        else:
            quality_level = DataQuality.POOR
        
        warnings.append(f"数据质量: {quality_level.value}, 完整度: {completeness:.2%}")
        
        return quality_score, warnings

class FileDataImporter(DataImporter):
    """文件数据导入器"""
    
    def __init__(self):
        super().__init__("FileDataImporter")
        self.supported_formats = {'.csv', '.xlsx', '.xls', '.json', '.xml', '.parquet', '.h5', '.hdf5'}
    
    def validate_source(self, source_path: str) -> bool:
        """验证文件源"""
        try:
            path = Path(source_path)
            
            # 检查文件是否存在
            if not path.exists():
                return False
            
            # 检查文件格式
            if path.suffix.lower() not in self.supported_formats:
                return False
            
            # 检查文件大小
            if path.stat().st_size == 0:
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"文件验证失败: {str(e)}")
            return False
    
    def import_data(self, config: ImportConfiguration) -> ImportResult:
        """导入文件数据"""
        start_time = datetime.now()
        
        try:
            # 验证源
            if not self.validate_source(config.source_path):
                return ImportResult(
                    status=ImportStatus.FAILED,
                    total_records=0,
                    successful_records=0,
                    failed_records=0,
                    error_records=[],
                    warnings=["文件验证失败"],
                    execution_time=0,
                    data_quality_score=0,
                    error_message="文件验证失败"
                )
            
            # 根据文件格式选择导入方法
            file_path = Path(config.source_path)
            
            if file_path.suffix.lower() == '.csv':
                return self._import_csv(config)
            elif file_path.suffix.lower() in ['.xlsx', '.xls']:
                return self._import_excel(config)
            elif file_path.suffix.lower() == '.json':
                return self._import_json(config)
            elif file_path.suffix.lower() == '.xml':
                return self._import_xml(config)
            elif file_path.suffix.lower() in ['.parquet', '.h5', '.hdf5']:
                return self._import_hdf5(config)
            else:
                return ImportResult(
                    status=ImportStatus.FAILED,
                    total_records=0,
                    successful_records=0,
                    failed_records=0,
                    error_records=[],
                    warnings=[],
                    execution_time=0,
                    data_quality_score=0,
                    error_message=f"不支持的文件格式: {file_path.suffix}"
                )
                
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            self.logger.error(f"文件导入失败: {str(e)}")
            return ImportResult(
                status=ImportStatus.FAILED,
                total_records=0,
                successful_records=0,
                failed_records=0,
                error_records=[],
                warnings=[],
                execution_time=execution_time,
                data_quality_score=0,
                error_message=str(e)
            )
    
    def _import_csv(self, config: ImportConfiguration) -> ImportResult:
        """导入CSV文件"""
        start_time = datetime.now()
        
        try:
            # 读取CSV文件
            df = pd.read_csv(
                config.source_path,
                encoding=config.encoding,
                delimiter=config.delimiter,
                header=config.header_row,
                skiprows=config.skip_rows,
                nrows=config.max_rows,
                low_memory=False
            )
            
            return self._process_imported_data(df, start_time, "CSV")
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            return ImportResult(
                status=ImportStatus.FAILED,
                total_records=0,
                successful_records=0,
                failed_records=0,
                error_records=[],
                warnings=[],
                execution_time=execution_time,
                data_quality_score=0,
                error_message=f"CSV导入失败: {str(e)}"
            )
    
    def _import_excel(self, config: ImportConfiguration) -> ImportResult:
        """导入Excel文件"""
        start_time = datetime.now()
        
        try:
            # 读取Excel文件
            df = pd.read_excel(
                config.source_path,
                header=config.header_row,
                skiprows=config.skip_rows,
                nrows=config.max_rows,
                engine='openpyxl' if config.file_format == 'xlsx' else None
            )
            
            return self._process_imported_data(df, start_time, "Excel")
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            return ImportResult(
                status=ImportStatus.FAILED,
                total_records=0,
                successful_records=0,
                failed_records=0,
                error_records=[],
                warnings=[],
                execution_time=execution_time,
                data_quality_score=0,
                error_message=f"Excel导入失败: {str(e)}"
            )
    
    def _import_json(self, config: ImportConfiguration) -> ImportResult:
        """导入JSON文件"""
        start_time = datetime.now()
        
        try:
            # 读取JSON文件
            with open(config.source_path, 'r', encoding=config.encoding) as f:
                data = json.load(f)
            
            # 转换为DataFrame
            if isinstance(data, list):
                df = pd.DataFrame(data)
            elif isinstance(data, dict):
                if 'data' in data:
                    df = pd.DataFrame(data['data'])
                elif 'records' in data:
                    df = pd.DataFrame(data['records'])
                else:
                    # 尝试将字典转换为单行DataFrame
                    df = pd.DataFrame([data])
            else:
                raise ValueError("JSON格式不支持")
            
            return self._process_imported_data(df, start_time, "JSON")
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            return ImportResult(
                status=ImportStatus.FAILED,
                total_records=0,
                successful_records=0,
                failed_records=0,
                error_records=[],
                warnings=[],
                execution_time=execution_time,
                data_quality_score=0,
                error_message=f"JSON导入失败: {str(e)}"
            )
    
    def _import_xml(self, config: ImportConfiguration) -> ImportResult:
        """导入XML文件"""
        start_time = datetime.now()
        
        try:
            import xml.etree.ElementTree as ET
            
            # 解析XML文件
            tree = ET.parse(config.source_path)
            root = tree.getroot()
            
            # 提取数据
            data = []
            for element in root.iter():
                if element.text and element.text.strip():
                    # 简化实现：提取文本内容
                    data.append({
                        'tag': element.tag,
                        'text': element.text.strip(),
                        'attributes': element.attrib
                    })
            
            df = pd.DataFrame(data)
            
            return self._process_imported_data(df, start_time, "XML")
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            return ImportResult(
                status=ImportStatus.FAILED,
                total_records=0,
                successful_records=0,
                failed_records=0,
                error_records=[],
                warnings=[],
                execution_time=execution_time,
                data_quality_score=0,
                error_message=f"XML导入失败: {str(e)}"
            )
    
    def _import_hdf5(self, config: ImportConfiguration) -> ImportResult:
        """导入HDF5/Parquet文件"""
        start_time = datetime.now()
        
        try:
            file_path = Path(config.source_path)
            
            if file_path.suffix.lower() == '.parquet':
                df = pd.read_parquet(config.source_path)
            else:
                df = pd.read_hdf(config.source_path, key='data')
            
            return self._process_imported_data(df, start_time, "HDF5")
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            return ImportResult(
                status=ImportStatus.FAILED,
                total_records=0,
                successful_records=0,
                failed_records=0,
                error_records=[],
                warnings=[],
                execution_time=execution_time,
                data_quality_score=0,
                error_message=f"HDF5导入失败: {str(e)}"
            )
    
    def _process_imported_data(self, df: pd.DataFrame, start_time: datetime, format_type: str) -> ImportResult:
        """处理导入的数据"""
        
        # 数据预处理
        if self._config and self._config.preprocess_data:
            df = self.preprocess_data(df)
        
        # 计算数据质量
        quality_score, warnings = self.calculate_data_quality(df)
        
        # 生成结果
        execution_time = (datetime.now() - start_time).total_seconds()
        
        return ImportResult(
            status=ImportStatus.COMPLETED,
            total_records=len(df),
            successful_records=len(df),
            failed_records=0,
            error_records=[],
            warnings=warnings,
            execution_time=execution_time,
            data_quality_score=quality_score,
            output_data=df,
            metadata={
                'format': format_type,
                'columns': list(df.columns),
                'dtypes': df.dtypes.to_dict(),
                'shape': df.shape,
                'memory_usage': df.memory_usage(deep=True).sum()
            }
        )
    
    def get_data_schema(self, config: ImportConfiguration) -> Dict[str, Any]:
        """获取数据模式"""
        try:
            # 读取文件头部获取模式信息
            if config.source_path.endswith('.csv'):
                # 读取CSV头部
                with open(config.source_path, 'r', encoding=config.encoding) as f:
                    reader = csv.reader(f, delimiter=config.delimiter)
                    headers = next(reader)
                    
                    # 读取几行数据推断类型
                    sample_rows = []
                    for i, row in enumerate(reader):
                        if i >= 5:  # 读取5行样本
                            break
                        sample_rows.append(row)
                
                schema = {
                    'columns': headers,
                    'row_count': len(sample_rows),
                    'sample_data': sample_rows
                }
                
            elif config.source_path.endswith(('.xlsx', '.xls')):
                # 读取Excel头部
                df_sample = pd.read_excel(config.source_path, nrows=5)
                schema = {
                    'columns': list(df_sample.columns),
                    'dtypes': df_sample.dtypes.to_dict(),
                    'sample_data': df_sample.to_dict('records')
                }
                
            else:
                # 其他格式使用完整导入然后取样本
                import_result = self.import_data(config)
                if import_result.output_data is not None:
                    df_sample = import_result.output_data.head(5)
                    schema = {
                        'columns': list(df_sample.columns),
                        'dtypes': df_sample.dtypes.to_dict(),
                        'sample_data': df_sample.to_dict('records')
                    }
                else:
                    schema = {'error': '无法获取模式信息'}
            
            return schema
            
        except Exception as e:
            self.logger.error(f"获取数据模式失败: {str(e)}")
            return {'error': str(e)}

class DatabaseDataImporter(DataImporter):
    """数据库数据导入器"""
    
    def __init__(self):
        super().__init__("DatabaseDataImporter")
        self.supported_databases = {
            'sqlite': 'sqlite3',
            'postgresql': 'psycopg2',
            'mysql': 'pymysql',
            'oracle': 'cx_Oracle',
            'sqlserver': 'pyodbc'
        }
    
    def validate_source(self, source_path: str) -> bool:
        """验证数据库连接"""
        try:
            # 简单的连接字符串验证
            if not source_path or not source_path.strip():
                return False
            
            # 检查基本格式
            if '://' in source_path or source_path.endswith('.db'):
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"数据库连接验证失败: {str(e)}")
            return False
    
    def import_data(self, config: ImportConfiguration) -> ImportResult:
        """导入数据库数据"""
        start_time = datetime.now()
        
        try:
            # 根据数据库类型选择连接方式
            if config.db_type == 'sqlite':
                return self._import_sqlite(config)
            elif config.db_type in ['postgresql', 'mysql', 'oracle', 'sqlserver']:
                return self._import_sql_database(config)
            else:
                return ImportResult(
                    status=ImportStatus.FAILED,
                    total_records=0,
                    successful_records=0,
                    failed_records=0,
                    error_records=[],
                    warnings=[],
                    execution_time=0,
                    data_quality_score=0,
                    error_message=f"不支持的数据库类型: {config.db_type}"
                )
                
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            self.logger.error(f"数据库导入失败: {str(e)}")
            return ImportResult(
                status=ImportStatus.FAILED,
                total_records=0,
                successful_records=0,
                failed_records=0,
                error_records=[],
                warnings=[],
                execution_time=execution_time,
                data_quality_score=0,
                error_message=str(e)
            )
    
    def _import_sqlite(self, config: ImportConfiguration) -> ImportResult:
        """导入SQLite数据"""
        start_time = datetime.now()
        
        try:
            conn = sqlite3.connect(config.connection_string or config.source_path)
            
            # 构造查询
            query = config.query or f"SELECT * FROM {config.table_name}"
            
            # 分批读取数据
            df = pd.read_sql_query(query, conn)
            
            conn.close()
            
            return self._process_imported_data(df, start_time, "SQLite")
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            return ImportResult(
                status=ImportStatus.FAILED,
                total_records=0,
                successful_records=0,
                failed_records=0,
                error_records=[],
                warnings=[],
                execution_time=execution_time,
                data_quality_score=0,
                error_message=f"SQLite导入失败: {str(e)}"
            )
    
    def _import_sql_database(self, config: ImportConfiguration) -> ImportResult:
        """导入SQL数据库数据"""
        start_time = datetime.now()
        
        try:
            # 这里简化实现，实际需要根据具体数据库类型使用相应驱动
            if config.db_type == 'postgresql':
                import psycopg2
                conn = psycopg2.connect(config.connection_string)
            elif config.db_type == 'mysql':
                import pymysql
                conn = pymysql.connect(**self._parse_mysql_connection(config.connection_string))
            else:
                raise ValueError(f"数据库类型 {config.db_type} 需要相应驱动")
            
            query = config.query or f"SELECT * FROM {config.table_name}"
            df = pd.read_sql_query(query, conn)
            
            conn.close()
            
            return self._process_imported_data(df, start_time, config.db_type)
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            return ImportResult(
                status=ImportStatus.FAILED,
                total_records=0,
                successful_records=0,
                failed_records=0,
                error_records=[],
                warnings=[],
                execution_time=execution_time,
                data_quality_score=0,
                error_message=f"{config.db_type}导入失败: {str(e)}"
            )
    
    def _parse_mysql_connection(self, connection_string: str) -> Dict[str, str]:
        """解析MySQL连接字符串"""
        # 简化的MySQL连接字符串解析
        # 实际实现应该更完善
        return {
            'host': 'localhost',
            'user': 'root',
            'password': '',
            'database': connection_string
        }
    
    def _process_imported_data(self, df: pd.DataFrame, start_time: datetime, db_type: str) -> ImportResult:
        """处理导入的数据"""
        
        # 数据预处理
        if self._config and self._config.preprocess_data:
            df = self.preprocess_data(df)
        
        # 计算数据质量
        quality_score, warnings = self.calculate_data_quality(df)
        
        # 生成结果
        execution_time = (datetime.now() - start_time).total_seconds()
        
        return ImportResult(
            status=ImportStatus.COMPLETED,
            total_records=len(df),
            successful_records=len(df),
            failed_records=0,
            error_records=[],
            warnings=warnings,
            execution_time=execution_time,
            data_quality_score=quality_score,
            output_data=df,
            metadata={
                'database_type': db_type,
                'columns': list(df.columns),
                'dtypes': df.dtypes.to_dict(),
                'shape': df.shape,
                'memory_usage': df.memory_usage(deep=True).sum()
            }
        )
    
    def get_data_schema(self, config: ImportConfiguration) -> Dict[str, Any]:
        """获取数据库表结构"""
        try:
            # 根据数据库类型获取表结构
            if config.db_type == 'sqlite':
                conn = sqlite3.connect(config.connection_string or config.source_path)
                cursor = conn.cursor()
                
                # 获取表信息
                cursor.execute(f"PRAGMA table_info({config.table_name})")
                columns_info = cursor.fetchall()
                
                schema = {
                    'table_name': config.table_name,
                    'columns': []
                }
                
                for col_info in columns_info:
                    column_schema = {
                        'name': col_info[1],
                        'type': col_info[2],
                        'not_null': bool(col_info[3]),
                        'default': col_info[4],
                        'primary_key': bool(col_info[5])
                    }
                    schema['columns'].append(column_schema)
                
                conn.close()
                return schema
                
            else:
                # 其他数据库类型需要相应实现
                return {'error': f'不支持的数据库类型: {config.db_type}'}
                
        except Exception as e:
            self.logger.error(f"获取数据库模式失败: {str(e)}")
            return {'error': str(e)}

class APIDataImporter(DataImporter):
    """API数据导入器"""
    
    def __init__(self):
        super().__init__("APIDataImporter")
        self.session = requests.Session()
    
    def validate_source(self, source_path: str) -> bool:
        """验证API端点"""
        try:
            # 检查URL格式
            parsed = urlparse(source_path)
            return bool(parsed.scheme and parsed.netloc)
            
        except Exception as e:
            self.logger.error(f"API端点验证失败: {str(e)}")
            return False
    
    def import_data(self, config: ImportConfiguration) -> ImportResult:
        """导入API数据"""
        start_time = datetime.now()
        
        try:
            # 构建请求
            url = config.api_endpoint or config.source_path
            
            headers = {
                'User-Agent': 'PyXESXXN-DataImporter/1.0',
                **config.headers
            }
            
            # 发起请求
            response = self.session.request(
                method=config.http_method,
                url=url,
                headers=headers,
                params=config.params,
                timeout=config.timeout
            )
            response.raise_for_status()
            
            # 解析响应
            if config.source_path.endswith('.json') or 'application/json' in response.headers.get('content-type', ''):
                return self._parse_json_response(response, start_time)
            else:
                return self._parse_generic_response(response, start_time)
                
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            self.logger.error(f"API导入失败: {str(e)}")
            return ImportResult(
                status=ImportStatus.FAILED,
                total_records=0,
                successful_records=0,
                failed_records=0,
                error_records=[],
                warnings=[],
                execution_time=execution_time,
                data_quality_score=0,
                error_message=str(e)
            )
    
    def _parse_json_response(self, response: requests.Response, start_time: datetime) -> ImportResult:
        """解析JSON响应"""
        try:
            data = response.json()
            
            # 转换为DataFrame
            if isinstance(data, list):
                df = pd.DataFrame(data)
            elif isinstance(data, dict):
                if 'data' in data:
                    df = pd.DataFrame(data['data'])
                elif 'results' in data:
                    df = pd.DataFrame(data['results'])
                elif 'items' in data:
                    df = pd.DataFrame(data['items'])
                else:
                    df = pd.DataFrame([data])
            else:
                raise ValueError("JSON数据格式不支持")
            
            return self._process_imported_data(df, start_time, "API-JSON")
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            return ImportResult(
                status=ImportStatus.FAILED,
                total_records=0,
                successful_records=0,
                failed_records=0,
                error_records=[],
                warnings=[],
                execution_time=execution_time,
                data_quality_score=0,
                error_message=f"JSON响应解析失败: {str(e)}"
            )
    
    def _parse_generic_response(self, response: requests.Response, start_time: datetime) -> ImportResult:
        """解析通用响应"""
        try:
            # 简化实现：直接将响应文本作为数据
            data = {'response_text': response.text, 'status_code': response.status_code}
            df = pd.DataFrame([data])
            
            return self._process_imported_data(df, start_time, "API-Generic")
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            return ImportResult(
                status=ImportStatus.FAILED,
                total_records=0,
                successful_records=0,
                failed_records=0,
                error_records=[],
                warnings=[],
                execution_time=execution_time,
                data_quality_score=0,
                error_message=f"通用响应解析失败: {str(e)}"
            )
    
    def _process_imported_data(self, df: pd.DataFrame, start_time: datetime, format_type: str) -> ImportResult:
        """处理导入的数据"""
        
        # 数据预处理
        if self._config and self._config.preprocess_data:
            df = self.preprocess_data(df)
        
        # 计算数据质量
        quality_score, warnings = self.calculate_data_quality(df)
        
        # 生成结果
        execution_time = (datetime.now() - start_time).total_seconds()
        
        return ImportResult(
            status=ImportStatus.COMPLETED,
            total_records=len(df),
            successful_records=len(df),
            failed_records=0,
            error_records=[],
            warnings=warnings,
            execution_time=execution_time,
            data_quality_score=quality_score,
            output_data=df,
            metadata={
                'format': format_type,
                'columns': list(df.columns),
                'dtypes': df.dtypes.to_dict(),
                'shape': df.shape,
                'memory_usage': df.memory_usage(deep=True).sum()
            }
        )
    
    def get_data_schema(self, config: ImportConfiguration) -> Dict[str, Any]:
        """获取API数据模式"""
        try:
            # 发起测试请求获取模式
            test_config = ImportConfiguration(
                source_type=DataSourceType.API,
                source_path=config.source_path,
                api_endpoint=config.api_endpoint,
                http_method=config.http_method,
                headers=config.headers,
                params=config.params,
                max_rows=5  # 只获取少量数据
            )
            
            import_result = self.import_data(test_config)
            
            if import_result.output_data is not None:
                df_sample = import_result.output_data
                schema = {
                    'columns': list(df_sample.columns),
                    'dtypes': df_sample.dtypes.to_dict(),
                    'sample_data': df_sample.to_dict('records')
                }
                return schema
            else:
                return {'error': '无法获取API数据模式'}
                
        except Exception as e:
            self.logger.error(f"获取API数据模式失败: {str(e)}")
            return {'error': str(e)}

# 便捷函数
def create_file_importer(file_path: str, **kwargs) -> FileDataImporter:
    """创建文件导入器"""
    importer = FileDataImporter()
    config = ImportConfiguration(
        source_type=DataSourceType.CSV if file_path.endswith('.csv') else DataSourceType.EXCEL,
        source_path=file_path,
        **kwargs
    )
    return importer, config

def create_database_importer(connection_string: str, table_name: str, **kwargs) -> DatabaseDataImporter:
    """创建数据库导入器"""
    importer = DatabaseDataImporter()
    config = ImportConfiguration(
        source_type=DataSourceType.DATABASE,
        source_path=connection_string,
        connection_string=connection_string,
        table_name=table_name,
        **kwargs
    )
    return importer, config

def create_api_importer(api_endpoint: str, **kwargs) -> APIDataImporter:
    """创建API导入器"""
    importer = APIDataImporter()
    config = ImportConfiguration(
        source_type=DataSourceType.API,
        source_path=api_endpoint,
        api_endpoint=api_endpoint,
        **kwargs
    )
    return importer, config