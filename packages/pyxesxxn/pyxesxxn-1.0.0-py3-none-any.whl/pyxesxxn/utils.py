# SPDX-FileCopyrightText: PyXESXXN Contributors
#
# SPDX-License-Identifier: MIT

"""Utility modules for PyXESXXN energy system analysis."""

from __future__ import annotations

import json
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Union
from pathlib import Path


class DataHandler:
    """Handle data loading, processing, and validation for PyXESXXN models."""
    
    def __init__(self, data_path: Optional[str] = None):
        """Initialize data handler.
        
        Parameters
        ----------
        data_path : str, optional
            Path to data directory, by default None
        """
        self.data_path = Path(data_path) if data_path else None
        self._cache: Dict[str, Any] = {}
    
    def load_csv(self, filename: str, **kwargs) -> pd.DataFrame:
        """Load CSV file into DataFrame.
        
        Parameters
        ----------
        filename : str
            Name of CSV file
        **kwargs
            Additional arguments for pandas.read_csv
            
        Returns
        -------
        pd.DataFrame
            Loaded data
        """
        if self.data_path:
            file_path = self.data_path / filename
        else:
            file_path = Path(filename)
        
        return pd.read_csv(file_path, **kwargs)
    
    def load_json(self, filename: str) -> Dict[str, Any]:
        """Load JSON file into dictionary.
        
        Parameters
        ----------
        filename : str
            Name of JSON file
            
        Returns
        -------
        Dict[str, Any]
            Loaded JSON data
        """
        if self.data_path:
            file_path = self.data_path / filename
        else:
            file_path = Path(filename)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def validate_data(self, data: pd.DataFrame, required_columns: List[str]) -> bool:
        """Validate DataFrame structure.
        
        Parameters
        ----------
        data : pd.DataFrame
            Data to validate
        required_columns : List[str]
            List of required column names
            
        Returns
        -------
        bool
            True if data is valid, False otherwise
        """
        missing_columns = [col for col in required_columns if col not in data.columns]
        return len(missing_columns) == 0


class TimeSeries:
    """Handle time series data for energy system analysis."""
    
    def __init__(self, data: Optional[pd.Series] = None):
        """Initialize time series.
        
        Parameters
        ----------
        data : pd.Series, optional
            Time series data, by default None
        """
        self.data = data if data is not None else pd.Series()
    
    def resample(self, frequency: str) -> TimeSeries:
        """Resample time series to different frequency.
        
        Parameters
        ----------
        frequency : str
            Target frequency (e.g., 'H', 'D', 'M')
            
        Returns
        -------
        TimeSeries
            Resampled time series
        """
        if self.data.empty:
            return TimeSeries()
        
        resampled = self.data.resample(frequency).mean()
        return TimeSeries(resampled)
    
    def normalize(self) -> TimeSeries:
        """Normalize time series to [0, 1] range.
        
        Returns
        -------
        TimeSeries
            Normalized time series
        """
        if self.data.empty:
            return TimeSeries()
        
        normalized = (self.data - self.data.min()) / (self.data.max() - self.data.min())
        return TimeSeries(normalized)
    
    def get_statistics(self) -> Dict[str, float]:
        """Get descriptive statistics of time series.
        
        Returns
        -------
        Dict[str, float]
            Dictionary of statistics
        """
        if self.data.empty:
            return {}
        
        return {
            'mean': float(self.data.mean()),
            'std': float(self.data.std()),
            'min': float(self.data.min()),
            'max': float(self.data.max()),
            'median': float(self.data.median())
        }


class GeographicData:
    """Handle geographic and spatial data for energy system modeling."""
    
    def __init__(self):
        """Initialize geographic data handler."""
        self.coordinates: Dict[str, tuple] = {}
        self.regions: Dict[str, List[str]] = {}
    
    def add_location(self, name: str, latitude: float, longitude: float):
        """Add geographic location.
        
        Parameters
        ----------
        name : str
            Location name
        latitude : float
            Latitude coordinate
        longitude : float
            Longitude coordinate
        """
        self.coordinates[name] = (latitude, longitude)
    
    def calculate_distance(self, loc1: str, loc2: str) -> float:
        """Calculate distance between two locations using Haversine formula.
        
        Parameters
        ----------
        loc1 : str
            First location name
        loc2 : str
            Second location name
            
        Returns
        -------
        float
            Distance in kilometers
        """
        if loc1 not in self.coordinates or loc2 not in self.coordinates:
            raise ValueError(f"Location not found: {loc1} or {loc2}")
        
        lat1, lon1 = self.coordinates[loc1]
        lat2, lon2 = self.coordinates[loc2]
        
        # Haversine formula
        R = 6371  # Earth radius in km
        dlat = np.radians(lat2 - lat1)
        dlon = np.radians(lon2 - lon1)
        a = np.sin(dlat/2)**2 + np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.sin(dlon/2)**2
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
        
        return R * c


class Visualization:
    """Create visualizations for energy system analysis results."""
    
    def __init__(self):
        """Initialize visualization tools."""
        self.figures: List[Any] = []
    
    def plot_time_series(self, data: pd.Series, title: str = "Time Series") -> None:
        """Plot time series data.
        
        Parameters
        ----------
        data : pd.Series
            Time series data to plot
        title : str, optional
            Plot title, by default "Time Series"
        """
        try:
            import matplotlib.pyplot as plt
            
            plt.figure(figsize=(10, 6))
            data.plot()
            plt.title(title)
            plt.xlabel('Time')
            plt.ylabel('Value')
            plt.grid(True)
            plt.tight_layout()
            plt.show()
            
        except ImportError:
            print("Matplotlib not available for plotting")
    
    def create_energy_flow_chart(self, flows: Dict[str, float]) -> None:
        """Create energy flow chart (sankey diagram placeholder).
        
        Parameters
        ----------
        flows : Dict[str, float]
            Dictionary of energy flows
        """
        print("Energy Flow Chart:")
        for source, flow in flows.items():
            print(f"  {source}: {flow:.2f} units")


class ReportGenerator:
    """Generate analysis reports for energy system models."""
    
    def __init__(self, title: str = "PyXESXXN Analysis Report"):
        """Initialize report generator.
        
        Parameters
        ----------
        title : str, optional
            Report title, by default "PyXESXXN Analysis Report"
        """
        self.title = title
        self.sections: List[Dict[str, Any]] = []
    
    def add_section(self, title: str, content: str, data: Optional[Dict] = None):
        """Add section to report.
        
        Parameters
        ----------
        title : str
            Section title
        content : str
            Section content
        data : Dict, optional
            Additional data for the section, by default None
        """
        self.sections.append({
            'title': title,
            'content': content,
            'data': data or {}
        })
    
    def generate_markdown(self) -> str:
        """Generate markdown report.
        
        Returns
        -------
        str
            Markdown formatted report
        """
        report = f"# {self.title}\n\n"
        
        for i, section in enumerate(self.sections, 1):
            report += f"## {i}. {section['title']}\n\n"
            report += f"{section['content']}\n\n"
            
            if section['data']:
                report += "**Data Summary:**\n\n"
                for key, value in section['data'].items():
                    report += f"- {key}: {value}\n"
                report += "\n"
        
        return report
    
    def save_report(self, filename: str, format: str = "markdown"):
        """Save report to file.
        
        Parameters
        ----------
        filename : str
            Output filename
        format : str, optional
            Report format, by default "markdown"
        """
        if format == "markdown":
            content = self.generate_markdown()
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
        else:
            raise ValueError(f"Unsupported format: {format}")