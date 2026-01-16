__docformat__ = 'restructuredtext'

from .petscPreconditioner import PETScPreconditioner

__all__ = ["SSORPreconditioner"]

class SSORPreconditioner(PETScPreconditioner):
    """
    SSOR preconditioner for :class:`~morepdepy.solvers.petsc.petscSolver.PETScSolver`.

    """

    pctype = "sor"
