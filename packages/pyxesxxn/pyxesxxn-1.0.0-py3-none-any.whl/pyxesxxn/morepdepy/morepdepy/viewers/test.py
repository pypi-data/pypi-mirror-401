"""
Test implementation of the viewers
"""

__all__ = []

from morepdepy.tests.doctestPlus import _LateImportDocTestSuite
import morepdepy.tests.testProgram

def _suite():
    return _LateImportDocTestSuite(testModuleNames = (
        'vtkViewer.test',),
                                   docTestModuleNames = (
        'tsvViewer',
        ), base = __name__)

if __name__ == '__main__':
    morepdepy.tests.testProgram.main(defaultTest='_suite')
