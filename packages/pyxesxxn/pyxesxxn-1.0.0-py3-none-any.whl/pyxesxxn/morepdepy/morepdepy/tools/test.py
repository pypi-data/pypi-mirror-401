__all__ = []

from morepdepy.tests.doctestPlus import _LateImportDocTestSuite
import morepdepy.tests.testProgram

def _suite():
    theSuite = _LateImportDocTestSuite(docTestModuleNames = (
            'dimensions.physicalField',
            'numerix',
            'dump',
            'vector',
            'sharedtempfile',
            'timer'
        ), base = __name__)

    return theSuite

if __name__ == '__main__':
    morepdepy.tests.testProgram.main(defaultTest='_suite')
