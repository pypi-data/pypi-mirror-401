""" MorePDEpy is an object oriented, partial differential equation (PDE) solver

MorePDEpy is based on a standard finite volume (FV) approach.  The framework has
been developed for engineering applications and scientific computing.
"""

from setuptools import setup

import versioneer

VERSION = versioneer.get_version()

DIST = setup(
    version=VERSION,
    cmdclass=dict(
        **versioneer.get_cmdclass()
    ),
)
