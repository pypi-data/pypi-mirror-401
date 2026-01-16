"""Utility modules, functions, and values

.. attribute:: serialComm
    :type: ~morepdepy.tools.comms.commWrapper.CommWrapper

    Serial MPI communicator when running in parallel.

.. attribute:: parallelComm
    :type: ~morepdepy.tools.comms.commWrapper.CommWrapper

    Parallel MPI communicator when running in parallel.
"""


from morepdepy.solvers import serialComm, parallelComm
serial, parallel = serialComm, parallelComm

from morepdepy.tests.doctestPlus import register_skipper

register_skipper(flag="SERIAL",
                 test=lambda: parallelComm.Nproc == 1,
                 why="more than one processor found",
                 skipWarning=False)

register_skipper(flag="PARALLEL",
                 test=lambda: parallelComm.Nproc > 1,
                 why="only one processor found",
                 skipWarning=False)

register_skipper(flag="PARALLEL_2",
                 test=lambda: parallelComm.Nproc == 2,
                 why="other than 2 processors found",
                 skipWarning=False)

register_skipper(flag="PROCESSOR_0",
                 test=lambda: parallelComm.procID == 0,
                 why="not running on processor 0",
                 skipWarning=False)

register_skipper(flag="PROCESSOR_NOT_0",
                 test=lambda: parallelComm.procID > 0,
                 why="running on processor 0",
                 skipWarning=False)

for M in (2, 3):
    for N in range(M):
        register_skipper(flag="PROCESSOR_%d_OF_%d" % (N, M),
                         test=lambda N=N, M=M: parallelComm.procID == N and parallelComm.Nproc == M,
                         why="not running on processor %d of %d" % (N, M),
                         skipWarning=False)

from morepdepy.tools import dump
from morepdepy.tools import numerix
from morepdepy.tools import vector
from .dimensions.physicalField import PhysicalField
from morepdepy.tools.numerix import *
from morepdepy.tools.sharedtempfile import SharedTemporaryFile

__all__ = ["serialComm",
           "parallelComm",
           "dump",
           "numerix",
           "vector",
           "PhysicalField",
           "serial",
           "parallel",
           "SharedTemporaryFile"]

import os
if 'MOREPDEPY_INCLUDE_NUMERIX_ALL' in os.environ:
    import warnings
    class MorePDEpyDeprecationWarning(DeprectationWarning):
        pass
    warnings.warn("""
The ability to include `numerix` functions in `morepdepy` namespace
with MOREPDEPY_INCLUDE_NUMERIX_ALL environment variable will
likely be removed in the future. If needed, same effect can be
accomplished with `from morepdepy.tools.numerix import *`
""", FutureWarning)
    __all__.extend(numerix.__all__)
