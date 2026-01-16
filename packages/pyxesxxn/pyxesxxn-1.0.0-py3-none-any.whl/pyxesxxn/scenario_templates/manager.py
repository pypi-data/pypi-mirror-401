"""
Scenario Template Manager for managing multiple scenario templates.
"""

import os
import json
import pandas as pd
from typing import Dict, List, Any, Optional, Type, Union
from pathlib import Path
import importlib.util

from .base import BaseScenarioTemplate
from .urban import UrbanScenarioTemplate
from .rural import RuralScenarioTemplate
from .port import PortScenarioTemplate
from pypsa import Network


class ScenarioTemplateManager:
    """Manager for creating, storing, and accessing scenario templates."""
    
    def __init__(self, templates_dir: Optional[str] = None):
        """Initialize the scenario template manager.
        
        Parameters
        ----------
        templates_dir : str, optional
            Directory to store custom scenario templates
        """
        self.templates_dir = templates_dir
        self._built_in_templates = {}
        self._custom_templates = {}
        self._register_built_in_templates()
        
        if templates_dir and not os.path.exists(templates_dir):
            os.makedirs(templates_dir)
    
    def _register_built_in_templates(self) -> None:
        """Register built-in scenario templates."""
        self._built_in_templates = {
            "urban": UrbanScenarioTemplate,
            "rural": RuralScenarioTemplate,
            "port": PortScenarioTemplate
        }
    
    def list_available_templates(self) -> Dict[str, Dict[str, Any]]:
        """List all available scenario templates.
        
        Returns
        -------
        Dict[str, Dict[str, Any]]
            Dictionary with template names as keys and template info as values
        """
        all_templates = {}
        
        # Add built-in templates
        for name, template_class in self._built_in_templates.items():
            try:
                template_instance = template_class()
                all_templates[name] = {
                    "name": name,
                    "description": template_instance.description,
                    "type": "built-in",
                    "energy_carriers": template_instance.get_energy_carriers(),
                    "equipment_types": list(template_instance.get_equipment_types().keys()),
                    "topology_rules": template_instance.get_topology_rules()
                }
            except Exception as e:
                print(f"Warning: Could not load built-in template '{name}': {e}")
        
        # Add custom templates
        for name, template in self._custom_templates.items():
            all_templates[name] = {
                "name": name,
                "description": template.description if hasattr(template, 'description') else "Custom template",
                "type": "custom",
                "energy_carriers": template.get_energy_carriers() if hasattr(template, 'get_energy_carriers') else [],
                "equipment_types": list(template.get_equipment_types().keys()) if hasattr(template, 'get_equipment_types') else [],
                "topology_rules": template.get_topology_rules() if hasattr(template, 'get_topology_rules') else {}
            }
        
        return all_templates
    
    def create_template(self, template_type: str, name: Optional[str] = None, **kwargs) -> BaseScenarioTemplate:
        """Create a scenario template instance.
        
        Parameters
        ----------
        template_type : str
            Type of template to create ('urban', 'rural', 'port' or custom template name)
        name : str, optional
            Custom name for the template instance
        **kwargs
            Additional arguments passed to template creation
            
        Returns
        -------
        BaseScenarioTemplate
            Created scenario template instance
            
        Raises
        ------
        ValueError
            If template type is not supported
        """
        if template_type in self._built_in_templates:
            template_class = self._built_in_templates[template_type]
            template_instance = template_class()
        elif template_type in self._custom_templates:
            template_instance = self._custom_templates[template_type]()
        else:
            raise ValueError(
                f"Template type '{template_type}' not found. "
                f"Available types: {list(self._built_in_templates.keys()) + list(self._custom_templates.keys())}"
            )
        
        if name:
            template_instance.name = name
            
        return template_instance
    
    def create_network(self, template_type: str, name: Optional[str] = None, 
                      network_name: str = "scenario_network", **kwargs) -> Network:
        """Create a network using a specific template.
        
        Parameters
        ----------
        template_type : str
            Type of template to use
        name : str, optional
            Custom name for the template instance
        network_name : str
            Name for the created network
        **kwargs
            Arguments passed to template network creation
            
        Returns
        -------
        Network
            Created network with the specified template configuration
            
        Raises
        ------
        ValueError
            If template type is not supported
        """
        template = self.create_template(template_type, name, **kwargs)
        network = template.create_network(**kwargs)
        network.name = network_name
        
        return network
    
    def register_custom_template(self, name: str, template_class: Type[BaseScenarioTemplate]) -> None:
        """Register a custom scenario template.
        
        Parameters
        ----------
        name : str
            Name for the custom template
        template_class : Type[BaseScenarioTemplate]
            Template class to register
        """
        if not issubclass(template_class, BaseScenarioTemplate):
            raise ValueError("Template class must inherit from BaseScenarioTemplate")
        
        self._custom_templates[name] = template_class
        print(f"Custom template '{name}' registered successfully")
    
    def unregister_custom_template(self, name: str) -> bool:
        """Unregister a custom template.
        
        Parameters
        ----------
        name : str
            Name of the custom template to unregister
            
        Returns
        -------
        bool
            True if template was unregistered successfully, False if not found
        """
        if name in self._custom_templates:
            del self._custom_templates[name]
            return True
        return False
    
    def save_template(self, template: BaseScenarioTemplate, filename: Optional[str] = None) -> str:
        """Save a template configuration to file.
        
        Parameters
        ----------
        template : BaseScenarioTemplate
            Template to save
        filename : str, optional
            Filename for saving (defaults to template name)
            
        Returns
        -------
        str
            Path where template was saved
            
        Raises
        ------
        ValueError
            If templates_dir is not configured
        """
        if not self.templates_dir:
            raise ValueError("Templates directory not configured")
        
        if not filename:
            filename = f"{template.name.lower().replace(' ', '_')}_template.json"
        
        filepath = os.path.join(self.templates_dir, filename)
        
        template_config = {
            "name": template.name,
            "description": template.description,
            "config": template.config if hasattr(template, 'config') else {}
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(template_config, f, indent=2, ensure_ascii=False)
        
        print(f"Template saved to: {filepath}")
        return filepath
    
    def load_template(self, filename: str) -> Dict[str, Any]:
        """Load a template configuration from file.
        
        Parameters
        ----------
        filename : str
            Filename to load from
            
        Returns
        -------
        Dict[str, Any]
            Loaded template configuration
            
        Raises
        ------
        ValueError
            If templates_dir is not configured or file not found
        """
        if not self.templates_dir:
            raise ValueError("Templates directory not configured")
        
        filepath = os.path.join(self.templates_dir, filename)
        
        if not os.path.exists(filepath):
            raise ValueError(f"Template file not found: {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            template_config = json.load(f)
        
        return template_config
    
    def export_template_info(self, template_type: str, output_file: str) -> None:
        """Export detailed template information to file.
        
        Parameters
        ----------
        template_type : str
            Type of template to export
        output_file : str
            Output file path
        """
        if template_type not in self._built_in_templates and template_type not in self._custom_templates:
            raise ValueError(f"Template type '{template_type}' not found")
        
        template_class = self._built_in_templates.get(template_type, self._custom_templates[template_type])
        template_instance = template_class()
        
        info = {
            "template_name": template_type,
            "description": template_instance.description,
            "energy_carriers": template_instance.get_energy_carriers(),
            "equipment_types": template_instance.get_equipment_types(),
            "topology_rules": template_instance.get_topology_rules()
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(info, f, indent=2, ensure_ascii=False)
        
        print(f"Template information exported to: {output_file}")
    
    def compare_templates(self, template_types: List[str]) -> pd.DataFrame:
        """Compare multiple templates and return comparison table.
        
        Parameters
        ----------
        template_types : List[str]
            List of template types to compare
            
        Returns
        -------
        pd.DataFrame
            Comparison table with template characteristics
        """
        comparison_data = []
        
        for template_type in template_types:
            if template_type not in self._built_in_templates and template_type not in self._custom_templates:
                print(f"Warning: Template '{template_type}' not found, skipping...")
                continue
            
            try:
                template_class = self._built_in_templates.get(template_type, self._custom_templates[template_type])
                template_instance = template_class()
                
                row = {
                    "Template": template_type,
                    "Description": template_instance.description,
                    "Energy_Carriers": len(template_instance.get_energy_carriers()),
                    "Equipment_Types": len(template_instance.get_equipment_types()),
                    "Density": template_instance.get_topology_rules().get("density", "unknown"),
                    "Renewable_Integration": template_instance.get_topology_rules().get("renewable_integration", "unknown")
                }
                comparison_data.append(row)
            except Exception as e:
                print(f"Warning: Could not load template '{template_type}': {e}")
        
        return pd.DataFrame(comparison_data)
    
    def get_template_capabilities(self, template_type: str) -> Dict[str, Any]:
        """Get detailed capabilities of a template.
        
        Parameters
        ----------
        template_type : str
            Type of template to analyze
            
        Returns
        -------
        Dict[str, Any]
            Template capabilities information
        """
        if template_type not in self._built_in_templates and template_type not in self._custom_templates:
            raise ValueError(f"Template type '{template_type}' not found")
        
        template_class = self._built_in_templates.get(template_type, self._custom_templates[template_type])
        template_instance = template_class()
        
        return {
            "template_name": template_type,
            "description": template_instance.description,
            "energy_carriers": template_instance.get_energy_carriers(),
            "equipment_types": template_instance.get_equipment_types(),
            "topology_rules": template_instance.get_topology_rules(),
            "components_available": {
                "buses": True,
                "generators": True,
                "loads": True,
                "storage": True,
                "links": True,
                "transformers": True
            },
            "special_features": self._get_template_special_features(template_type, template_instance)
        }
    
    def _get_template_special_features(self, template_type: str, template_instance) -> List[str]:
        """Get special features for different template types."""
        special_features = []
        
        if template_type == "urban":
            special_features = [
                "smart_grid_integration",
                "ev_charging_infrastructure",
                "district_heating",
                "load_forecasting",
                "voltage_regulation"
            ]
        elif template_type == "rural":
            special_features = [
                "micro_grid_operations",
                "biomass_utilization",
                "water_pumping_systems",
                "agricultural_loads",
                "islanded_operation"
            ]
        elif template_type == "port":
            special_features = [
                "ship_to_shore_power",
                "container_terminal_operations",
                "hydrogen_production",
                "offshore_wind_connection",
                "port_logistics_optimization"
            ]
        else:
            # For custom templates, try to get from topology rules
            special_features = template_instance.get_topology_rules().get("special_features", [])
        
        return special_features
    
    def get_available_scenarios(self) -> List[str]:
        """Get list of all available scenario names."""
        scenarios = []
        
        # Built-in scenarios
        scenarios.extend(list(self._built_in_templates.keys()))
        
        # Custom scenarios
        scenarios.extend(list(self._custom_templates.keys()))
        
        return sorted(list(set(scenarios)))
    
    def create_scenario_bundle(self, scenario_configs: List[Dict[str, Any]], 
                             output_dir: str, bundle_name: str) -> Dict[str, str]:
        """Create a bundle of multiple scenarios.
        
        Parameters
        ----------
        scenario_configs : List[Dict[str, Any]]
            List of scenario configurations with 'type' and parameters
        output_dir : str
            Output directory for the bundle
        bundle_name : str
            Name for the scenario bundle
            
        Returns
        -------
        Dict[str, str]
            Dictionary mapping scenario names to network files
        """
        bundle_dir = os.path.join(output_dir, f"{bundle_name}_bundle")
        os.makedirs(bundle_dir, exist_ok=True)
        
        scenario_files = {}
        
        for config in scenario_configs:
            template_type = config.get('type')
            scenario_name = config.get('name', template_type)
            params = config.get('params', {})
            
            try:
                network = self.create_network(template_type, **params)
                network_file = os.path.join(bundle_dir, f"{scenario_name}.nc")
                network.export_to_netcdf(network_file)
                scenario_files[scenario_name] = network_file
                
                print(f"Scenario '{scenario_name}' created and saved to {network_file}")
                
            except Exception as e:
                print(f"Error creating scenario '{scenario_name}': {e}")
        
        # Save bundle metadata
        bundle_metadata = {
            "bundle_name": bundle_name,
            "scenarios": list(scenario_files.keys()),
            "scenario_files": scenario_files,
            "created_at": pd.Timestamp.now().isoformat()
        }
        
        metadata_file = os.path.join(bundle_dir, "bundle_metadata.json")
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(bundle_metadata, f, indent=2, ensure_ascii=False)
        
        print(f"Scenario bundle '{bundle_name}' created successfully")
        print(f"Metadata saved to: {metadata_file}")
        
        return scenario_files