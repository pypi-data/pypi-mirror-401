"""
Time series data processing and management for dynamic simulation.

This module provides classes and utilities for handling time series data
in dynamic energy system simulations, including data loading, interpolation,
sampling, and processing capabilities.
"""

import abc
import warnings
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union, Tuple, Callable
import logging

import numpy as np
import pandas as pd

from .base import SimulationConfig, SimulationState


class DataSourceType(Enum):
    """Type of data source."""
    CSV = "csv"
    HDF5 = "hdf5"
    NETCDF = "netcdf"
    EXCEL = "excel"
    REST_API = "rest_api"
    DATABASE = "database"
    SIMULATION = "simulation"
    SYNTHETIC = "synthetic"


class TimeSeriesMode(Enum):
    """Time series processing mode."""
    BATCH = "batch"
    STREAMING = "streaming"
    REAL_TIME = "real_time"
    ON_DEMAND = "on_demand"


@dataclass
class TimeSeriesConfig:
    """Configuration for time series data processing."""
    
    # Data source settings
    data_source_type: DataSourceType
    source_path: str
    data_format: str = "auto"
    
    # Time settings
    time_column: str = "timestamp"
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    time_zone: Optional[str] = None
    
    # Data processing settings
    resample_frequency: Optional[str] = None  # e.g., "1H", "15T", "1D"
    interpolation_method: str = "linear"
    extrapolation_method: str = "constant"
    
    # Columns and variables
    variable_columns: List[str] = field(default_factory=list)
    metadata_columns: List[str] = field(default_factory=list)
    target_variable: Optional[str] = None
    
    # Processing options
    remove_duplicates: bool = True
    handle_missing_data: str = "interpolate"  # "drop", "interpolate", "zero"
    missing_threshold: float = 0.5  # Maximum fraction of missing data allowed
    
    # Validation settings
    validate_data: bool = True
    outlier_detection: bool = False
    outlier_threshold: float = 3.0  # Standard deviations
    
    # Output settings
    cache_results: bool = True
    output_directory: str = "./time_series_output"
    save_processed_data: bool = False
    
    # Streaming settings
    streaming_mode: bool = False
    buffer_size: int = 1000
    update_frequency: float = 60.0  # seconds
    
    # Custom processing functions
    preprocessing_functions: List[str] = field(default_factory=list)
    postprocessing_functions: List[str] = field(default_factory=list)
    
    def validate(self) -> List[str]:
        """Validate time series configuration.
        
        Returns
        -------
        List[str]
            List of validation errors
        """
        errors = []
        
        # Check required fields
        if not self.source_path:
            errors.append("Source path must be specified")
        
        # Check variable columns
        if not self.variable_columns:
            errors.append("Variable columns must be specified")
        
        # Check time settings
        if self.start_time and self.end_time:
            if self.start_time >= self.end_time:
                errors.append("Start time must be before end time")
        
        # Check resample frequency
        if self.resample_frequency:
            try:
                pd.Timedelta(self.resample_frequency)
            except Exception:
                errors.append(f"Invalid resample frequency: {self.resample_frequency}")
        
        # Check missing data handling
        valid_missing_methods = ["drop", "interpolate", "zero"]
        if self.handle_missing_data not in valid_missing_methods:
            errors.append(f"Invalid missing data method: {self.handle_missing_data}")
        
        return errors


class TimeSeriesData:
    """Container for time series data.
    
    This class manages time series data with metadata, validation,
    and processing capabilities.
    """
    
    def __init__(self, 
                 data: pd.DataFrame,
                 config: TimeSeriesConfig,
                 source_info: Optional[Dict[str, Any]] = None):
        """Initialize time series data.
        
        Parameters
        ----------
        data : pd.DataFrame
            Time series data
        config : TimeSeriesConfig
            Configuration
        source_info : Dict[str, Any], optional
            Source information
        """
        self.data = data.copy()
        self.config = config
        self.source_info = source_info or {}
        
        # Validate and process data
        self._validate_data()
        self._process_data()
        
        # Processing history
        self.processing_history = []
        self.metadata = {
            'creation_time': datetime.now(),
            'last_modified': datetime.now(),
            'version': '1.0',
            'total_records': len(self.data),
            'time_range': (self.data.index.min(), self.data.index.max()) if len(self.data) > 0 else (None, None)
        }
    
    def _validate_data(self) -> None:
        """Validate time series data."""
        if self.config.validate_data:
            errors = []
            
            # Check time column
            if self.config.time_column not in self.data.columns:
                errors.append(f"Time column '{self.config.time_column}' not found")
            
            # Check variable columns
            missing_vars = set(self.config.variable_columns) - set(self.data.columns)
            if missing_vars:
                errors.append(f"Missing variable columns: {missing_vars}")
            
            # Check for missing data
            for var in self.config.variable_columns:
                if var in self.data.columns:
                    missing_ratio = self.data[var].isnull().sum() / len(self.data)
                    if missing_ratio > self.config.missing_threshold:
                        errors.append(f"Variable '{var}' has {missing_ratio:.2%} missing data")
            
            # Check for outliers
            if self.config.outlier_detection:
                self._detect_outliers()
            
            if errors:
                raise ValueError(f"Data validation failed: {errors}")
    
    def _process_data(self) -> None:
        """Process time series data according to configuration."""
        # Set time index
        if self.config.time_column in self.data.columns:
            self.data = self.data.set_index(self.config.time_column)
        
        # Remove duplicates
        if self.config.remove_duplicates:
            self.data = self.data[~self.data.index.duplicated(keep='first')]
        
        # Sort by time
        self.data = self.data.sort_index()
        
        # Filter by time range
        if self.config.start_time:
            self.data = self.data[self.data.index >= self.config.start_time]
        if self.config.end_time:
            self.data = self.data[self.data.index <= self.config.end_time]
        
        # Handle missing data
        if self.config.handle_missing_data == "interpolate":
            self.data[self.config.variable_columns] = self.data[self.config.variable_columns].interpolate(
                method=self.config.interpolation_method
            )
        elif self.config.handle_missing_data == "zero":
            self.data[self.config.variable_columns] = self.data[self.config.variable_columns].fillna(0)
        elif self.config.handle_missing_data == "drop":
            self.data = self.data.dropna(subset=self.config.variable_columns)
        
        # Resample data
        if self.config.resample_frequency:
            self.data = self.data.resample(self.config.resample_frequency).mean()
        
        # Update metadata
        self.metadata.update({
            'total_records': len(self.data),
            'time_range': (self.data.index.min(), self.data.index.max()) if len(self.data) > 0 else (None, None),
            'last_modified': datetime.now()
        })
    
    def _detect_outliers(self) -> None:
        """Detect outliers in the data."""
        for var in self.config.variable_columns:
            if var in self.data.columns:
                series = self.data[var].dropna()
                if len(series) > 0:
                    mean = series.mean()
                    std = series.std()
                    threshold = self.config.outlier_threshold * std
                    
                    outliers = np.abs(series - mean) > threshold
                    if outliers.any():
                        logging.warning(f"Detected {outliers.sum()} outliers in variable '{var}'")
                        # Store outlier information
                        if 'outliers' not in self.metadata:
                            self.metadata['outliers'] = {}
                        self.metadata['outliers'][var] = {
                            'count': outliers.sum(),
                            'indices': outliers[outliers].index.tolist(),
                            'threshold': threshold
                        }
    
    def get_data(self, 
                 variables: Optional[List[str]] = None,
                 time_range: Optional[Tuple[datetime, datetime]] = None) -> pd.DataFrame:
        """Get time series data.
        
        Parameters
        ----------
        variables : List[str], optional
            Variables to return
        time_range : Tuple[datetime, datetime], optional
            Time range to filter data
            
        Returns
        -------
        pd.DataFrame
            Filtered time series data
        """
        data = self.data.copy()
        
        # Filter by variables
        if variables:
            available_vars = [var for var in variables if var in data.columns]
            data = data[available_vars]
        else:
            data = data[self.config.variable_columns]
        
        # Filter by time range
        if time_range:
            start_time, end_time = time_range
            data = data[(data.index >= start_time) & (data.index <= end_time)]
        
        return data
    
    def get_variable(self, variable: str, time_range: Optional[Tuple[datetime, datetime]] = None) -> pd.Series:
        """Get single variable time series.
        
        Parameters
        ----------
        variable : str
            Variable name
        time_range : Tuple[datetime, datetime], optional
            Time range to filter data
            
        Returns
        -------
        pd.Series
            Variable time series
        """
        data = self.get_data([variable], time_range)
        return data[variable] if len(data) > 0 else pd.Series(dtype=float)
    
    def interpolate(self, 
                   target_times: pd.DatetimeIndex,
                   variables: Optional[List[str]] = None,
                   method: str = "linear") -> pd.DataFrame:
        """Interpolate data to target time points.
        
        Parameters
        ----------
        target_times : pd.DatetimeIndex
            Target time points
        variables : List[str], optional
            Variables to interpolate
        method : str
            Interpolation method
            
        Returns
        -------
        pd.DataFrame
            Interpolated data
        """
        if variables is None:
            variables = self.config.variable_columns
        
        available_vars = [var for var in variables if var in self.data.columns]
        if not available_vars:
            return pd.DataFrame(index=target_times)
        
        interpolated = {}
        for var in available_vars:
            interpolated[var] = self.data[var].reindex(
                target_times.union(self.data.index)
            ).interpolate(method=method).reindex(target_times)
        
        result = pd.DataFrame(interpolated, index=target_times)
        
        # Record processing
        self.processing_history.append({
            'operation': 'interpolate',
            'timestamp': datetime.now(),
            'method': method,
            'target_times': len(target_times),
            'variables': available_vars
        })
        
        return result
    
    def resample(self, frequency: str, method: str = "mean") -> 'TimeSeriesData':
        """Resample data to different frequency.
        
        Parameters
        ----------
        frequency : str
            New frequency (e.g., "1H", "15T")
        method : str
            Aggregation method
            
        Returns
        -------
        TimeSeriesData
            Resampled data
        """
        # Create new configuration
        new_config = self.config
        new_config.resample_frequency = frequency
        
        # Resample data
        if method == "mean":
            resampled_data = self.data.resample(frequency).mean()
        elif method == "sum":
            resampled_data = self.data.resample(frequency).sum()
        elif method == "max":
            resampled_data = self.data.resample(frequency).max()
        elif method == "min":
            resampled_data = self.data.resample(frequency).min()
        else:
            raise ValueError(f"Unknown aggregation method: {method}")
        
        # Create new TimeSeriesData instance
        result = TimeSeriesData(resampled_data, new_config, self.source_info)
        result.metadata['original_frequency'] = self.metadata.get('current_frequency', 'unknown')
        result.metadata['current_frequency'] = frequency
        
        return result
    
    def add_variable(self, 
                    name: str, 
                    data: pd.Series, 
                    metadata: Optional[Dict[str, Any]] = None) -> None:
        """Add new variable to time series.
        
        Parameters
        ----------
        name : str
            Variable name
        data : pd.Series
            Variable data
        metadata : Dict[str, Any], optional
            Variable metadata
        """
        if len(data) != len(self.data):
            raise ValueError("Data length must match existing data")
        
        # Align indices
        if not data.index.equals(self.data.index):
            data = data.reindex(self.data.index)
        
        self.data[name] = data
        self.config.variable_columns.append(name)
        
        # Update metadata
        if metadata:
            if 'variables' not in self.metadata:
                self.metadata['variables'] = {}
            self.metadata['variables'][name] = metadata
    
    def remove_variable(self, name: str) -> None:
        """Remove variable from time series.
        
        Parameters
        ----------
        name : str
            Variable name
        """
        if name in self.data.columns:
            del self.data[name]
        if name in self.config.variable_columns:
            self.config.variable_columns.remove(name)
        
        self.metadata['last_modified'] = datetime.now()
    
    def get_statistics(self, variables: Optional[List[str]] = None) -> Dict[str, Dict[str, float]]:
        """Get statistical summary of variables.
        
        Parameters
        ----------
        variables : List[str], optional
            Variables to analyze
            
        Returns
        -------
        Dict[str, Dict[str, float]]
            Statistics for each variable
        """
        if variables is None:
            variables = self.config.variable_columns
        
        available_vars = [var for var in variables if var in self.data.columns]
        if not available_vars:
            return {}
        
        stats = {}
        for var in available_vars:
            series = self.data[var].dropna()
            if len(series) > 0:
                stats[var] = {
                    'count': len(series),
                    'mean': series.mean(),
                    'std': series.std(),
                    'min': series.min(),
                    'max': series.max(),
                    'median': series.median(),
                    'q25': series.quantile(0.25),
                    'q75': series.quantile(0.75),
                    'missing_count': self.data[var].isnull().sum(),
                    'missing_percentage': self.data[var].isnull().sum() / len(self.data) * 100
                }
        
        return stats
    
    def export_data(self, 
                   file_path: str, 
                   variables: Optional[List[str]] = None,
                   format: str = "csv") -> bool:
        """Export time series data to file.
        
        Parameters
        ----------
        file_path : str
            Output file path
        variables : List[str], optional
            Variables to export
        format : str
            Export format ('csv', 'hdf5', 'excel')
            
        Returns
        -------
        bool
            True if successfully exported
        """
        try:
            data = self.get_data(variables)
            
            if format.lower() == "csv":
                data.to_csv(file_path)
            elif format.lower() == "hdf5":
                data.to_hdf(file_path, key='time_series', mode='w')
            elif format.lower() == "excel":
                data.to_excel(file_path)
            else:
                raise ValueError(f"Unsupported format: {format}")
            
            logging.info(f"Exported time series data to {file_path}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to export data: {e}")
            return False
    
    def __len__(self) -> int:
        """Return number of data points."""
        return len(self.data)
    
    def __getitem__(self, key: str) -> pd.Series:
        """Get variable by name."""
        return self.data[key]
    
    def __repr__(self) -> str:
        """String representation."""
        return (f"TimeSeriesData(variables={len(self.config.variable_columns)}, "
                f"records={len(self.data)}, "
                f"time_range={self.metadata['time_range']})")


class TimeSeriesProcessor(abc.ABC):
    """Abstract base class for time series processors.
    
    This class defines the interface for time series data processing
    components that can load, transform, and manage time series data.
    """
    
    def __init__(self, config: TimeSeriesConfig):
        """Initialize time series processor.
        
        Parameters
        ----------
        config : TimeSeriesConfig
            Processor configuration
        """
        self.config = config
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        
        # Validate configuration
        validation_errors = config.validate()
        if validation_errors:
            raise ValueError(f"Invalid configuration: {validation_errors}")
    
    @abc.abstractmethod
    def load_data(self) -> TimeSeriesData:
        """Load time series data.
        
        Returns
        -------
        TimeSeriesData
            Loaded time series data
        """
        pass
    
    @abc.abstractmethod
    def process_data(self, data: TimeSeriesData) -> TimeSeriesData:
        """Process time series data.
        
        Parameters
        ----------
        data : TimeSeriesData
            Input time series data
            
        Returns
        -------
        TimeSeriesData
            Processed time series data
        """
        pass


class CSVTimeSeriesProcessor(TimeSeriesProcessor):
    """Time series processor for CSV files."""
    
    def load_data(self) -> TimeSeriesData:
        """Load time series data from CSV file.
        
        Returns
        -------
        TimeSeriesData
            Loaded time series data
        """
        try:
            # Determine delimiter
            delimiter = "," if self.config.data_format == "auto" else self.config.data_format
            
            # Load CSV data
            data = pd.read_csv(
                self.config.source_path,
                delimiter=delimiter,
                parse_dates=[self.config.time_column] if self.config.time_column else False,
                index_col=self.config.time_column if self.config.time_column else None
            )
            
            # Create source info
            source_info = {
                'source_type': 'csv',
                'file_path': self.config.source_path,
                'file_size': len(data),
                'columns': list(data.columns)
            }
            
            return TimeSeriesData(data, self.config, source_info)
            
        except Exception as e:
            self.logger.error(f"Failed to load CSV data: {e}")
            raise
    
    def process_data(self, data: TimeSeriesData) -> TimeSeriesData:
        """Process CSV time series data.
        
        Parameters
        ----------
        data : TimeSeriesData
            Input time series data
            
        Returns
        -------
        TimeSeriesData
            Processed time series data
        """
        # Apply CSV-specific processing here
        return data


class HDF5TimeSeriesProcessor(TimeSeriesProcessor):
    """Time series processor for HDF5 files."""
    
    def load_data(self) -> TimeSeriesData:
        """Load time series data from HDF5 file.
        
        Returns
        -------
        TimeSeriesData
            Loaded time series data
        """
        try:
            # Load HDF5 data
            data = pd.read_hdf(self.config.source_path)
            
            # Create source info
            source_info = {
                'source_type': 'hdf5',
                'file_path': self.config.source_path,
                'file_size': len(data),
                'columns': list(data.columns)
            }
            
            return TimeSeriesData(data, self.config, source_info)
            
        except Exception as e:
            self.logger.error(f"Failed to load HDF5 data: {e}")
            raise
    
    def process_data(self, data: TimeSeriesData) -> TimeSeriesData:
        """Process HDF5 time series data.
        
        Parameters
        ----------
        data : TimeSeriesData
            Input time series data
            
        Returns
        -------
        TimeSeriesData
            Processed time series data
        """
        # Apply HDF5-specific processing here
        return data


class SyntheticTimeSeriesProcessor(TimeSeriesProcessor):
    """Time series processor for synthetic data generation."""
    
    def __init__(self, config: TimeSeriesConfig):
        """Initialize synthetic data processor.
        
        Parameters
        ----------
        config : TimeSeriesConfig
            Processor configuration
        """
        super().__init__(config)
        
        # Generate synthetic data configuration
        if not config.end_time:
            config.end_time = config.start_time or datetime.now()
        if not config.start_time:
            config.start_time = config.end_time - timedelta(hours=24)
    
    def load_data(self) -> TimeSeriesData:
        """Generate synthetic time series data.
        
        Returns
        -------
        TimeSeriesData
            Generated time series data
        """
        try:
            # Create time index
            if self.config.resample_frequency:
                time_index = pd.date_range(
                    start=self.config.start_time,
                    end=self.config.end_time,
                    freq=self.config.resample_frequency
                )
            else:
                time_index = pd.date_range(
                    start=self.config.start_time,
                    end=self.config.end_time,
                    freq='1H'
                )
            
            # Generate synthetic data for each variable
            data = {}
            for var in self.config.variable_columns:
                if 'solar' in var.lower():
                    # Generate solar irradiance pattern
                    hours = time_index.hour / 24.0
                    daily_cycle = np.maximum(0, np.sin(np.pi * (hours - 6) / 12))
                    data[var] = daily_cycle * (800 + np.random.normal(0, 50, len(time_index)))
                elif 'wind' in var.lower():
                    # Generate wind speed pattern
                    base_speed = 8.0
                    variations = np.random.normal(0, 2, len(time_index))
                    data[var] = np.maximum(0, base_speed + variations)
                elif 'load' in var.lower():
                    # Generate load pattern with daily and weekly cycles
                    hours = time_index.hour + time_index.dayofweek * 24
                    daily_pattern = 1000 + 200 * np.sin(2 * np.pi * hours / 24) + 100 * np.sin(2 * np.pi * hours / 168)
                    noise = np.random.normal(0, 50, len(time_index))
                    data[var] = np.maximum(0, daily_pattern + noise)
                elif 'temperature' in var.lower():
                    # Generate temperature pattern
                    hours = time_index.hour / 24.0
                    daily_variation = 5 * np.sin(2 * np.pi * (hours - 6) / 24)
                    seasonal = 10 * np.sin(2 * np.pi * time_index.dayofyear / 365.25)
                    data[var] = 20 + daily_variation + seasonal + np.random.normal(0, 2, len(time_index))
                else:
                    # Generate random data for unknown variables
                    data[var] = np.random.normal(100, 10, len(time_index))
            
            # Create DataFrame
            result_df = pd.DataFrame(data, index=time_index)
            
            # Create source info
            source_info = {
                'source_type': 'synthetic',
                'generation_method': 'mathematical_models',
                'time_range': (self.config.start_time, self.config.end_time),
                'frequency': self.config.resample_frequency,
                'variables': self.config.variable_columns
            }
            
            return TimeSeriesData(result_df, self.config, source_info)
            
        except Exception as e:
            self.logger.error(f"Failed to generate synthetic data: {e}")
            raise
    
    def process_data(self, data: TimeSeriesData) -> TimeSeriesData:
        """Process synthetic time series data.
        
        Parameters
        ----------
        data : TimeSeriesData
            Input time series data
            
        Returns
        -------
        TimeSeriesData
            Processed time series data
        """
        # Apply synthetic data-specific processing here
        return data


class TimeSeriesManager:
    """Manager for time series data processing and retrieval.
    
    This class provides a unified interface for managing multiple time
    series data sources and processing pipelines.
    """
    
    def __init__(self, config: SimulationConfig):
        """Initialize time series manager.
        
        Parameters
        ----------
        config : SimulationConfig
            Simulation configuration
        """
        self.config = config
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        
        # Data storage
        self.time_series_data: Dict[str, TimeSeriesData] = {}
        self.processors: Dict[str, TimeSeriesProcessor] = {}
        
        # Current state
        self.current_time_index = None
        self.time_series_mode = TimeSeriesMode.BATCH
        
        # Performance metrics
        self.loading_times = {}
        self.processing_times = {}
    
    def register_data_source(self, 
                           name: str,
                           processor: TimeSeriesProcessor) -> None:
        """Register time series data source.
        
        Parameters
        ----------
        name : str
            Data source name
        processor : TimeSeriesProcessor
            Data processor instance
        """
        self.processors[name] = processor
        self.logger.info(f"Registered data source: {name}")
    
    def load_data(self, name: str, force_reload: bool = False) -> TimeSeriesData:
        """Load time series data.
        
        Parameters
        ----------
        name : str
            Data source name
        force_reload : bool
            Force reload even if data exists
            
        Returns
        -------
        TimeSeriesData
            Loaded time series data
        """
        if name not in self.processors:
            raise ValueError(f"Data source '{name}' not registered")
        
        # Return cached data if available and not forcing reload
        if not force_reload and name in self.time_series_data:
            return self.time_series_data[name]
        
        # Load data using processor
        start_time = datetime.now()
        try:
            data = self.processors[name].load_data()
            loading_time = (datetime.now() - start_time).total_seconds()
            self.loading_times[name] = loading_time
            
            # Process data
            processed_data = self.processors[name].process_data(data)
            
            # Cache result
            self.time_series_data[name] = processed_data
            
            self.logger.info(f"Loaded data source '{name}' in {loading_time:.2f} seconds")
            return processed_data
            
        except Exception as e:
            self.logger.error(f"Failed to load data source '{name}': {e}")
            raise
    
    def get_data(self, 
                 name: str,
                 variables: Optional[List[str]] = None,
                 time_range: Optional[Tuple[datetime, datetime]] = None,
                 interpolate: bool = False) -> pd.DataFrame:
        """Get time series data.
        
        Parameters
        ----------
        name : str
            Data source name
        variables : List[str], optional
            Variables to return
        time_range : Tuple[datetime, datetime], optional
            Time range to filter data
        interpolate : bool
            Whether to interpolate data
            
        Returns
        -------
        pd.DataFrame
            Time series data
        """
        # Load data if not already loaded
        if name not in self.time_series_data:
            self.load_data(name)
        
        data = self.time_series_data[name]
        
        # Get base data
        result = data.get_data(variables, time_range)
        
        # Interpolate if requested
        if interpolate and self.current_time_index is not None:
            result = data.interpolate(self.current_time_index, variables)
        
        return result
    
    def get_current_values(self, 
                          variables: List[str],
                          time: Optional[datetime] = None) -> Dict[str, float]:
        """Get current values for specified variables.
        
        Parameters
        ----------
        variables : List[str]
            Variables to retrieve
        time : datetime, optional
            Time for value retrieval
            
        Returns
        -------
        Dict[str, float]
            Variable values
        """
        if time is None:
            time = datetime.now()
        
        values = {}
        
        # Search through all loaded data sources
        for name, data in self.time_series_data.items():
            data_vars = [var for var in variables if var in data.config.variable_columns]
            for var in data_vars:
                try:
                    # Find closest time point
                    time_diffs = np.abs(data.data.index - time)
                    closest_idx = time_diffs.argmin()
                    value = data.data[var].iloc[closest_idx]
                    values[f"{name}.{var}"] = float(value)
                except Exception as e:
                    self.logger.warning(f"Failed to get value for {name}.{var}: {e}")
                    values[f"{name}.{var}"] = 0.0
        
        return values
    
    def set_time_index(self, time_index: pd.DatetimeIndex) -> None:
        """Set simulation time index for interpolation.
        
        Parameters
        ----------
        time_index : pd.DatetimeIndex
            Simulation time index
        """
        self.current_time_index = time_index
        self.logger.info(f"Set time index with {len(time_index)} time points")
    
    def get_interpolated_data(self, 
                            source_name: str,
                            time_index: Optional[pd.DatetimeIndex] = None) -> pd.DataFrame:
        """Get interpolated data for simulation time index.
        
        Parameters
        ----------
        source_name : str
            Data source name
        time_index : pd.DatetimeIndex, optional
            Target time index
            
        Returns
        -------
        pd.DataFrame
            Interpolated data
        """
        if time_index is None:
            time_index = self.current_time_index
        
        if time_index is None:
            raise ValueError("No time index specified for interpolation")
        
        if source_name not in self.time_series_data:
            self.load_data(source_name)
        
        data = self.time_series_data[source_name]
        return data.interpolate(time_index)
    
    def get_statistics(self, source_name: str, variables: Optional[List[str]] = None) -> Dict[str, Dict[str, float]]:
        """Get statistics for data source.
        
        Parameters
        ----------
        source_name : str
            Data source name
        variables : List[str], optional
            Variables to analyze
            
        Returns
        -------
        Dict[str, Dict[str, float]]
            Statistics for each variable
        """
        if source_name not in self.time_series_data:
            self.load_data(source_name)
        
        data = self.time_series_data[source_name]
        return data.get_statistics(variables)
    
    def export_data(self, 
                   source_name: str,
                   file_path: str,
                   variables: Optional[List[str]] = None,
                   format: str = "csv") -> bool:
        """Export time series data.
        
        Parameters
        ----------
        source_name : str
            Data source name
        file_path : str
            Output file path
        variables : List[str], optional
            Variables to export
        format : str
            Export format
            
        Returns
        -------
        bool
            True if successfully exported
        """
        if source_name not in self.time_series_data:
            self.load_data(source_name)
        
        data = self.time_series_data[source_name]
        return data.export_data(file_path, variables, format)
    
    def cleanup_cache(self) -> None:
        """Clean up cached data to free memory."""
        # Keep only essential data or clear all if memory is limited
        cache_count = len(self.time_series_data)
        self.logger.info(f"Cleaning up {cache_count} cached datasets")
        
        self.time_series_data.clear()
        self.time_series_data = {}
        
        self.logger.info("Cache cleanup completed")
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary.
        
        Returns
        -------
        Dict[str, Any]
            Performance summary
        """
        return {
            'loaded_sources': len(self.time_series_data),
            'total_sources': len(self.processors),
            'loading_times': self.loading_times.copy(),
            'processing_times': self.processing_times.copy(),
            'current_mode': self.time_series_mode.value,
            'time_index_size': len(self.current_time_index) if self.current_time_index is not None else 0
        }


# Utility functions
def create_time_series_manager(config: SimulationConfig) -> TimeSeriesManager:
    """Create time series manager with default processors.
    
    Parameters
    ----------
    config : SimulationConfig
        Simulation configuration
        
    Returns
    -------
    TimeSeriesManager
        Configured time series manager
    """
    manager = TimeSeriesManager(config)
    
    # Register default processors based on configuration
    if config.weather_data_file:
        processor = get_processor_for_file(config.weather_data_file)
        if processor:
            manager.register_data_source("weather", processor)
    
    if config.load_data_file:
        processor = get_processor_for_file(config.load_data_file)
        if processor:
            manager.register_data_source("load", processor)
    
    if config.price_data_file:
        processor = get_processor_for_file(config.price_data_file)
        if processor:
            manager.register_data_source("price", processor)
    
    if config.renewable_data_file:
        processor = get_processor_for_file(config.renewable_data_file)
        if processor:
            manager.register_data_source("renewable", processor)
    
    return manager


def get_processor_for_file(file_path: str) -> Optional[TimeSeriesProcessor]:
    """Get appropriate processor for file type.
    
    Parameters
    ----------
    file_path : str
        File path
        
    Returns
    -------
    TimeSeriesProcessor, optional
        Appropriate processor or None
    """
    if not file_path or file_path == "synthetic":
        # Create synthetic data processor
        config = TimeSeriesConfig(
            data_source_type=DataSourceType.SYNTHETIC,
            source_path="synthetic",
            variable_columns=["load", "wind_speed", "solar_irradiance", "temperature"],
            start_time=datetime.now() - timedelta(days=7),
            end_time=datetime.now()
        )
        return SyntheticTimeSeriesProcessor(config)
    
    # Determine file type and create appropriate processor
    if file_path.lower().endswith('.csv'):
        config = TimeSeriesConfig(
            data_source_type=DataSourceType.CSV,
            source_path=file_path,
            variable_columns=[]  # Will be detected
        )
        return CSVTimeSeriesProcessor(config)
    elif file_path.lower().endswith(('.h5', '.hdf5')):
        config = TimeSeriesConfig(
            data_source_type=DataSourceType.HDF5,
            source_path=file_path,
            variable_columns=[]  # Will be detected
        )
        return HDF5TimeSeriesProcessor(config)
    
    return None


# Define imports for compatibility
try:
    from enum import Enum
except ImportError:
    # Fallback for Python < 3.4
    class Enum:
        def __init__(self, *args):
            for item in args:
                setattr(self, item.replace(' ', '_'), item)


# Define __all__ for module exports
__all__ = [
    # Core classes
    'TimeSeriesManager',
    'TimeSeriesData',
    'TimeSeriesProcessor',
    
    # Configuration classes
    'TimeSeriesConfig',
    
    # Concrete processors
    'CSVTimeSeriesProcessor',
    'HDF5TimeSeriesProcessor',
    'SyntheticTimeSeriesProcessor',
    
    # Enumerations
    'DataSourceType',
    'TimeSeriesMode',
    
    # Utility functions
    'create_time_series_manager',
    'get_processor_for_file'
]