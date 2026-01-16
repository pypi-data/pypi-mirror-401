__docformat__ = 'restructuredtext'

from PyTrilinos import AztecOO

from morepdepy.solvers.trilinos.trilinosAztecOOSolver import TrilinosAztecOOSolver
from morepdepy.solvers.trilinos.preconditioners.multilevelDDPreconditioner import MultilevelDDPreconditioner

__all__ = ["LinearGMRESSolver"]

class LinearGMRESSolver(TrilinosAztecOOSolver):

    """Interface to the generalized minimal residual (:term:`GMRES`) solver
    in :ref:`TRILINOS`.

    Uses the
    :class:`~morepdepy.solvers.trilinos.preconditioners.multilevelDDPreconditioner.MultilevelDDPreconditioner`
    by default.
    """

    solver = AztecOO.AZ_gmres

    DEFAULT_PRECONDITIONER = MultilevelDDPreconditioner
