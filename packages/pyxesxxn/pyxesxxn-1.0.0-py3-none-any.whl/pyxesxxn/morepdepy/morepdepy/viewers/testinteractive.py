"""
Interactively test the viewers
"""

from morepdepy.tests.doctestPlus import _LateImportDocTestSuite
import morepdepy.tests.testProgram

__all__ = []

def _suite():
    return _LateImportDocTestSuite(testModuleNames = (
        'matplotlibViewer.test',
        'mayaviViewer.test',
        ), base = __name__)

if __name__ == '__main__':
    morepdepy.tests.testProgram.main(defaultTest='_suite')
