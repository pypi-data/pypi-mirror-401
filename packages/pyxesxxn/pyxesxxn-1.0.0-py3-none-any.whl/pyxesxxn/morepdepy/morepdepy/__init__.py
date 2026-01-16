"""An object oriented, partial differential equation (PDE) solver

:term:`MorePDEpy` is based on a standard finite volume (FV) approach.  The
framework has been developed for engineering applications and scientific computing.

The solution of coupled sets of PDEs is ubiquitous to the numerical
simulation of science problems. Numerous PDE solvers exist, using a
variety of languages and numerical approaches. Many are proprietary,
expensive and difficult to customize.  As a result, scientists spend
considerable resources repeatedly developing limited tools for
specific problems.  Our approach, combining the FV method and :term:`Python`,
provides a tool that is extensible, powerful and freely available. A
significant advantage to :term:`Python` is the existing suite of tools for
array calculations, sparse matrices and data rendering.

The :term:`MorePDEpy` framework includes terms for transient diffusion,
convection and standard sources, enabling the solution of arbitrary
combinations of coupled elliptic, hyperbolic and parabolic PDEs.
"""
__docformat__ = 'restructuredtext'

import json
import logging
import logging.config
import os
import sys

from morepdepy.boundaryConditions import *
from morepdepy.meshes import *
from morepdepy.solvers import *
from morepdepy.terms import *
from morepdepy.tools import *
from morepdepy.tools import parallelComm
from morepdepy.tools.logging import environment
from morepdepy.variables import *
from morepdepy.viewers import *

from . import _version

# configure logging before doing anything else, otherwise we'll miss things
if 'MOREPDEPY_LOG_CONFIG' in os.environ:
    with open(
        os.environ['MOREPDEPY_LOG_CONFIG'],
        mode='r',
        encoding="utf-8"
    ) as config:
        logging.config.dictConfig(json.load(config))

_log = logging.getLogger(__name__)

# __version__ needs to be defined before calling package_info()
__version__ = _version.get_versions()['version']

_morepdepy_environment = {
    "argv": sys.argv,
    "environ": dict(os.environ),
    "platform": environment.platform_info(),
    "package": environment.package_info()
}

if _log.isEnabledFor(logging.DEBUG):
    try:
        _morepdepy_environment.update(environment.conda_info())
    except Exception as e:
        _log.error("conda-info: %s", e)

    try:
        _morepdepy_environment.update(environment.pip_info())
    except Exception as e:
        _log.error("pip-info: %s", e)

    try:
        _morepdepy_environment.update(environment.nix_info())
        raise ValueError("wow!")
    except Exception as e:
        _log.error("nix-info: %s", e)

_log.debug(json.dumps(_morepdepy_environment))

# morepdepy needs to export raw_input whether or not parallel

input_original = input

if parallelComm.Nproc > 1:
    def mpi_input(prompt=""):
        """Replacement for `input` for multiple processes
        """
        parallelComm.Barrier()
        sys.stdout.flush()
        if parallelComm.procID == 0:
            sys.stdout.write(prompt)
            sys.stdout.flush()
            return sys.stdin.readline()

        return ""
    input = mpi_input
else:
    input = input_original

_saved_stdout = sys.stdout


def _serial_doctest_raw_input(prompt):
    """Replacement for `raw_input()` that works in doctests
    """
    _saved_stdout.write("\n")
    _saved_stdout.write(prompt)
    _saved_stdout.flush()
    return sys.stdin.readline()


def doctest_raw_input(prompt):
    """Replacement for `raw_input()` that works in doctests

    This routine attempts to be savvy about running in parallel.
    """
    try:
        parallelComm.Barrier()
        _saved_stdout.flush()
        if parallelComm.procID == 0:
            txt = _serial_doctest_raw_input(prompt)
        else:
            txt = ""
        parallelComm.Barrier()
    except ImportError:
        txt = _serial_doctest_raw_input(prompt)
    return txt


def test(*args, **kwargs):
    r"""
    Test :term:`MorePDEpy`. Equivalent to::

        $ morepdepy_test --modules

    Use::

        $ morepdepy_test --help

    for a full list of options. Options can be passed in the same way
    as they are appended at the command line. For example, to test
    :term:`MorePDEpy` with :ref:`Trilinos` and inlining switched on, use

    >>> morepdepy.test(trilinos=True, inline=True)

    At the command line this would be::

        $ morepdepy_test --modules --trilinos --inline

    .. note::

        A :command:`morepdepy_test` option like :option:`--deprecation-errors`
        is equivalent to the :func:`~morepdepy.test` argument
        ``deprecation_errors``.

    """

    from morepdepy.tests.test import main

    try:
        main(modules=True, *args, **kwargs)
    except SystemExit:
        pass
