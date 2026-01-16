"""
压缩工具模块

提供统一的压缩处理功能，减少代码重复，支持多种压缩格式。
"""

import os
import tempfile
import gzip
import zipfile
import bz2
from pathlib import Path
from typing import Union, Optional, Dict, Any, Callable
from enum import Enum

from .data_export import ExportCompression


class CompressionHandler:
    """压缩处理器"""
    
    @staticmethod
    def get_compressed_path(original_path: str, compression: ExportCompression, 
                          file_extension: str) -> str:
        """
        根据压缩类型获取压缩后的文件路径
        
        Args:
            original_path: 原始文件路径
            compression: 压缩类型
            file_extension: 文件扩展名
            
        Returns:
            压缩后的文件路径
        """
        path = original_path
        
        if compression == ExportCompression.GZIP:
            if not path.endswith('.gz'):
                path += '.gz'
        elif compression == ExportCompression.BZIP2:
            if not path.endswith('.bz2'):
                path += '.bz2'
        elif compression == ExportCompression.ZIP:
            if not path.endswith('.zip'):
                path = path.rstrip(file_extension) + '.zip'
        
        return path
    
    @staticmethod
    def write_with_compression(data: Union[str, bytes], 
                             file_path: str, 
                             compression: ExportCompression,
                             encoding: str = 'utf-8',
                             internal_filename: Optional[str] = None) -> str:
        """
        使用压缩方式写入数据
        
        Args:
            data: 要写入的数据
            file_path: 文件路径
            compression: 压缩类型
            encoding: 编码格式
            internal_filename: ZIP压缩时的内部文件名
            
        Returns:
            实际写入的文件路径
        """
        actual_path = file_path
        
        if compression == ExportCompression.GZIP:
            # 确保文件扩展名正确
            if not actual_path.endswith('.gz'):
                actual_path += '.gz'
            
            # 使用gzip写入
            if isinstance(data, str):
                with gzip.open(actual_path, 'wt', encoding=encoding) as f:
                    f.write(data)
            else:
                with gzip.open(actual_path, 'wb') as f:
                    f.write(data)
                    
        elif compression == ExportCompression.BZIP2:
            # 确保文件扩展名正确
            if not actual_path.endswith('.bz2'):
                actual_path += '.bz2'
            
            # 使用bz2写入
            if isinstance(data, str):
                with bz2.open(actual_path, 'wt', encoding=encoding) as f:
                    f.write(data)
            else:
                with bz2.open(actual_path, 'wb') as f:
                    f.write(data)
                    
        elif compression == ExportCompression.ZIP:
            # 确保文件扩展名正确
            if not actual_path.endswith('.zip'):
                actual_path = actual_path.rstrip('.') + '.zip'
            
            # 创建zip文件
            with zipfile.ZipFile(actual_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                if internal_filename:
                    filename = internal_filename
                else:
                    # 使用原始文件名
                    filename = os.path.basename(file_path).replace('.zip', '')
                
                if isinstance(data, str):
                    zipf.writestr(filename, data.encode(encoding))
                else:
                    zipf.writestr(filename, data)
                    
        else:
            # 无压缩
            if isinstance(data, str):
                with open(actual_path, 'w', encoding=encoding) as f:
                    f.write(data)
            else:
                with open(actual_path, 'wb') as f:
                    f.write(data)
        
        return actual_path
    
    @staticmethod
    def write_dataframe_with_compression(df, 
                                       file_path: str, 
                                       compression: ExportCompression,
                                       write_func: Callable,
                                       write_kwargs: Dict[str, Any] = None,
                                       internal_filename: Optional[str] = None) -> str:
        """
        使用压缩方式写入DataFrame
        
        Args:
            df: pandas DataFrame
            file_path: 文件路径
            compression: 压缩类型
            write_func: 写入函数（如df.to_csv, df.to_json等）
            write_kwargs: 写入函数的参数
            internal_filename: ZIP压缩时的内部文件名
            
        Returns:
            实际写入的文件路径
        """
        if write_kwargs is None:
            write_kwargs = {}
        
        actual_path = file_path
        
        if compression == ExportCompression.ZIP:
            # 对于ZIP压缩，需要特殊处理
            if not actual_path.endswith('.zip'):
                actual_path = actual_path.rstrip('.') + '.zip'
            
            # 创建临时文件
            with tempfile.NamedTemporaryFile(mode='w', suffix='.tmp', delete=False) as tmp:
                tmp_path = tmp.name
                
                # 写入临时文件
                write_func(tmp_path, **write_kwargs)
            
            # 将临时文件添加到zip
            with zipfile.ZipFile(actual_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                if internal_filename:
                    filename = internal_filename
                else:
                    # 使用原始文件名
                    filename = os.path.basename(file_path).replace('.zip', '')
                
                zipf.write(tmp_path, filename)
            
            # 删除临时文件
            os.unlink(tmp_path)
            
        elif compression == ExportCompression.GZIP:
            # 确保文件扩展名正确
            if not actual_path.endswith('.gz'):
                actual_path += '.gz'
            
            # 使用gzip写入
            with gzip.open(actual_path, 'wt', encoding=write_kwargs.get('encoding', 'utf-8')) as f:
                write_kwargs_copy = write_kwargs.copy()
                write_kwargs_copy['path_or_buf'] = f
                write_func(**write_kwargs_copy)
                
        elif compression == ExportCompression.BZIP2:
            # 确保文件扩展名正确
            if not actual_path.endswith('.bz2'):
                actual_path += '.bz2'
            
            # 使用bz2写入
            with bz2.open(actual_path, 'wt', encoding=write_kwargs.get('encoding', 'utf-8')) as f:
                write_kwargs_copy = write_kwargs.copy()
                write_kwargs_copy['path_or_buf'] = f
                write_func(**write_kwargs_copy)
                
        else:
            # 无压缩
            write_func(file_path, **write_kwargs)
        
        return actual_path
    
    @staticmethod
    def get_hdf5_compression_params(compression: ExportCompression) -> Dict[str, Any]:
        """
        获取HDF5压缩参数
        
        Args:
            compression: 压缩类型
            
        Returns:
            HDF5压缩参数字典
        """
        params = {}
        
        if compression == ExportCompression.GZIP:
            params['complib'] = 'zlib'
            params['complevel'] = 9
        elif compression == ExportCompression.BZIP2:
            params['complib'] = 'bzip2'
            params['complevel'] = 9
        elif compression == ExportCompression.ZIP:
            # HDF5不支持ZIP压缩，使用gzip作为替代
            params['complib'] = 'zlib'
            params['complevel'] = 9
        
        return params
    
    @staticmethod
    def get_parquet_compression_params(compression: ExportCompression) -> Dict[str, Any]:
        """
        获取Parquet压缩参数
        
        Args:
            compression: 压缩类型
            
        Returns:
            Parquet压缩参数字典
        """
        params = {}
        
        if compression == ExportCompression.GZIP:
            params['compression'] = 'gzip'
        elif compression == ExportCompression.BZIP2:
            params['compression'] = 'bzip2'
        elif compression == ExportCompression.ZIP:
            # Parquet不支持ZIP压缩，使用snappy作为替代
            params['compression'] = 'snappy'
        else:
            params['compression'] = None
        
        return params


def create_compression_handler() -> CompressionHandler:
    """创建压缩处理器实例"""
    return CompressionHandler()