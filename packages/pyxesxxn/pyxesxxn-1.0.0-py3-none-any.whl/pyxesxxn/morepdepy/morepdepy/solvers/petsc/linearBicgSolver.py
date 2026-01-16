__docformat__ = 'restructuredtext'

from morepdepy.solvers.petsc.petscKrylovSolver import PETScKrylovSolver

__all__ = ["LinearBicgSolver"]

class LinearBicgSolver(PETScKrylovSolver):

    """Interface to the biconjugate gradient solver (:term:`BiCG`) in
    :ref:`PETSC`.
    """
      
    solver = 'bicg'
