"""Equipment database module for PyXESXXN equipment library.

This module provides a simple equipment database for storing and managing
equipment metadata and configurations.
"""

from typing import Dict, List, Optional, Any
import warnings


class EquipmentDatabase:
    """Simple equipment database for PyXESXXN equipment library.
    
    This is a placeholder implementation to enable basic functionality
    while the full database implementation is being developed.
    """
    
    def __init__(self):
        """Initialize equipment database."""
        self._equipment_metadata = {}
        self._equipment_configs = {}
        self._initialized = False
    
    def initialize_default_equipment(self) -> None:
        """Initialize database with default equipment configurations."""
        # Create simple placeholder data
        default_equipment = [
            {
                'id': 'urban_solar_pv_1',
                'name': 'Urban Solar PV System',
                'category': 'generation',
                'type': 'solar_pv',
                'scenario': 'urban',
                'config': {'capacity': 100, 'efficiency': 0.20}
            },
            {
                'id': 'rural_battery_1',
                'name': 'Rural Battery Storage',
                'category': 'storage', 
                'type': 'battery_storage',
                'scenario': 'rural',
                'config': {'capacity': 50, 'efficiency': 0.90}
            }
        ]
        
        for equipment in default_equipment:
            self._equipment_metadata[equipment['id']] = equipment
            self._equipment_configs[equipment['id']] = equipment.get('config', {})
        
        self._initialized = True
        warnings.warn("EquipmentDatabase initialized with placeholder data", UserWarning)
    
    def get_all_equipment(self) -> List[Dict[str, Any]]:
        """Get all equipment from database.
        
        Returns
        -------
        List[Dict[str, Any]]
            List of all equipment metadata
        """
        return list(self._equipment_metadata.values())
    
    def get_equipment_metadata(self, equipment_id: str) -> Optional[Dict[str, Any]]:
        """Get equipment metadata by ID.
        
        Parameters
        ----------
        equipment_id : str
            Equipment identifier
            
        Returns
        -------
        Dict[str, Any], optional
            Equipment metadata or None if not found
        """
        return self._equipment_metadata.get(equipment_id)
    
    def add_equipment(self, equipment_metadata: Dict[str, Any]) -> None:
        """Add equipment to database.
        
        Parameters
        ----------
        equipment_metadata : Dict[str, Any]
            Equipment metadata to add
        """
        equipment_id = equipment_metadata.get('id')
        if not equipment_id:
            raise ValueError("Equipment metadata must include 'id' field")
        
        self._equipment_metadata[equipment_id] = equipment_metadata
        self._equipment_configs[equipment_id] = equipment_metadata.get('config', {})
    
    def remove_equipment(self, equipment_id: str) -> bool:
        """Remove equipment from database.
        
        Parameters
        ----------
        equipment_id : str
            Equipment identifier
            
        Returns
        -------
        bool
            True if equipment was removed, False if not found
        """
        if equipment_id in self._equipment_metadata:
            del self._equipment_metadata[equipment_id]
            del self._equipment_configs[equipment_id]
            return True
        return False