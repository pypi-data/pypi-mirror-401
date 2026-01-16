"""
数据导出模块

支持多种数据格式和目标的数据导出功能：
- 文件导出：CSV、Excel、JSON、XML、Parquet等格式
- 数据库导出：关系型数据库、NoSQL数据库
- API导出：REST API数据推送
- 云存储导出：S3、Azure Blob、Google Cloud Storage
- 流式导出：大数据分批导出
- 增量导出：仅导出变更的数据
- 数据后处理：导出前数据转换和验证
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

from .compression_utils import CompressionHandler

class DataExportFormat(Enum):
    """导出格式"""
    CSV = "csv"
    EXCEL = "excel"
    JSON = "json"
    XML = "xml"
    PARQUET = "parquet"
    HDF5 = "hdf5"
    DATABASE = "database"
    API = "api"

class ExportStatus(Enum):
    """导出状态"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    PARTIAL = "partial"

class ExportCompression(Enum):
    """压缩类型"""
    NONE = "none"
    GZIP = "gzip"
    ZIP = "zip"
    BZIP2 = "bz2"

@dataclass
class ExportConfiguration:
    """导出配置"""
    # 基本配置
    format_type: DataExportFormat
    destination_path: str
    compression: ExportCompression = ExportCompression.NONE
    
    # 文件配置
    encoding: str = "utf-8"
    delimiter: str = ","
    include_header: bool = True
    index: bool = False
    sheet_name: str = "Sheet1"
    
    # 数据库配置
    db_type: Optional[str] = None
    connection_string: Optional[str] = None
    table_name: Optional[str] = None
    if_exists: str = "replace"  # replace, append, fail
    create_table: bool = True
    
    # API配置
    api_endpoint: Optional[str] = None
    http_method: str = "POST"
    headers: Dict[str, str] = field(default_factory=dict)
    auth_type: Optional[str] = None
    auth_credentials: Dict[str, str] = field(default_factory=dict)
    
    # 云存储配置
    cloud_provider: Optional[str] = None
    bucket_name: Optional[str] = None
    access_key: Optional[str] = None
    secret_key: Optional[str] = None
    region: Optional[str] = None
    
    # 高级配置
    batch_size: int = 1000
    timeout: int = 300
    retry_attempts: int = 3
    validate_data: bool = True
    preprocess_data: bool = False
    parallel_processing: bool = False
    max_workers: int = 4
    create_directory: bool = True

@dataclass
class ExportResult:
    """导出结果"""
    status: ExportStatus
    total_records: int
    exported_records: int
    failed_records: int
    file_size: Optional[int]
    execution_time: float
    output_path: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    error_message: Optional[str] = None

class DataExporter(ABC):
    """数据导出器基类"""
    
    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger(__name__)
        self._config = None
        
    @abstractmethod
    def validate_destination(self, destination_path: str) -> bool:
        """验证导出目标"""
        pass
    
    @abstractmethod
    def export_data(self, df: pd.DataFrame, config: ExportConfiguration) -> ExportResult:
        """导出数据"""
        pass
    
    def preprocess_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """数据预处理"""
        self.logger.info("开始数据预处理")
        
        try:
            # 数据验证
            if df.empty:
                self.logger.warning("数据为空")
                return df
            
            # 处理NaN值
            df = df.fillna('')  # 将NaN替换为空字符串
            
            # 数据类型转换
            for col in df.columns:
                if df[col].dtype == 'object':
                    # 确保字符串列
                    df[col] = df[col].astype(str)
                    # 去除特殊字符
                    df[col] = df[col].str.replace('\x00', '')  # 去除null字符
            
            # 去除索引
            if not self._config.include_header:
                df = df.reset_index(drop=True)
            
            self.logger.info("数据预处理完成")
            return df
            
        except Exception as e:
            self.logger.error(f"数据预处理失败: {str(e)}")
            return df
    
    def validate_data(self, df: pd.DataFrame) -> Tuple[bool, List[str]]:
        """数据验证"""
        warnings = []
        
        # 检查空数据
        if df.empty:
            return False, ["数据为空"]
        
        # 检查列名
        invalid_columns = []
        for col in df.columns:
            if pd.isna(col) or str(col).strip() == '':
                invalid_columns.append(col)
        
        if invalid_columns:
            warnings.append(f"发现{len(invalid_columns)}个无效列名")
        
        # 检查数据类型
        for col in df.columns:
            try:
                # 尝试检测数据类型问题
                if df[col].dtype == 'object':
                    # 检查过长的字符串
                    max_length = df[col].str.len().max()
                    if max_length > 10000:  # 设置合理的长度限制
                        warnings.append(f"列{col}包含过长的字符串（最大长度: {max_length}）")
            except:
                pass
        
        # 检查内存使用
        memory_usage = df.memory_usage(deep=True).sum()
        if memory_usage > 100 * 1024 * 1024:  # 100MB
            warnings.append(f"数据内存使用量较大: {memory_usage / 1024 / 1024:.2f}MB")
        
        is_valid = len([w for w in warnings if "无效" in w]) == 0
        
        return is_valid, warnings

class FileDataExporter(DataExporter):
    """文件数据导出器"""
    
    def __init__(self):
        super().__init__("FileDataExporter")
        self.supported_formats = {
            DataExportFormat.CSV: ['.csv'],
            DataExportFormat.EXCEL: ['.xlsx', '.xls'],
            DataExportFormat.JSON: ['.json'],
            DataExportFormat.XML: ['.xml'],
            DataExportFormat.PARQUET: ['.parquet'],
            DataExportFormat.HDF5: ['.h5', '.hdf5']
        }
    
    def validate_destination(self, destination_path: str) -> bool:
        """验证文件导出目标"""
        try:
            path = Path(destination_path)
            
            # 创建目录（如果需要）
            if self._config and self._config.create_directory:
                path.parent.mkdir(parents=True, exist_ok=True)
            
            # 检查目录权限
            if path.exists():
                return os.access(path, os.W_OK)
            else:
                return os.access(path.parent, os.W_OK)
                
        except Exception as e:
            self.logger.error(f"文件导出目标验证失败: {str(e)}")
            return False
    
    def export_data(self, df: pd.DataFrame, config: ExportConfiguration) -> ExportResult:
        """导出文件数据"""
        start_time = datetime.now()
        
        try:
            self._config = config
            
            # 验证目标
            if not self.validate_destination(config.destination_path):
                return ExportResult(
                    status=ExportStatus.FAILED,
                    total_records=len(df),
                    exported_records=0,
                    failed_records=len(df),
                    file_size=0,
                    execution_time=0,
                    output_path=config.destination_path,
                    error_message="文件导出目标验证失败"
                )
            
            # 根据格式选择导出方法
            if config.format_type == DataExportFormat.CSV:
                return self._export_csv(df, config)
            elif config.format_type == DataExportFormat.EXCEL:
                return self._export_excel(df, config)
            elif config.format_type == DataExportFormat.JSON:
                return self._export_json(df, config)
            elif config.format_type == DataExportFormat.XML:
                return self._export_xml(df, config)
            elif config.format_type == DataExportFormat.PARQUET:
                return self._export_parquet(df, config)
            elif config.format_type == DataExportFormat.HDF5:
                return self._export_hdf5(df, config)
            else:
                return ExportResult(
                    status=ExportStatus.FAILED,
                    total_records=len(df),
                    exported_records=0,
                    failed_records=len(df),
                    file_size=0,
                    execution_time=0,
                    output_path=config.destination_path,
                    error_message=f"不支持的导出格式: {config.format_type}"
                )
                
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            self.logger.error(f"文件导出失败: {str(e)}")
            return ExportResult(
                status=ExportStatus.FAILED,
                total_records=len(df),
                exported_records=0,
                failed_records=len(df),
                file_size=0,
                execution_time=execution_time,
                output_path=config.destination_path,
                error_message=str(e)
            )
    
    def _export_csv(self, df: pd.DataFrame, config: ExportConfiguration) -> ExportResult:
        """导出CSV文件"""
        start_time = datetime.now()
        
        try:
            # 数据预处理
            if config.preprocess_data:
                df = self.preprocess_data(df)
            
            # 数据验证
            is_valid, warnings = self.validate_data(df)
            if not is_valid:
                return ExportResult(
                    status=ExportStatus.FAILED,
                    total_records=len(df),
                    exported_records=0,
                    failed_records=len(df),
                    file_size=0,
                    execution_time=0,
                    output_path=config.destination_path,
                    error_message="数据验证失败"
                )
            
            # 根据压缩类型处理文件路径和导出逻辑
            output_path = config.destination_path
            
            # 使用压缩工具函数处理文件路径
            compression_handler = CompressionHandler()
            actual_path = compression_handler.get_compressed_path(
                output_path, config.compression, '.csv'
            )
            
            # 使用压缩工具函数写入DataFrame
            write_kwargs = {
                'sep': config.delimiter,
                'index': config.index,
                'header': config.include_header,
                'encoding': config.encoding
            }
            
            compression_handler.write_dataframe_with_compression(
                df, actual_path, config.compression, df.to_csv, write_kwargs
            )
            
            # 更新配置中的路径
            config.destination_path = actual_path
            
            return self._create_export_result(df, start_time, "CSV", warnings)
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            return ExportResult(
                status=ExportStatus.FAILED,
                total_records=len(df),
                exported_records=0,
                failed_records=len(df),
                file_size=0,
                execution_time=execution_time,
                output_path=config.destination_path,
                error_message=f"CSV导出失败: {str(e)}"
            )
    
    def _export_excel(self, df: pd.DataFrame, config: ExportConfiguration) -> ExportResult:
        """导出Excel文件"""
        start_time = datetime.now()
        
        try:
            # 数据预处理
            if config.preprocess_data:
                df = self.preprocess_data(df)
            
            # 数据验证
            is_valid, warnings = self.validate_data(df)
            if not is_valid:
                return ExportResult(
                    status=ExportStatus.FAILED,
                    total_records=len(df),
                    exported_records=0,
                    failed_records=len(df),
                    file_size=0,
                    execution_time=0,
                    output_path=config.destination_path,
                    error_message="数据验证失败"
                )
            
            # 导出Excel
            # 根据压缩类型处理文件路径和写入方式
            if config.compression == ExportCompression.ZIP:
                # 确保文件扩展名为.zip
                if not config.destination_path.endswith('.zip'):
                    config.destination_path = config.destination_path.rstrip('.xlsx') + '.zip'
                
                # 创建zip文件，内部文件名为原始Excel文件名
                import zipfile
                import os
                zip_filename = config.destination_path
                excel_filename = os.path.basename(zip_filename).replace('.zip', '.xlsx')
                
                # 创建临时Excel文件
                import tempfile
                with tempfile.NamedTemporaryFile(mode='wb', suffix='.xlsx', delete=False) as tmp:
                    tmp_path = tmp.name
                    df.to_excel(
                        tmp_path,
                        sheet_name=config.sheet_name,
                        index=config.index,
                        header=config.include_header
                    )
                
                # 将临时文件添加到zip
                with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    zipf.write(tmp_path, excel_filename)
                
                # 删除临时文件
                os.unlink(tmp_path)
            else:
                # 无压缩
                df.to_excel(
                    config.destination_path,
                    sheet_name=config.sheet_name,
                    index=config.index,
                    header=config.include_header
                )
            
            return self._create_export_result(df, start_time, "Excel", warnings)
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            return ExportResult(
                status=ExportStatus.FAILED,
                total_records=len(df),
                exported_records=0,
                failed_records=len(df),
                file_size=0,
                execution_time=execution_time,
                output_path=config.destination_path,
                error_message=f"Excel导出失败: {str(e)}"
            )
    
    def _export_json(self, df: pd.DataFrame, config: ExportConfiguration) -> ExportResult:
        """导出JSON文件"""
        start_time = datetime.now()
        
        try:
            # 数据预处理
            if config.preprocess_data:
                df = self.preprocess_data(df)
            
            # 数据验证
            is_valid, warnings = self.validate_data(df)
            if not is_valid:
                return ExportResult(
                    status=ExportStatus.FAILED,
                    total_records=len(df),
                    exported_records=0,
                    failed_records=len(df),
                    file_size=0,
                    execution_time=0,
                    output_path=config.destination_path,
                    error_message="数据验证失败"
                )
            
            # 转换为JSON
            if df.empty:
                data = []
            else:
                data = df.to_dict('records')
            
            # 使用压缩工具函数处理文件路径和写入方式
            compression_handler = CompressionHandler()
            actual_path = compression_handler.get_compressed_path(
                config.destination_path, config.compression, '.json'
            )
            
            # 使用压缩工具函数写入数据
            json_str = json.dumps(data, indent=2, ensure_ascii=False)
            compression_handler.write_with_compression(
                json_str, actual_path, config.compression, config.encoding
            )
            
            # 更新配置中的路径
            config.destination_path = actual_path
            
            return self._create_export_result(df, start_time, "JSON", warnings)
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            return ExportResult(
                status=ExportStatus.FAILED,
                total_records=len(df),
                exported_records=0,
                failed_records=len(df),
                file_size=0,
                execution_time=execution_time,
                output_path=config.destination_path,
                error_message=f"JSON导出失败: {str(e)}"
            )
    
    def _export_xml(self, df: pd.DataFrame, config: ExportConfiguration) -> ExportResult:
        """导出XML文件"""
        start_time = datetime.now()
        
        try:
            # 数据预处理
            if config.preprocess_data:
                df = self.preprocess_data(df)
            
            # 数据验证
            is_valid, warnings = self.validate_data(df)
            if not is_valid:
                return ExportResult(
                    status=ExportStatus.FAILED,
                    total_records=len(df),
                    exported_records=0,
                    failed_records=len(df),
                    file_size=0,
                    execution_time=0,
                    output_path=config.destination_path,
                    error_message="数据验证失败"
                )
            
            # 转换为XML
            xml_str = df.to_xml(index=config.index)
            
            # 使用压缩工具函数处理文件路径和写入方式
            compression_handler = CompressionHandler()
            actual_path = compression_handler.get_compressed_path(
                config.destination_path, config.compression, '.xml'
            )
            
            # 使用压缩工具函数写入数据
            compression_handler.write_with_compression(
                xml_str, actual_path, config.compression, config.encoding
            )
            
            # 更新配置中的路径
            config.destination_path = actual_path
            
            return self._create_export_result(df, start_time, "XML", warnings)
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            return ExportResult(
                status=ExportStatus.FAILED,
                total_records=len(df),
                exported_records=0,
                failed_records=len(df),
                file_size=0,
                execution_time=execution_time,
                output_path=config.destination_path,
                error_message=f"XML导出失败: {str(e)}"
            )
    
    def _export_parquet(self, df: pd.DataFrame, config: ExportConfiguration) -> ExportResult:
        """导出Parquet文件"""
        start_time = datetime.now()
        
        try:
            # 数据预处理
            if config.preprocess_data:
                df = self.preprocess_data(df)
            
            # 数据验证
            is_valid, warnings = self.validate_data(df)
            if not is_valid:
                return ExportResult(
                    status=ExportStatus.FAILED,
                    total_records=len(df),
                    exported_records=0,
                    failed_records=len(df),
                    file_size=0,
                    execution_time=0,
                    output_path=config.destination_path,
                    error_message="数据验证失败"
                )
            
            # 导出Parquet
            df.to_parquet(config.destination_path, index=config.index)
            
            return self._create_export_result(df, start_time, "Parquet", warnings)
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            return ExportResult(
                status=ExportStatus.FAILED,
                total_records=len(df),
                exported_records=0,
                failed_records=len(df),
                file_size=0,
                execution_time=execution_time,
                output_path=config.destination_path,
                error_message=f"Parquet导出失败: {str(e)}"
            )
    
    def _export_hdf5(self, df: pd.DataFrame, config: ExportConfiguration) -> ExportResult:
        """导出HDF5文件"""
        start_time = datetime.now()
        
        try:
            # 数据预处理
            if config.preprocess_data:
                df = self.preprocess_data(df)
            
            # 数据验证
            is_valid, warnings = self.validate_data(df)
            if not is_valid:
                return ExportResult(
                    status=ExportStatus.FAILED,
                    total_records=len(df),
                    exported_records=0,
                    failed_records=len(df),
                    file_size=0,
                    execution_time=0,
                    output_path=config.destination_path,
                    error_message="数据验证失败"
                )
            
            # 导出HDF5
            # 根据压缩类型设置参数
            hdf_kwargs = {
                'key': 'data',
                'mode': 'w',
                'index': config.index
            }
            
            if config.compression == ExportCompression.GZIP:
                hdf_kwargs['complib'] = 'zlib'
                hdf_kwargs['complevel'] = 9
            elif config.compression == ExportCompression.BZ2:
                hdf_kwargs['complib'] = 'bzip2'
                hdf_kwargs['complevel'] = 9
            elif config.compression == ExportCompression.ZIP:
                hdf_kwargs['complib'] = 'zlib'
                hdf_kwargs['complevel'] = 9
                # 确保文件扩展名为.h5.gz
                if not config.destination_path.endswith('.h5.gz'):
                    config.destination_path = config.destination_path.rstrip('.h5') + '.h5.gz'
            else:
                # 无压缩
                pass
            
            df.to_hdf(config.destination_path, **hdf_kwargs)
            
            return self._create_export_result(df, start_time, "HDF5", warnings)
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            return ExportResult(
                status=ExportStatus.FAILED,
                total_records=len(df),
                exported_records=0,
                failed_records=len(df),
                file_size=0,
                execution_time=execution_time,
                output_path=config.destination_path,
                error_message=f"HDF5导出失败: {str(e)}"
            )
    
    def _create_export_result(self, df: pd.DataFrame, start_time: datetime, format_type: str, warnings: List[str]) -> ExportResult:
        """创建导出结果"""
        execution_time = (datetime.now() - start_time).total_seconds()
        
        # 获取文件大小
        file_size = 0
        if os.path.exists(self._config.destination_path):
            file_size = os.path.getsize(self._config.destination_path)
        
        return ExportResult(
            status=ExportStatus.COMPLETED,
            total_records=len(df),
            exported_records=len(df),
            failed_records=0,
            file_size=file_size,
            execution_time=execution_time,
            output_path=self._config.destination_path,
            metadata={
                'format': format_type,
                'columns': list(df.columns),
                'dtypes': df.dtypes.to_dict(),
                'shape': df.shape,
                'compression': self._config.compression.value,
                'warnings': warnings
            }
        )

class DatabaseDataExporter(DataExporter):
    """数据库数据导出器"""
    
    def __init__(self):
        super().__init__("DatabaseDataExporter")
    
    def validate_destination(self, destination_path: str) -> bool:
        """验证数据库连接"""
        try:
            # 简单的数据库连接验证
            if not destination_path or not destination_path.strip():
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"数据库连接验证失败: {str(e)}")
            return False
    
    def export_data(self, df: pd.DataFrame, config: ExportConfiguration) -> ExportResult:
        """导出数据库数据"""
        start_time = datetime.now()
        
        try:
            self._config = config
            
            # 数据预处理
            if config.preprocess_data:
                df = self.preprocess_data(df)
            
            # 数据验证
            is_valid, warnings = self.validate_data(df)
            if not is_valid:
                return ExportResult(
                    status=ExportStatus.FAILED,
                    total_records=len(df),
                    exported_records=0,
                    failed_records=len(df),
                    file_size=0,
                    execution_time=0,
                    output_path=config.destination_path,
                    error_message="数据验证失败"
                )
            
            # 根据数据库类型选择导出方法
            if config.db_type == 'sqlite':
                return self._export_sqlite(df, config)
            else:
                return self._export_sql_database(df, config)
                
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            self.logger.error(f"数据库导出失败: {str(e)}")
            return ExportResult(
                status=ExportStatus.FAILED,
                total_records=len(df),
                exported_records=0,
                failed_records=len(df),
                file_size=0,
                execution_time=execution_time,
                output_path=config.destination_path,
                error_message=str(e)
            )
    
    def _export_sqlite(self, df: pd.DataFrame, config: ExportConfiguration) -> ExportResult:
        """导出到SQLite"""
        start_time = datetime.now()
        
        try:
            conn = sqlite3.connect(config.connection_string or config.destination_path)
            
            # 写入数据
            df.to_sql(
                config.table_name,
                conn,
                if_exists=config.if_exists,
                index=config.index,
                chunksize=config.batch_size
            )
            
            conn.close()
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return ExportResult(
                status=ExportStatus.COMPLETED,
                total_records=len(df),
                exported_records=len(df),
                failed_records=0,
                file_size=os.path.getsize(config.destination_path) if os.path.exists(config.destination_path) else 0,
                execution_time=execution_time,
                output_path=config.destination_path,
                metadata={
                    'database_type': 'SQLite',
                    'table_name': config.table_name,
                    'columns': list(df.columns),
                    'shape': df.shape
                }
            )
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            return ExportResult(
                status=ExportStatus.FAILED,
                total_records=len(df),
                exported_records=0,
                failed_records=len(df),
                file_size=0,
                execution_time=execution_time,
                output_path=config.destination_path,
                error_message=f"SQLite导出失败: {str(e)}"
            )
    
    def _export_sql_database(self, df: pd.DataFrame, config: ExportConfiguration) -> ExportResult:
        """导出到SQL数据库"""
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
            
            # 写入数据
            df.to_sql(
                config.table_name,
                conn,
                if_exists=config.if_exists,
                index=config.index,
                chunksize=config.batch_size,
                flavor='sqlalchemy'
            )
            
            conn.close()
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return ExportResult(
                status=ExportStatus.COMPLETED,
                total_records=len(df),
                exported_records=len(df),
                failed_records=0,
                file_size=0,
                execution_time=execution_time,
                output_path=config.destination_path,
                metadata={
                    'database_type': config.db_type,
                    'table_name': config.table_name,
                    'columns': list(df.columns),
                    'shape': df.shape
                }
            )
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            return ExportResult(
                status=ExportStatus.FAILED,
                total_records=len(df),
                exported_records=0,
                failed_records=len(df),
                file_size=0,
                execution_time=execution_time,
                output_path=config.destination_path,
                error_message=f"{config.db_type}导出失败: {str(e)}"
            )
    
    def _parse_mysql_connection(self, connection_string: str) -> Dict[str, str]:
        """解析MySQL连接字符串"""
        # 简化的MySQL连接字符串解析
        return {
            'host': 'localhost',
            'user': 'root',
            'password': '',
            'database': connection_string
        }

class APIDataExporter(DataExporter):
    """API数据导出器"""
    
    def __init__(self):
        super().__init__("APIDataExporter")
        self.session = requests.Session()
    
    def validate_destination(self, destination_path: str) -> bool:
        """验证API端点"""
        try:
            parsed = urlparse(destination_path)
            return bool(parsed.scheme and parsed.netloc)
            
        except Exception as e:
            self.logger.error(f"API端点验证失败: {str(e)}")
            return False
    
    def export_data(self, df: pd.DataFrame, config: ExportConfiguration) -> ExportResult:
        """导出API数据"""
        start_time = datetime.now()
        
        try:
            self._config = config
            
            # 数据预处理
            if config.preprocess_data:
                df = self.preprocess_data(df)
            
            # 数据验证
            is_valid, warnings = self.validate_data(df)
            if not is_valid:
                return ExportResult(
                    status=ExportStatus.FAILED,
                    total_records=len(df),
                    exported_records=0,
                    failed_records=len(df),
                    file_size=0,
                    execution_time=0,
                    output_path=config.destination_path,
                    error_message="数据验证失败"
                )
            
            # 转换为JSON
            data = df.to_dict('records') if not df.empty else []
            
            # 构建请求
            url = config.api_endpoint or config.destination_path
            headers = {
                'Content-Type': 'application/json',
                'User-Agent': 'PyXESXXN-DataExporter/1.0',
                **config.headers
            }
            
            # 发起请求
            response = self.session.request(
                method=config.http_method,
                url=url,
                headers=headers,
                json=data if config.http_method == 'POST' else None,
                timeout=config.timeout
            )
            response.raise_for_status()
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return ExportResult(
                status=ExportStatus.COMPLETED,
                total_records=len(df),
                exported_records=len(df),
                failed_records=0,
                file_size=0,
                execution_time=execution_time,
                output_path=config.destination_path,
                metadata={
                    'format': 'API',
                    'columns': list(df.columns),
                    'shape': df.shape,
                    'response_status': response.status_code,
                    'warnings': warnings
                }
            )
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            self.logger.error(f"API导出失败: {str(e)}")
            return ExportResult(
                status=ExportStatus.FAILED,
                total_records=len(df),
                exported_records=0,
                failed_records=len(df),
                file_size=0,
                execution_time=execution_time,
                output_path=config.destination_path,
                error_message=str(e)
            )

# 便捷函数
def create_file_exporter(file_path: str, format_type: DataExportFormat, **kwargs) -> FileDataExporter:
    """创建文件导出器"""
    exporter = FileDataExporter()
    config = ExportConfiguration(
        format_type=format_type,
        destination_path=file_path,
        **kwargs
    )
    return exporter, config

def create_database_exporter(connection_string: str, table_name: str, **kwargs) -> DatabaseDataExporter:
    """创建数据库导出器"""
    exporter = DatabaseDataExporter()
    config = ExportConfiguration(
        format_type=DataExportFormat.DATABASE,
        destination_path=connection_string,
        connection_string=connection_string,
        table_name=table_name,
        **kwargs
    )
    return exporter, config

def create_api_exporter(api_endpoint: str, **kwargs) -> APIDataExporter:
    """创建API导出器"""
    exporter = APIDataExporter()
    config = ExportConfiguration(
        format_type=DataExportFormat.API,
        destination_path=api_endpoint,
        api_endpoint=api_endpoint,
        **kwargs
    )
    return exporter, config