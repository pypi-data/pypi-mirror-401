"""Test numeric implementation of the mesh
"""

__all__ = []

from morepdepy.tests.doctestPlus import _LateImportDocTestSuite
import morepdepy.tests.testProgram

def _suite():
    return _LateImportDocTestSuite(docTestModuleNames=(
        'matplotlibViewer',
        'matplotlib1DViewer',
        'matplotlib2DViewer',
        'matplotlib2DGridViewer',
        'matplotlib2DContourViewer',
        'matplotlib2DGridContourViewer',
        'matplotlibStreamViewer',
        'matplotlibVectorViewer',
        ), base = __name__)

if __name__ == '__main__':
    morepdepy.tests.testProgram.main(defaultTest='_suite')
