__docformat__ = 'restructuredtext'

from .petscPreconditioner import PETScPreconditioner

__all__ = ["ILUPreconditioner"]

class ILUPreconditioner(PETScPreconditioner):
    """Incomplete LU preconditioner for :class:`~morepdepy.solvers.petsc.petscSolver.PETScSolver`.
    """

    pctype = "ilu"
