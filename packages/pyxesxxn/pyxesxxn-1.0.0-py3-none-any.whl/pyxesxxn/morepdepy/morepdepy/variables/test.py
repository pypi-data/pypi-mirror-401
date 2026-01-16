"""Test numeric implementation of the mesh
"""

__all__ = []

from morepdepy.tests.doctestPlus import _LateImportDocTestSuite
import morepdepy.tests.testProgram

def _suite():
    return _LateImportDocTestSuite(
        docTestModuleNames = (
            'morepdepy.variables.variable',
            'morepdepy.variables.meshVariable',
            'morepdepy.variables.cellVariable',
            'morepdepy.variables.faceVariable',
            'morepdepy.variables.operatorVariable',
            'morepdepy.variables.betaNoiseVariable',
            'morepdepy.variables.exponentialNoiseVariable',
            'morepdepy.variables.gammaNoiseVariable',
            'morepdepy.variables.gaussianNoiseVariable',
            'morepdepy.variables.uniformNoiseVariable',
            'morepdepy.variables.modularVariable',
            'morepdepy.variables.binaryOperatorVariable',
            'morepdepy.variables.unaryOperatorVariable',
            'morepdepy.variables.coupledCellVariable',
            'morepdepy.variables.cellToFaceVariable',
            'morepdepy.variables.faceGradVariable',
            'morepdepy.variables.gaussCellGradVariable',
            'morepdepy.variables.faceGradContributionsVariable',
            'morepdepy.variables.surfactantConvectionVariable',
            'morepdepy.variables.surfactantVariable',
            'morepdepy.variables.levelSetDiffusionVariable',
            'morepdepy.variables.distanceVariable'
        ))

if __name__ == '__main__':
    morepdepy.tests.testProgram.main(defaultTest='_suite')
