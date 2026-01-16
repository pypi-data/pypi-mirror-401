__docformat__ = 'restructuredtext'

from PyTrilinos import AztecOO

from morepdepy.solvers.trilinos.trilinosAztecOOSolver import TrilinosAztecOOSolver
from morepdepy.solvers.trilinos.preconditioners.jacobiPreconditioner import JacobiPreconditioner

__all__ = ["LinearBicgstabSolver"]

class LinearBicgstabSolver(TrilinosAztecOOSolver):

    """Interface to the Biconjugate Gradient (Stabilized) (:term:`BiCGSTAB`)
    solver in :ref:`TRILINOS`.

    Uses the
    :class:`~morepdepy.solvers.trilinos.preconditioners.jacobiPreconditioner.JacobiPreconditioner`
    by default.
    """

    solver = AztecOO.AZ_bicgstab

    DEFAULT_PRECONDITIONER = JacobiPreconditioner
