__docformat__ = 'restructuredtext'

from .petscPreconditioner import PETScPreconditioner

__all__ = ["ICPreconditioner"]

class ICPreconditioner(PETScPreconditioner):
    """Incomplete Choleski preconditioner for :class:`~morepdepy.solvers.petsc.petscSolver.PETScSolver`.
    """

    pctype = "icc"
