"""MethodofDRO Integration Module for PyXESXXN.

This module provides integration with the MethodofDRO (Distributionally Robust Optimization) library,
enabling robust machine learning models for energy system analysis and optimization.

The DRO methods can be particularly useful for:
- Robust load forecasting under distribution uncertainty
- Robust renewable energy generation prediction
- Robust energy demand forecasting
- Robust price prediction in energy markets
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Optional, Tuple, Union
import warnings

try:
    import sys
    import os
    
    methodofdro_path = os.path.join(os.path.dirname(__file__), 'methodofdro', 'src')
    if methodofdro_path not in sys.path:
        sys.path.insert(0, methodofdro_path)
    
    from dro.linear_model import (
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
        ORWDRO
    )
    
    from dro.neural_model import (
        BaseNNDRO,
        Chi2NNDRO,
        WNNDRO,
        HRNNDRO
    )
    
    from dro.tree_model import (
        KLDRO_LGBM,
        CVaRDRO_LGBM,
        Chi2DRO_LGBM,
        KLDRO_XGB,
        Chi2DRO_XGB,
        CVaRDRO_XGB
    )
    
    from dro.data import (
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
    
    _DRO_AVAILABLE = True
except ImportError as e:
    _DRO_AVAILABLE = False
    _IMPORT_ERROR = str(e)
    
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


class DROConfig:
    """Configuration class for Distributionally Robust Optimization models.
    
    This class provides a unified interface for configuring different DRO models
    with consistent parameters for energy system applications.
    """
    
    def __init__(
        self,
        model_type: str = 'logistic',
        eps: float = 0.1,
        solver: str = 'ECOS',
        fit_intercept: bool = True,
        **kwargs
    ):
        """Initialize DRO configuration.
        
        Args:
            model_type: Type of base model ('svm', 'logistic', 'ols', 'lad')
            eps: Robustness parameter (>= 0)
            solver: Optimization solver ('MOSEK', 'ECOS', 'SCS')
            fit_intercept: Whether to fit intercept term
            **kwargs: Additional model-specific parameters
        """
        self.model_type = model_type
        self.eps = eps
        self.solver = solver
        self.fit_intercept = fit_intercept
        self.extra_params = kwargs
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary.
        
        Returns:
            Dictionary containing all configuration parameters
        """
        config = {
            'model_type': self.model_type,
            'eps': self.eps,
            'solver': self.solver,
            'fit_intercept': self.fit_intercept
        }
        config.update(self.extra_params)
        return config


class DROWrapper:
    """Wrapper class for DRO models with energy system-specific utilities.
    
    This wrapper provides a convenient interface for using DRO models
    in energy system analysis and optimization tasks.
    """
    
    def __init__(
        self,
        model_class: type,
        input_dim: int,
        config: Optional[DROConfig] = None,
        **kwargs
    ):
        """Initialize DRO wrapper.
        
        Args:
            model_class: DRO model class (e.g., Chi2DRO, KLDRO)
            input_dim: Input feature dimension
            config: DRO configuration object
            **kwargs: Additional model parameters
        """
        if not _DRO_AVAILABLE:
            raise ImportError(
                f"MethodofDRO is not available. Please install required dependencies: {_IMPORT_ERROR}"
            )
        
        self.model_class = model_class
        self.input_dim = input_dim
        self.config = config or DROConfig()
        self.model = None
        self.extra_params = kwargs
    
    def initialize_model(self):
        """Initialize the underlying DRO model."""
        model_params = {
            'input_dim': self.input_dim,
            'model_type': self.config.model_type,
            'fit_intercept': self.config.fit_intercept,
            'solver': self.config.solver
        }
        model_params.update(self.extra_params)
        
        self.model = self.model_class(**model_params)
        
        if hasattr(self.model, 'update'):
            self.model.update({'eps': self.config.eps})
    
    def fit(self, X, y) -> Dict[str, Any]:
        """Train the DRO model.
        
        Args:
            X: Training features (n_samples, n_features)
            y: Training targets (n_samples,)
            
        Returns:
            Training results dictionary
        """
        if self.model is None:
            self.initialize_model()
        
        return self.model.fit(X, y)
    
    def predict(self, X):
        """Make predictions with the trained DRO model.
        
        Args:
            X: Test features (n_samples, n_features)
            
        Returns:
            Predictions
        """
        if self.model is None:
            raise RuntimeError("Model must be fitted before prediction")
        
        return self.model.predict(X)
    
    def evaluate(self, X, y) -> Dict[str, float]:
        """Evaluate model performance.
        
        Args:
            X: Test features
            y: True targets
            
        Returns:
            Dictionary of evaluation metrics
        """
        if self.model is None:
            raise RuntimeError("Model must be fitted before evaluation")
        
        if hasattr(self.model, 'evaluate'):
            return self.model.evaluate(X, y)
        else:
            from sklearn.metrics import accuracy_score, mean_squared_error
            
            y_pred = self.predict(X)
            
            if self.config.model_type in ['svm', 'logistic']:
                return {'accuracy': accuracy_score(y, y_pred)}
            else:
                return {'mse': mean_squared_error(y, y_pred)}
    
    def get_worst_distribution(self):
        """Get the worst-case distribution from the DRO model.
        
        Returns:
            Worst-case distribution weights
        """
        if self.model is None:
            raise RuntimeError("Model must be fitted first")
        
        if hasattr(self.model, 'worst_distribution'):
            return self.model.worst_distribution()
        else:
            warnings.warn("This model does not support worst-case distribution analysis")
            return None


def create_linear_dro(
    input_dim: int,
    dro_type: str = 'chi2',
    config: Optional[DROConfig] = None,
    **kwargs
) -> DROWrapper:
    """Factory function to create linear DRO models.
    
    Args:
        input_dim: Input feature dimension
        dro_type: Type of DRO ('chi2', 'kl', 'cvar', 'tv', 'mmd', 'wasserstein')
        config: DRO configuration object
        **kwargs: Additional model parameters
        
    Returns:
        Configured DROWrapper instance
        
    Raises:
        ValueError: If dro_type is not supported
    """
    if not _DRO_AVAILABLE:
        raise ImportError(
            f"MethodofDRO is not available. Please install required dependencies: {_IMPORT_ERROR}"
        )
    
    dro_models = {
        'chi2': Chi2DRO,
        'kl': KLDRO,
        'cvar': CVaRDRO,
        'tv': TVDRO,
        'mmd': MMD_DRO,
        'wasserstein': WassersteinDRO,
        'sinkhorn': SinkhornLinearDRO,
        'marginal_cvar': MarginalCVaRDRO,
        'conditional_cvar': ConditionalCVaRDRO,
        'hr': HR_DRO_LR,
        'mot': MOTDRO,
        'or_wasserstein': ORWDRO
    }
    
    if dro_type not in dro_models:
        raise ValueError(
            f"Unsupported DRO type: {dro_type}. "
            f"Supported types: {list(dro_models.keys())}"
        )
    
    return DROWrapper(dro_models[dro_type], input_dim, config, **kwargs)


def create_tree_dro(
    dro_type: str = 'kl',
    model_type: str = 'lgbm',
    config: Optional[DROConfig] = None,
    **kwargs
) -> Any:
    """Factory function to create tree-based DRO models.
    
    Args:
        dro_type: Type of DRO ('kl', 'cvar', 'chi2')
        model_type: Tree model type ('lgbm', 'xgb')
        config: DRO configuration object
        **kwargs: Additional model parameters
        
    Returns:
        Configured tree-based DRO model
        
    Raises:
        ValueError: If dro_type or model_type is not supported
    """
    if not _DRO_AVAILABLE:
        raise ImportError(
            f"MethodofDRO is not available. Please install required dependencies: {_IMPORT_ERROR}"
        )
    
    tree_models = {
        'lgbm': {
            'kl': KLDRO_LGBM,
            'cvar': CVaRDRO_LGBM,
            'chi2': Chi2DRO_LGBM
        },
        'xgb': {
            'kl': KLDRO_XGB,
            'cvar': CVaRDRO_XGB,
            'chi2': Chi2DRO_XGB
        }
    }
    
    if model_type not in tree_models:
        raise ValueError(
            f"Unsupported tree model type: {model_type}. "
            f"Supported types: {list(tree_models.keys())}"
        )
    
    if dro_type not in tree_models[model_type]:
        raise ValueError(
            f"Unsupported DRO type for {model_type}: {dro_type}. "
            f"Supported types: {list(tree_models[model_type].keys())}"
        )
    
    model_class = tree_models[model_type][dro_type]
    
    if config is None:
        config = DROConfig(eps=0.1)
    
    return model_class(eps=config.eps, **kwargs)


def create_neural_dro(
    input_dim: int,
    dro_type: str = 'chi2',
    config: Optional[DROConfig] = None,
    **kwargs
) -> Any:
    """Factory function to create neural network DRO models.
    
    Args:
        input_dim: Input feature dimension
        dro_type: Type of DRO ('chi2', 'wasserstein', 'hr')
        config: DRO configuration object
        **kwargs: Additional model parameters
        
    Returns:
        Configured neural network DRO model
        
    Raises:
        ValueError: If dro_type is not supported
    """
    if not _DRO_AVAILABLE:
        raise ImportError(
            f"MethodofDRO is not available. Please install required dependencies: {_IMPORT_ERROR}"
        )
    
    neural_models = {
        'chi2': Chi2NNDRO,
        'wasserstein': WNNDRO,
        'hr': HRNNDRO
    }
    
    if dro_type not in neural_models:
        raise ValueError(
            f"Unsupported neural DRO type: {dro_type}. "
            f"Supported types: {list(neural_models.keys())}"
        )
    
    model_class = neural_models[dro_type]
    
    if config is None:
        config = DROConfig(eps=0.1)
    
    return model_class(input_dim=input_dim, **kwargs)


def check_dro_dependencies() -> Dict[str, bool]:
    """Check if all DRO dependencies are available.
    
    Returns:
        Dictionary with dependency availability status
    """
    deps = {
        'dro_available': _DRO_AVAILABLE,
        'cvxpy': False,
        'torch': False,
        'xgboost': False,
        'lightgbm': False
    }
    
    if _DRO_AVAILABLE:
        try:
            import cvxpy
            deps['cvxpy'] = True
        except ImportError:
            pass
        
        try:
            import torch
            deps['torch'] = True
        except ImportError:
            pass
        
        try:
            import xgboost
            deps['xgboost'] = True
        except ImportError:
            pass
        
        try:
            import lightgbm
            deps['lightgbm'] = True
        except ImportError:
            pass
    
    return deps


def get_available_dro_models() -> Dict[str, list]:
    """Get list of available DRO models by category.
    
    Returns:
        Dictionary with available models for each category
    """
    if not _DRO_AVAILABLE:
        return {
            'linear': [],
            'neural': [],
            'tree': []
        }
    
    return {
        'linear': [
            'Chi2DRO', 'KLDRO', 'CVaRDRO', 'TVDRO', 'MarginalCVaRDRO',
            'MMD_DRO', 'ConditionalCVaRDRO', 'HR_DRO_LR',
            'WassersteinDRO', 'WassersteinDROsatisficing',
            'SinkhornLinearDRO', 'MOTDRO', 'ORWDRO'
        ],
        'neural': [
            'Chi2NNDRO', 'WNNDRO', 'HRNNDRO'
        ],
        'tree': [
            'KLDRO_LGBM', 'CVaRDRO_LGBM', 'Chi2DRO_LGBM',
            'KLDRO_XGB', 'Chi2DRO_XGB', 'CVaRDRO_XGB'
        ]
    }


__all__ = [
    'DROConfig',
    'DROWrapper',
    'create_linear_dro',
    'create_tree_dro',
    'create_neural_dro',
    'check_dro_dependencies',
    'get_available_dro_models',
    '_DRO_AVAILABLE',
    'BaseLinearDRO',
    'Chi2DRO',
    'KLDRO',
    'CVaRDRO',
    'TVDRO',
    'MarginalCVaRDRO',
    'MMD_DRO',
    'ConditionalCVaRDRO',
    'HR_DRO_LR',
    'WassersteinDRO',
    'WassersteinDROsatisficing',
    'SinkhornLinearDRO',
    'MOTDRO',
    'ORWDRO',
    'BaseNNDRO',
    'Chi2NNDRO',
    'WNNDRO',
    'HRNNDRO',
    'KLDRO_LGBM',
    'CVaRDRO_LGBM',
    'Chi2DRO_LGBM',
    'KLDRO_XGB',
    'Chi2DRO_XGB',
    'CVaRDRO_XGB',
    'classification_basic',
    'classification_DN21',
    'classification_SNVD20',
    'classification_LWLC',
    'regression_basic',
    'regression_DN20_1',
    'regression_DN20_2',
    'regression_DN20_3',
    'regression_LWLC',
]
