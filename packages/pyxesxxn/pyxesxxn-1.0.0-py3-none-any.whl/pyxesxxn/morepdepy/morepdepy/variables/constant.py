__all__ = []

from morepdepy.variables.variable import Variable

class _Constant(Variable):
    def __repr__(self):
        return str(self)
