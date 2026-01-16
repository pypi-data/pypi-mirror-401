from morepdepy.tools import numerix
from morepdepy.tools.comms.commWrapper import CommWrapper

__all__ = ["DummyComm"]

class DummyComm(CommWrapper):
    @property
    def procID(self):
        return 0
        
    @property
    def Nproc(self):
        return 1
