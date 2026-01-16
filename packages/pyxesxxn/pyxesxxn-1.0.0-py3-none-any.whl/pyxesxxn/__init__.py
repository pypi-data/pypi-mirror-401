"""PyXESXXN - Python for eXtended Energy System Analysis.

A fully independent multi-carrier energy system modeling and optimization library.
PyXESXXN provides comprehensive tools for analyzing and optimizing complex energy systems
with multiple energy carriers (electricity, heat, hydrogen, natural gas, etc.).

Key Features:
- Multi-carrier energy system modeling
- Advanced optimization algorithms  
- Scenario-based equipment libraries
- Renewable energy integration
- Carbon neutrality pathway analysis
- Fault location and self-healing capabilities
- Fully independent architecture (no PyPSA dependency)

Quick Start:
    >>> import pyxesxxn as px
    >>> network = px.Network()
    >>> network.add_bus("bus1", "electricity")
    >>> network.add_generator("gen1", "bus1", 100)

This is a free closed-source library. All rights reserved.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

__author__ = "PyXESXXN Development Team"
__copyright__ = "Copyright 2025 PyXESXXN Development Team. All Rights Reserved."

# Version information - dynamically loaded from version.py
from .version import (
    __version__, 
    __version_base__, 
    __version_major_minor__,
    __version_info__,
    get_version_info,
    is_compatible_with,
    get_version_summary,
    parse_version,
    is_compatible,
    VersionInfo
)

# =============================================================================
# Core Network Components
# =============================================================================

from .network import (
    PyXESXXNNetwork,
    Network,
    EnergySystem,
    Component,
    Bus,
    Generator,
    Load,
    Line,
    StorageUnit,
    ComponentType,
    EnergyCarrier,
    ComponentConfig
)

# =============================================================================
# Network Operations and Management
# =============================================================================

from .networks import (
    NetworkOperation,
    Scenario,
    NetworkCollection,
    AdvancedNetwork,
    create_network,
    compare_networks,
    convert_network
)

# =============================================================================
# Multi-Carrier Optimization
# =============================================================================

from .multi_carrier import (
    EnergyHubModel,
    HubConfiguration,
    MultiCarrierConverter,
    EnergyFlow,
    OptimizationModel,
    EnergySystemEnvironment,
    TaskGenerator,
    MultiAgentTaskScheduler,
    ParallelHeuristics,
    AdaptiveTreeGP,
    MachineAgent
)

# =============================================================================
# Equipment Libraries
# =============================================================================

from .equipment_library.base import (
    EquipmentCategory,
    EquipmentType,
    EquipmentConfig
)

from .equipment_library import (
    EquipmentLibrary,
    UrbanEquipmentLibrary,
    RuralEquipmentLibrary,
    PortEquipmentLibrary
)

from .equipment_library.scenario_equipment import (
    UniversalEquipmentLibrary,
    IslandEquipmentLibrary,
    IndustrialEquipmentLibrary,
    RailwayEquipmentLibrary
)

# =============================================================================
# Optimization Framework
# =============================================================================

from .optimization import (
    OptimizationType,
    SolverType,
    OptimizationConfig,
    OptimizationVariable,
    OptimizationConstraint,
    Optimizer,
    LinearOptimizer,
    NonlinearOptimizer,
    MultiObjectiveOptimizer,
    StochasticOptimizer
)

# =============================================================================
# Analysis Modules
# =============================================================================

from .analysis import (
    EnergyFlowAnalysis,
    ReliabilityAnalysis,
    EconomicAnalysis,
    EnvironmentalAnalysis
)

# =============================================================================
# Exception Hierarchy
# =============================================================================

from .exceptions import (
    PyXESXXNError,
    ConfigurationError,
    CalculationError,
    OptimizationError,
    ValidationError,
    ConvergenceError,
    InputError,
    FileError,
    DependencyError,
    NotImplementedFeatureError,
    WarningManager,
    raise_config_error,
    raise_calculation_error,
    raise_validation_error
)

# =============================================================================
# Utility Modules
# =============================================================================

from .utils import (
    DataHandler,
    TimeSeries,
    GeographicData,
    Visualization,
    ReportGenerator
)

# =============================================================================
# Geospatial Analysis
# =============================================================================

from .geospatial import (
    GeospatialProcessor,
    SpatialClusteringEngine,
    SpatialLoadResourceMatcher,
    RegionAnalyzer,
    GeospatialVisualizer
)

# =============================================================================
# Scenario Evaluation
# =============================================================================

from .scenario_evaluation import (
    SecurityEvaluator,
    EconomicEvaluator,
    EnvironmentalEvaluator,
    ComprehensiveEvaluator,
    ReliabilityEvaluator,
    RiskEvaluator,
    SocialEvaluator
)

# =============================================================================
# Scenario Templates - 暂时注释，避免依赖PyPSA
# =============================================================================

# from .scenario_templates import (
#     ScenarioTemplate,
#     UrbanScenario,
#     RuralScenario,
#     IndustrialScenario,
#     IslandScenario,
#     PortScenario,
#     RailwayScenario,
#     ScenarioManager
# )

# =============================================================================
# Statistics - 暂时注释，避免依赖PyPSA
# =============================================================================

# from .statistics import (
#     StatisticalAnalyzer,
#     ExpressionBuilder,
#     GroupingManager
# )

# =============================================================================
# Thermodynamics
# =============================================================================

from .thermodynamics import (
    ThermodynamicModel,
    IdealGasModel,
    RealGasModel,
    CompressionCalculator,
    GasProperties
)

# =============================================================================
# Innovation Modules
# =============================================================================

# Carbon Capture and Storage
from .carbon_capture_storage import (
    CCSMSESFlexibleCHP,
    CCSConfiguration,
    MSESConfiguration,
    CarbonCaptureTechnology,
    MoltenSaltType,
    ECEFModel
)

# Power Flow and OPF Methods
from .power_flow_enhanced import (
    PowerFlowMethod,
    ConvergenceStatus,
    PowerFlowResult,
    PowerFlowValidator,
    EnhancedPowerFlowSolver,
    NewtonRaphsonSolver,
    PowerFlowAnalysis,
    create_enhanced_power_flow_solver,
    run_power_flow_analysis
)

from .power_flow_holomorphic_opf import (
    HolomorphicOPFResult,
    HolomorphicOPFSolver,
    HolomorphicOPFAnalysis,
    create_holomorphic_opf_solver,
    run_holomorphic_opf
)

# Metro Power Flow Methods
from .power_flow_holomorphic_metro import (
    DCNodeType,
    ConverterControlMode,
    MetroPowerFlowResult,
    ConverterModel,
    HolomorphicMetroPowerFlowSolver,
    MetroPowerFlowAnalysis,
    create_holomorphic_metro_solver,
    run_holomorphic_metro_power_flow
)

# Energy System Power Flow and Exergy Analysis
from .power_flow_energy_system import (
    EnergyCarrierType,
    CouplingComponentType,
    ConvergenceCriteria,
    EnergyFlowResult,
    ExergyFlowResult,
    CouplingComponent,
    GasTurbine,
    CHP,
    ElectricBoiler,
    P2G,
    EnergySystemPowerFlowSolver,
    EnergySystemAnalysis,
    ExergyFlowAnalyzer,
    create_energy_system_solver,
    run_energy_system_power_flow,
    calculate_exergy_flow,
    parse_matlab_case_file,
    create_network_from_matlab_case,
    batch_process_matlab_cases
)

# Electro-Thermal-Hydrogen Integrated Energy System Power Flow and Exergy Analysis
from .power_flow_electro_thermal_hydrogen import (
    SubSystemType,
    ComponentType,
    ElectroThermalHydrogenPowerFlowResult,
    ElectroThermalHydrogenExergyFlowResult,
    ElectroThermalHydrogenPowerFlowSolver,
    ElectroThermalHydrogenPowerFlowAnalysis,
    create_electro_thermal_hydrogen_solver,
    run_electro_thermal_hydrogen_power_flow
)

# Uncertainty Modeling
from .uncertainty_modeling import (
    AdvancedUncertaintyModel,
    ConfidenceBandConfig,
    PDFConfidenceBand
)

# Renewable Equipment
from .renewable_equipment import (
    BiogasCHPPSystem,
    GeothermalHeatPumpSystem,
    PVSystem,
    BiogasCHPPConfiguration,
    GeothermalHeatPumpConfiguration,
    PVSystemConfiguration,
    BiogasSource,
    HeatPumpType,
    PVSystemType
)

# Fault Location and Self-Healing
from .topology_metering_fusion import (
    TopologyMeteringFusion,
    NeutralGroundingType,
    SwitchType,
    MeasurementType,
    DistributionNode,
    DistributionBranch
)

from .multimodal_preprocessing import (
    MultimodalPreprocessor,
    DataType,
    NormalizationMethod,
    MissingValueMethod,
    FaultType,
    DataQualityMetrics
)

from .simulation_interface import (
    SimulationInterface,
    SimulationConfig,
    SimulationResult,
    SimulationPlatform,
    SimulationMode,
    FaultScenario
)

# Visualization
from .visualization import (
    PowerGridVisualizer,
    VisualizationConfig,
    VisualizationResult,
    VisualizationType,
    ColorScheme
)

# =============================================================================
# Core Closed Source Functionality
# =============================================================================

from .core import (
    _CoreEngine,
    _ClosedSourceAlgorithm,
    _AdvancedOptimizer,
    _ProprietaryMethod,
    _EnergySystemSimulator,
    _AdvancedPowerFlowSolver,
    _MultiCarrierOptimizer,
    _ProprietaryEquipmentLibrary
)

# =============================================================================
# Examples and Tutorials
# =============================================================================

from .examples import (
    create_simple_network,
    create_urban_energy_system,
    create_renewable_integration_model,
    create_multi_carrier_hub
)

from .cmasrl import cmasrl_wrapper

# =============================================================================
# Reinforcement Learning Integration
# =============================================================================

from .rl_integration import (
    RLAgentFactory,
    get_available_algorithms,
    check_dependencies
)

# =============================================================================
# Reinforcement Learning Modules (MIP-DQN and PI-TD3)
# =============================================================================

try:
    from .OES_DRL_Mixed_Integer_Programming import (
        MIPDQNWrapper,
        MIPDQNConfig,
        EnergySystemEnvironment,
        BatteryParameters,
        DGParameters
    )
    _mip_drl_available = True
except ImportError:
    _mip_drl_available = False
    MIPDQNWrapper = None
    MIPDQNConfig = None
    EnergySystemEnvironment = None
    BatteryParameters = None
    DGParameters = None

try:
    from .EV2Gym_PI_TD3 import (
        EV2GymPIWrapper,
        PI_TD3Config,
        EVChargingEnvironment,
        EVChargingConfig
    )
    _ev2gym_pi_available = True
except ImportError:
    _ev2gym_pi_available = False
    EV2GymPIWrapper = None
    PI_TD3Config = None
    EVChargingEnvironment = None
    EVChargingConfig = None

# =============================================================================
# Stochastic Optimization Modules (SFLA and FICA)
# =============================================================================

try:
    from .stochastic_optimization import (
        StochasticOptimizer,
        ChanceConstraintConfig,
        OptimizationResult,
        SFLAWrapper,
        SFLAConfig,
        FICAWrapper,
        FICAConfig
    )
    _stochastic_opt_available = True
except ImportError:
    _stochastic_opt_available = False
    StochasticOptimizer = None
    ChanceConstraintConfig = None
    OptimizationResult = None
    SFLAWrapper = None
    SFLAConfig = None
    FICAWrapper = None
    FICAConfig = None

# =============================================================================
# BuildingGym Integration
# =============================================================================

try:
    from .building_gym_integration import (
        BuildingGymConfig,
        BuildingGymWrapper,
        create_building_gym_environment,
        get_available_algorithms as get_buildinggym_algorithms,
        check_buildinggym_dependencies
    )
    _buildinggym_available = True
except ImportError:
    _buildinggym_available = False
    BuildingGymConfig = None
    BuildingGymWrapper = None
    create_building_gym_environment = None
    get_buildinggym_algorithms = None
    check_buildinggym_dependencies = None

# =============================================================================
# Grid Feedback Optimizer Integration
# =============================================================================

try:
    from .grid_feedback_integration import (
        GridFeedbackConfig,
        GridFeedbackOptimizer,
        create_grid_feedback_optimizer,
        optimize_grid,
        check_grid_feedback_dependencies
    )
    _grid_feedback_available = True
except ImportError:
    _grid_feedback_available = False
    GridFeedbackConfig = None
    GridFeedbackOptimizer = None
    create_grid_feedback_optimizer = None
    optimize_grid = None
    check_grid_feedback_dependencies = None

# =============================================================================
# PDE Integration (FiPy-based PDE Solver)
# =============================================================================

try:
    from .pde_integration import (
        PDESolver,
        PDEConfig,
        PDEResult,
        PDEMesh,
        PDEBoundaryCondition,
        PDESolverType,
        solve_diffusion_1d,
        solve_diffusion_2d,
        solve_convection_diffusion,
        solve_heat_equation,
        create_mesh_1d,
        create_mesh_2d,
        create_mesh_3d,
        check_pde_dependencies,
        get_available_solvers
    )
    _pde_available = True
except ImportError:
    _pde_available = False
    PDESolver = None
    PDEConfig = None
    PDEResult = None
    PDEMesh = None
    PDEBoundaryCondition = None
    PDESolverType = None
    solve_diffusion_1d = None
    solve_diffusion_2d = None
    solve_convection_diffusion = None
    solve_heat_equation = None
    create_mesh_1d = None
    create_mesh_2d = None
    create_mesh_3d = None
    check_pde_dependencies = None
    get_available_solvers = None

# =============================================================================
# EverythingMoopy Integration (Multi-objective Optimization)
# =============================================================================

try:
    from .everythingmoopy_integration import (
        check_everythingmoopy_available,
        get_available_algorithms as get_everythingmoopy_algorithms,
        get_available_problems,
        create_optimizer as create_everythingmoopy_optimizer,
        optimize_standard_problem,
        EverythingMoopyConfig,
        EverythingMoopyOptimizer,
        EnergySystemOptimizationProblem,
        PerformanceIndicator,
        OptimizationVisualizer,
        _EVERYTHINGMOOPY_AVAILABLE
    )
    _everythingmoopy_available = True
except ImportError:
    _everythingmoopy_available = False
    check_everythingmoopy_available = None
    get_everythingmoopy_algorithms = None
    get_available_problems = None
    create_everythingmoopy_optimizer = None
    optimize_standard_problem = None
    EverythingMoopyConfig = None
    EverythingMoopyOptimizer = None
    EnergySystemOptimizationProblem = None
    PerformanceIndicator = None
    OptimizationVisualizer = None

# =============================================================================
# VistaDpy (PyVista) Integration - 3D Visualization
# =============================================================================

try:
    from .vista_integration import (
        PyVistaConfig,
        EnergyNetworkVisualizer,
        MeshGenerator,
        SpatialAnalyzer,
        check_pyvista_available,
        get_pyvista_version,
        get_vtk_version,
        create_visualizer,
        create_mesh_generator,
        create_spatial_analyzer,
        _PYVISTA_AVAILABLE
    )
    _vista_available = True
except ImportError:
    _vista_available = False
    PyVistaConfig = None
    EnergyNetworkVisualizer = None
    MeshGenerator = None
    SpatialAnalyzer = None
    check_pyvista_available = None
    get_pyvista_version = None
    get_vtk_version = None
    create_visualizer = None
    create_mesh_generator = None
    create_spatial_analyzer = None

try:
    from .vistaDpy_wrapper import (
        VistaConfig,
        VistaVisualizer,
        VistaMeshGenerator,
        quick_plot,
        quick_flow_plot,
        check_vista_available,
        get_vista_version,
        _PYVISTA_AVAILABLE as _VISTA_WRAPPER_AVAILABLE
    )
    _vista_wrapper_available = True
except ImportError:
    _vista_wrapper_available = False
    VistaConfig = None
    VistaVisualizer = None
    VistaMeshGenerator = None
    quick_plot = None
    quick_flow_plot = None
    check_vista_available = None
    get_vista_version = None
    _VISTA_WRAPPER_AVAILABLE = False

# =============================================================================
# RefinedModelSim Integration - Travel Demand Modeling
# =============================================================================

try:
    from .refinedmodelsim_wrapper import (
        RefinedModelSimConfig,
        TravelModel,
        EnergyTransportIntegration,
        ScenarioManager,
        quick_travel_model,
        quick_ev_demand,
        check_refinedmodelsim_available,
        get_refinedmodelsim_version,
        _REFINEDMODELSIM_AVAILABLE
    )
    _refinedmodelsim_available = True
except ImportError:
    _refinedmodelsim_available = False
    RefinedModelSimConfig = None
    TravelModel = None
    EnergyTransportIntegration = None
    ScenarioManager = None
    quick_travel_model = None
    quick_ev_demand = None
    check_refinedmodelsim_available = None
    get_refinedmodelsim_version = None
    _REFINEDMODELSIM_AVAILABLE = False

# =============================================================================
# MethodofDRO Integration - Distributionally Robust Optimization
# =============================================================================

try:
    from .methodofdro_integration import (
        DROConfig,
        DROWrapper,
        create_linear_dro,
        create_tree_dro,
        create_neural_dro,
        check_dro_dependencies,
        get_available_dro_models,
        _DRO_AVAILABLE,
        BaseLinearDRO,
        Chi2DRO,
        KLDRO,
        CVaRDRO,
        TVDRO,
        MarginalCVaRDRO,
        MMD_DRO,
        ConditionalCVaRDRO,
        HR_DRO_LR,
        WassersteinDRO,
        WassersteinDROsatisficing,
        SinkhornLinearDRO,
        MOTDRO,
        ORWDRO,
        BaseNNDRO,
        Chi2NNDRO,
        WNNDRO,
        HRNNDRO,
        KLDRO_LGBM,
        CVaRDRO_LGBM,
        Chi2DRO_LGBM,
        KLDRO_XGB,
        Chi2DRO_XGB,
        CVaRDRO_XGB,
        classification_basic,
        classification_DN21,
        classification_SNVD20,
        classification_LWLC,
        regression_basic,
        regression_DN20_1,
        regression_DN20_2,
        regression_DN20_3,
        regression_LWLC
    )
    _methodofdro_available = True
except ImportError:
    _methodofdro_available = False
    DROConfig = None
    DROWrapper = None
    create_linear_dro = None
    create_tree_dro = None
    create_neural_dro = None
    check_dro_dependencies = None
    get_available_dro_models = None
    _DRO_AVAILABLE = False
    BaseLinearDRO = None
    Chi2DRO = None
    KLDRO = None
    CVaRDRO = None
    TVDRO = None
    MarginalCVaRDRO = None
    MMD_DRO = None
    ConditionalCVaRDRO = None
    HR_DRO_LR = None
    WassersteinDRO = None
    WassersteinDROsatisficing = None
    SinkhornLinearDRO = None
    MOTDRO = None
    ORWDRO = None
    BaseNNDRO = None
    Chi2NNDRO = None
    WNNDRO = None
    HRNNDRO = None
    KLDRO_LGBM = None
    CVaRDRO_LGBM = None
    Chi2DRO_LGBM = None
    KLDRO_XGB = None
    Chi2DRO_XGB = None
    CVaRDRO_XGB = None
    classification_basic = None
    classification_DN21 = None
    classification_SNVD20 = None
    classification_LWLC = None
    regression_basic = None
    regression_DN20_1 = None
    regression_DN20_2 = None
    regression_DN20_3 = None
    regression_LWLC = None

# =============================================================================
# FaultModel Integration - Prognostics and Health Management
# =============================================================================

try:
    from .faultmodel_integration import (
        FaultModelConfig,
        FaultModelWrapper,
        PrognosticsModel,
        StateEstimator,
        Predictor,
        UncertainData,
        check_faultmodel_available,
        get_faultmodel_version,
        _FAULTMODEL_AVAILABLE,
        ElectricMachineryModel,
        ElectricMachineryConfig,
        ElectricMachineryState,
        ElectricMachineryFaultPredictor,
        ElectricMachineryStateEstimator,
        ElectricMachineryHealthAssessor,
        ElectricExcavatorModel,
        ElectricCraneModel,
        ElectricLoaderModel,
        ElectricForkliftModel
    )
    _faultmodel_available = True
except ImportError:
    _faultmodel_available = False
    FaultModelConfig = None
    FaultModelWrapper = None
    PrognosticsModel = None
    StateEstimator = None
    Predictor = None
    UncertainData = None
    check_faultmodel_available = None
    get_faultmodel_version = None
    _FAULTMODEL_AVAILABLE = False
    ElectricMachineryModel = None
    ElectricMachineryConfig = None
    ElectricMachineryState = None
    ElectricMachineryFaultPredictor = None
    ElectricMachineryStateEstimator = None
    ElectricMachineryHealthAssessor = None
    ElectricExcavatorModel = None
    ElectricCraneModel = None
    ElectricLoaderModel = None
    ElectricForkliftModel = None

# =============================================================================
# EnergyOPCUA Integration - OPC UA Communication for Energy Systems
# =============================================================================

try:
    from .energyopcua_integration import (
        EnergyOPCUAConfig,
        EnergyOPCUAClient,
        EnergyOPCUAServer,
        OPCUAConnectionStatus,
        OPCUAMessageType,
        check_opcua_available,
        get_opcua_version
    )
    _opcua_available = True
except ImportError:
    _opcua_available = False
    EnergyOPCUAConfig = None
    EnergyOPCUAClient = None
    EnergyOPCUAServer = None
    OPCUAConnectionStatus = None
    OPCUAMessageType = None
    check_opcua_available = None
    get_opcua_version = None

# =============================================================================
# Electric Machinery Manufacturing Module
# =============================================================================

try:
    from .electric_machinery_manufacturing import (
        MachineryType,
        ProductionStatus,
        QualityLevel,
        EnergyConsumptionData,
        MachineryParameters,
        ProductionMetrics,
        QualityInspectionResult,
        ElectricMachinery,
        ProductionLine,
        EnergyOptimizer,
        QualityControlManager,
        create_excavator,
        create_crane,
        create_loader
    )
    _electric_machinery_available = True
except ImportError:
    _electric_machinery_available = False
    MachineryType = None
    ProductionStatus = None
    QualityLevel = None
    EnergyConsumptionData = None
    MachineryParameters = None
    ProductionMetrics = None
    QualityInspectionResult = None
    ElectricMachinery = None
    ProductionLine = None
    EnergyOptimizer = None
    QualityControlManager = None
    create_excavator = None
    create_crane = None
    create_loader = None

# =============================================================================
# Public API Definition
# =============================================================================

__all__ = [
    # Core network components
    "PyXESXXNNetwork",
    "Network",
    "EnergySystem",
    "Component",
    "Bus",
    "Generator",
    "Load",
    "Line",
    "StorageUnit",
    "ComponentType",
    "EnergyCarrier",
    "ComponentConfig",
    
    # Network operations
    "NetworkOperation",
    "Scenario",
    "NetworkCollection",
    "AdvancedNetwork",
    "create_network",
    "compare_networks",
    "convert_network",
    
    # Multi-carrier optimization
    "EnergyHubModel",
    "HubConfiguration",
    "MultiCarrierConverter",
    "EnergyFlow",
    "OptimizationModel",
    "EnergySystemEnvironment",
    "TaskGenerator",
    "MultiAgentTaskScheduler",
    "ParallelHeuristics",
    "AdaptiveTreeGP",
    "MachineAgent",
    
    # Equipment library
    "EquipmentCategory",
    "EquipmentType",
    "EquipmentConfig",
    "EquipmentLibrary",
    "UniversalEquipmentLibrary",
    "UrbanEquipmentLibrary",
    "RuralEquipmentLibrary",
    "PortEquipmentLibrary",
    "IslandEquipmentLibrary",
    "IndustrialEquipmentLibrary",
    "RailwayEquipmentLibrary",
    
    # Optimization framework
    "Optimizer",
    "LinearOptimizer",
    "NonlinearOptimizer",
    "MultiObjectiveOptimizer",
    "StochasticOptimizer",
    "EnergyFlowAnalysis",
    "ReliabilityAnalysis",
    "EconomicAnalysis",
    "EnvironmentalAnalysis",
    
    # Exception hierarchy
    "PyXESXXNError",
    "ConfigurationError",
    "CalculationError",
    "OptimizationError",
    "ValidationError",
    "ConvergenceError",
    "InputError",
    "FileError",
    "DependencyError",
    "NotImplementedFeatureError",
    "WarningManager",
    "raise_config_error",
    "raise_calculation_error",
    "raise_validation_error",
    
    # Utilities
    "DataHandler",
    "TimeSeries",
    "GeographicData",
    "Visualization",
    "ReportGenerator",
    
    # Geospatial modules
    "GeospatialProcessor",
    "SpatialClusteringEngine",
    "SpatialLoadResourceMatcher",
    "RegionAnalyzer",
    "GeospatialVisualizer",
    
    # Scenario Evaluation
    "SecurityEvaluator",
    "EconomicEvaluator",
    "EnvironmentalEvaluator",
    "ComprehensiveEvaluator",
    "ReliabilityEvaluator",
    "RiskEvaluator",
    "SocialEvaluator",
    
    # Scenario Templates - 暂时注释，避免依赖PyPSA
    # "ScenarioTemplate",
    # "UrbanScenario",
    # "RuralScenario",
    # "IndustrialScenario",
    # "IslandScenario",
    # "PortScenario",
    # "RailwayScenario",
    # "ScenarioManager",
    
    # Statistics - 暂时注释，避免依赖PyPSA
    # "StatisticalAnalyzer",
    # "ExpressionBuilder",
    # "GroupingManager",
    
    # Thermodynamics
    "ThermodynamicModel",
    "IdealGasModel",
    "RealGasModel",
    "CompressionCalculator",
    "GasProperties",
    
    # Innovation modules
    "CCSMSESFlexibleCHP",
    "CCSConfiguration",
    "MSESConfiguration",
    "CarbonCaptureTechnology",
    "MoltenSaltType",
    "ECEFModel",
    "AdvancedUncertaintyModel",
    "ConfidenceBandConfig",
    "PDFConfidenceBand",
    "BiogasCHPPSystem",
    "GeothermalHeatPumpSystem",
    "PVSystem",
    "BiogasCHPPConfiguration",
    "GeothermalHeatPumpConfiguration",
    "PVSystemConfiguration",
    "BiogasSource",
    "HeatPumpType",
    "PVSystemType",
    
    # Fault location and self-healing
    "TopologyMeteringFusion",
    "NeutralGroundingType",
    "SwitchType",
    "MeasurementType",
    "DistributionNode",
    "DistributionBranch",
    "MultimodalPreprocessor",
    "DataType",
    "NormalizationMethod",
    "MissingValueMethod",
    "FaultType",
    "DataQualityMetrics",
    "SimulationInterface",
    "SimulationConfig",
    "SimulationResult",
    "SimulationPlatform",
    "SimulationMode",
    "FaultScenario",
    "PowerGridVisualizer",
    "VisualizationConfig",
    "VisualizationResult",
    "VisualizationType",
    "ColorScheme",
    
    # Power Flow and OPF Methods
    "PowerFlowMethod",
    "ConvergenceStatus",
    "PowerFlowResult",
    "PowerFlowValidator",
    "EnhancedPowerFlowSolver",
    "NewtonRaphsonSolver",
    "PowerFlowAnalysis",
    "create_enhanced_power_flow_solver",
    "run_power_flow_analysis",
    "HolomorphicOPFResult",
    "HolomorphicOPFSolver",
    "HolomorphicOPFAnalysis",
    "create_holomorphic_opf_solver",
    "run_holomorphic_opf",
    
    # Metro Power Flow Methods
    "DCNodeType",
    "ConverterControlMode",
    "MetroPowerFlowResult",
    "ConverterModel",
    "HolomorphicMetroPowerFlowSolver",
    "MetroPowerFlowAnalysis",
    "create_holomorphic_metro_solver",
    "run_holomorphic_metro_power_flow",
    
    # Energy System Power Flow and Exergy Analysis
    "EnergyCarrierType",
    "CouplingComponentType",
    "ConvergenceCriteria",
    "EnergyFlowResult",
    "ExergyFlowResult",
    "CouplingComponent",
    "GasTurbine",
    "CHP",
    "ElectricBoiler",
    "P2G",
    "EnergySystemPowerFlowSolver",
    "EnergySystemAnalysis",
    "ExergyFlowAnalyzer",
    "create_energy_system_solver",
    "run_energy_system_power_flow",
    "calculate_exergy_flow",
    
    # Electro-Thermal-Hydrogen Integrated Energy System Power Flow and Exergy Analysis
    "SubSystemType",
    "ComponentType",
    "ElectroThermalHydrogenPowerFlowResult",
    "ElectroThermalHydrogenExergyFlowResult",
    "ElectroThermalHydrogenPowerFlowSolver",
    "ElectroThermalHydrogenPowerFlowAnalysis",
    "create_electro_thermal_hydrogen_solver",
    "run_electro_thermal_hydrogen_power_flow",
    
    # Examples
    "create_simple_network",
    "create_urban_energy_system",
    "create_renewable_integration_model",
    "create_multi_carrier_hub",
    
    # Core Closed Source Functionality
    "_CoreEngine",
    "_ClosedSourceAlgorithm",
    "_AdvancedOptimizer",
    "_ProprietaryMethod",
    "_EnergySystemSimulator",
    "_AdvancedPowerFlowSolver",
    "_MultiCarrierOptimizer",
    "_ProprietaryEquipmentLibrary",
    
    # Multi-agent Safe Reinforcement Learning
    "cmasrl_wrapper",
    
    # Reinforcement Learning Integration
    "RLAgentFactory",
    "get_available_algorithms",
    "check_dependencies",
    
    # Reinforcement Learning (MIP-DQN and PI-TD3)
    "MIPDQNWrapper",
    "MIPDQNConfig",
    "EnergySystemEnvironment",
    "BatteryParameters",
    "DGParameters",
    "EV2GymPIWrapper",
    "PI_TD3Config",
    "EVChargingEnvironment",
    "EVChargingConfig",
    
    # Stochastic Optimization (SFLA and FICA)
    "StochasticOptimizer",
    "ChanceConstraintConfig",
    "OptimizationResult",
    "SFLAWrapper",
    "SFLAConfig",
    "FICAWrapper",
    "FICAConfig",
    
    # BuildingGym Integration
    "BuildingGymConfig",
    "BuildingGymWrapper",
    "create_building_gym_environment",
    "get_buildinggym_algorithms",
    "check_buildinggym_dependencies",
    
    # Grid Feedback Optimizer Integration
    "GridFeedbackConfig",
    "GridFeedbackOptimizer",
    "create_grid_feedback_optimizer",
    "optimize_grid",
    "check_grid_feedback_dependencies",
    
    # PDE Integration (FiPy-based PDE Solver)
    "PDESolver",
    "PDEConfig",
    "PDEResult",
    "PDEMesh",
    "PDEBoundaryCondition",
    "PDESolverType",
    "solve_diffusion_1d",
    "solve_diffusion_2d",
    "solve_convection_diffusion",
    "solve_heat_equation",
    "create_mesh_1d",
    "create_mesh_2d",
    "create_mesh_3d",
    "check_pde_dependencies",
    "get_available_solvers",
    
    # EverythingMoopy Integration
    "check_everythingmoopy_available",
    "get_everythingmoopy_algorithms",
    "get_available_problems",
    "create_everythingmoopy_optimizer",
    "optimize_standard_problem",
    "EverythingMoopyConfig",
    "EverythingMoopyOptimizer",
    "EnergySystemOptimizationProblem",
    "PerformanceIndicator",
    "OptimizationVisualizer",
    
    # VistaDpy (PyVista) Integration
    "PyVistaConfig",
    "EnergyNetworkVisualizer",
    "MeshGenerator",
    "SpatialAnalyzer",
    "check_pyvista_available",
    "get_pyvista_version",
    "get_vtk_version",
    "create_visualizer",
    "create_mesh_generator",
    "create_spatial_analyzer",
      "VistaConfig",
    "VistaVisualizer",
    "VistaMeshGenerator",
    "quick_plot",
    "quick_flow_plot",
    "check_vista_available",
    "get_vista_version",
    
    # RefinedModelSim Integration
    "RefinedModelSimConfig",
    "TravelModel",
    "EnergyTransportIntegration",
    "ScenarioManager",
    "quick_travel_model",
    "quick_ev_demand",
    "check_refinedmodelsim_available",
    "get_refinedmodelsim_version",
    
    # MethodofDRO Integration
    "DROConfig",
    "DROWrapper",
    "create_linear_dro",
    "create_tree_dro",
    "create_neural_dro",
    "check_dro_dependencies",
    "get_available_dro_models",
    "_DRO_AVAILABLE",
    "BaseLinearDRO",
    "Chi2DRO",
    "KLDRO",
    "CVaRDRO",
    "TVDRO",
    "MarginalCVaRDRO",
    "MMD_DRO",
    "ConditionalCVaRDRO",
    "HR_DRO_LR",
    "WassersteinDRO",
    "WassersteinDROsatisficing",
    "SinkhornLinearDRO",
    "MOTDRO",
    "ORWDRO",
    "BaseNNDRO",
    "Chi2NNDRO",
    "WNNDRO",
    "HRNNDRO",
    "KLDRO_LGBM",
    "CVaRDRO_LGBM",
    "Chi2DRO_LGBM",
    "KLDRO_XGB",
    "Chi2DRO_XGB",
    "CVaRDRO_XGB",
    "classification_basic",
    "classification_DN21",
    "classification_SNVD20",
    "classification_LWLC",
    "regression_basic",
    "regression_DN20_1",
    "regression_DN20_2",
    "regression_DN20_3",
    "regression_LWLC",
    
    # FaultModel Integration - Prognostics and Health Management
    "FaultModelConfig",
    "FaultModelWrapper",
    "PrognosticsModel",
    "StateEstimator",
    "Predictor",
    "UncertainData",
    "check_faultmodel_available",
    "get_faultmodel_version",
    "_FAULTMODEL_AVAILABLE",
    "ElectricMachineryModel",
    "ElectricMachineryConfig",
    "ElectricMachineryState",
    "ElectricMachineryFaultPredictor",
    "ElectricMachineryStateEstimator",
    "ElectricMachineryHealthAssessor",
    "ElectricExcavatorModel",
    "ElectricCraneModel",
    "ElectricLoaderModel",
    "ElectricForkliftModel",
      
    # EnergyOPCUA Integration
    "EnergyOPCUAConfig",
    "EnergyOPCUAClient",
    "EnergyOPCUAServer",
    "OPCUAConnectionStatus",
    "OPCUAMessageType",
    "check_opcua_available",
    "get_opcua_version",
    
    # Electric Machinery Manufacturing
    "MachineryType",
    "ProductionStatus",
    "QualityLevel",
    "EnergyConsumptionData",
    "MachineryParameters",
    "ProductionMetrics",
    "QualityInspectionResult",
    "ElectricMachinery",
    "ProductionLine",
    "EnergyOptimizer",
    "QualityControlManager",
    "create_excavator",
    "create_crane",
    "create_loader",
]

# =============================================================================
# Convenience Imports for Common Use Cases
# =============================================================================

# Alias for common imports
import pyxesxxn.network as network
import pyxesxxn.optimization as optimization
import pyxesxxn.analysis as analysis
import pyxesxxn.equipment_library as equipment
import pyxesxxn.geospatial as geospatial
import pyxesxxn.cmasrl as cmasrl
import pyxesxxn.energy_components as energy_components

# Convenience function for quick network creation
def create_network(name: str = "default_network", carrier: str = "electricity") -> Network:
    """Create a new energy system network with default settings.
    
    Args:
        name: Network name
        carrier: Primary energy carrier type
        
    Returns:
        New Network instance
    """
    from .network import Network
    network = Network(name=name)
    # Add a default bus with the specified carrier
    network.add_bus(f"bus_{name}_default", carrier)
    return network

# Convenience function for quick optimization setup
def create_optimizer(network: Network, solver: str = "highs") -> Any:
    """Create an optimizer for the given network.
    
    Args:
        network: Network to optimize
        solver: Optimization solver type
        
    Returns:
        Configured Optimizer instance
    """
    try:
        from .optimization.pyxesxxn_impl import PyXESXXNLinearOptimizer, OptimizationConfig, SolverType, OptimizationType
        config = OptimizationConfig(
            name=f"optimizer_{network.name}",
            optimization_type=OptimizationType.LINEAR,
            solver=SolverType.SCIPY
        )
        optimizer = PyXESXXNLinearOptimizer(config)
        return optimizer
    except Exception:
        from .optimization import LinearOptimizer
        return LinearOptimizer()