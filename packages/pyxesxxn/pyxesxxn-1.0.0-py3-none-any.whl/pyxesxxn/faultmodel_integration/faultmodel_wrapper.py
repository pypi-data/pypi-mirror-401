"""Fault Model Wrapper for ProgPy Integration.

This module provides a wrapper interface for integrating NASA's Prognostics Python Package (ProgPy)
into the PyXESXXN framework, enabling advanced prognostics and health management capabilities.
"""

from typing import Optional, Dict, Any, List, Union
import warnings

try:
    import sys
    import os
    
    faultmodel_path = os.path.join(os.path.dirname(__file__), '..', 'faultmodel', 'src')
    if faultmodel_path not in sys.path:
        sys.path.insert(0, faultmodel_path)
    
    from faultmodel import PrognosticsModel
    from faultmodel import predictors, state_estimators, uncertain_data
    from faultmodel.predictors import MonteCarlo, UnscentedTransform, Predictor
    from faultmodel.state_estimators import KalmanFilter, UnscentedKalmanFilter, ParticleFilter
    from faultmodel.uncertain_data import UnweightedSamples, MultivariateNormalDist
    
    _FAULTMODEL_AVAILABLE = True
    
    def get_faultmodel_version():
        """Get the version of the integrated faultmodel package."""
        try:
            import faultmodel
            return getattr(faultmodel, '__version__', 'unknown')
        except Exception:
            return 'unknown'
    
except ImportError as e:
    _FAULTMODEL_AVAILABLE = False
    
    PrognosticsModel = None
    predictors = None
    state_estimators = None
    uncertain_data = None
    MonteCarlo = None
    UnscentedTransform = None
    Predictor = None
    KalmanFilter = None
    UnscentedKalmanFilter = None
    ParticleFilter = None
    UnweightedSamples = None
    MultivariateNormalDist = None
    StateEstimator = None
    
    def get_faultmodel_version():
        return None


class FaultModelConfig:
    """Configuration for fault model integration.
    
    Attributes:
        process_noise: Process noise level for state estimation
        measurement_noise: Measurement noise level
        prediction_horizon: Time horizon for predictions (in seconds)
        num_samples: Number of samples for Monte Carlo simulation
        integration_method: Integration method for continuous models
        use_particle_filter: Whether to use particle filter for state estimation
        num_particles: Number of particles for particle filter
    """
    
    def __init__(
        self,
        process_noise: float = 0.01,
        measurement_noise: float = 0.1,
        prediction_horizon: float = 3600.0,
        num_samples: int = 100,
        integration_method: str = 'euler',
        use_particle_filter: bool = False,
        num_particles: int = 100,
        **kwargs
    ):
        self.process_noise = process_noise
        self.measurement_noise = measurement_noise
        self.prediction_horizon = prediction_horizon
        self.num_samples = num_samples
        self.integration_method = integration_method
        self.use_particle_filter = use_particle_filter
        self.num_particles = num_particles
        
        for key, value in kwargs.items():
            setattr(self, key, value)


class FaultModelWrapper:
    """Wrapper for fault model integration with PyXESXXN.
    
    This class provides a unified interface for using ProgPy's prognostics
    capabilities within the PyXESXXN framework.
    
    Attributes:
        config: Configuration for the fault model
        model: The underlying prognostics model
        state_estimator: State estimator instance
        predictor: Predictor instance
    """
    
    def __init__(self, config: Optional[FaultModelConfig] = None):
        """Initialize the fault model wrapper.
        
        Args:
            config: Configuration for the fault model. If None, uses default config.
            
        Raises:
            ImportError: If faultmodel (ProgPy) is not available
        """
        if not _FAULTMODEL_AVAILABLE:
            raise ImportError(
                "Faultmodel (ProgPy) is not available. "
                "Please install it using: pip install progpy"
            )
        
        self.config = config or FaultModelConfig()
        self.model = None
        self.state_estimator = None
        self.predictor = None
    
    def set_model(self, model: PrognosticsModel):
        """Set the prognostics model.
        
        Args:
            model: A PrognosticsModel instance from ProgPy
        """
        self.model = model
        self._setup_state_estimator()
        self._setup_predictor()
    
    def _setup_state_estimator(self):
        """Setup state estimator based on configuration."""
        if self.model is None:
            return
            
        if self.config.use_particle_filter:
            self.state_estimator = ParticleFilter(
                self.model,
                num_particles=self.config.num_particles
            )
        else:
            self.state_estimator = UnscentedKalmanFilter(self.model)
    
    def _setup_predictor(self):
        """Setup predictor based on configuration."""
        if self.model is None:
            return
            
        if self.config.num_samples > 1:
            self.predictor = MonteCarlo(self.model)
        else:
            self.predictor = UnscentedTransform(self.model)
    
    def estimate_state(self, t: float, u: Dict[str, float], z: Dict[str, float]):
        """Estimate current state using state estimator.
        
        Args:
            t: Current time
            u: Input dictionary
            z: Measurement dictionary
            
        Returns:
            Estimated state
        """
        if self.state_estimator is None:
            raise ValueError("State estimator not initialized. Call set_model first.")
        
        self.state_estimator.estimate(t, u, z)
        return self.state_estimator.x
    
    def predict(
        self,
        future_loading,
        dt: float = 0.1,
        **kwargs
    ):
        """Predict future states and time of event.
        
        Args:
            future_loading: Future loading function or profile
            dt: Time step for prediction
            **kwargs: Additional arguments for predictor
            
        Returns:
            Prediction results containing times, states, outputs, event states, and time of event
        """
        if self.predictor is None:
            raise ValueError("Predictor not initialized. Call set_model first.")
        
        if self.state_estimator is None:
            raise ValueError("State estimator not initialized. Call estimate_state first.")
        
        horizon = kwargs.get('horizon', self.config.prediction_horizon)
        return self.predictor.predict(
            self.state_estimator.x.sample(self.config.num_samples),
            future_loading,
            dt=dt,
            horizon=horizon
        )
    
    def simulate(
        self,
        future_loading,
        dt: float = 0.1,
        horizon: Optional[float] = None
    ):
        """Simulate model behavior under future loading.
        
        Args:
            future_loading: Future loading function or profile
            dt: Time step for simulation
            horizon: Simulation horizon. If None, uses config.prediction_horizon
            
        Returns:
            Simulation results
        """
        if self.model is None:
            raise ValueError("Model not initialized. Call set_model first.")
        
        horizon = horizon or self.config.prediction_horizon
        return self.model.simulate_to_threshold(
            future_loading,
            dt=dt,
            horizon=horizon
        )


def check_faultmodel_available() -> bool:
    """Check if faultmodel (ProgPy) is available.
    
    Returns:
        True if faultmodel is available, False otherwise
    """
    return _FAULTMODEL_AVAILABLE


UncertainData = Union[UnweightedSamples, MultivariateNormalDist] if _FAULTMODEL_AVAILABLE else None
