__docformat__ = 'restructuredtext'

from .petscPreconditioner import PETScPreconditioner

__all__ = ["LUPreconditioner"]

class LUPreconditioner(PETScPreconditioner):
    """LU preconditioner for :class:`~morepdepy.solvers.petsc.petscSolver.PETScSolver`.

    """

    pctype = "lu"
