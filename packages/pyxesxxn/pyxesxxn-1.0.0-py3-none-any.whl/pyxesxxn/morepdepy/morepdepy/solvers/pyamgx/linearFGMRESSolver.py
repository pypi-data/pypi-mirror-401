from morepdepy.solvers.pyamgx import PyAMGXSolver
from morepdepy.solvers.pyamgx.preconditioners import JacobiPreconditioner

__all__ = ["LinearFGMRESSolver"]

class LinearFGMRESSolver(PyAMGXSolver):
    """Interface to the Flexible Generalized Minimum RESidual
    (:term:`FGMRES`) solver in :ref:`PYAMGX`.

    Uses a
    :class:`~morepdepy.solvers.pyamgx.preconditioners.JacobiPreconditioner` by
    default.
    """

    CONFIG_DICT = {
        "config_version": 2,
        "determinism_flag": 1,
        "exception_handling" : 1,
        "solver": {
            "monitor_residual": 1,
            "solver": "FGMRES",
        }
    }

    DEFAULT_PRECONDITIONER = JacobiPreconditioner
