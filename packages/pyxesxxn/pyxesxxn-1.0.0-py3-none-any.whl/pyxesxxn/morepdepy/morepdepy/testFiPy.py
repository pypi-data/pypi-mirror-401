"""Test suite for :term:`MorePDEpy` modules
"""
__docformat__ = 'restructuredtext'


__all__ = []

from morepdepy.tests.lateImportTest import _LateImportTestSuite
import morepdepy.tests.testProgram

def _suite():
    return _LateImportTestSuite(testModuleNames = (
        'solvers.test',
        'terms.test',
        'tools.test',
        'matrices.test',
        'meshes.test',
        'variables.test',
        'viewers.test',
        'boundaryConditions.test',
    ), base = __name__)

if __name__ == '__main__':
    morepdepy.tests.testProgram.main(defaultTest='_suite')
