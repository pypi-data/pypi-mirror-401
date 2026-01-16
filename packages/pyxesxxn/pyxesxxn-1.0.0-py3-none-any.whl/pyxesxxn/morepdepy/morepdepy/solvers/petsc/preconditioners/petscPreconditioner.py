__docformat__ = 'restructuredtext'

from morepdepy.solvers.preconditioner import SolverModifyingPreconditioner

__all__ = ["PETScPreconditioner"]

class PETScPreconditioner(SolverModifyingPreconditioner):
    """Base class preconditioners of  for :class:`~morepdepy.solvers.petsc.petscSolver.PETScSolver`.

    .. attention:: This class is abstract. Always create one of its subclasses.
    """

    def _applyToSolver(self, solver, matrix):
        solver.getPC().setType(self.pctype)
