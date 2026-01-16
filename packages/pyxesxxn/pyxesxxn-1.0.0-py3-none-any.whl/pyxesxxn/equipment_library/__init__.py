"""
Equipment Library Module for Scenario-Specific Energy Equipment.

This module provides a comprehensive collection of specialized equipment
for different energy system scenarios including urban, rural, and port
environments. It includes device parameters, performance models, and
easy-to-use interfaces for rapid system modeling.

Key Features:
- Pre-configured equipment for different scenarios
- Standardized equipment interfaces
- Performance and cost models
- Easy integration with PyXESXXN networks
- Scenario-specific equipment categories

Equipment Categories:
- Urban Equipment: EV charging stations, district heating, smart appliances
- Rural Equipment: Biomass generators, small hydro, rural microgrids
- Port Equipment: Shore power, hydrogen refueling, port logistics equipment
- Universal Equipment: Storage, renewable generation, grid equipment

Example Usage:
    from pyxesxxn.equipment_library import EquipmentLibrary, EquipmentConfig
    
    # Load equipment library
    library = EquipmentLibrary()
    
    # Get urban charging station
    ev_station = library.get_equipment('urban_ev_charging_station')
    
    # Add to PyXESXXN network
    network = pyxesxxn.PyXESXXNNetwork()
    components = ev_station.create_components(network)
"""

import warnings
from typing import Dict, List, Any, Optional, Union, Type, Tuple
import numpy as np
import pandas as pd

from .base import BaseEquipment, EquipmentConfig, EquipmentCategory, EquipmentType
from .urban import UrbanEquipmentLibrary
from .rural import RuralEquipmentLibrary
from .port import PortEquipmentLibrary
from .equipment_database import EquipmentDatabase
from .mobile_storage import MobileStorageEquipment, MobileStorageConfig

# Module-level configuration
DEFAULT_SCENARIOS = ['urban', 'rural', 'port']
DEFAULT_EQUIPMENT_TYPES = ['generation', 'storage', 'conversion', 'transport', 'loads']

# Equipment library instance
_equipment_database = None

def get_equipment_database() -> 'EquipmentDatabase':
    """Get or create the global equipment database instance."""
    global _equipment_database
    if _equipment_database is None:
        try:
            from .equipment_database import EquipmentDatabase
            _equipment_database = EquipmentDatabase()
        except ImportError:
            raise ImportError("EquipmentDatabase not available")
    return _equipment_database

def initialize_equipment_library() -> 'EquipmentDatabase':
    """Initialize the equipment library with default configurations.
    
    Returns
    -------
    EquipmentDatabase
        Initialized equipment database
    """
    database = get_equipment_database()
    database.initialize_default_equipment()
    return database

class EquipmentLibrary:
    """Central equipment library management class.
    
    This class provides a unified interface to access and manage
    equipment across different scenarios. It supports loading,
    filtering, and instantiating equipment models.
    """
    
    def __init__(self, database: Optional['EquipmentDatabase'] = None):
        """Initialize equipment library.
        
        Parameters
        ----------
        database : EquipmentDatabase, optional
            Equipment database instance. If None, uses global instance.
        """
        self.database = database or get_equipment_database()
        self._scenario_equipment_map = self._build_scenario_map()
    
    def _build_scenario_map(self) -> Dict[str, Dict[str, Any]]:
        """Build mapping of equipment by scenario.
        
        Returns
        -------
        Dict[str, Dict[str, Any]]
            Mapping of scenario to equipment types and classes
        """
        return {
            'urban': {
                'equipment_library': UrbanEquipmentLibrary,
            },
            'rural': {
                'equipment_library': RuralEquipmentLibrary,
            },
            'port': {
                'equipment_library': PortEquipmentLibrary,
            }
        }
    
    def get_available_equipment(self, 
                               scenario: Optional[str] = None,
                               category: Optional['EquipmentCategory'] = None,
                               equipment_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get list of available equipment.
        
        Parameters
        ----------
        scenario : str, optional
            Filter by scenario (urban, rural, port)
        category : EquipmentCategory, optional
            Filter by equipment category
        equipment_type : str, optional
            Filter by specific equipment type
            
        Returns
        -------
        List[Dict[str, Any]]
            List of equipment metadata
        """
        equipment_list = []
        
        # Get all equipment from database
        all_equipment = self.database.get_all_equipment()
        
        for equipment in all_equipment:
            # Apply filters
            if scenario and equipment.get('scenario') != scenario:
                continue
            if category and equipment.get('category') != category:
                continue
            if equipment_type and equipment.get('type') != equipment_type:
                continue
            
            equipment_list.append(equipment)
        
        return equipment_list
    
    def get_equipment_class(self, equipment_id: str) -> Optional[Type['BaseEquipment']]:
        """Get equipment class by ID.
        
        Parameters
        ----------
        equipment_id : str
            Equipment identifier
            
        Returns
        -------
        Type[BaseEquipment], optional
            Equipment class or None if not found
        """
        equipment_metadata = self.database.get_equipment_metadata(equipment_id)
        if not equipment_metadata:
            return None
        
        scenario = equipment_metadata.get('scenario')
        
        if scenario in self._scenario_equipment_map:
            scenario_equipment = self._scenario_equipment_map[scenario]
            # Return the equipment library class for the scenario
            return scenario_equipment.get('equipment_library')
        
        return None
    
    def get_equipment(self, 
                     equipment_id: str, 
                     location: Optional[str] = None,
                     **kwargs) -> Optional['BaseEquipment']:
        """Get equipment instance.
        
        Parameters
        ----------
        equipment_id : str
            Equipment identifier
        location : str, optional
            Equipment location
        **kwargs
            Additional configuration parameters
            
        Returns
        -------
        BaseEquipment, optional
            Equipment instance or None if not found
        """
        equipment_class = self.get_equipment_class(equipment_id)
        if not equipment_class:
            return None
        
        # Get equipment metadata
        metadata = self.database.get_equipment_metadata(equipment_id)
        if not metadata:
            return None
        
        # Merge metadata with kwargs
        config_dict = metadata.get('config', {})
        config_dict.update(kwargs)
        
        try:
            # Create equipment instance
            equipment = equipment_class(
                equipment_id=equipment_id,
                location=location,
                **config_dict
            )
            return equipment
        except Exception as e:
            warnings.warn(f"Failed to create equipment {equipment_id}: {e}", UserWarning)
            return None
    
    def create_equipment_from_config(self, config: Dict[str, Any]) -> Optional['BaseEquipment']:
        """Create equipment from configuration dictionary.
        
        Parameters
        ----------
        config : Dict[str, Any]
            Equipment configuration
            
        Returns
        -------
        BaseEquipment, optional
            Equipment instance or None if creation fails
        """
        equipment_id = config.get('id')
        if not equipment_id:
            return None
        
        return self.get_equipment(equipment_id, **config)
    
    def add_custom_equipment(self, equipment: 'BaseEquipment') -> bool:
        """Add custom equipment to the library.
        
        Parameters
        ----------
        equipment : BaseEquipment
            Equipment instance to add
            
        Returns
        -------
        bool
            True if successfully added, False otherwise
        """
        try:
            # Generate metadata for custom equipment
            metadata = equipment.get_equipment_metadata()
            
            # Add to database
            success = self.database.add_equipment(metadata, equipment)
            return success
        except Exception as e:
            warnings.warn(f"Failed to add custom equipment: {e}", UserWarning)
            return False
    
    def remove_equipment(self, equipment_id: str) -> bool:
        """Remove equipment from the library.
        
        Parameters
        ----------
        equipment_id : str
            Equipment identifier to remove
            
        Returns
        -------
        bool
            True if successfully removed, False otherwise
        """
        return self.database.remove_equipment(equipment_id)
    
    def search_equipment(self, query: str, fields: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Search equipment by query string.
        
        Parameters
        ----------
        query : str
            Search query string
        fields : List[str], optional
            Fields to search in (defaults to name, description, type)
            
        Returns
        -------
        List[Dict[str, Any]]
            List of matching equipment
        """
        if fields is None:
            fields = ['name', 'description', 'type', 'category']
        
        all_equipment = self.database.get_all_equipment()
        results = []
        
        query_lower = query.lower()
        
        for equipment in all_equipment:
            # Search in specified fields
            match_found = False
            for field in fields:
                if field in equipment:
                    field_value = str(equipment[field]).lower()
                    if query_lower in field_value:
                        match_found = True
                        break
            
            if match_found:
                results.append(equipment)
        
        return results
    
    def get_equipment_compatibility(self, equipment_id: str) -> Dict[str, Any]:
        """Get equipment compatibility information.
        
        Parameters
        ----------
        equipment_id : str
            Equipment identifier
            
        Returns
        -------
        Dict[str, Any]
            Compatibility information
        """
        equipment = self.get_equipment(equipment_id)
        if not equipment:
            return {}
        
        return {
            'compatible_carriers': equipment.get_supported_carriers(),
            'compatible_voltage_levels': equipment.get_compatible_voltage_levels(),
            'compatible_scenarios': equipment.get_compatible_scenarios(),
            'integration_requirements': equipment.get_integration_requirements()
        }
    
    def get_scenario_equipment_summary(self, scenario: str) -> Dict[str, Any]:
        """Get summary of equipment available for a scenario.
        
        Parameters
        ----------
        scenario : str
            Scenario name (urban, rural, port)
            
        Returns
        -------
        Dict[str, Any]
            Scenario equipment summary
        """
        equipment_list = self.get_available_equipment(scenario=scenario)
        
        summary = {
            'scenario': scenario,
            'total_equipment': len(equipment_list),
            'equipment_by_category': {},
            'equipment_by_type': {},
            'equipment_list': equipment_list
        }
        
        for equipment in equipment_list:
            category = equipment.get('category', 'unknown')
            equipment_type = equipment.get('type', 'unknown')
            
            if category not in summary['equipment_by_category']:
                summary['equipment_by_category'][category] = 0
            summary['equipment_by_category'][category] += 1
            
            if equipment_type not in summary['equipment_by_type']:
                summary['equipment_by_type'][equipment_type] = 0
            summary['equipment_by_type'][equipment_type] += 1
        
        return summary
    
    def compare_equipment(self, equipment_ids: List[str]) -> pd.DataFrame:
        """Compare multiple equipment types.
        
        Parameters
        ----------
        equipment_ids : List[str]
            List of equipment identifiers to compare
            
        Returns
        -------
        pd.DataFrame
            Comparison table
        """
        comparison_data = []
        
        for equipment_id in equipment_ids:
            equipment = self.get_equipment(equipment_id)
            if not equipment:
                continue
            
            # Get comparison metrics
            metrics = equipment.get_comparison_metrics()
            metrics['equipment_id'] = equipment_id
            metrics['name'] = equipment.name
            
            comparison_data.append(metrics)
        
        if not comparison_data:
            return pd.DataFrame()
        
        return pd.DataFrame(comparison_data)
    
    def export_equipment_config(self, equipment_ids: List[str], file_path: str) -> bool:
        """Export equipment configurations to file.
        
        Parameters
        ----------
        equipment_ids : List[str]
            Equipment identifiers to export
        file_path : str
            Output file path
            
        Returns
        -------
        bool
            True if successfully exported, False otherwise
        """
        try:
            export_configs = []
            for equipment_id in equipment_ids:
                equipment = self.get_equipment(equipment_id)
                if equipment:
                    config = equipment.get_equipment_config()
                    export_configs.append(config)
            
            # Save to JSON file
            import json
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(export_configs, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            warnings.warn(f"Failed to export equipment config: {e}", UserWarning)
            return False
    
    def import_equipment_config(self, file_path: str) -> List[str]:
        """Import equipment configurations from file.
        
        Parameters
        ----------
        file_path : str
            Input file path
            
        Returns
        -------
        List[str]
            List of successfully imported equipment IDs
        """
        try:
            import json
            with open(file_path, 'r', encoding='utf-8') as f:
                configs = json.load(f)
            
            imported_ids = []
            for config in configs:
                equipment = self.create_equipment_from_config(config)
                if equipment:
                    success = self.add_custom_equipment(equipment)
                    if success:
                        imported_ids.append(config.get('id'))
            
            return imported_ids
        except Exception as e:
            warnings.warn(f"Failed to import equipment config: {e}", UserWarning)
            return []

# Initialize default equipment library
_default_library = None

def get_default_library() -> 'EquipmentLibrary':
    """Get the default equipment library instance.
    
    Returns
    -------
    EquipmentLibrary
        Default equipment library
    """
    global _default_library
    if _default_library is None:
        _default_library = EquipmentLibrary()
        # Initialize with default equipment
        _default_library.database.initialize_default_equipment()
    return _default_library

# Convenience functions
def list_available_equipment(scenario: Optional[str] = None) -> List[Dict[str, Any]]:
    """List all available equipment.
    
    Parameters
    ----------
    scenario : str, optional
        Filter by scenario
        
    Returns
    -------
    List[Dict[str, Any]]
        List of equipment metadata
    """
    library = get_default_library()
    return library.get_available_equipment(scenario=scenario)

def get_equipment(equipment_id: str, **kwargs) -> Optional['BaseEquipment']:
    """Get equipment by ID.
    
    Parameters
    ----------
    equipment_id : str
        Equipment identifier
    **kwargs
        Additional configuration parameters
        
    Returns
    -------
    BaseEquipment, optional
        Equipment instance
    """
    library = get_default_library()
    return library.get_equipment(equipment_id, **kwargs)

def search_equipment(query: str) -> List[Dict[str, Any]]:
    """Search equipment by query.
    
    Parameters
    ----------
    query : str
        Search query
        
    Returns
    -------
    List[Dict[str, Any]]
        List of matching equipment
    """
    library = get_default_library()
    return library.search_equipment(query)

# Define __all__ for module exports
__all__ = [
    # Core classes
    'EquipmentLibrary',
    'EquipmentDatabase',
    
    # Base classes
    'BaseEquipment',
    'EquipmentConfig',
    'EquipmentCategory',
    'EquipmentType',
    
    # Urban equipment
    'EVChargingStation',
    'DistrictHeatingPlant',
    'SmartAppliance',
    'UrbanBatteryStorage',
    'UrbanSolarPV',
    'UrbanWindTurbine',
    
    # Rural equipment
    'BiomassGenerator',
    'SmallHydroPlant',
    'RuralMicrogrid',
    'RuralBatteryStorage',
    'RuralPV',
    'RuralWindTurbine',
    'BiogasPlant',
    
    # Port equipment
    'ShorePowerStation',
    'HydrogenRefuelingStation',
    'PortBatteryStorage',
    'PortSolarPV',
    'PortWindTurbine',
    'ContainerCrane',
    'PortLogisticsEquipment',
    
    # Mobile storage equipment
    'MobileStorageEquipment',
    'MobileStorageConfig',
    
    # Convenience functions
    'get_equipment',
    'list_available_equipment',
    'search_equipment',
    'get_default_library',
    'initialize_equipment_library'
]