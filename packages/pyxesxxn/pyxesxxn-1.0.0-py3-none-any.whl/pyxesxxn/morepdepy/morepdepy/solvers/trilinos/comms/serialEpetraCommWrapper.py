from morepdepy.tools import numerix
from morepdepy.solvers.trilinos.comms.epetraCommWrapper import EpetraCommWrapper

__all__ = ["SerialEpetraCommWrapper"]

class SerialEpetraCommWrapper(EpetraCommWrapper):
    @property
    def procID(self):
        return 0

    @property
    def Nproc(self):
        return 1

    def Norm2(self, vec):
        return numerix.L2norm(numerix.asarray(vec))
