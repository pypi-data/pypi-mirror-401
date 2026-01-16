__docformat__ = 'restructuredtext'

from morepdepy.solvers.preconditioner import SolverModifyingPreconditioner

__all__ = ["TrilinosPreconditioner"]

class TrilinosPreconditioner(SolverModifyingPreconditioner):
    """Base class of preconditioners for :class:`~morepdepy.solvers.trilinos.trilinosSolver.TrilinosSolver`.

    .. attention:: This class is abstract. Always create one of its subclasses.
    """

    pass
