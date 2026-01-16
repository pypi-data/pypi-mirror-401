__docformat__ = 'restructuredtext'

__all__ = []

from morepdepy.terms.abstractConvectionTerm import _AbstractConvectionTerm


class _AsymmetricConvectionTerm(_AbstractConvectionTerm):

    def _getDefaultSolver(self, var, solver, *args, **kwargs):
        r"""
        Make sure the method actually does something.
        >>> print(_AsymmetricConvectionTerm((1,)).getDefaultSolver().__repr__()[:6])
        Linear
        """
        solver = solver or super(_AsymmetricConvectionTerm, self)._getDefaultSolver(var, solver, *args, **kwargs)
        if solver and not solver._canSolveAsymmetric():
            import warnings
            warnings.warn("%s cannot solve asymmetric matrices" % solver)
        from morepdepy.solvers import DefaultAsymmetricSolver
        return solver or DefaultAsymmetricSolver(*args, **kwargs)

def _test():
    import morepdepy.tests.doctestPlus
    return morepdepy.tests.doctestPlus.testmod()

if __name__ == "__main__":
    _test()

