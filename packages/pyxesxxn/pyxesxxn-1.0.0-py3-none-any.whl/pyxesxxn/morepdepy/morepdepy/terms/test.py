__all__ = []

from morepdepy.tests.doctestPlus import _LateImportDocTestSuite
import morepdepy.tests.testProgram

def _suite():

    return _LateImportDocTestSuite(docTestModuleNames = (
            'cellTerm',
            'abstractDiffusionTerm',
            'diffusionTerm',
            'term',
            'abstractConvectionTerm',
            'transientTerm',
            'powerLawConvectionTerm',
            'exponentialConvectionTerm',
            'upwindConvectionTerm',
            'implicitSourceTerm',
            'coupledBinaryTerm',
            'abstractBinaryTerm',
            'unaryTerm',
            'nonDiffusionTerm',
            'asymmetricConvectionTerm',
            'binaryTerm',
            'firstOrderAdvectionTerm',
            'advectionTerm',
            'vanLeerConvectionTerm'
            ), base = __name__)

if __name__ == '__main__':
    morepdepy.tests.testProgram.main(defaultTest='_suite')
