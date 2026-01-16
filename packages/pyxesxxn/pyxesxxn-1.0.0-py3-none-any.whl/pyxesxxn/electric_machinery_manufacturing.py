"""
Electric Machinery Manufacturing Module for PyXESXXN

This module provides comprehensive functionality for electric machinery 
production manufacturing, including equipment monitoring, quality control,
production scheduling, and energy optimization.
"""

from __future__ import annotations

import logging
from typing import Optional, List, Dict, Any, Union, Callable
from datetime import datetime, timedelta
from enum import Enum
from dataclasses import dataclass, field
import json

_logger = logging.getLogger(__name__)


class MachineryType(Enum):
    """Electric machinery type enumeration."""
    EXCAVATOR = "excavator"
    CRANE = "crane"
    LOADER = "loader"
    FORKLIFT = "forklift"
    DRILLING_RIG = "drilling_rig"
    CONVEYOR = "conveyor"
    ROBOTIC_ARM = "robotic_arm"
    WELDING_MACHINE = "welding_machine"
    CNC_MACHINE = "cnc_machine"
    PRESS_MACHINE = "press_machine"


class ProductionStatus(Enum):
    """Production status enumeration."""
    IDLE = "idle"
    RUNNING = "running"
    MAINTENANCE = "maintenance"
    ERROR = "error"
    COMPLETED = "completed"


class QualityLevel(Enum):
    """Quality level enumeration."""
    EXCELLENT = "excellent"
    GOOD = "good"
    ACCEPTABLE = "acceptable"
    POOR = "poor"
    DEFECTIVE = "defective"


@dataclass
class EnergyConsumptionData:
    """Energy consumption data for machinery."""
    timestamp: datetime
    voltage: float
    current: float
    power: float
    energy: float
    power_factor: float
    frequency: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "timestamp": self.timestamp.isoformat(),
            "voltage": self.voltage,
            "current": self.current,
            "power": self.power,
            "energy": self.energy,
            "power_factor": self.power_factor,
            "frequency": self.frequency
        }


@dataclass
class MachineryParameters:
    """Machinery operational parameters."""
    machinery_type: MachineryType
    model: str
    rated_power: float
    rated_voltage: float
    rated_current: float
    efficiency: float
    operating_temperature_range: tuple
    max_load_capacity: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "machinery_type": self.machinery_type.value,
            "model": self.model,
            "rated_power": self.rated_power,
            "rated_voltage": self.rated_voltage,
            "rated_current": self.rated_current,
            "efficiency": self.efficiency,
            "operating_temperature_range": self.operating_temperature_range,
            "max_load_capacity": self.max_load_capacity
        }


@dataclass
class ProductionMetrics:
    """Production performance metrics."""
    total_units_produced: int = 0
    units_per_hour: float = 0.0
    defect_rate: float = 0.0
    uptime_percentage: float = 0.0
    energy_efficiency: float = 0.0
    cycle_time: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "total_units_produced": self.total_units_produced,
            "units_per_hour": self.units_per_hour,
            "defect_rate": self.defect_rate,
            "uptime_percentage": self.uptime_percentage,
            "energy_efficiency": self.energy_efficiency,
            "cycle_time": self.cycle_time
        }


@dataclass
class QualityInspectionResult:
    """Quality inspection result."""
    timestamp: datetime
    inspector_id: str
    quality_level: QualityLevel
    defects: List[str] = field(default_factory=list)
    measurements: Dict[str, float] = field(default_factory=dict)
    notes: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "timestamp": self.timestamp.isoformat(),
            "inspector_id": self.inspector_id,
            "quality_level": self.quality_level.value,
            "defects": self.defects,
            "measurements": self.measurements,
            "notes": self.notes
        }


class ElectricMachinery:
    """
    Base class for electric machinery in manufacturing.
    
    This class provides core functionality for monitoring and controlling
    electric machinery in production environments.
    """
    
    def __init__(
        self,
        machinery_id: str,
        name: str,
        parameters: MachineryParameters
    ):
        """
        Initialize electric machinery.
        
        Args:
            machinery_id: Unique identifier for the machinery
            name: Machinery name
            parameters: Machinery operational parameters
        """
        self.machinery_id = machinery_id
        self.name = name
        self.parameters = parameters
        self.status = ProductionStatus.IDLE
        self.energy_history: List[EnergyConsumptionData] = []
        self.current_energy_data: Optional[EnergyConsumptionData] = None
        self.production_metrics = ProductionMetrics()
        self.inspection_history: List[QualityInspectionResult] = []
        self.last_maintenance: Optional[datetime] = None
        self.next_maintenance: Optional[datetime] = None
        self.operating_hours: float = 0.0
        
    def start_production(self) -> bool:
        """
        Start production on the machinery.
        
        Returns:
            True if started successfully, False otherwise
        """
        if self.status == ProductionStatus.RUNNING:
            _logger.warning(f"Machinery {self.machinery_id} is already running")
            return False
        
        if self.status == ProductionStatus.MAINTENANCE:
            _logger.warning(f"Machinery {self.machinery_id} is under maintenance")
            return False
        
        self.status = ProductionStatus.RUNNING
        _logger.info(f"Started production on machinery {self.machinery_id}")
        return True
    
    def stop_production(self) -> bool:
        """
        Stop production on the machinery.
        
        Returns:
            True if stopped successfully, False otherwise
        """
        if self.status != ProductionStatus.RUNNING:
            _logger.warning(f"Machinery {self.machinery_id} is not running")
            return False
        
        self.status = ProductionStatus.IDLE
        _logger.info(f"Stopped production on machinery {self.machinery_id}")
        return True
    
    def update_energy_data(self, energy_data: EnergyConsumptionData) -> None:
        """
        Update current energy consumption data.
        
        Args:
            energy_data: New energy consumption data
        """
        self.current_energy_data = energy_data
        self.energy_history.append(energy_data)
        
        if len(self.energy_history) > 1000:
            self.energy_history = self.energy_history[-1000:]
        
        _logger.debug(f"Updated energy data for machinery {self.machinery_id}")
    
    def calculate_energy_efficiency(self) -> float:
        """
        Calculate current energy efficiency.
        
        Returns:
            Energy efficiency ratio (0.0 to 1.0)
        """
        if not self.energy_history:
            return 0.0
        
        recent_data = self.energy_history[-10:]
        avg_power = sum(d.power for d in recent_data) / len(recent_data)
        
        if avg_power == 0:
            return 0.0
        
        efficiency = self.parameters.rated_power / avg_power
        return min(max(efficiency, 0.0), 1.0)
    
    def check_operating_conditions(self) -> Dict[str, Any]:
        """
        Check if operating conditions are within acceptable range.
        
        Returns:
            Dictionary with condition check results
        """
        if not self.current_energy_data:
            return {"status": "no_data", "message": "No energy data available"}
        
        conditions = {
            "voltage_ok": (
                self.parameters.rated_voltage * 0.9 <= 
                self.current_energy_data.voltage <= 
                self.parameters.rated_voltage * 1.1
            ),
            "current_ok": (
                self.current_energy_data.current <= 
                self.parameters.rated_current * 1.2
            ),
            "power_ok": (
                self.current_energy_data.power <= 
                self.parameters.rated_power * 1.1
            ),
            "power_factor_ok": (
                self.current_energy_data.power_factor >= 0.85
            )
        }
        
        all_ok = all(conditions.values())
        conditions["status"] = "ok" if all_ok else "warning"
        
        return conditions
    
    def schedule_maintenance(self, maintenance_date: datetime) -> None:
        """
        Schedule maintenance for the machinery.
        
        Args:
            maintenance_date: Date for scheduled maintenance
        """
        self.next_maintenance = maintenance_date
        _logger.info(f"Scheduled maintenance for machinery {self.machinery_id} on {maintenance_date}")
    
    def perform_maintenance(self) -> bool:
        """
        Perform maintenance on the machinery.
        
        Returns:
            True if maintenance completed successfully
        """
        self.status = ProductionStatus.MAINTENANCE
        self.last_maintenance = datetime.now()
        self.next_maintenance = None
        _logger.info(f"Performed maintenance on machinery {self.machinery_id}")
        return True
    
    def add_inspection_result(self, result: QualityInspectionResult) -> None:
        """
        Add quality inspection result.
        
        Args:
            result: Inspection result
        """
        self.inspection_history.append(result)
        
        if len(self.inspection_history) > 100:
            self.inspection_history = self.inspection_history[-100:]
        
        _logger.debug(f"Added inspection result for machinery {self.machinery_id}")
    
    def calculate_defect_rate(self) -> float:
        """
        Calculate defect rate based on inspection history.
        
        Returns:
            Defect rate as percentage (0.0 to 100.0)
        """
        if not self.inspection_history:
            return 0.0
        
        defective_count = sum(
            1 for r in self.inspection_history 
            if r.quality_level in [QualityLevel.POOR, QualityLevel.DEFECTIVE]
        )
        
        return (defective_count / len(self.inspection_history)) * 100
    
    def get_status_summary(self) -> Dict[str, Any]:
        """
        Get comprehensive status summary.
        
        Returns:
            Status summary dictionary
        """
        return {
            "machinery_id": self.machinery_id,
            "name": self.name,
            "status": self.status.value,
            "parameters": self.parameters.to_dict(),
            "current_energy": self.current_energy_data.to_dict() if self.current_energy_data else None,
            "energy_efficiency": self.calculate_energy_efficiency(),
            "operating_conditions": self.check_operating_conditions(),
            "defect_rate": self.calculate_defect_rate(),
            "last_maintenance": self.last_maintenance.isoformat() if self.last_maintenance else None,
            "next_maintenance": self.next_maintenance.isoformat() if self.next_maintenance else None,
            "operating_hours": self.operating_hours
        }


class ProductionLine:
    """
    Production line manager for coordinating multiple machinery.
    
    This class manages a production line consisting of multiple electric
    machinery units, coordinating their operation and monitoring overall
    production performance.
    """
    
    def __init__(self, line_id: str, name: str):
        """
        Initialize production line.
        
        Args:
            line_id: Unique identifier for the production line
            name: Production line name
        """
        self.line_id = line_id
        self.name = name
        self.machinery: Dict[str, ElectricMachinery] = {}
        self.production_schedule: List[Dict[str, Any]] = []
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self.total_energy_consumed: float = 0.0
        
    def add_machinery(self, machinery: ElectricMachinery) -> None:
        """
        Add machinery to the production line.
        
        Args:
            machinery: Electric machinery instance
        """
        self.machinery[machinery.machinery_id] = machinery
        _logger.info(f"Added machinery {machinery.machinery_id} to production line {self.line_id}")
    
    def remove_machinery(self, machinery_id: str) -> bool:
        """
        Remove machinery from the production line.
        
        Args:
            machinery_id: ID of machinery to remove
            
        Returns:
            True if removed successfully, False otherwise
        """
        if machinery_id in self.machinery:
            del self.machinery[machinery_id]
            _logger.info(f"Removed machinery {machinery_id} from production line {self.line_id}")
            return True
        return False
    
    def start_production_line(self) -> bool:
        """
        Start all machinery in the production line.
        
        Returns:
            True if all started successfully, False otherwise
        """
        self.start_time = datetime.now()
        success = True
        
        for machinery in self.machinery.values():
            if not machinery.start_production():
                success = False
                _logger.error(f"Failed to start machinery {machinery.machinery_id}")
        
        if success:
            _logger.info(f"Started production line {self.line_id}")
        else:
            _logger.warning(f"Partial failure starting production line {self.line_id}")
        
        return success
    
    def stop_production_line(self) -> bool:
        """
        Stop all machinery in the production line.
        
        Returns:
            True if all stopped successfully, False otherwise
        """
        self.end_time = datetime.now()
        success = True
        
        for machinery in self.machinery.values():
            if not machinery.stop_production():
                success = False
                _logger.error(f"Failed to stop machinery {machinery.machinery_id}")
        
        if success:
            _logger.info(f"Stopped production line {self.line_id}")
        else:
            _logger.warning(f"Partial failure stopping production line {self.line_id}")
        
        return success
    
    def calculate_total_energy_consumption(self) -> float:
        """
        Calculate total energy consumption for the production line.
        
        Returns:
            Total energy consumed in kWh
        """
        total = 0.0
        
        for machinery in self.machinery.values():
            if machinery.energy_history:
                total += sum(d.energy for d in machinery.energy_history)
        
        self.total_energy_consumed = total
        return total
    
    def calculate_production_efficiency(self) -> float:
        """
        Calculate overall production efficiency.
        
        Returns:
            Efficiency ratio (0.0 to 1.0)
        """
        if not self.machinery:
            return 0.0
        
        efficiencies = [m.calculate_energy_efficiency() for m in self.machinery.values()]
        return sum(efficiencies) / len(efficiencies) if efficiencies else 0.0
    
    def get_line_status(self) -> Dict[str, Any]:
        """
        Get comprehensive production line status.
        
        Returns:
            Production line status dictionary
        """
        machinery_statuses = {
            mid: m.get_status_summary() 
            for mid, m in self.machinery.items()
        }
        
        return {
            "line_id": self.line_id,
            "name": self.name,
            "machinery_count": len(self.machinery),
            "machinery_statuses": machinery_statuses,
            "total_energy_consumed": self.calculate_total_energy_consumption(),
            "production_efficiency": self.calculate_production_efficiency(),
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration_hours": (
                (self.end_time - self.start_time).total_seconds() / 3600
                if self.start_time and self.end_time else 0.0
            )
        }


class EnergyOptimizer:
    """
    Energy optimizer for electric machinery production.
    
    This class provides optimization algorithms for minimizing energy
    consumption while maintaining production quality and efficiency.
    """
    
    def __init__(self):
        """Initialize energy optimizer."""
        self.optimization_history: List[Dict[str, Any]] = []
        
    def optimize_production_schedule(
        self,
        production_line: ProductionLine,
        target_output: int,
        time_window: timedelta
    ) -> Dict[str, Any]:
        """
        Optimize production schedule for energy efficiency.
        
        Args:
            production_line: Production line to optimize
            target_output: Target production output
            time_window: Available time window
            
        Returns:
            Optimization result dictionary
        """
        optimization_result = {
            "timestamp": datetime.now().isoformat(),
            "line_id": production_line.line_id,
            "target_output": target_output,
            "time_window_hours": time_window.total_seconds() / 3600,
            "recommendations": []
        }
        
        for machinery in production_line.machinery.values():
            if machinery.current_energy_data:
                efficiency = machinery.calculate_energy_efficiency()
                
                if efficiency < 0.7:
                    optimization_result["recommendations"].append({
                        "machinery_id": machinery.machinery_id,
                        "type": "efficiency_improvement",
                        "current_efficiency": efficiency,
                        "suggestion": "Schedule maintenance or calibration"
                    })
                
                power_factor = machinery.current_energy_data.power_factor
                if power_factor < 0.85:
                    optimization_result["recommendations"].append({
                        "machinery_id": machinery.machinery_id,
                        "type": "power_factor_correction",
                        "current_power_factor": power_factor,
                        "suggestion": "Install power factor correction equipment"
                    })
        
        self.optimization_history.append(optimization_result)
        
        _logger.info(f"Completed optimization for production line {production_line.line_id}")
        return optimization_result
    
    def calculate_energy_savings_potential(
        self,
        production_line: ProductionLine
    ) -> Dict[str, Any]:
        """
        Calculate potential energy savings.
        
        Args:
            production_line: Production line to analyze
            
        Returns:
            Energy savings potential dictionary
        """
        current_consumption = production_line.calculate_total_energy_consumption()
        
        potential_savings = {
            "current_consumption_kwh": current_consumption,
            "potential_savings_kwh": 0.0,
            "potential_savings_percentage": 0.0,
            "savings_opportunities": []
        }
        
        for machinery in production_line.machinery.values():
            efficiency = machinery.calculate_energy_efficiency()
            
            if efficiency < 1.0:
                machinery_savings = current_consumption * (1.0 - efficiency) / len(production_line.machinery)
                potential_savings["potential_savings_kwh"] += machinery_savings
                
                potential_savings["savings_opportunities"].append({
                    "machinery_id": machinery.machinery_id,
                    "current_efficiency": efficiency,
                    "potential_savings_kwh": machinery_savings
                })
        
        if current_consumption > 0:
            potential_savings["potential_savings_percentage"] = (
                potential_savings["potential_savings_kwh"] / current_consumption * 100
            )
        
        return potential_savings


class QualityControlManager:
    """
    Quality control manager for production quality assurance.
    
    This class manages quality inspections, defect tracking, and
    quality improvement recommendations.
    """
    
    def __init__(self):
        """Initialize quality control manager."""
        self.inspection_standards: Dict[QualityLevel, Dict[str, Any]] = {
            QualityLevel.EXCELLENT: {"min_score": 95, "max_defects": 0},
            QualityLevel.GOOD: {"min_score": 85, "max_defects": 1},
            QualityLevel.ACCEPTABLE: {"min_score": 70, "max_defects": 3},
            QualityLevel.POOR: {"min_score": 50, "max_defects": 5},
            QualityLevel.DEFECTIVE: {"min_score": 0, "max_defects": 999}
        }
        
    def evaluate_quality(
        self,
        measurements: Dict[str, float],
        specifications: Dict[str, tuple]
    ) -> QualityLevel:
        """
        Evaluate product quality based on measurements.
        
        Args:
            measurements: Product measurements
            specifications: Specification limits (min, max) for each measurement
            
        Returns:
            Quality level
        """
        deviations = []
        
        for key, value in measurements.items():
            if key in specifications:
                min_val, max_val = specifications[key]
                if value < min_val or value > max_val:
                    deviations.append(key)
        
        if not deviations:
            return QualityLevel.EXCELLENT
        elif len(deviations) == 1:
            return QualityLevel.GOOD
        elif len(deviations) <= 3:
            return QualityLevel.ACCEPTABLE
        elif len(deviations) <= 5:
            return QualityLevel.POOR
        else:
            return QualityLevel.DEFECTIVE
    
    def generate_quality_report(
        self,
        production_line: ProductionLine
    ) -> Dict[str, Any]:
        """
        Generate comprehensive quality report.
        
        Args:
            production_line: Production line to analyze
            
        Returns:
            Quality report dictionary
        """
        report = {
            "timestamp": datetime.now().isoformat(),
            "line_id": production_line.line_id,
            "machinery_quality": {}
        }
        
        for machinery_id, machinery in production_line.machinery.items():
            defect_rate = machinery.calculate_defect_rate()
            
            if defect_rate < 1.0:
                quality_status = "excellent"
            elif defect_rate < 3.0:
                quality_status = "good"
            elif defect_rate < 5.0:
                quality_status = "acceptable"
            elif defect_rate < 10.0:
                quality_status = "poor"
            else:
                quality_status = "critical"
            
            report["machinery_quality"][machinery_id] = {
                "defect_rate": defect_rate,
                "quality_status": quality_status,
                "total_inspections": len(machinery.inspection_history)
            }
        
        return report


def create_excavator(
    machinery_id: str,
    name: str,
    model: str,
    rated_power: float = 200.0
) -> ElectricMachinery:
    """
    Create an electric excavator instance.
    
    Args:
        machinery_id: Unique identifier
        name: Excavator name
        model: Excavator model
        rated_power: Rated power in kW
        
    Returns:
        ElectricMachinery instance
    """
    parameters = MachineryParameters(
        machinery_type=MachineryType.EXCAVATOR,
        model=model,
        rated_power=rated_power,
        rated_voltage=380.0,
        rated_current=rated_power * 1000 / (380.0 * 1.732 * 0.9),
        efficiency=0.92,
        operating_temperature_range=(-20, 50),
        max_load_capacity=5000.0
    )
    
    return ElectricMachinery(machinery_id, name, parameters)


def create_crane(
    machinery_id: str,
    name: str,
    model: str,
    rated_power: float = 150.0
) -> ElectricMachinery:
    """
    Create an electric crane instance.
    
    Args:
        machinery_id: Unique identifier
        name: Crane name
        model: Crane model
        rated_power: Rated power in kW
        
    Returns:
        ElectricMachinery instance
    """
    parameters = MachineryParameters(
        machinery_type=MachineryType.CRANE,
        model=model,
        rated_power=rated_power,
        rated_voltage=380.0,
        rated_current=rated_power * 1000 / (380.0 * 1.732 * 0.9),
        efficiency=0.90,
        operating_temperature_range=(-20, 45),
        max_load_capacity=10000.0
    )
    
    return ElectricMachinery(machinery_id, name, parameters)


def create_loader(
    machinery_id: str,
    name: str,
    model: str,
    rated_power: float = 180.0
) -> ElectricMachinery:
    """
    Create an electric loader instance.
    
    Args:
        machinery_id: Unique identifier
        name: Loader name
        model: Loader model
        rated_power: Rated power in kW
        
    Returns:
        ElectricMachinery instance
    """
    parameters = MachineryParameters(
        machinery_type=MachineryType.LOADER,
        model=model,
        rated_power=rated_power,
        rated_voltage=380.0,
        rated_current=rated_power * 1000 / (380.0 * 1.732 * 0.9),
        efficiency=0.91,
        operating_temperature_range=(-20, 50),
        max_load_capacity=3000.0
    )
    
    return ElectricMachinery(machinery_id, name, parameters)
