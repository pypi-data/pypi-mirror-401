"""Test numeric implementation of the mesh
"""

__all__ = []

from morepdepy.tests.doctestPlus import _LateImportDocTestSuite
import morepdepy.tests.testProgram

def _suite():
    return _LateImportDocTestSuite(docTestModuleNames=(
        'vtkCellViewer',
        'vtkFaceViewer'
        ), base = __name__)

if __name__ == '__main__':
    morepdepy.tests.testProgram.main(defaultTest='_suite')
